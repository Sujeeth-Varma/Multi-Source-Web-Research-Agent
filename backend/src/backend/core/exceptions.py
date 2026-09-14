class BaseResearchException(Exception):
    """Base exception for research agent failures."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        super().__init__(message)
        self.message = message
        self.code = code


class ProviderException(BaseResearchException):
    """Raised when a search provider fails or encounters an API error."""
    def __init__(self, provider_name: str, message: str):
        super().__init__(f"[{provider_name}] {message}", code="PROVIDER_ERROR")
        self.provider_name = provider_name


class LLMUnavailableException(BaseResearchException):
    """Raised when the LLM service (Gemini) fails or is unreachable."""
    def __init__(self, message: str = "The research model was temporarily unavailable."):
        super().__init__(message, code="LLM_UNAVAILABLE")


class InvalidRequestException(BaseResearchException):
    """Raised for bad input or validation failures."""
    def __init__(self, message: str):
        super().__init__(message, code="INVALID_REQUEST")
