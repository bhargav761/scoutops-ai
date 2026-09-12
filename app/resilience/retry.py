import time
from collections.abc import Callable


def retry(
    function: Callable,
    attempts: int = 2,
    delay_seconds: int = 1,
):
    last_error = None

    for attempt in range(attempts):
        try:
            return function()

        except Exception as exc:
            last_error = exc

            message = str(exc).lower()

            # Do not repeatedly retry exhausted API quotas.
            if "429" in message or "resource_exhausted" in message:
                raise

            if attempt == attempts - 1:
                raise

            time.sleep(delay_seconds)

    raise last_error
