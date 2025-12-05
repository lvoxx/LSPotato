class FileGetFailedError(RuntimeError):
    def __init__(self, file_name, message: str = f"Can not download file."):
        if file_name is None:
            super().__init__(message)
        else:
            super().__init__(f"Can not download file {file_name}.")
