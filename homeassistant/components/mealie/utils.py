"""Mealie util functions."""

from awesomeversion import AwesomeVersion


def create_version(version: str) -> AwesomeVersion:
    """Convert beta versions to PEP440."""
    return AwesomeVersion(version.removeprefix("v").replace("beta-", "b"))
