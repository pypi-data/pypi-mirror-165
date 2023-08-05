"""
This is a main class for XMLLibrary class.
The class XMLLibrary implements a logic to process XML files:
    1) A constructor:
        - receives a XML file name
        - creates XML tree object
        - defines a root node for the XML tree object
        - set to None a node, which is a point for modification operation

    2) A method <set_xml_node_to_modify> defines a node, which is a point for 
       modification operation by a list of parameters:
       - a tag string is a mandatory parameter
       - an attrib_dict is a optional parameter, a dictionary of a node attributes
         (default value is None)
       - a node_value string is a optional parameter for a node.text property
         (default value is None)

    3) A method <do_modify_xml> is a universal metod for modify operations:
        1. Operation: ADD
           Action: to add a node with the given parameters as a child of node_to_modify
        2. Operation: MODIFY
           Action: to modify the node_to_modify to given parameters
        3. Operation: DELETE
           Action: 
            - if node_kind = __NODE_IS_ITSELF, then to delete the node_to_modify
            - if node_kind = __NODE_IS_CHILD, then to delete child node with given parameters 
                node under node_to_modify 

    4) Possibile values for param <node_kind>: 
                1 - modified_node, 
                2 - child of modified_node

       Possibile values for param <operation>: 
                1 - add node, 
                2 - del node, 
                3 - modify node

       Constraints for params:
            +------------------+-----------------+
            |     node_kind    |    operation    |
            +------------------+-----------------+
            |        1         |         1       |
            |        1         |         2       |
            |        1         |         3       |
            |        2         |         3       |
            +------------------+-----------------+

    Doc: https://digitology.tech/docs/python_3/library/xml.etree.elementtree.html
"""

__all__ = ['XMLLibrary']

from typing import List, Final
import xml.etree.ElementTree as ET
from .exceptions.xml_exception import XMLNodeNotExistException, \
                                                XMLEmptyNodeListException, \
                                                XMLManyNodeInListException, \
                                                XMLInvalidOperationException, \
                                                XMLInvalidNodeKindException, \
                                                XMLВiscrepancyNodeKindOperationException


class XMLLibrary:

    # todo: подумать, как писать сообщения о действиях, может быть вести лог

    """
    Params:
        xml_file: the xml file name
        xml_tree_root: the root node of the xml file
        xml_node_to_modify: the node to modify 
    """

    __NODE_IS_ITSELF: Final[int] = 1
    __NODE_IS_CHILD: Final[int] = 2

    __OPERATION_ADD: Final[int] = 1
    __OPERATION_MODIFY: Final[int] = 2
    __OPERATION_DELETE: Final[int] = 3

    def __init__(self, xml_file_name: str) -> None:
        self.xml_file: str = xml_file_name
        self.xml_tree: ET.ElementTree = ET.parse(xml_file_name)
        self.xml_tree_root: ET.Element = self.xml_tree.getroot()
        self.xml_node_to_modify: ET.Element = None


    # Получить узел с заданными параметрами в заданном родительском
    def __get_xml_node_by_params(self,
                                 parent_node: ET.Element,
                                 tag: str,
                                 attrib_dict: dict,
                                 node_value: str) -> ET.Element:

        # Если не задан tag узла, то exception
        if not tag or tag is None:
            raise XMLNodeNotExistException(tag, True)

        # Список узлов, соответствующих критериям выборки
        tmp_nodes_list: List(ET.Element) = []

        # Сколько узлов с заданным tag среди дочерних
        tag_count: int = 0

        # Проходим по всем узлам дерева с тегом = tag
        for tmp_node in parent_node.iter(tag):

            tag_count += 1
            
            # Если значение в узле есть, но != заданному значению, то переходим к следующему узлу
            if node_value and node_value is not None and tmp_node.text != node_value:
                continue

            # Если не заданы аттрибуты, то включаем узел в список
            if attrib_dict is None:
                tmp_nodes_list.append(tmp_node)
                continue

            # Если заданы аттрибуты, то проверяем соответствие аттрибутов
            tmp_node_attrib = tmp_node.attrib
            is_attrib_match: bool = True
            for attrib_key, attrib_value in attrib_dict.items():
                if tmp_node_attrib.has_key(attrib_key) and tmp_node_attrib[attrib_key] == attrib_value:
                    continue
                is_attrib_match = False
                break

            # Если словарь аттрибутов полностью есть в текущем узле, то добавляем узел в список
            if is_attrib_match:
                tmp_nodes_list.append(tmp_node)


        # Если не найдено ни одного узла с заданным tag
        if tag_count == 0:
            raise XMLNodeNotExistException(tag)

        # Если не найдено ни одного узла с заданными условиями
        if len(tmp_nodes_list) == 0:
            raise XMLEmptyNodeListException(parent_node,
                                            tag,
                                            attrib_dict,
                                            node_value)

        # Если найдено несколько узлов с заданными условиями
        # todo: Нужна ли эта проверка? Может быть задать опцией?
        if len(tmp_nodes_list) > 1:
            raise XMLManyNodeInListException(parent_node,
                                             tag,
                                             attrib_dict,
                                             node_value)

        return tmp_nodes_list[0]


    # Сохранить XML в файд
    def do_save_xml_tree(self, xml_file_name: str) -> None:
        self.xml_tree.write(xml_file_name)


    # Получить узел, который определен для модификации
    def get_xml_node_to_modify(self) -> ET.Element:
        """
        The method returns the node to modify
        """
        return self.xml_node_to_modify


    # Определить узел, который по параметрам/условиям определен для модификации
    def set_xml_node_to_modify(self, tag: str, 
                                     attrib_dict: dict = None, 
                                     node_value: str = None) -> None:
        """
        To set the node to modify by the node tag, the attributes (by dictionary) and the node value
        """
        self.xml_node_to_modify = self.__get_xml_node_by_params(self.xml_tree_root, tag, attrib_dict, node_value)
    

    # Добавить узел в XML структуру
    def __add_node_function(self,
                            tag: str,
                            attrib_dict: dict,
                            node_value: str,
                            node_kind: int = __NODE_IS_ITSELF) -> None:

        new_tag: ET.Element = ET.Element(tag)
        if attrib_dict is not None:
            new_tag.attrib = attrib_dict
        if node_value is not None:
            new_tag.text = node_value
        print(type(self))
        print(type(self.xml_node_to_modify))
        self.xml_node_to_modify.append(new_tag)


    # Удалить узел из XML структуры
    def __del_node_function(self,
                            tag: str,
                            attrib_dict: dict,
                            node_value: str,
                            node_kind: int) -> None:

        if node_kind == self.NODE_IS_ITSELF:
            # Удалить узел to_modify
            parent_node: ET.Element = self.xml_node_to_modify.getparent()
            if parent_node is None:
                # todo: что делать, если удаляемый узел to_modify = root?
                pass
            else:
                parent_node.remove(self.xml_node_to_modify)
        else:
            # Найти узел с заданными параметрами в узле to_modify
            xml_node_to_del: ET.Element = self.get_xml_node_by_params(self.xml_node_to_modify,
                                                                      tag,
                                                                      attrib_dict,
                                                                      node_value)
            self.xml_node_to_modify.remove(xml_node_to_del)


    # Модифицировать узел в XML структуры
    def __modify_node_function(self,
                               tag: str,
                               attrib_dict: dict,
                               node_value: str,
                               node_kind: int = __NODE_IS_ITSELF) -> None:

        # Изменить узел to_modify
        self.xml_node_to_modify.tag = tag
        if attrib_dict is not None:
            self.xml_node_to_modify.attrib = attrib_dict
        if node_value is not None:
            self.xml_node_to_modify.text = node_value


    # Единая функция модификации XML структуры
    def do_modify_xml(self, operation: int,
                            tag: str = None,
                            attrib_dict: dict = None,
                            node_value: str = None,
                            node_kind: int = __NODE_IS_ITSELF) -> None:

        # Проверить ограничение на корректность значений типа узла, операции и
        # соответствие типа узла и операции
        def __do_check_operation_constraint(operation: int, node_kind: int) -> None:
            
            if operation not in [self.__OPERATION_ADD,
                                 self.__OPERATION_MODIFY,
                                 self.__OPERATION_DELETE]:
                raise XMLInvalidOperationException(operation)

            if node_kind not in [self.__NODE_IS_CHILD,
                                 self.__NODE_IS_ITSELF]:
                raise XMLInvalidNodeKindException(node_kind)

            acceptable_match_list: List= [[self.__NODE_IS_ITSELF, self.__OPERATION_ADD],
                                          [self.__NODE_IS_ITSELF, self.__OPERATION_MODIFY],
                                          [self.__NODE_IS_ITSELF, self.__OPERATION_DELETE],
                                          [self.__NODE_IS_CHILD, self.__OPERATION_DELETE]
                                         ]
            if [node_kind, operation] not in acceptable_match_list:
                raise XMLВiscrepancyNodeKindOperationException(node_kind, operation)


        # Проверить соответствие между типом узла и операцией
        __do_check_operation_constraint(operation, node_kind)

        # Список функций для выполнения операций в XML структуре
        function_operation: List = [self.__add_node_function,
                                    self.__del_node_function,
                                    self.__modify_node_function
                                ]

#        if operation == self.__OPERATION_ADD:
#            self.add_node_function(tag, attrib_dict, node_value, node_kind)
        function_operation[operation - 1](tag, attrib_dict, node_value, node_kind)

