#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/utils/network.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday April 4th 2023 12:33:43 pm                                                  #
# Modified   : Tuesday April 4th 2023 02:40:57 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Module for Network Related Utilities"""
# ProtonVPN isn't supported on WSL2
import os
from abc import ABC, abstractmethod
import subprocess
from dotenv import load_dotenv


# ------------------------------------------------------------------------------------------------ #
class VPN(ABC):
    """Base class for VPN classes."""

    @abstractmethod
    def login(self) -> None:
        """Logs in to the VPN"""

    @abstractmethod
    def status(self) -> None:
        """Checks status of connection."""

    @abstractmethod
    def change_ip(self) -> None:
        """Changes the VPN IP address."""

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnects the VPN"""


# ------------------------------------------------------------------------------------------------ #
class ProtonVPN(VPN):
    """ProtonVPN Manager"""

    def __init__(self) -> None:
        load_dotenv()
        self._uid = os.getenv("VPN_USERNAME")
        self._pwd = os.getenv("VPN_PASSWORD") + "\n"

    def login(self) -> None:
        """Logs in to the VPN"""
        command = "protonvpn-cli login " + self._uid
        proc = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        proc.stdin.write(self._pwd)
        proc.stdin.flush()

    def change_ip(self):
        command = "sudo protonvpn-cli c -r"
        _ = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def disconnect(self):
        command = "sudo protonvpn-cli d"
        _ = subprocess.Popen(
            command,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
