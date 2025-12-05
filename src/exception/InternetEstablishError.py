class InternetEstablishError(RuntimeError):
    def __init__(
        self,
        message: str = "Can not establish internet connection. Please try again later.",
    ):
        super().__init__(message)
