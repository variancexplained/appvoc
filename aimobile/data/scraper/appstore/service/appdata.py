#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : AI-Enabled Opportunity Discovery in Mobile Applications                             #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/appstore/service/appdata.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/john-james-ai/aimobile                                           #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday March 30th 2023 07:45:46 pm                                                #
# Modified   : Thursday April 6th 2023 01:32:15 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""App Store app data scraper module."""
import requests
import re
import json
import logging

import pandas as pd
from urllib.parse import quote_plus
from aimobile.data.scraper.appstore.dal.genera import (
    AppStoreException,
    AppStoreMarkets,
)
from aimobile.data.scraper.utils.http import HTTPRequest

from aimobile.data.scraper.appstore.entity.appdata import AppStoreAppData
from aimobile.data.scraper.appstore.entity.project import AppStoreProject
from aimobile.data.scraper.appstore.dal.datacentre import DataCentre


# ------------------------------------------------------------------------------------------------ #
class Regex:
    STARS = re.compile(r"<span class=\"total\">[\s\S]*?</span>")


class AppStoreScraper:
    """iTunes App Store scraper

    This class implements methods to retrieve information about iTunes App
    Store apps in various ways. Much has been adapted from the itunes-app-scraper,
    which can be found at  https://github.com/digitalmethodsinitiative/itunes-app-scraper

    Args:
        project (Project): The project definition, in terms of the search term, number of results
            per page, and maximum number of pages to scrape.
        country (str): Two letter country code. Default is 'us'
        lang (str): Two character language code. Default is 'en'
    """

    def __init__(
        self,
        project: AppStoreProject,
        requests: HTTPRequest,
        datacentre: DataCentre,
    ) -> None:
        self._project = project
        self._requests = requests
        self._datacentre = datacentre

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def search(self, term) -> list:
        """Retrieve suggested app data for search query

        Args:
            term (str): Search term.

        Returns (list): List of dictionaries containing app data
        """
        self._setup()

        # Format URL and Headers
        url = "https://search.itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=Software&media=software&term="
        url += quote_plus(term)

        country = self.get_store_id_for_country(self._country)
        headers = {"X-Apple-Store-Front": "%s,24 t:native" % country, "Accept-Language": self._lang}

        # Make the request
        response = self._request.get(url, headers=headers)

        # Parse the search results and obtain them in dataframe format.
        result = self._parse_search(response)

        # Update the project num results, num pages, duration etc...
        self._project.update(num_results=len(result))

        # Save everything to the database
        self._persist(result=result)

        self._teardown()

    def _setup(self) -> None:
        """Some initialization"""
        self._project.start()
        self._datacentre.project_repository.add(self._project)

    def _persist(self, result: list) -> None:
        """Saves the app and project data to the database."""

        self._datacentre.appdata_repository.load(result)
        self._datacentre.project_repository.update(self._project)
        self._datacentre.save()

    def _teardown(self) -> None:
        """Some final bookeeping."""
        self._project.end()
        # Set the status to success, unless an exception has occurred and
        # post the project to the database and release the resources.
        self._datacentre.project_repository.update(self._project)
        self._datacentre.dispose()

    def _parse_search(self, response: requests.Response) -> pd.DataFrame:
        """Extracts app metadata and stores in a pandas DataFrame.

        Args:
            response (requests.Response): An HTTP request Response object.

        Returns: pd.DataFrame:
        """
        applist = []

        if response.status_code == 200:
            response = response.json()

        results = response["storePlatformData"]["native-search-lockup-search"]["results"]
        for id, appdata in results.items():
            for genre in appdata["genres"]:
                appdata["id"] = id
                appdata["category_id"] = genre["genreId"]
                appdata["category"] = genre["name"]
                app = AppStoreAppData.from_dict(appdata=appdata)
                applist.append(app)

        return applist

    def get_app_data_for_collection_category(self, collection: str, category: str) -> list:
        """Retrieve app IDs in given App Store collection and category

        Args:
            collection (str): Collection ID. One of the values in `AppStoreCollections`.
            category (int):  Category ID. One of the values in AppStoreCategories.

        Return:  List List of dictionaries containing app data
        """
        country = self.get_store_id_for_country(self._country)
        params = (collection, category, self._num_results_per_page, country)
        url = (
            "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/ws/RSS/%s/%s/limit=%s/json?s=%s"
            % params
        )

        response = self._request.get(url)

        result = self._parse_collection(response)

        self._save(result)

    def get_app_data_for_developer(self, developer_id):
        """Retrieve App data linked to given developer

        Args:
            developer_id (int): Developer ID

        Return list:  List of App IDs linked to developer
        """
        url = "https://itunes.apple.com/lookup?id=%s&country=%s&entity=software" % (
            developer_id,
            self._country,
        )

        response = self._request.get(url)

        result = self._parse_response(response)

        self._save(result)

        if "results" in result:
            return [app for app in result["results"] if app["wrapperType"] == "software"]
        else:
            # probably an invalid developer ID
            return []

    def get_similar_app_ids_for_app(self, app_id):
        """Retrieve list of App IDs of apps similar to given app

        This one is a bit special because the response is not JSON, but HTML.
        We extract a JSON blob from the HTML which contains the relevant App
        IDs.

        Args:
            app_id (str): App ID for which similar apps are identified.

        Return list:  List of similar app IDs
        """
        url = "https://itunes.apple.com/us/app/app/id%s" % app_id

        country = self.get_store_id_for_country(self._country)
        headers = {"X-Apple-Store-Front": "%s,32" % country, "Accept-Language": self._lang}

        response = self._request.get(url=url, headers=headers)

        result = self._parse_response(response)

        self._save(result)

        # result = requests.get(url, headers=headers).text
        if "customersAlsoBoughtApps" not in result:
            return []

        blob = re.search(r"customersAlsoBoughtApps\":\s*(\[[^\]]+\])", result)
        if not blob:
            return []

        try:
            ids = json.loads(blob[1])
        except (json.JSONDecodeError, IndexError):
            return []

        return ids

    def get_store_id_for_country(self, country):
        """
        Get store ID for country code

        :param str country:  Two-letter country code
        :param str country:  Two-letter country code for the store to search in.
                             Defaults to 'nl'.
        """
        country = country.upper()

        if hasattr(AppStoreMarkets, country):
            return getattr(AppStoreMarkets, country)
        else:
            raise AppStoreException("Country code not found for {0}".format(country))

    def _register_project(self) -> None:
        """Creates a project in the database."""

    def _update_project(self) -> None:
        """Update project page_count, app_count, end time, duration, and status."""

    def _finalize_project(self) -> None:
        """Update project end time, duration, and status."""

    def _parse_collection(self, response: requests.Response) -> pd.DataFrame:
        """Extracts app metadata and stores in a pandas DataFrame.

        Args:
            response (requests.Response): An HTTP request Response object.

        Returns: pd.DataFrame:
        """
        applist = []

        result = response.json()
        results = result["storePlatformData"]["native-search-lockup-search"]["results"]
        for id, appdata in results.items():
            for genre in appdata["genres"]:
                appdata = {}
                appdata["id"] = id
                appdata["name"] = appdata["name"]
                appdata["subtitle"] = appdata["subtitle"]
                appdata["category_id"] = genre["genreId"]
                appdata["category"] = genre["name"]
                appdata["price"] = appdata["offers"][0]["price"]
                appdata["user_rating"] = appdata["userRating"].get("value", 0)
                appdata["ratings"] = appdata["userRating"].get("ratingCount", 0)
                appdata["watch"] = True if "watch" in appdata["deviceFamilies"] else False
                appdata["ipad"] = True if "ipad" in appdata["deviceFamilies"] else False
                appdata["iphone"] = True if "iphone" in appdata["deviceFamilies"] else False
                appdata["ipod"] = True if "ipod" in appdata["deviceFamilies"] else False
                appdata["developer_name"] = appdata["artistName"]
                appdata["source"] = "appstore"
                applist.append(appdata)

        return pd.DataFrame(data=applist)
