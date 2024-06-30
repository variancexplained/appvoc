#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /tests/test_infrastructure/test_persistence/test_mysql.py                           #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday March 31st 2023 09:09:07 am                                                  #
# Modified   : Sunday June 30th 2024 02:01:37 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
import logging
import os
from datetime import datetime

import pandas as pd
import pytest
from sqlalchemy.exc import SQLAlchemyError

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"
# ------------------------------------------------------------------------------------------------ #


@pytest.mark.db
class TestMySQLDatabase:  # pragma: no cover
    # ============================================================================================ #
    def test_setup(self, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        db = container.data.db()
        query = "DROP TABLE IF EXISTS iris;"
        with db as connection:
            connection.execute(query=query)
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_insert_without_commit(self, container, dataframe, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        db = container.data.db()
        db.connect()
        _ = db.insert(data=dataframe, tablename="iris")
        db.rollback()  # Rollback has no effect when not in transaction.

        query = "SELECT * FROM iris;"
        df = db.query(query=query)
        db.close()
        assert df.shape[0] != 0
        self.test_setup(container=container, caplog=caplog)
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\nCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_insert_in_context(self, container, dataframe, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        db = container.data.db()
        with db as connection:
            rows_inserted = connection.insert(data=dataframe, tablename="iris")
        assert isinstance(rows_inserted, int)
        assert rows_inserted == dataframe.shape[0]
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\nCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_properties(self, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        db = container.data.db()
        assert db.name == "appvoc_test"
        assert db.is_connected is True
        db.close()
        assert db.is_connected is False
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_query(self, container, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        QUERY = "SELECT * FROM iris WHERE iris.Name = :name;"
        PARAMS = {"name": "Iris-virginica"}

        db = container.data.db()
        with db as connection:
            df = connection.query(query=QUERY, params=PARAMS)
        assert isinstance(df, pd.DataFrame)
        logger.debug(df)

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_update(self, container, dataframe, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        query = "UPDATE iris SET PetalWidth = :pw WHERE iris.Name = :name;"
        params = {"pw": 99, "name": "Iris-setosa"}

        db = container.data.db()
        with db as database:
            rows_updated = database.update(query=query, params=params)
        logger.debug(f"\n\nRows Updated{rows_updated}")
        assert isinstance(rows_updated, int)
        assert rows_updated == len(dataframe[dataframe["Name"] == "Iris-setosa"])
        query = "SELECT * FROM iris WHERE iris.Name = :name;"
        params = {"name": "Iris-setosa"}
        db.connect()
        df = db.query(query=query, params=params)
        db.close()
        logger.debug(f"\n\n{df}")
        self.test_query(container=container, caplog=caplog)
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_delete(self, container, dataframe, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        query = "DELETE FROM iris WHERE Name = :name;"
        params = {"name": "Iris-virginica"}

        db = container.data.db()
        with db as database:
            rows_deleted = database.delete(query=query, params=params)
        logger.debug(f"\n\nRows Deleted{rows_deleted}")
        assert isinstance(rows_deleted, int)
        assert rows_deleted == len(dataframe[dataframe["Name"] == "Iris-virginica"])

        query = "SELECT EXISTS(SELECT 1 FROM iris WHERE Name = :name LIMIT 1);"
        db.connect()
        exists = db.exists(query=query, params=params)
        assert exists is False
        db.close()
        logger.debug(f"\n\n{exists}\n{type(exists)}")
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_transaction_insert(self, container, dataframe, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        query = "SELECT * FROM iris;"
        # Confirm beginning state, not in transaction
        db = container.data.db()
        db.connect()
        result = db.in_transaction()
        assert result is False

        # Get current number of rows
        df = db.query(query=query)
        starting_rows = df.shape[0]

        # Start transaction and confirm state
        # db.begin() Apparently execute causes a transaction to begin automatically.
        result = db.in_transaction()
        assert result is True

        # Insert rows and rollback
        db.insert(data=dataframe, tablename="iris")
        db.rollback()

        # Confirm rollback
        df = db.query(query=query)
        assert df.shape[0] == starting_rows

        # Try again without rollback
        db.insert(data=dataframe, tablename="iris")

        # Get current number of rows
        df = db.query(query=query)

        # Confirm new rows added.
        assert df.shape[0] > starting_rows
        db.close()

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_transaction_update(self, container, dataframe, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        # Query to get petalwidth
        select_query = "SELECT iris.PetalWidth FROM iris WHERE iris.Name = :name AND iris.PetalLength = :pl AND iris.SepalWidth = :sw AND iris.SepalLength = :sl;"
        select_params = {"name": "Iris-setosa", "pl": 1.4, "sw": 3.5, "sl": 5.1}

        # Confirm beginning state, not in transaction
        db = container.data.db()
        db.connect()
        result = db.in_transaction()
        assert result is False

        # Get current PetalWidth for the row. Should be 99.0
        pw = db.query(query=select_query, params=select_params)
        logger.debug(f"\n\nPetalWidth = {pw}")
        assert pw["PetalWidth"].values[0] == 99.0

        # Confirm in transaction as consequency of prior query
        result = db.in_transaction()
        assert result is True

        # Update rows
        # Query to update
        query = "UPDATE iris SET PetalWidth = :pw WHERE iris.Name = :name;"
        params = {"pw": 55.0, "name": "Iris-setosa"}
        db.update(query=query, params=params)
        db.rollback()

        # Confirm rollback
        pw = db.query(query=select_query, params=select_params)
        logger.debug(f"\n\nPetalWidth = {pw}")
        assert pw["PetalWidth"].values[0] == 99.0

        # Try again without rollback
        db.update(query=query, params=params)

        # Confirm rows updated
        pw = db.query(query=select_query, params=select_params)
        logger.debug(f"\n\nPetalWidth = {pw}")
        assert pw["PetalWidth"].values[0] == 55.0
        db.close()

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_transaction_insert_autocommit(self, container, dataframe, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        query = "SELECT * FROM iris;"
        # Confirm beginning state, not in transaction
        db = container.data.db()
        db.connect(autocommit=True)
        result = db.in_transaction()
        assert result is False

        # Get current number of rows
        df = db.query(query=query)
        starting_rows = df.shape[0]

        # Start transaction and confirm state
        # db.begin() Apparently execute causes a transaction to begin automatically.
        result = db.in_transaction()
        assert result is True

        # Insert rows and rollback
        db.insert(data=dataframe, tablename="iris")
        db.rollback()

        # Confirm rollback had no effect
        df = db.query(query=query)
        assert df.shape[0] > starting_rows

        # close
        db.close()

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_transaction_update_autocommit(self, container, dataframe, caplog):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        # Query to get petalwidth
        select_query = "SELECT iris.PetalWidth FROM iris WHERE iris.Name = :name AND iris.PetalLength = :pl AND iris.SepalWidth = :sw AND iris.SepalLength = :sl;"

        select_params = {"name": "Iris-setosa", "pl": 1.4, "sw": 3.5, "sl": 5.1}

        # Confirm beginning state, not in transaction
        db = container.data.db()
        db.connect(autocommit=True)
        result = db.in_transaction()
        assert result is False

        # Get current PetalWidth for the row. Should be 99.0
        pw = db.query(query=select_query, params=select_params)
        logger.debug(f"\n\nPetalWidth = {pw}")
        assert pw["PetalWidth"].values[0] == 99.0

        # Confirm in transaction as consequency of prior query
        result = db.in_transaction()
        assert result is True

        # Update rows
        # Query to update
        query = "UPDATE iris SET PetalWidth = :pw WHERE iris.Name = :name;"
        params = {"pw": 55.0, "name": "Iris-setosa"}
        db.update(query=query, params=params)
        db.rollback()

        # Confirm rollback had no effect
        pw = db.query(query=select_query, params=select_params)
        logger.debug(f"\n\nPetalWidth = {pw}")
        assert pw["PetalWidth"].values[0] == 55.0

        db.close()
        db.dispose()

        with pytest.raises(SQLAlchemyError):
            db.query(query=select_query, params=select_params)

        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)

    # ============================================================================================ #
    def test_backup_restore(
        self,
        container,
        app_repo_loaded,
        rating_repo_loaded,
        review_repo_loaded,
        caplog,
    ):
        start = datetime.now()
        logger.info(
            "\n\nStarted {} {} at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                start.strftime("%I:%M:%S %p"),
                start.strftime("%m/%d/%Y"),
            )
        )
        logger.info(double_line)
        # ---------------------------------------------------------------------------------------- #
        directory = "tests/data/database/backup"
        os.makedirs(name=directory, exist_ok=True)
        filename = "appvoc_" + datetime.now().strftime("%Y-%m-%dT%H%M%S") + ".sql"
        filepath = os.path.join(directory, filename)
        filepath = os.path.abspath(filepath)
        db = container.data.db()
        logger.debug("Backing up database")
        db.backup(filepath=filepath)
        logger.debug("Backup complete")
        assert os.path.exists(filepath)

        # Delete Appdata
        query = "DELETE FROM app;"
        params = {}
        db.delete(query=query, params=params)
        logger.debug("Deleted app")
        db.commit()

        # Delete Rating
        query = "DELETE FROM rating;"
        params = {}
        db.delete(query=query, params=params)
        logger.debug("Deleted rating")
        db.commit()

        # Delete Review
        query = "DELETE FROM review;"
        params = {}
        db.delete(query=query, params=params)
        logger.debug("Deleted reviews")
        db.commit()

        # Restore
        logger.debug("Restoring database")
        db.restore(filepath=filepath)
        logger.debug("Database restored")
        db.commit()

        # Get app
        query = "SELECT * FROM app;"
        params = None
        app = db.query(query=query, params=params)
        assert app.shape[0] == 100
        logger.debug(app.head())

        # Get rating
        query = "SELECT * FROM rating;"
        params = None
        rating = db.query(query=query, params=params)
        assert rating.shape[0] == 100
        logger.debug(rating.head())

        # Get app
        query = "SELECT * FROM review;"
        params = None
        review = db.query(query=query, params=params)
        assert review.shape[0] == 100
        logger.debug(review.head())
        # ---------------------------------------------------------------------------------------- #
        end = datetime.now()
        duration = round((end - start).total_seconds(), 1)

        logger.info(
            "\n\tCompleted {} {} in {} seconds at {} on {}".format(
                self.__class__.__name__,
                inspect.stack()[0][3],
                duration,
                end.strftime("%I:%M:%S %p"),
                end.strftime("%m/%d/%Y"),
            )
        )
        logger.info(single_line)
