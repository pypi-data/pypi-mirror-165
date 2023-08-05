class FileAlreadyExistsException(Exception):
    """
    It should be risen if a new file already exists (to protect user from rename errors).
    """

    def __init__(self, message):
        self.message = f'File {message} exists. It is impossible to rewrite existing file.'
        super().__init__(self.message)