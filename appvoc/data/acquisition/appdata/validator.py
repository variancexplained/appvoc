#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/acquisition/appdata/validator.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 1st 2023 10:52:26 pm                                                 #
# Modified   : Wednesday August 30th 2023 11:31:38 am                                              #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
import requests

from appvoc.data.acquisition.base import Validator


# ------------------------------------------------------------------------------------------------ #
@dataclass
class AppDataValidator(Validator):
    """Validates response. Inherits the following from Validator

    response: Any = None
    valid: bool = True
    status_code: int = None
    error_code: int = None
    msg: str = None
    client_error: bool = False
    server_error: bool = False
    """

    def is_valid(self, response: requests.Response) -> bool:
        """Validates the response object"""
        self.response = response
        self.valid = True

        self._validate_status_code()
        if self.valid:
            self._validate_response_type()
            if self.valid:
                self._validate_response_content()
        return self.valid

    def _validate_response_type(self) -> bool:
        """Ensures the response is the correct type"""
        if self.response is None:
            self.valid = False
            self.data_error = True
            self.msg = "No response"
            self._logger.debug(self.msg)

        elif not isinstance(self.response, requests.Response):
            self.valid = False
            self.server_error = True
            self.msg = (
                f"Invalid response type: Response is of type {type(self.response)}."
            )
            self._logger.debug(self.msg)

        return self.valid

    def _validate_response_content(self) -> bool:  # pragma: no cover
        try:
            if not isinstance(self.response.json(), dict):
                self.data_error = True
                self.msg = f"Invalid Response: Response json is of type {type(self.response.json())}."
                self._logger.debug(msg=self.msg)
                self.valid = False
            elif len(self.response.json()["results"]) == 0:
                self.data_error = True
                self.msg = "Invalid Response: Response json 'results' has zero length."
                self._logger.debug(msg=self.msg)
                self.valid = False
        except requests.JSONDecodeError:
            self.valid = False

        return self.valid
