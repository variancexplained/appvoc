#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appstore/data/acquisition/rating/validator.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 1st 2023 10:52:26 pm                                                 #
# Modified   : Wednesday August 2nd 2023 03:11:26 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
import requests

from appstore.data.acquisition.base import Validator, ErrorCodes


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingValidator(Validator):
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
            if self._is_valid_response_content():
                pass
        return self.valid

    def _is_valid_response_type(self) -> bool:
        """Ensures the response is the correct type"""
        if self.response is None:
            self.error_code = ErrorCodes.no_response
            self.msg = "No response"
            self.valid = False

        elif not isinstance(self.response, dict):
            self.error_code = ErrorCodes.response_type_error
            self.msg = f"Invalid response type: Response is of type {type(self.response)}."
            self.valid = False

        return self.valid

    def _is_valid_response_content(self) -> bool:
        keys = ["ratingAverage", "totalNumberOfReviews", "ratingCount", "ratingCountList"]
        for key in keys:
            if key not in self.response:
                self.error_code = ErrorCodes.data_error
                self.msg = f"Invalid Response: {key} is missing from response."
                self.valid = False
            elif key == "ratingCountList":
                if len(self.response["ratingCountList"]) != 5:
                    self.error_code = ErrorCodes.data_error
                    self.msg = "Invalid Response: ratingCount histogram missing data."
                    self.valid = False

        return self.valid
