"""pytest plugin — loaded via `-p pytest_plugin` in pytest.ini.

Runs before Django settings load, so tests get a real SECRET_KEY instead of
the dev placeholder (which settings.py rejects when DEBUG=False).
"""

import os

os.environ.setdefault("SECRET_KEY", "test-only-insecure-secret-key")
