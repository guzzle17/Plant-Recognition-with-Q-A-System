"""
AWS utility functions and helpers.

This module provides utility functions for working with AWS services,
including retry logic and error handling.
"""

import time
from functools import wraps
from typing import Callable, Any
from app.core.logging import get_logger
from app.core.exceptions import BedrockServiceError

logger = get_logger(__name__)


def retry_on_throttle(max_retries: int = 3, initial_delay: float = 1.0):
    """
    Decorator to retry AWS API calls on throttling errors.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries (doubles each time)

    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    error_msg = str(e).lower()

                    # Check if it's a throttling error
                    if any(term in error_msg for term in ["throttl", "rate", "limit"]):
                        if attempt < max_retries:
                            logger.warning(
                                f"Throttling detected, retrying in {delay}s "
                                f"(attempt {attempt + 1}/{max_retries})"
                            )
                            time.sleep(delay)
                            delay *= 2  # Exponential backoff
                            continue

                    # If it's not a throttling error, raise immediately
                    raise

            # If all retries failed, raise the last exception
            raise BedrockServiceError(
                f"Failed after {max_retries} retries",
                details={"last_error": str(last_exception)}
            )

        return wrapper
    return decorator

