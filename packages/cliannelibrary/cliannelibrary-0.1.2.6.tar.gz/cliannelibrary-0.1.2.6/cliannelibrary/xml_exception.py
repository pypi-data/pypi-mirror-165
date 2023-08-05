from platform import node
import xml.etree.ElementTree as ET


class XMLNodeNotExistException(Exception):
    """
    It should be risen if a xml node is not defined
    """

    def __init__(self, tag: str, is_empty: bool=False):
        if is_empty:
            self.message = f'The TAG of XML node is not defined - EMPTY. It is impossible to find the XML node.'
        else:
            self.message = f'XML node {tag} does not exist. It is impossible to find the XML node.'
        super().__init__(self.message)


class XMLEmptyNodeListException(Exception):
    """
    It should be risen if a list of xml nodes is empty
    """

    def __init__(self, parent_node: ET.Element,
                       tag: str,
                       attrib_dict: dict,
                       node_value: str):
        fmessage = f'Node [{parent_node.tag}] has no child XML nodes with given conditions:\n     tag = {tag}'
        if attrib_dict is not None:
            fmessage += f'\n     attributes = {attrib_dict}'
        if node_value is not None:
            fmessage += f'\n     text = {node_value}'
        self.message = fmessage
        super().__init__(self.message)


class XMLManyNodeInListException(Exception):
    """
    It should be risen if a list of xml nodes includes more than 1 node
    """

    def __init__(self, parent_node: ET.Element,
                       tag: str,
                       attrib_dict: dict,
                       node_value: str):
        fmessage = f'Node [{parent_node.tag}] has too much child XML nodes with given conditions:\n     tag = {tag}'
        if attrib_dict is not None:
            fmessage += f'\n     attributes = {attrib_dict}'
        if node_value is not None:
            fmessage += f'\n     text = {node_value}'
        self.message = fmessage
        super().__init__(self.message)


class XMLInvalidOperationException(Exception):
    """
    It should be risen if it is invalid operation
    """

    def __init__(self, operation: int):
        self.message = f'There is invalid operation #{operation}.'
        super().__init__(self.message)


class XMLInvalidNodeKindException(Exception):
    """
    It should be risen if it is kind of node
    """

    def __init__(self, node_kind: int):
        self.message = f'There is invalid kind # {node_kind} for XML node.'
        super().__init__(self.message)


class XMLВiscrepancyNodeKindOperationException(Exception):
    # todo: Сделать более понятным сообщение об ошибке и поменять параметры
    """
    It should be risen if it constraint between node_kind and operation is broken
    """

    def __init__(self, operation: int, node_kind: int):
        self.message = f'There are invalid operation #{operation} for XML node kind #{node_kind}.'
        super().__init__(self.message)


