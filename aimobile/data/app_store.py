#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/data/app_store.py                                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Monday March 27th 2023 12:41:54 pm                                                  #
# Modified   : Tuesday March 28th 2023 02:41:11 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import os
from datetime import datetime
import logging
import time
import random

from tqdm import tqdm
import pandas as pd
from itunes_app_scraper.scraper import AppStoreScraper
from app_store_scraper import AppStore

from aimobile.data.base import APPLE_CATEGORIES, AppCentre, AppCentreBuilder
from aimobile.services.io import IOService


# ------------------------------------------------------------------------------------------------ #
class AppleCentre(AppCentre):
    """Class encapsulating the Apple Appstore Data

    Args:
        directory (str): The home directory for data and reviews.
    """

    def __init__(self, directory: str, io: IOService = IOService) -> None:
        self._directory = directory
        self._io = io
        self._app_data = None  # Contains the data for a category
        self._app_reviews = None  # Contains the reviews for a category
        self._category = None  # The current category

    def get_category_data(self, category: str) -> pd.DataFrame:
        """Returns a DataFrame with app data for a category.

        Args:
            category (str): The app category
        """
        if self._category == category:
            return self._app_data
        else:
            self._category = category
            filename = category + "_data.pkl"
            filepath = os.path.join(self._directory, filename)
            self._app_data = self._io.read(filepath=filepath)
            return self._app_data

    def get_category_reviews(self, category: str) -> pd.DataFrame:
        """Return the reviews for a category in DataFrame format.

        Args:
            category (str): The app category
        """
        if self._category == category:
            return self._app_reviews
        else:
            self._category = category
            filename = category + "_reviews.pkl"
            filepath = os.path.join(self._directory, filename)
            self._app_reviews = self._io.read(filepath=filepath)
            return self._app_reviews

    def get_app_data(self, category: str, app_id: str) -> dict:
        """Return the app data

        Args:
            category (str): The app category
            app_id (str): The app id
        """
        if self._category == category:

            return self._app_data[self._app_data["app_id"] == app_id].to_dict()
        else:
            data = self.get_category_data(category=category)
            return data[data["app_id"] == app_id].to_dict()

    def get_app_review(self, category: str, app_id: str) -> dict:
        """Return the app review

        Args:
            app_id (str): The app id
        """
        if self._category == category:
            return self._app_reviews[self._app_reviews["app_id"] == app_id].to_dict()
        else:
            reviews = self.get_category_reviews(category=category)
            return reviews[reviews["app_id"] == app_id].to_dict()


# ------------------------------------------------------------------------------------------------ #
class AppleCentreBuilder(AppCentreBuilder):
    """Constructs the AppCentre using data scraped from the AppStore."""

    def __init__(self, io: IOService = IOService) -> None:
        self._appcentre = None
        self._scraper = None
        self._started = None
        self._ended = None
        self._duration = None
        self._directory = None
        self._io = io
        self._logger = logging.getLogger(
            f"{self.__module__}.{self.__class__.__name__}",
        )

    @property
    def appcentre(self) -> AppleCentre:
        return self._appcentre

    def build_app_centre(
        self,
        directory: str = "data/apple/",
        categories: list = None,
        num_apps: int = 1e10,
        reviews_after: datetime = datetime(year=2020, month=1, day=1),
    ) -> None:
        """Controls the construction of the AppleCentre object

        Args:
            directory (str): The home directory for the AppleCentre files
            categories (list): list of dictionaries. Each k,v pair is a category name and id
            num_apps (int): The maximum number of app_ids to return per query. Default 1e10.
            reviews_after (datetime): The start date for reviews

        """
        self._directory = directory
        self._reviews_after = reviews_after
        categories = categories or APPLE_CATEGORIES

        # Perform some boilerplate at startup
        self._setup()

        # Instantiate the scraper
        scraper = AppStoreScraper()

        # Iterate over the categories of apps in the appstore.
        for category, category_id in tqdm(categories.items()):
            app_ids = scraper.get_app_ids_for_collection(
                category=category_id, num=num_apps, country="us"
            )
            for app_id in app_ids:
                detail = scraper.get_app_details(
                    app_id=app_id,
                    country="us",
                    add_ratings=True,
                    flatten=True,
                    sleep=random.randint(5, 10),
                )
                ratings = detail["user_ratings"]
                del detail["user_ratings"]

        self._teardown()

    def _build_category(self, category: str, category_id: int) -> None:
        """Controls the construction of the category data"""

        self._logger.info(f"\nLoading the {category} category.")

        app_data = []
        app_ratings = []
        app_reviews = []

        # Obtain all the app_ids for the category.
        app_ids = self._scraper.get_app_ids_for_collection(category=category_id)

        # Iterate over ids and obtain app data, ratings and reviews.
        for app_id in app_ids:
            details = self._scraper.get_app_details(
                app_id=app_id,
                country="us",
                add_ratings=True,
                flatten=True,
                sleep=random.randint(5, 10),
            )
            ratings = details["user_ratings"]
            del details["user_ratings"]

        # Build and save the app metadata for the category.
        app_data = self._build_save_category_data(category=category, app_ids=app_ids)

        # Persist the app data in the designated data directory.
        self._build_save_category_reviews(category=category, app_data=app_data)

    def _build_save_category_data(self, category: str, app_ids: list) -> list:
        """Creates and saves the app metadata for the category."""

        self._logger.info(f"\n\tLoading the {category} category metadata.")

        # Obtain the app metadata for app_ids
        app_data = list(
            self._scraper.get_multiple_app_details(
                app_ids=app_ids,
                country="us",
                add_ratings=True,
                sleep=random.randint(5, 10),
            )
        )

        return app_data

    def _build_save_category_reviews(self, category: str, app_data: list) -> None:
        """Extracts and saves the review data for all apps in the category"""

        category_reviews = None

        self._logger.info(f"\n\tLoading the {category} category reviews.")

        app_ids = list(app_data["app_id"])
        app_names = list(app_data["app_name"])

        for app_name, app_id in zip(app_names, app_ids):

            # Instantiate Appstore for app
            app = AppStore(country="us", app_name=app_name, app_id=app_id)

            # Scrape reviews posted since January 1, 2020.
            # Delay 15-25 seconds between calls.
            app.review(after=self._reviews_after, sleep=random.randint(5, 10))
            reviews = app.reviews

            # Add app name and id to the review data
            for review in reviews:
                review["app_name"] = app_name
                review["app_id"] = app_id

            self._logger.info(
                f"\n\tScraping of {app_name} app is complete. Review count = {app.reviews_count}"
            )

            # Convert the reviews to a DataFrame
            df = pd.DataFrame(reviews)
            category_reviews = (
                df if category_reviews is None else pd.concat([category_reviews, df], axis=0)
            )

            # Wait 5 to 10 seconds to start scraping next app
            time.sleep(random.randint(5, 10))

        # Save category reviews to the category directory.
        filename = category.lower() + "_reviews.pkl"
        self._save(category=category, filename=filename, data=category_reviews)

    def _setup(self) -> None:
        self._started = datetime.now()
        os.makedirs(self._directory, exist_ok=True)
        self._logger.info(f"\n{self.__class__.__name__} has started.")
        self._appcentre = AppleCentre(directory=self._directory)

    def _teardown(self) -> None:
        self._ended = datetime.now()
        self._duration = (self._ended - self._started).total_seconds()
        self._logger.info(
            f"\n{self.__class__.__name__} has ended. Duration = {self._duration} seconds"
        )

    def _save(self, category: str, filename: str, data: pd.DataFrame) -> None:
        filepath = os.path.join(self._directory, filename)
        self._io.write(filepath, data=data)
