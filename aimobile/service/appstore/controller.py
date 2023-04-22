#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /aimobile/service/appstore/controller.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday April 20th 2023 05:33:57 am                                                #
# Modified   : Saturday April 22nd 2023 12:41:38 pm                                                #
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
from typing import Union

from dependency_injector.wiring import inject, Provide
import pandas as pd

from aimobile.infrastructure.dal.uow import AppStoreUoW
from aimobile.service.appstore.appdata import AppStoreAppScraper
from aimobile.service.appstore.review import AppStoreReviewScraper
from aimobile.container import AIMobileContainer
from aimobile.service.base import Controller


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP DATA CONTROLLER                                          #
# ------------------------------------------------------------------------------------------------ #
class AppStoreAppController(Controller):
    """AppStore App Data Controller has overall responsibility for App Store scraping process.

    Args:
        uow (UnitofWork): Unit of Work class containing the appdata repository
        scraper (AppStoreAppScraper): A scraper object that returns data from the target urls.
        max_pages (int): The maximum number of pages to process.
        verbose (int): Indicates progress reporting verbosity in terms of the number of pages
            between progress reports to the log.
    """

    @inject
    def __init__(
        self,
        uow: AppStoreUoW = Provide[AIMobileContainer.appstore.uow],
        scraper: type[AppStoreAppScraper] = AppStoreAppScraper,
        max_pages: int = sys.maxsize,
        max_results_per_page: int = 200,
        verbose: int = 10,
    ) -> None:
        self._uow = uow
        self._scraper = scraper
        self._verbose = verbose
        self._max_pages = max_pages
        self._max_results_per_page = max_results_per_page

        # Stats
        self._pages = 0
        self._apps = 0
        self._started = None
        self._duration = None
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    def scrape(self, terms: Union[str, list]) -> None:
        """Scrapes app data matching the search term from the target URL.

        Args:
            terms (Union[str,list]): Search term or a list of search terms.
        """
        load_dotenv()
        status = os.getenv("APPSTORE_DATA_SCRAPED")
        if status in [True, "True", "true"]:
            msg = "\n\nAppstore AppData Scraped Status is Complete. Skipping App Store App Data Scraping Operation."
            self._logger.info(msg)
        else:
            self._scrape(terms=terms)

        self._teardown()

    def summarize(self) -> pd.DataFrame:
        """Returns a DataFrame summarizing the data extracted"""
        return self._uow.appdata_repository.summarize()

    def archive(self) -> None:
        """Saves the repository to an archive"""
        self._uow.appdata_repository.export()

    def _scrape(self, terms: Union[str, list]) -> None:
        self._setup()
        terms = [terms] if isinstance(terms, str) else terms

        for term in terms:
            for scraper in self._scraper(
                term=term, max_pages=self._max_pages, limit=self._max_results_per_page
            ):
                self._persist(scraper.result)
                self._update_stats(scraper.result)
                self._announce(term=term)

    def _setup(self) -> None:
        self._started = datetime.datetime.now()
        self._pages = 0
        self._apps = 0

    def _teardown(self) -> None:
        self._uow.appdata_repository.export()

    def _persist(self, result: pd.DataFrame) -> None:
        self._uow.appdata_repository.add(data=result)
        self._uow.save()

    def _update_stats(self, result: pd.DataFrame) -> None:
        self._pages += 1
        self._apps += result.shape[0]
        seconds = (datetime.datetime.now() - self._started).total_seconds()
        self._duration = str(datetime.timedelta(seconds=seconds))

    def _announce(self, term: str) -> None:
        if self._pages % self._verbose == 0:
            msg = f"Term: {term.capitalize()}\tPages: {self._pages}\tApps: {self._apps}\tElapsed Time: {self._duration}"
            self._logger.info(msg)


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP DATA CONTROLLER                                          #
# ------------------------------------------------------------------------------------------------ #
class AppStoreReviewController(Controller):
    """Controls the App Store Review scraping process

    Args:
        scraper (AppStoreAppScraper): A scraper object that returns data from the target urls.
        uow (UnitofWork): Unit of Work class containing the appdata repository
        io (IOService): A file IO object.
    """

    @inject
    def __init__(
        self,
        uow: AppStoreUoW = Provide[AIMobileContainer.appstore.uow],
        scraper: type[AppStoreReviewScraper] = AppStoreReviewScraper,
        max_pages: int = sys.maxsize,
        max_results_per_page: int = 400,
        verbose: int = 5,
    ) -> None:
        self._uow = uow
        self._scraper = scraper
        self._max_pages = max_pages
        self._max_results_per_page = max_results_per_page
        self._verbose = verbose

        # Stats
        self._pages = 0
        self._reviews = 0
        self._started = None
        self._duration = None
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
        return self._uow.review_repository.summarize()

    def archive(self) -> None:
        """Saves the repository to an archive"""
        self._uow.review_repository.export()

    def _scrape(self, category_ids: str) -> None:
        self._setup()
        category_ids = [category_ids] if isinstance(category_ids, (str, int)) else category_ids
        for category_id in category_ids:
            apps = self._get_apps(category_id=category_id)

            for _, row in apps.iterrows():
                app_pages = 0

                for scraper in self._scraper(
                    app_id=row["id"],
                    app_name=row["name"],
                    category_id=row["category_id"],
                    category=row["category"],
                    max_pages=self._max_pages,
                    max_results_per_page=self._max_results_per_page,
                ):
                    self._persist(scraper.result)
                    self._update_stats(scraper.result)
                    app_pages += 1
                    if app_pages >= self._max_pages:
                        break
                    self._announce(row)

    def _setup(self) -> None:
        self._started = datetime.datetime.now()
        self._apps = 0
        self._reviews = 0
        self._pages = 0

    def _teardown(self) -> None:
        self._uow.review_repository.export()

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        """Obtains apps for the category, removing any apps for which reviews exist."""
        apps = self._uow.appdata_repository.get_by_category(category_id=category_id)
        try:
            reviews = self._uow.review_repository.get_by_category(category_id=category_id)
            apps_reviewed = reviews["app_id"].unique()
            apps = apps.loc[~apps["id"].isin(apps_reviewed)]
        except Exception:
            pass
        return apps

    def _persist(self, result: pd.DataFrame) -> None:
        self._uow.review_repository.add(data=result)
        self._uow.save()

    def _update_stats(self, result: pd.DataFrame) -> None:
        self._apps += 1
        self._pages += 1
        self._reviews += result.shape[0]
        seconds = (datetime.datetime.now() - self._started).total_seconds()
        self._duration = str(datetime.timedelta(seconds=seconds))

    def _announce(self, row: pd.Series) -> None:
        if self._pages % self._verbose == 0:
            msg = f"Category: {row['category_id']}-{row['category']} Apps: {self._apps} Reviews: {self._reviews} Elapsed Time: {self._duration}"
            self._logger.info(msg)
