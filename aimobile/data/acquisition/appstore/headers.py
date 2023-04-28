#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/appstore/headers.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 8th 2023 09:57:42 am                                                 #
# Modified   : Friday April 28th 2023 02:10:05 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Headers Module."""
from __future__ import annotations
import random

from aimobile.data.acquisition.appstore import HEADERS, STOREFRONTS
from aimobile.data.acquisition.appstore.base import Header


# ------------------------------------------------------------------------------------------------ #
#                                      BROWSER HEADERS                                              #
# ------------------------------------------------------------------------------------------------ #


class BrowserHeader(Header):
    """Iteratively and randomly returns HTTP Browser headers

    Args:
        headers (list): List of browser header dictionaries
    """

    def __init__(self, headers: list = HEADERS) -> None:
        self._headers = headers
        self._header = None

    def __iter__(self):
        """Initializes the iteration"""
        return self

    def __next__(self):
        """Returns a randomly selected header."""

        while True:
            header = random.choice(self._headers)
            if header != self._header:
                self._header = header
                return header


# ------------------------------------------------------------------------------------------------ #
#                                    STOREFRONT HEADERS                                            #
# ------------------------------------------------------------------------------------------------ #


class AppleStoreFrontHeader(Header):
    """Iteratively serves up Apple App Store Headers

    Args:
        headers (list): List of header dictionaries containing App StoreFront Headers
    """

    def __init__(self, headers=STOREFRONTS) -> None:
        self._headers = headers
        self._header = None

    def __iter__(self):
        """Initializes the iteration"""
        return self

    def __next__(self):
        """Returns a randomly selected header."""

        while True:
            header = random.choice(self._headers)
            if header != self._header:
                self._header = header
                return header
