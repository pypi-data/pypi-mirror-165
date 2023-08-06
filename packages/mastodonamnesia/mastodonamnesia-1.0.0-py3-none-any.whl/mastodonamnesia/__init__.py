"""Package 'mastodonamnesia' level definitions."""
import sys

from typing_extensions import Final

CODE_VERSION_MAJOR: Final[int] = 1  # Current major version of this code
CODE_VERSION_MINOR: Final[int] = 0  # Current minor version of this code
CODE_VERSION_PATCH: Final[int] = 0  # Current patch version of this code

__version__: Final[
    str
] = f"{CODE_VERSION_MAJOR}.{CODE_VERSION_MINOR}.{CODE_VERSION_PATCH}"
__package_name__: Final[str] = "mastodonamnesia"
USER_AGENT: Final[
    str
] = f"MastodonAmnesia_v{__version__}_Python_{sys.version.split()[0]}"
