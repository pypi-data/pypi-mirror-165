#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os
from random import randint
from json.decoder import JSONDecodeError

from baseblock import BaseObject
from baseblock import FileIO
from baseblock import Stopwatch


class PageCacheReader(BaseObject):
    """ Read and Summarize the entire Page Cache """

    def __init__(self):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)
        self._cache_path = self._get_cache_path()

    def _read_cached_file(self,
                          file_path: str) -> dict or None:
        try:
            return FileIO.read_json(file_path)
        except JSONDecodeError as e:
            if self.isEnabledForWarning:
                self.logger.warning('\n'.join([
                    "Unable to Read Cached File",
                    f"\tFile Path: {file_path}"]))
            self.logger.exception(e)

    @staticmethod
    def _get_cache_path() -> str:
        """ Get the Cache Path and Create the Cache Directory if it does not exist

        Returns:
            str: the absolute path to the cached directory
        """
        cache_path = os.path.normpath(
            os.path.join(
                os.environ["PROJECT_BASE"],
                "resources/cache",
                os.environ["CACHE_NAME"]))

        FileIO.exists_or_create(cache_path)

        return cache_path

    def _walk_cache(self) -> list:
        """ Walk through Cache and Load File Paths 

        Returns:
            list: list of absolute paths to cached files
        """
        file_paths = []
        for subdir, _, files in os.walk(self._cache_path):
            for f in files:
                file_paths.append(os.path.join(
                    os.environ["PROJECT_BASE"], subdir, f))
        return file_paths

    def random(self,  # TODO: I think this should go in a new component ... ?
               number_of_attempts: int = 1000) -> dict:
        file_paths = self._walk_cache()

        for i in range(number_of_attempts):
            file_path = file_paths[randint(0, len(file_paths))]

            d_page = self._read_cached_file(file_path)
            if not d_page:
                continue
            if 'is_empty' in d_page and d_page['is_empty'] is True:
                continue

            return d_page

    def process(self) -> dict:
        sw = Stopwatch()

        d_results = {}
        file_paths = self._walk_cache()

        for file_path in file_paths:
            d_page = self._read_cached_file(file_path)
            if d_page:
                d_results[d_page["entity"]["name"]] = d_page

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Page Cache Reader Completed",
                f"\tTotal Results: {len(d_results)}",
                f"\tTotal Time: {str(sw)}"]))

        return d_results
