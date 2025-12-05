class ExtractZipFileError(RuntimeError):
    def __init__(
        self, zip_file, message: str = f"Can not extract zip file. Check your hardware."
    ):
        if zip_file is None:
            super().__init__(message)
        else:
            super().__init__(f"Can not extract {zip_file}")
