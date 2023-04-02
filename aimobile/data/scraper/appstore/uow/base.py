#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/uow/base.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 06:56:50 pm                                                  #
# Modified   : Friday March 31st 2023 07:34:48 pm                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------ #
class UnitOfWork(ABC):
    """Abstract base class defining the interface for the UnitOfWork subclasses.

    A unit of work describes a single database transaction involving multiple database
    operations, which are committed later when the codee from the service demands it, or
    the object context has ended.

    """

    @abstractmethod
    def __enter__(self):
        """ "Automatically creates and returns the databasee connection object."""

    @abstractmethod
    def __exit__(self, type, value, traceback):
        """Releases the resources occupied by the current context."""

    @abstractmethod
    def commit(self):
        """Saves the pending database operations to the database."""

    @abstractmethod
    def rollback(self):
        """Returns the database state to that of the last commit."""
