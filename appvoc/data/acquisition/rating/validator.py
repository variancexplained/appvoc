#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.12                                                                             #
# Filename   : /appvoc/data/acquisition/rating/validator.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 1st 2023 10:52:26 pm                                                 #
# Modified   : Wednesday August 9th 2023 03:33:51 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass
import requests

from appvoc.data.acquisition.base import Validator


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RatingValidator(Validator):
    """Validates response. Inherits the following from Validator

    response: Any = None
    valid: bool = True
    status_code: int = None
    msg: str = None
    data_error: bool = False
    client_error: bool = False
    server_error: bool = False
    """

    def is_valid(self, response: requests.Response) -> bool:
        """Validates the response object"""
        self.response = response
        self.valid = True

        self._validate_response_type()
        if self.valid:
            self._validate_response_content()
        return self.valid

    def _validate_response_type(self) -> bool:
        """Ensures the response is the correct type"""
        if self.response is None:
            self.valid = False
            self.data_error = True
            self.msg = "\n\nNo response"
            self._logger.debug(self.msg)

        elif not isinstance(self.response, dict):
            self.valid = False
            self.data_error = True
            self.msg = (
                f"\n\nInvalid response type: Response is of type {type(self.response)}."
            )
            self._logger.debug(self.msg)

        return self.valid

    def _validate_response_content(self) -> bool:
        keys = [
            "ratingAverage",
            "totalNumberOfReviews",
            "ratingCount",
            "ratingCountList",
        ]
        for key in keys:
            if key not in self.response:
                self.valid = False
                self.data_error = True
                self.msg = f"\n\nInvalid Response: {key} is missing from response."
                self._logger.debug(self.msg)
                break

            elif key == "ratingCountList":
                if len(self.response["ratingCountList"]) != 5:
                    self.valid = False
                    self.data_error = True
                    self.msg = (
                        "\n\nInvalid Response: ratingCount histogram missing data."
                    )
                    self._logger.debug(self.msg)
                    break

        return self.valid
