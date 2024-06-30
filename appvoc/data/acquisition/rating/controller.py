#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AppVoC                                                                              #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /appvoc/data/acquisition/rating/controller.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                      #
# URL        : https://github.com/variancexplained/appvoc                                          #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 11:32:21 pm                                                  #
# Modified   : Sunday June 30th 2024 02:01:39 am                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Rating Controller"""
import logging

import pandas as pd
from dependency_injector.wiring import Provide, inject

from appvoc.container import AppVoCContainer
from appvoc.data.acquisition.base import Controller
from appvoc.data.acquisition.rating.director import RatingDirector
from appvoc.data.acquisition.rating.job import RatingJobRun
from appvoc.data.acquisition.rating.result import RatingResponse
from appvoc.data.acquisition.rating.scraper import RatingScraper
from appvoc.data.repo.uow import UoW


# ------------------------------------------------------------------------------------------------ #
#                            APPSTORE APP RATING CONTROLLER                                        #
# ------------------------------------------------------------------------------------------------ #
class RatingController(Controller):
    """Controls the App Store Review scraping process

    Args:
        scraper (ReviewScraper): A scraper object that returns data from the target urls.
        uow (UnitofWork): Unit of Work class containing the app repo
        io (IOService): A file IO object.

    """

    @inject
    def __init__(
        self,
        director: type[RatingDirector] = RatingDirector,
        scraper: type[RatingScraper] = RatingScraper,
        uow: UoW = Provide[AppVoCContainer.data.uow],
        failure_threshold: int = 10,
        batchsize: int = 100,
        verbose: int = 10,
    ) -> None:
        super().__init__()
        self._scraper = scraper
        self._uow = uow
        self._failure_threshold = failure_threshold
        self._director = director(uow=uow)
        self._batchsize = batchsize
        self._verbose = verbose
        self._batch = 0
        self._failures = 0

        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    async def scrape(self) -> None:
        """Entry point for scraping operation"""
        if not super().is_locked():
            await self._scrape()
        else:  # pragma: no cover
            msg = f"Running {self.__class__.__name__} is not authorized at this time."
            self._logger.info(msg)

    async def _scrape(self) -> None:
        jobrun = self._director.next()
        while jobrun is not None:
            jobrun = self.start_jobrun(jobrun=jobrun)
            apps = self._get_apps(category_id=jobrun.category_id)
            scraper = self._scraper(apps=apps, batch_size=self._batchsize)
            # Iterate over results returned from the scraper
            async for result in scraper.scrape():
                if result.is_valid():
                    self._failures = 0
                    self._batch += 1
                    self.persist(result)
                    jobrun = self.update_jobrun(jobrun=jobrun, result=result)
                    if self._batch % self._verbose == 0:
                        jobrun.announce()
                else:
                    self._failures += 1
                    if self._failures > self._failure_threshold:
                        msg = f"\nFailures exceeded the failure threshold. Ending job run for job {jobrun.jobid}.\n"
                        self._logger.exception(msg)
                        break
            self.end_jobrun(jobrun=jobrun)
            jobrun = self._director.next()

    def _get_apps(self, category_id: int) -> pd.DataFrame:
        """Obtains apps for the category, removing any apps for which ratings exist."""

        # Obtain all apps for the category from the app repo.
        apps = self._uow.app_repo.get_by_category(category_id=category_id)
        msg = f"\n\nA total of {len(apps)} apps in category {category_id}."

        # Obtain apps which we have already processed
        try:
            ratings = self._uow.rating_repo.get_by_category(category_id=category_id)
            apps_processed = ratings["id"].values
            msg += f"\nThere are {len(apps_processed)} apps in category {category_id} which have already been processed."
        except Exception as e:  # pragma: no cover
            apps_processed = []
            msg += f"\nException of type {type(e)} encountered. Assuming no apps processed for category."

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

    def persist(self, result: RatingResponse) -> None:
        """Persists the result from the scraping operation.

        Args:
            result (RatingResponse): The result from the scraping operation
        """
        data = result.get_result()
        if len(data) > 0:
            try:
                self._uow.rating_repo.load(data=data)
                self._uow.save()
            except Exception as e:  # pragma: no cover
                msg = f"{type(e)} exception occurred in persist. Rolling back. \n{e}"
                self._logger.exception(msg)
                self._uow.rollback()

    def start_jobrun(self, jobrun: RatingJobRun) -> RatingJobRun:
        """Starts a jobrun and adds a jobrun to the repository.

        Args:
            jobrun (RatingJobRun): The current job run.

        """
        jobrun.start()
        self._director.add_jobrun(jobrun=jobrun)
        return jobrun

    def update_jobrun(
        self, jobrun: RatingJobRun, result: RatingResponse
    ) -> RatingJobRun:
        """Adds results to jobrun, and persists.

        Args:
            jobrun (RatingJobRun): The current job run.
            result (RatingResponse): The result from the scraping operation

        """
        jobrun.add_response(result=result)
        self._director.update_jobrun(jobrun=jobrun)
        return jobrun

    def end_jobrun(self, jobrun: RatingJobRun) -> None:
        """Persists job to the Database

        Args:
            result (ReviewResponse) -> Parsed result object
        """
        jobrun.end()
        # Get the associated job and end it.
        job = self._uow.job_repo.get(id=jobrun.jobid)
        job.end(completed=jobrun.completed)
        # Persist the jobrun and the job.
        self._director.update_job(job=job)
        self._director.update_jobrun(jobrun=jobrun)
        # Archive the ratings
        self._uow.rating_repo.export()
