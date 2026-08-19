class DomainError(Exception):
    """Base class for errors raised by the domain/application layers."""


class UnknownDiagnosisCodeError(DomainError):
    def __init__(self, codes: list[str]):
        self.codes = codes
        super().__init__(f"Unknown diagnosis code(s): {', '.join(codes)}")
