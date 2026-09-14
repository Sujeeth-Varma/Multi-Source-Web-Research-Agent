import os
import logging
from typing import Optional, List, Any
from backend.core.config import settings

logger = logging.getLogger(__name__)


class LangfuseObserver:
    """Helper wrapper for Langfuse observability tracing and LangChain callbacks."""

    def __init__(self):
        self.enabled = bool(settings.LANGFUSE_PUBLIC_KEY and settings.LANGFUSE_SECRET_KEY)
        self._client = None
        self._handler = None
        
        if self.enabled:
            try:
                # Export environment variables required by langfuse v4 OpenTelemetry SDK
                os.environ["LANGFUSE_PUBLIC_KEY"] = settings.LANGFUSE_PUBLIC_KEY
                os.environ["LANGFUSE_SECRET_KEY"] = settings.LANGFUSE_SECRET_KEY
                os.environ["LANGFUSE_HOST"] = settings.get_langfuse_host()
                
                from langfuse import Langfuse
                from langfuse.langchain import CallbackHandler
                
                self._client = Langfuse()
                self._handler = CallbackHandler()
                
                logger.info(f"Langfuse observability initialized for host: {settings.get_langfuse_host()}")
            except Exception as exc:
                logger.warning(f"Failed to initialize Langfuse client/callback: {exc}")
                self.enabled = False

    def get_callbacks(self) -> Optional[List[Any]]:
        """Returns LangChain callbacks list if Langfuse is configured."""
        if self.enabled and self._handler:
            return [self._handler]
        return None

    def flush(self):
        """Flushes buffered traces and spans to the Langfuse backend immediately."""
        if self.enabled and self._client:
            try:
                self._client.flush()
            except Exception as exc:
                logger.warning(f"Failed to flush Langfuse events: {exc}")


observer = LangfuseObserver()
