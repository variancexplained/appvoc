#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/acquisition/scraper/base/response.py                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday April 29th 2023 06:33:14 am                                                #
# Modified   : Saturday April 29th 2023 08:33:17 am                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod

from aimobile.data.acquisition.scraper.base.result import Result
from aimobile.infrastructure.web.session import SessionHandler


# ------------------------------------------------------------------------------------------------ #
class ResponseParser(ABC):
    @abstractmethod
    def parse(self, session: SessionHandler) -> Result:
        """Parses a session response and returns a Result object."""
