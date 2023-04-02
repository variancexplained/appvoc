#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/scraper/appstore/uow/sqlite.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 07:38:30 pm                                                  #
# Modified   : Saturday April 1st 2023 12:14:06 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from aimobile.data.scraper.appstore.uow.base import UnitOfWork


class SQLiteUnitOfWork(UnitOfWork):
    """An implementation of a UnitOfWork for a SQLite storage database.
    Methods: __enter__, __exit__, commit, rollback, books
    """

    def __init__(self, location):
        """SQLiteUnitOfWork's constructor."""
        self.location = location

    def __enter__(self):
        """View @app.domain.ports.UnitOfWork."""
        self.conn = sqlite3.connect(self.location)
        return self

    def __exit__(self, type, value, traceback):
        """View @app.domain.ports.UnitOfWork."""
        self.conn.close()

    def commit(self):
        """View @app.domain.ports.UnitOfWork."""
        self.conn.commit()

    def rollback(self):
        """View @app.domain.ports.UnitOfWork."""
        self.conn.rollback()

    @property
    def books(self) -> SQLiteBookRepository:
        """View @app.domain.ports.UnitOfWork."""
        return SQLiteBookRepository(self.conn.cursor())
