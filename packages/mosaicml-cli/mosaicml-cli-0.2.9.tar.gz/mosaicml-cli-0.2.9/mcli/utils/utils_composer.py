"""Composer Utils for validating composer configs"""
from pathlib import Path

from mcli.config import COMPOSER_INSTALLED


def is_composer_installed() -> bool:
    """Returns `True` if the `composer` library is installed.
    """
    return COMPOSER_INSTALLED


def assert_composer_installed():
    """Raises an `ImportError` if `composer` is not installed.
    """
    if not COMPOSER_INSTALLED:
        raise ImportError('Could not find composer library. Please install it using `pip install mosaicml`.')


def get_composer_directory() -> Path:
    """Returns the directory path for `composer`, if installed.

    Returns:
        Path: path to `composer` root directory
    """
    assert_composer_installed()

    # pylint: disable-next=import-outside-toplevel
    import composer  # type: ignore
    return Path(composer.__file__).parents[0]
