#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/exceptions.py                                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday April 7th 2023 10:08:23 pm                                                   #
# Modified   : Friday April 7th 2023 10:47:51 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
#                                       EXCEPTIONS                                                 #
# ------------------------------------------------------------------------------------------------ #
class EntityNotFound(Exception):
    """Exception raised when an entity is not found.

    Args:
        message (str): The string message to be displayed.
    """

    def __init__(self, message) -> None:
        super().__init__(message)


# ------------------------------------------------------------------------------------------------ #
class ProjectNotFound(EntityNotFound):
    """Exception raised when a row is not found in the project table.

    Args:
        id (int): The id for the project being queried.
    """

    def __init__(self, id: int) -> None:
        self._id = id
        self._message = f"Project id={id} not found in the Project Repository"
        super().__init__(self._message)


# ------------------------------------------------------------------------------------------------ #
class ProjectsNotFound(EntityNotFound):
    """Exception raised when no projects were found matching the query."""

    def __init__(self) -> None:
        super().__init__("No Projects were found in the repository matching search criteria.")


# ------------------------------------------------------------------------------------------------ #
class AppNotFound(EntityNotFound):
    """Exception raised when a row is not found in the appdata table.

    Args:
        id (int): The id for the app being queried.
    """

    def __init__(self, id: int) -> None:
        self._id = id
        self._message = f"App id={id} not found in the AppData Repository"
        super().__init__(self._message)


# ------------------------------------------------------------------------------------------------ #
class AppsNotFound(EntityNotFound):
    """Exception raised when no apps were found matching the query."""

    def __init__(self) -> None:
        super().__init__("No Apps were found in the repository matching search criteria.")
