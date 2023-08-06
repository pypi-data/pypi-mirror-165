from enum import Enum


class environment(str, Enum):
    """Environment type."""

    docker = "docker"
    conda = "conda"
