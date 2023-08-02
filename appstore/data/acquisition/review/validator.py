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
# Modified   : Wednesday August 2nd 2023 12:51:33 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
import requests

from appstore.data.acquisition.base import Validator, ErrorCodes

# ------------------------------------------------------------------------------------------------ #
NO_RESPONSE = 699


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

        if self._is_valid_response_type():
            if self._is_valid_response_code():
                if self._is_valid_response_content():
                    pass
        return self.valid

    def _is_valid_response_type(self) -> bool:
        """Ensures the response is the correct type"""
        if self.response is None:
            self.error_code = ErrorCodes.no_response
            self.msg = "No response"
            self.valid = False

        if not isinstance(self.response, requests.Response):
            self.error_code = ErrorCodes.response_type_error
            self.msg = f"Invalid response type: Response is of type {type(self.response)}."
            self.valid = False

        return self.valid

    def _is_valid_response_code(self) -> bool:
        """Checks and sets status code, and error codes."""
        self.status_code = int(self.response.status_code)
        if self.status_code != 200:
            self.msg = f"Invalid response status code: {self.status_code}."
            self.valid = False
        if self.status_code > 399 and self.status_code < 500:
            self.client_error = True
        elif self.status_code > 499 and self.status_code < 600:
            self.server_error = True
        return self.valid

    def _is_valid_response_content(self) -> bool:
        if not isinstance(self.response.json(), dict):
            self.error_code = ErrorCodes.data_error
            self.msg = f"Invalid Response: Response json is of type {type(self.response.json())}."
            self.valid = False
        elif "userReviewList" not in self.response.json():
            self.error_code = ErrorCodes.data_error
            self.msg = "Invalid Response: Response json has no 'userReviewList' key."
            self.valid = False
        elif not isinstance(self.response.json()["userReviewList"], list):
            self.error_code = ErrorCodes.data_error
            self.msg = f"Invalid Response: Response json 'userReviewList' is of type {type(self.response.json()['userReviewList'])}, not a list."
            self.valid = False
        elif len(self.response.json()["userReviewList"]) == 0:
            self.error_code = ErrorCodes.data_error
            self.msg = "Invalid Response: Response json 'userReviewList' has zero length."
            self.valid = False
        return self.valid
