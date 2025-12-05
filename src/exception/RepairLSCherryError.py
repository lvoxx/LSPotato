class RepairLSCherryError(RuntimeError):
    def __init__(self, version, message: str = "Can not repair LSCherry."):
        if version is None:
            super().__init__(message)
        else:
            super().__init__(f"Can not repair LSCherry version {version}.")
