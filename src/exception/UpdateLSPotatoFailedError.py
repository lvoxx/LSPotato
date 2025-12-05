class UpdateLSPotatoFailedError(RuntimeError):
    def __init__(
        self,
        message: str = "Can not update LSPotato. Check for lastest updates on Github.",
    ):
        super().__init__(message)
