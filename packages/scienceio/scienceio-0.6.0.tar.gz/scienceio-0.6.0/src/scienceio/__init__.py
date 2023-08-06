import os

from .scienceio import ScienceIO  # noqa

__version__ = os.environ.get("SCIENCEIO_SDK_VERSION", "v0.0.1")
