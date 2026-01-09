import os

from slowapi import Limiter
from slowapi.util import get_remote_address

# During pytest runs the client reuses the same remote address which can
# hit rate limits across test cases. Detect pytest and relax limits to
# avoid flaky 429 responses in tests.
if os.getenv("PYTEST_CURRENT_TEST") or os.getenv("TESTING"):
    limiter = Limiter(key_func=get_remote_address, default_limits=["10000/minute"])
else:
    limiter = Limiter(key_func=get_remote_address)
