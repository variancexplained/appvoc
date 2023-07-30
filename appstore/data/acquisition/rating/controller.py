#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Appstore Ratings & Reviews Analysis                                                 #
# Version    : 0.1.19                                                                              #
# Python     : 3.10.11                                                                             #
# Filename   : /appstore/data/acquisition/rating/controller.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/appstore                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 11:32:21 pm                                                  #
# Modified   : Sunday July 30th 2023 06:35:09 am                                                   #
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
from appstore.data.acquisition.rating.job import RatingJobRun
from appstore.data.acquisition.rating.scraper import RatingScraper
from appstore.data.storage.uow import UoW
from appstore.data.acquisition.rating.result import RatingResult
from appstore.data.acquisition.base import Controller
from appstore.container import AppstoreContainer
from .job import RatingJobMonitor


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
        monitor: type[RatingJobMonitor] = RatingJobMonitor,
        batchsize: int = 100,
        verbose: int = 1000,
    ) -> None:
        super().__init__()
        self._uow = uow
        self._scraper = scraper
        self._monitor = monitor
        self._batchsize = batchsize
        self._verbose = verbose

        self._job = None
        self._job_run = None

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def scrape(self) -> None:
        """Entry point for scraping operation"""
        if not super().is_locked():
            await self._scrape()
        else:
            msg = f"Running {self.__class__.__name__} is not authorized at this time."
            self._logger.info(msg)

    async def _scrape(self) -> None:
        while True:
            job = self._uow.job_repo.get_next(controller=self.__class__.__name__)
            if job:
                self.start_job_run(job=job)
                job.start()
                self.start_job_run(job=job)
                apps = self._get_apps(category_id=job.category_id)
                # Iterate over results returned from the scraper
                async for result in self._scraper(apps=apps, batch_size=self._batchsize):
                    if result.is_valid():
                        await self._persist(result)
                        self._update_stats(result)
                        self._announce()

                job.end()
                self._uow.job_repo.update(job=job)
                self._uow.rating_repo.archive()
            else:
                self._teardown()

    def start_job_run(self, job: Job) -> None:
        """Starts the job and creates a job run."""
        job.start()
        job_run = RatingJobRun.create(job=job)
        job_run.start_job_run()

    def _teardown(self) -> None:
        msg = f"{self.__class__.__name__} has completed."
        self._logger.info(msg)
        jobs = self._uow.job_repo.get_by_controller(controller=self.__class__.__name__)
        self._logger.info(f"Jobs\n{jobs}")
        self._logger.info(f"Summary\n{self._uow.rating_repo.summary}")

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
                self._uow.rating_repo.add(data=result.as_df()),
            )
            self._uow.save()
        except Exception:
            self._uow.rollback()

    def _update_stats(self, result: RatingResult) -> None:
        seconds = (datetime.datetime.now() - self._started).total_seconds()
        self._apps += result.success
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
