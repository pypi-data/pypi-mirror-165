import sys
from importlib.metadata import PackageNotFoundError, version

# Check that we're not running on an unsupported Python version.
if sys.version_info < (3, 9):
    print("matrix_alertbot requires Python 3.9 or above.")
    sys.exit(1)

try:
    __version__ = version("matrix_alertbot")
except PackageNotFoundError:
    # package is not installed
    pass
