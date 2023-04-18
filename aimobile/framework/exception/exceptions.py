#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/exceptions.py                                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday April 7th 2023 10:08:23 pm                                                   #
# Modified   : Sunday April 16th 2023 02:27:53 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
#                                       EXCEPTIONS                                                 #
# ------------------------------------------------------------------------------------------------ #
class ProgrammingError(Exception):
    """Exception raised when a programming error is encountered.

    Args:
        message (str): The string message to be displayed.
    """

    def __init__(self, message) -> None:
        super().__init__(message)


# ------------------------------------------------------------------------------------------------ #
class InvalidMode(Exception):
    """Exception raised when an invalid mode is encountered.

    Args:
        message (str): The string message to be displayed.
    """

    def __init__(self, message) -> None:
        super().__init__(message)


# ------------------------------------------------------------------------------------------------ #
class ObjectNotFound(Exception):
    """Object not found exception

    Args:
        id (int): Object id. Optional.
        name (str): Object name. Optional.
    """

    def __init__(self, id: int = None, name: str = None) -> None:
        id = "" if id is None else f" id = {id}"
        name = "" if name is None else f" name = {name}"
        message = f"Object {id} {name} not found in the Repository."
        super().__init__(message)
