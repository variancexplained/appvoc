#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Voice of the Mobile Technology Customer                                  #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /tests/test_data_acquisition/test_appstore/test_controllers/test_appstore_appdata_controller.py #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday April 30th 2023 09:11:00 pm                                                  #
# Modified   : Sunday May 7th 2023 12:58:24 pm                                                     #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import inspect
from datetime import datetime
import pytest
import logging

from aimobile.data.acquisition.project import Project
from aimobile.data.acquisition.appstore.appdata.controller import AppStoreAppDataController


# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
double_line = f"\n{100 * '='}"
single_line = f"\n{100 * '-'}"


@pytest.mark.ctrl
@pytest.mark.appdata_ctrl
class TestAppStoreAppDataController:  # pragma: no cover
    # ============================================================================================ #
    def test_no_project_exists(self, project_repo, appdata_repo, caplog):
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
        MAX_PAGES = 2
        MAX_RESULTS_PER_PAGE = 5
        VERBOSE = 2
        CONTROLLER = "AppStoreAppDataController"
        TERM = "health"
        controller = AppStoreAppDataController(
            max_pages=MAX_PAGES, max_results_per_page=MAX_RESULTS_PER_PAGE, verbose=VERBOSE
        )
        controller.scrape(terms="health")
        df = project_repo.getall()
        assert df.shape[0] == 1
        project = project_repo.get_project(controller=CONTROLLER, term=TERM)
        assert isinstance(project, Project)
        project.controller == CONTROLLER
        project.term == TERM
        project.pages == 2
        project.apps = 10
        project.status == "complete"

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
    def test_project_complete(self, caplog):
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
        MAX_PAGES = 2
        MAX_RESULTS_PER_PAGE = 5
        VERBOSE = 2
        controller = AppStoreAppDataController(
            max_pages=MAX_PAGES, max_results_per_page=MAX_RESULTS_PER_PAGE, verbose=VERBOSE
        )
        controller.scrape(terms="health")
        # Observe log: should skip, job complete.
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
    def test_incomplete(self, project_repo, caplog):
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
        MAX_PAGES = 2
        MAX_RESULTS_PER_PAGE = 5
        VERBOSE = 2
        CONTROLLER = "AppStoreAppDataController"
        TERM = "health"
        # Get current project
        project = project_repo.get_project(controller=CONTROLLER, term=TERM)
        assert project.status == "complete"
        assert isinstance(project, Project)

        # Update status to in-process and update the repository
        project.status = "in-process"
        project_repo.update(data=project)
        project_repo.save()

        # Rerun the project, should start on page 2
        controller = AppStoreAppDataController(
            max_pages=MAX_PAGES, max_results_per_page=MAX_RESULTS_PER_PAGE, verbose=VERBOSE
        )
        controller.scrape(terms="health")

        # Get project and confirm additional pages added.
        project = project_repo.get_project(controller=CONTROLLER, term=TERM)
        assert project.pages == 4
        assert project.apps == 20
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
