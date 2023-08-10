#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/review/validator.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 1st 2023 10:52:26 pm                                                 #
# Modified   : Wednesday August 9th 2023 07:34:46 pm                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
import requests

from appstore.data.acquisition.base import Validator


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ReviewValidator(Validator):
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
            self.msg = f"Invalid response type: Response is of type {type(self.response)}."
            self._logger.debug(self.msg)

        return self.valid

    def _validate_response_content(self) -> bool:  # pragma: no cover
        if not isinstance(self.response.json(), dict):
            self.data_error = True
            self.msg = f"Invalid Response: Response json is of type {type(self.response.json())}."
            self._logger.debug(msg=self.msg)
            self.valid = False
        elif "userReviewList" not in self.response.json():
            self.data_error = True
            self.msg = "Invalid Response: Response json has no 'userReviewList' key."
            self._logger.debug(msg=self.msg)
            self.valid = False
        elif not isinstance(self.response.json()["userReviewList"], list):
            self.data_error = True
            self.msg = f"Invalid Response: Response json 'userReviewList' is of type {type(self.response.json()['userReviewList'])}, not a list."
            self._logger.debug(msg=self.msg)
            self.valid = False
        elif len(self.response.json()["userReviewList"]) == 0:
            self.data_error = True
            self.msg = "Invalid Response: Response json 'userReviewList' has zero length."
            self._logger.debug(msg=self.msg)
            self.valid = False
        return self.valid
