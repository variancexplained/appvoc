#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/rating/controller.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 11:32:21 pm                                                  #
# Modified   : Wednesday July 26th 2023 02:09:10 pm                                                #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Rating Controller"""
import logging
import datetime

import asyncio
import pandas as pd
from dependency_injector.wiring import Provide, inject

from appstore.data.acquisition import AppStoreCategories
from appstore.data.acquisition.rating.scraper import RatingScraper
from appstore.data.storage.uow import UoW
from appstore.data.acquisition.rating.result import RatingResult
from appstore.data.acquisition.base import Controller
from appstore.container import AppstoreContainer


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP RATING CONTROLLER                                        #
# ------------------------------------------------------------------------------------------------ #
class RatingController(Controller):
    """Controls the App Store Review scraping process

    Args:
        scraper (ReviewScraper): A scraper object that returns data from the target urls.
        uow (UnitofWork): Unit of Work class containing the appdata repo
        io (IOService): A file IO object.

    """

    @inject
    def __init__(
        self,
        scraper: type[RatingScraper] = RatingScraper,
        uow: UoW = Provide[AppstoreContainer.data.uow],
        batchsize: int = 100,
        verbose: int = 1000,
    ) -> None:
        super().__init__()
        self._uow = uow
        self._scraper = scraper
        self._batchsize = batchsize
        self._verbose = verbose

        # Stats
        self._categories = 0
        self._apps = 0
        self._started = None
        self._duration = None
        self._apps_per_second = 0
        self._total = 0
        self._success = 0
        self._fail = 0
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def scrape(self, category_ids: str) -> None:
        """Scrapes app data matching the search term from the target URL.

        Args:
            category_ids (str): Category id or a list of category ids from AppStoreCategories
        """
        if super().scrape():
            await self._scrape(category_ids=category_ids)
        else:
            msg = f"Running {self.__class__.__name__} is not authorized at this time."
            self._logger.info(msg)

    def archive(self) -> None:
        """Saves the repo to an archive"""
        self._uow.rating_repo.export()

    async def _scrape(self, category_ids: str) -> None:
        self._setup()

        category_ids = [category_ids] if isinstance(category_ids, (str, int)) else category_ids

        for category_id in category_ids:
            self._categories += 1
            self._current_category_id = category_id
            # Grab a dataframe containing apps for which rating data is to be obtained
            apps = self._get_apps(category_id=category_id)
            # Iterate over list of apps, returning a dictionary for each app in the category
            async for result in self._scraper(apps=apps, batch_size=self._batchsize):
                if not result:
                    break
                else:
                    await self._persist(result)
                    self._update_stats(result)
                    self._announce()

    def _setup(self) -> None:
        self._started = datetime.datetime.now()
        self._categories = 0
        self._apps = 0

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        """Obtains apps for the category, removing any apps for which ratings exist."""

        # Obtain all apps for the category from the appdata repo.
        apps = self._uow.appdata_repo.get_by_category(category_id=category_id)
        msg = f"\n\nA total of {len(apps)} apps in category {category_id} to process."

        # Obtain apps which we have already processed
        try:
            ratings = self._uow.rating_repo.get_by_category(category_id=category_id)
            apps_processed = ratings["id"].values
            msg += f"\nThere are {len(apps_processed)} apps in category {category_id} which have already been processed."
        except Exception as e:
            apps_processed = []
            msg += f"\nException of type {type(e)} encountered. Assuming no apps processed for category.\n{e}"

        # Remove apps already processed
        if len(apps_processed) > 0:
            apps = apps.loc[~apps["id"].isin(apps_processed)]
            msg += f"\nApps remaining: {len(apps)}"

        self._logger.info(msg)

        return apps

    async def _persist(self, result: RatingResult) -> None:
        try:
            await asyncio.gather(
                self._uow.rating_repo.add(data=result.results),
            )
            self._uow.save()
        except Exception:
            self._uow.rollback()

    def _update_stats(self, result: RatingResult) -> None:
        seconds = (datetime.datetime.now() - self._started).total_seconds()
        self._apps += result.results.shape[0]
        self._apps_per_second = round(self._apps / seconds, 2)
        self._duration = str(datetime.timedelta(seconds=seconds))
        self._total += result.total
        self._success += result.success
        self._fail += result.fail

    def _announce(self) -> None:
        # Report progress in terms of the number of apps processed and time.
        if self._total % self._verbose == 0:
            category = AppStoreCategories.NAMES[self._current_category_id]
            width = 32
            msg = f"\n\n{self.__class__.__name__}\n"
            msg += f"\t{'Category:'.rjust(width,' ')} | {self._current_category_id}-{category}\n"
            msg += f"\t{'Total Requests:'.rjust(width,' ')} | {self._total}\n"
            msg += f"\t{'Successful Requests:'.rjust(width,' ')} | {self._success}\n"
            msg += f"\t{'Failed Requests:'.rjust(width,' ')} | {self._fail}\n"
            msg += f"\t{'Apps:'.rjust(width,' ')} | {self._apps}\n"
            msg += f"\t{'Elapsed:'.rjust(width,' ')} | {self._duration}\n"
            msg += f"\t{'Apps Per Second:'.rjust(width,' ')} | {self._apps_per_second}\n"

            self._logger.info(msg)
