__title__ = "discord.py-ipc"
__author__ = "Sn1F3rt"
__license__ = "Apache Software License"
__copyright__ = "Copyright (c) 2022 Sn1F3rt"
__version__ = "1.1.0"

from typing import NamedTuple, Literal

from .client import Client
from .server import Server
from .errors import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    release_level: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=1, minor=1, micro=0, release_level="final", serial=0
)
