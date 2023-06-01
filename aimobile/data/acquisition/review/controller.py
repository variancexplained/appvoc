#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Controller    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /aimobile/data/acquisition/review/controller.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday April 20th 2023 05:33:57 am                                                #
# Modified   : Thursday June 1st 2023 11:16:32 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""AppStore Scraper Controller Module"""
import os
import sys
import logging
from dotenv import load_dotenv
import datetime

import numpy as np

import pandas as pd


from aimobile.data.acquisition import AppStoreCategories
from aimobile.data.acquisition.review.scraper import ReviewScraper
from aimobile.data.acquisition.rating.scraper import RatingScraper

from aimobile.data.acquisition.base import Controller


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE REVIEW CONTROLLER                                            #
# ------------------------------------------------------------------------------------------------ #
class ReviewController(Controller):
    """Controls the App Store Review scraping process

    Args:
        scraper (ReviewScraper): A scraper object that returns data from the target urls.
        min_ratings (int): Since we want apps with a minimum number of reviews, and we don't
            have the number of reviews per app, we are using the number of ratings as
            a proxy for the number of reviews. The default is 20
        max_pages (int): Puts a maximum on the total number of pages to request.
        max_results_per_page (int): This is the limit of results to return on each request.
        verbose (int): An indicator of the level of progress reporting verbosity. Progress
            will be printed to stdout for each 'verbose' number of apps processed.

    Inherited Member Variables:
        uow (UoW): Unit of Work Class containing all repositories.
    """

    def __init__(
        self,
        scraper: type[ReviewScraper] = ReviewScraper,
        min_ratings: int = 20,
        max_pages: int = sys.maxsize,
        max_results_per_page: int = 400,
        verbose: int = 10,
    ) -> None:
        super().__init__()
        self._scraper = scraper
        self._min_ratings = min_ratings
        self._max_pages = max_pages
        self._max_results_per_page = max_results_per_page
        self._verbose = verbose

        # State managers
        self._current_category_id = None
        self._current_category = None
        self._current_app_id = None
        self._current_app_name = None

        # Stats
        self._project_stats = {
            "categories": 0,
            "apps": 0,
            "reviews": 0,
            "pages": 0,
            "started": None,
            "ended": None,
            "duration": None,
        }
        self._category_stats = {
            "category_id": None,
            "category": None,
            "apps": 0,
            "apps_with_min_ratings": 0,
            "apps_with_reviews": 0,
            "apps_to_process": 0,
            "app_count": 0,
            "reviews": 0,
            "reviews_per_app": [],
            "min_reviews_per_app": 0,
            "max_reviews_per_app": 0,
            "ave_reviews_per_app": 0,
            "pages": 0,
            "started": None,
            "ended": None,
            "duration": None,
        }
        self._app_stats = {"id": None, "name": None, "reviews": 0}

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def scrape(self, category_ids: str) -> None:
        """Scrapes app data matching the search term from the target URL.

        Args:
            category_ids (str): Category id or a list of category ids from AppStoreCategories
        """
        load_dotenv()
        status = os.getenv("APPSTORE_REVIEWS_SCRAPED")
        if status in [True, "True", "true"]:
            msg = "\n\nAppstore Review Scraped Status is Complete. Skipping App Store Review Scraping Operation."
            self._logger.info(msg)
        else:
            self._scrape(category_ids=category_ids)

        self._teardown()

    def summarize(self) -> pd.DataFrame:
        """Returns a DataFrame summarizing the data extracted"""
        return self.uow.review_repository.summarize()

    def archive(self) -> None:
        """Saves the repository to an archive"""
        self.uow.review_repository.export()

    def _scrape(self, category_ids: str) -> None:
        category_ids = [category_ids] if isinstance(category_ids, (str, int)) else category_ids

        self._start_project(category_ids=category_ids)

        for category_id in category_ids:
            apps = self._start_category(category_id=category_id)

            for _, row in apps.iterrows():
                self._start_app(row=row)

                for scraper in self._scraper(
                    app_id=row["id"],
                    app_name=row["name"],
                    category_id=row["category_id"],
                    category=row["category"],
                    max_pages=self._max_pages,
                    max_results_per_page=self._max_results_per_page,
                ):
                    self._start_page()
                    self._save_page(scraper.result)
                    self._end_page(scraper.result)

                self._end_app()

            self._end_category()

        self._end_project()

    def _start_project(self, category_ids: list) -> None:
        self._project_stats["categories"] = len(category_ids)
        self._project_stats["started"] = datetime.datetime.now()
        msg = f"\n\nController with {self._project_stats['categories']} categories started at {self._project_stats['started'].strftime('%m/%d/%Y, %H:%M:%S')}\n"
        self._logger.info(msg)

    def _end_project(self) -> None:
        self._project_stats["ended"] = datetime.datetime.now()
        self._project_stats["duration"] = str(
            datetime.timedelta(
                seconds=(
                    self._project_stats["ended"] - self._project_stats["started"]
                ).total_seconds()
            )
        )
        self._announce_project_end()

    def _announce_project_end(self) -> None:
        width = 24
        msg = f"\n\n{'Controller Summary'}\n"
        msg += f"\t{'Categories:'.rjust(width, ' ')} | {self._project_stats['categories']}\n"
        msg += f"\t{'Apps:'.rjust(width, ' ')} | {self._project_stats['apps']}\n"
        msg += f"\t{'Reviews:'.rjust(width, ' ')} | {self._project_stats['reviews']}\n"
        msg += f"\t{'Scrapers:'.rjust(width, ' ')} | {self._project_stats['pages']}\n"
        msg += f"\t{'Started:'.rjust(width, ' ')} | {self._project_stats['started']}\n"
        msg += f"\t{'Ended:'.rjust(width, ' ')} | {self._project_stats['ended']}\n"
        msg += f"\t{'Duration:'.rjust(width, ' ')} | {self._project_stats['duration']}\n"
        self._logger.info(msg)

    def _teardown(self) -> None:
        self.uow.review_repository.export()

    def _start_category(self, category_id: int) -> pd.DataFrame:
        """Obtains apps for the category, removing any apps for which reviews exist."""

        self._current_category_id = category_id
        self._current_category = AppStoreCategories.NAMES[category_id]

        self._category_stats["category_id"] = self._current_category_id
        self._category_stats["category"] = self._current_category
        self._category_stats["reviews_per_app"] = []
        self._category_stats["app_count"] = 0
        self._category_stats["reviews"] = 0
        self._category_stats["min_reviews_per_app"] = 0
        self._category_stats["max_reviews_per_app"] = 0
        self._category_stats["ave_reviews_per_app"] = 0
        self._category_stats["pages"] = 0
        self._category_stats["started"] = datetime.datetime.now()

        # Obtain all apps for the category from the repository.
        apps = self.uow.appdata_repository.get_by_category(category_id=category_id)
        self._category_stats["apps"] = len(apps)

        # Filter the apps that have greater than 'min_ratings'
        apps = apps.loc[apps["ratings"] > self._min_ratings]
        self._category_stats["apps_with_min_ratings"] = len(apps)

        # Obtain apps for which we've already processed the reviews.
        reviews = self.uow.review_repository.get_by_category(category_id=category_id)
        apps_with_reviews = reviews["app_id"].unique()
        self._category_stats["apps_with_reviews"] = len(apps_with_reviews)

        # Remove apps for which reviews exist from the list of apps to process.
        if len(apps_with_reviews) > 0:
            apps = apps.loc[~apps["id"].isin(apps_with_reviews)]
        self._category_stats["apps_to_process"] = len(apps)

        # Announce Category
        self._announce_category_start()
        return apps

    def _announce_category_start(self) -> None:
        width = 32
        msg = f"\n\nCategory: {self._current_category_id}-{self._current_category} Started at {self._category_stats['started'].strftime('%m/%d/%Y, %H:%M:%S')}\n"
        msg += f"\t{'Apps in Category:'.rjust(width, ' ')} | {self._category_stats['apps']}\n"
        msg += f"\t{'Apps with Min Ratings:'.rjust(width, ' ')} | {self._category_stats['apps_with_min_ratings']}\n"
        msg += f"\t{'Apps with Reviews:'.rjust(width, ' ')} | {self._category_stats['apps_with_reviews']}\n"
        msg += f"\t{'Apps to Process:'.rjust(width, ' ')} | {self._category_stats['apps_to_process']}\n"
        self._logger.info(msg)

    def _end_category(self) -> None:
        self._category_stats["min_reviews_per_app"] = np.min(
            self._category_stats["reviews_per_app"]
        )
        self._category_stats["max_reviews_per_app"] = np.max(
            self._category_stats["reviews_per_app"]
        )
        self._category_stats["ave_reviews_per_app"] = np.mean(
            self._category_stats["reviews_per_app"]
        )
        self._category_stats["ended"] = datetime.datetime.now()
        self._category_stats["duration"] = str(
            datetime.timedelta(
                seconds=(
                    self._category_stats["ended"] - self._category_stats["started"]
                ).total_seconds()
            )
        )
        self._announce_category_end()

    def _announce_category_end(self) -> None:
        width = 24
        msg = f"\n\nCategory: {self._current_category_id}-{self._current_category}\n"
        msg += f"\t{'App Count:'.rjust(width, ' ')} | {self._category_stats['app_count']}\n"
        msg += f"\t{'Reviews:'.rjust(width, ' ')} | {self._category_stats['reviews']}\n"
        msg += f"\t{'Min Reviews per App:'.rjust(width, ' ')} | {self._category_stats['min_reviews_per_app']}\n"
        msg += f"\t{'Max Reviews per App:'.rjust(width, ' ')} | {self._category_stats['max_reviews_per_app']}\n"
        msg += f"\t{'Ave Reviews per App:'.rjust(width, ' ')} | {self._category_stats['ave_reviews_per_app']}\n"
        self._logger.info(msg)

    def _start_app(self, row: pd.Series) -> None:
        self._current_app_id = row["id"]
        self._current_app_name = row["name"]

        self._category_stats["app_count"] += 1
        self._project_stats["apps"] += 1
        self._app_stats["id"] = self._current_app_id
        self._app_stats["name"] = self._current_app_name
        self._app_stats["reviews"] = 0

    def _end_app(self) -> None:
        self._category_stats["reviews_per_app"].append(self._app_stats["reviews"])
        if self._category_stats["app_count"] % self._verbose == 0:
            self._announce_batch()

    def _start_page(self) -> None:
        self._project_stats["pages"] += 1
        self._category_stats["pages"] += 1

    def _save_page(self, result: pd.DataFrame) -> None:
        self.uow.review_repository.add(data=result)
        self.uow.save()

    def _end_page(self, result: pd.DataFrame) -> None:
        """Updates stats and announces progress."""
        self._project_stats["reviews"] += result.shape[0]
        self._project_stats["ended"] = datetime.datetime.now()
        duration = (self._project_stats["ended"] - self._project_stats["started"]).total_seconds()
        self._project_stats["reviews_per_second"] = round(
            self._project_stats["reviews"] / duration, 2
        )
        self._project_stats["duration"] = str(datetime.timedelta(seconds=(duration)))

        self._category_stats["reviews"] += result.shape[0]
        self._category_stats["ended"] = datetime.datetime.now()
        self._category_stats["duration"] = str(
            datetime.timedelta(
                seconds=(
                    self._category_stats["ended"] - self._category_stats["started"]
                ).total_seconds()
            )
        )

        self._app_stats["reviews"] += result.shape[0]

    def _announce_batch(self) -> None:
        msg = f"Category: {self._category_stats['category_id']}-{self._category_stats['category']}\
            \tApps: {self._category_stats['app_count']}\tReviews: {self._category_stats['reviews']}\
            \tElapsed Time: {self._category_stats['duration']}\
            \tRate: {self._project_stats['reviews_per_second']} reviews/second."
        self._logger.info(msg)


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP RATING CONTROLLER                                        #
# ------------------------------------------------------------------------------------------------ #
class RatingController(Controller):
    """Controls the App Store Review scraping process

    Args:
        scraper (ReviewScraper): A scraper object that returns data from the target urls.
        uow (UnitofWork): Unit of Work class containing the appdata repository
        io (IOService): A file IO object.

    Inherited Member Variables:
        uow (UoW): Unit of Work Class containing all repositories.
    """

    def __init__(
        self,
        scraper: type[ReviewScraper] = RatingScraper,
        batchsize: int = 20,
    ) -> None:
        super().__init__()
        self._scraper = scraper
        self._batchsize = batchsize

        # Stats
        self._apps = 0
        self._started = None
        self._duration = None
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def scrape(self, category_ids: str) -> None:
        """Scrapes app data matching the search term from the target URL.

        Args:
            category_ids (str): Category id or a list of category ids from AppStoreCategories
        """
        load_dotenv()
        status = os.getenv("APPSTORE_RATINGS_SCRAPED")
        if status in [True, "True", "true"]:
            msg = "\n\nAppstore Review Scraped Status is Complete. Skipping App Store Review Scraping Operation."
            self._logger.info(msg)
        else:
            self._scrape(category_ids=category_ids)

        self._teardown()

    def summarize(self) -> pd.DataFrame:
        """Returns a DataFrame summarizing the data extracted"""
        return self.uow.review_repository.summarize()

    def archive(self) -> None:
        """Saves the repository to an archive"""
        self.uow.review_repository.export()

    def _scrape(self, category_ids: str) -> None:
        self._setup()

        category_ids = [category_ids] if isinstance(category_ids, (str, int)) else category_ids

        for category_id in category_ids:
            self._current_category_id = category_id
            # Grab a dataframe containing apps for which rating data is to be obtained
            apps = self._get_apps(category_id=category_id)
            # Convert the dataframe to list a dictionaries.
            apps = apps.to_dict("records")

            batch = []
            # Iterate over list of apps, returning a dictionary for each app in the category
            for scraper in self._scraper(apps=apps):
                self._apps += 1
                if scraper.result is not None:
                    batch.append(scraper.result)
                    # Persist, update and report stats each batchsize iterations.
                    if self._apps % self._batchsize == 0:
                        if len(batch) > 0:
                            # Convert the batch, i.e. list of dicts to a dataframe
                            results = pd.DataFrame(data=batch)
                            self._persist(results)
                            self._update_stats()
                            self._announce()
                            batch = []

    def _setup(self) -> None:
        self._started = datetime.datetime.now()
        self._apps = 0

    def _teardown(self) -> None:
        self._update_stats()
        self._announce()

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        """Obtains apps for the category, removing any apps for which reviews exist."""

        # Obtain all apps for the category from the repository.
        apps = self.uow.appdata_repository.get_by_category(category_id=category_id)
        msg = f"\n\nA total of {len(apps)} apps in category {category_id} to process."

        # Obtain apps for which reviews exist.
        ratings = self.uow.rating_repository.get_by_category(category_id=category_id)
        apps_processed = ratings["id"].unique()
        msg += f"\nThere are {len(apps_processed)} apps in category {category_id} which have already been processed."

        # Remove apps for which reviews exist from the list of apps to process.
        if len(apps_processed) > 0:
            apps = apps.loc[~apps["id"].isin(apps_processed)]
            msg += f"\nApps remaining: {len(apps)}"

        self._logger.info(msg)

        return apps

    def _persist(self, results: pd.DataFrame) -> None:
        try:
            self.uow.rating_repository.add(data=results)
            self.uow.save()
        except Exception:
            self._insert(batch=results)

    def _insert(self, batch: pd.DataFrame) -> None:
        """Inserts DataFrame row by row

        Args:
            batch (pd.DataFrame): Data which failed initial insert.
        """
        for _, row in batch.iterrows():
            df = row.to_frame()
            try:
                self.uow.rating_repository.add(data=df)
                self.uow.save()
            except Exception:
                pass

    def _update_stats(self) -> None:
        seconds = (datetime.datetime.now() - self._started).total_seconds()
        self._apps_per_second = round(self._apps / seconds, 2)
        self._duration = str(datetime.timedelta(seconds=seconds))

    def _announce(self) -> None:
        # Report progress in terms of the number of apps processed and time.
        category = AppStoreCategories.NAMES[self._current_category_id]
        msg = f"Category: {self._current_category_id}-{category}\tApps: {self._apps}\tElapsed Time: {self._duration}\tRate: {self._apps_per_second} apps per second."
        self._logger.info(msg)
