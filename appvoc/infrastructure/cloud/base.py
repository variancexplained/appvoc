#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/manage/base.py                                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday August 24th 2023 06:12:37 pm                                               #
# Modified   : Thursday August 24th 2023 07:17:12 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Defines interfaces for Data Management"""
from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------ #
class CloudStorageManager(ABC):
    """Defines interface for cloud storage managers"""

    @abstractmethod
    def upload(self, filepath: str, *args, **kwargs) -> bool:
        """Uploads a file to the cloud service provider"""

    @abstractmethod
    def download(self, filepath: str, *args, **kwargs) -> bool:
        """Downloads a file from the cloud service provider"""

    @abstractmethod
    def exists(self, *args, **kwargs) -> bool:
        """Evaluates existence of an object on the cloud service."""

    @abstractmethod
    def remove(self, *args, **kwargs) -> bool:
        """Removes an object from cloud service."""
