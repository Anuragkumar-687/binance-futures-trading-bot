"""Custom exceptions for the trading bot."""


class ValidationError(Exception):
    """Raised when user input fails validation."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class OrderExecutionError(Exception):
    """Raised when an order cannot be executed on the exchange."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
