#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Enter Project Name in Workspace Settings                                            #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.8                                                                              #
# Filename   : /aimobile/data/scraper/appstore/service/appdata.py                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : Enter URL in Workspace Settings                                                     #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday March 30th 2023 07:45:46 pm                                                #
# Modified   : Tuesday April 4th 2023 08:10:43 am                                                  #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""App Store app data scraper module."""
import requests
import json
import time
import re
import os
import logging
from datetime import datetime

from urllib.parse import quote_plus
from aimobile.data.scraper.appstore.service.genera import (
    AppStoreException,
    AppStoreMarkets,
    COUNTRIES,
)


class Regex:
    STARS = re.compile(r"<span class=\"total\">[\s\S]*?</span>")


class AppStoreScraper:
    """iTunes App Store scraper

    This class implements methods to retrieve information about iTunes App
    Store apps in various ways. Much has been adapted from the itunes-app-scraper,
    which can be found at  https://github.com/digitalmethodsinitiative/itunes-app-scraper

    Args:
        country (str): Two letter country code. Default is 'us'
        lang (str): Two character language code. Default is 'en'
        num_results_per_page (int): The number of results to return per page.
        pages (int): The max number of page requests.
        retries (int): The number of retry attempts if an exception is encountered.
        backoff_factor (int): Specifies the base factor for exponential backoff on retries
        sleep (tuple): Lower and upper bound of randomly set sleep times.
    """

    def __init__(
        self,
        country: str = "us",
        lang: str = "en-us",
        num_results_per_page: int = 200,
        pages: int = 20000,
        retries: int = 5,
        backoff_factor: int = 2,
        sleep: tuple = (1, 5),
    ) -> None:
        self._country = country
        self._lang = lang
        self._num_results_per_page = num_results_per_page
        self._pages = pages
        self._retries = retries
        self._backoff_factor = backoff_factor
        self._sleep = sleep

        self._logger = logging.getLogger(f"{self.__module__}.{self.__class__.__name__}")

    def search(self, term) -> list:
        """Retrieve suggested app IDs for search query

        Args:
            term (str): Search term.

        Returns (list): List of dictionaries containing app data
        """
        url = "https://search.itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=Software&media=software&term="
        url += quote_plus(term)

        amount = int(self._num_results_per_page) * int(self._pages)

        country = self.get_store_id_for_country(self._country)
        headers = {"X-Apple-Store-Front": "%s,24 t:native" % country, "Accept-Language": self._lang}

        try:
            result = requests.get(url, headers=headers).json()
        except ConnectionError as ce:
            raise AppStoreException("Cannot connect to store: {0}".format(str(ce)))
        except json.JSONDecodeError:
            raise AppStoreException("Could not parse app store response")

        return [app for app in result["bubbles"][0]["results"][:amount]]

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

        try:
            result = requests.get(url).json()
        except json.JSONDecodeError:
            raise AppStoreException("Could not parse app store response")

        return [entry for entry in result["feed"]["entry"]]

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

        try:
            result = requests.get(url).json()
        except json.JSONDecodeError:
            raise AppStoreException("Could not parse app store response")

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

        result = requests.get(url, headers=headers).text
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

    def get_app_ratings(self, app_id, countries=None, sleep=1):
        """
        Get app ratings for given app ID

        :param app_id:  App ID to retrieve details for. Can be either the
                        numerical trackID or the textual BundleID.
        :countries:     List of countries (lowercase, 2 letter code) or single country (e.g. 'de')
                        to generate the rating for
                        if left empty, it defaults to mostly european countries (see below)
        :param int sleep: Seconds to sleep before request to prevent being
                                          temporary blocked if there are many requests in a
                                          short time. Defaults to 1.

        :return dict:  App ratings, as scraped from the app store.
        """
        dataset = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        if countries is None:
            countries = COUNTRIES
        elif isinstance(countries, str):  # only a string provided
            countries = [countries]
        else:
            countries = countries

        for country in countries:
            url = "https://itunes.apple.com/%s/customer-reviews/id%s?displayable-kind=11" % (
                country,
                app_id,
            )
            store_id = self.get_store_id_for_country(country)
            headers = {"X-Apple-Store-Front": "%s,12 t:native" % store_id}

            try:
                if sleep is not None:
                    time.sleep(sleep)
                result = requests.get(url, headers=headers).text
            except Exception:
                try:
                    # handle the retry here.
                    # Take an extra sleep as back off and then retry the URL once.
                    time.sleep(2)
                    result = requests.get(url, headers=headers).text
                except Exception:
                    raise AppStoreException(
                        "Could not parse app store rating response for ID %s" % app_id
                    )

            ratings = self._parse_rating(result)

            if ratings is not None:
                dataset[1] = dataset[1] + ratings[1]
                dataset[2] = dataset[2] + ratings[2]
                dataset[3] = dataset[3] + ratings[3]
                dataset[4] = dataset[4] + ratings[4]
                dataset[5] = dataset[5] + ratings[5]

                # debug
        # ,print("-----------------------")
        # ,print('%d ratings' % (dataset[1] + dataset[2] + dataset[3] + dataset[4] + dataset[5]))
        # ,print(dataset)

        return dataset

    def _parse_rating(self, text):
        matches = Regex.STARS.findall(text)

        if len(matches) != 5:
            # raise AppStoreException("Cant get stars - expected 5 - but got %d" % len(matches))
            return None

        ratings = {}
        star = 5

        for match in matches:
            value = match
            value = value.replace('<span class="total">', "")
            value = value.replace("</span>", "")
            ratings[star] = int(value)
            star = star - 1

        return ratings

    def _log_error(self, app_store_country, message):
        """
        Write the error to a local file to capture the error.

        :param str app_store_country: the country for the app store
        :param str message: the error message to log
        """
        log_dir = "log/"
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)

        app_log = os.path.join(log_dir, "{0}_log.txt".format(app_store_country))
        errortime = datetime.now().strftime("%Y%m%d_%H:%M:%S - ")
        fh = open(app_log, "a")
        fh.write("%s %s \n" % (errortime, message))
        fh.close()
