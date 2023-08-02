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
# Modified   : Wednesday August 2nd 2023 07:20:21 am                                               #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Rating Controller"""
import logging
from datetime import datetime
import asyncio

import pandas as pd
from dependency_injector.wiring import Provide, inject


from appstore.data.acquisition.rating.scraper import RatingScraper
from appstore.data.storage.uow import UoW
from appstore.data.acquisition.rating.job import RatingJobRun
from appstore.data.acquisition.rating.result import RatingResult
from appstore.data.acquisition.base import Controller
from appstore.data.acquisition.rating.director import RatingDirector
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
        director: RatingDirector = Provide[AppstoreContainer.director.rating],
        batchsize: int = 100,
        verbose: int = 1000,
    ) -> None:
        super().__init__()
        self._scraper = scraper
        self._uow = uow
        self._director = director
        self._batchsize = batchsize
        self._verbose = verbose
        self._batch = 0

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def scrape(self) -> None:
        """Entry point for scraping operation"""
        if not super().is_locked():
            await self._scrape()
        else:
            msg = f"Running {self.__class__.__name__} is not authorized at this time."
            self._logger.info(msg)

    async def _scrape(self) -> None:
        for jobrun in self._director:
            if jobrun is not None:
                jobrun.start()
                apps = self._get_apps(category_id=jobrun.category_id)
                # Iterate over results returned from the scraper
                async for result in self._scraper(apps=apps, batch_size=self._batchsize):
                    self._batch += 1
                    if result.is_valid():
                        await self.persist(result)
                        self.update_jobrun(jobrun=jobrun, result=result)
                        if self._batch % self._verbose == 0:
                            jobrun.announce()
                self.end_jobrun(jobrun=jobrun)

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        """Obtains apps for the category, removing any apps for which ratings exist."""

        # Obtain all apps for the category from the appdata repo.
        apps = self._uow.appdata_repo.get_by_category(category_id=category_id)
        msg = f"\n\nA total of {len(apps)} apps in category {category_id}."

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

        if len(apps) > 0:
            msg += f"\nApps remaining: {len(apps)}"
            self._logger.info(msg)
        else:
            msg += f"All apps have been processed for category: {category_id}"
            self._logger.info(msg)
        return apps

    async def persist(self, result: RatingResult) -> None:
        try:
            await asyncio.gather(
                self._uow.rating_repo.add(data=result.get_result()),
            )
            self._uow.save()
        except Exception:
            self._uow.rollback()

    def update_jobrun(self, jobrun: RatingJobRun, result: RatingResult) -> None:
        jobrun.add_result(result=result)
        self._uow.review_jobrun_repo.update(jobrun=jobrun)
        self._uow.save()

    def end_jobrun(self, jobrun: RatingJobRun) -> None:
        """Persists job to the Database

        Args:
            result (ReviewResult) -> Parsed result object
        """
        jobrun.end()
        self._uow.rating_jobrun_repo.update(jobrun=jobrun)
        job = self._uow.job_repo.get(id=jobrun.jobid)
        job.completed = datetime.now()
        job.complete = True
        self._uow.job_repo.update(job=job)
        self._uow.review_repo.archive()
        self._uow.save()
