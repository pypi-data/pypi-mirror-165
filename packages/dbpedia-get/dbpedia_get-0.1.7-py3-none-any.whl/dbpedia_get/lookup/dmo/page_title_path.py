#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os

from baseblock import EnvIO
from baseblock import BaseObject


class PageTitlePath(BaseObject):
    """ I/O Operations for a DBpedia page from disk (cache) """

    def __init__(self):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        Updated:
            25-Aug-2022
            craigtrim@gmail.com
            *   provide a default cache-name option
        """
        BaseObject.__init__(self, __name__)
        self._cache_name = EnvIO.str_or_default('CACHE_NAME', 'default')

    @staticmethod
    def _file_title(title: str) -> str:
        title = title.replace(' ', '_').lower().strip()

        for ch in ['/', '|', '@', '#', '$', '%', '^', '&',
                   '*', '(', ')', '[', ']', '{', '}', '\\', ':']:
            if ch in title:
                title = title.replace(ch, '_').strip()

        for ch in ['"', "'", '?', '!']:
            if ch in title:
                title = title.replace(ch, '').strip()

        while '__' in title:
            title = title.replace('__', '_')

        return title

    def process(self,
                title: str,
                make_dirs: bool = False) -> str:

        file_title = self._file_title(title)

        def _cleanse_path(a_ch: str) -> str:
            if a_ch is None:
                return "_"
            if a_ch.isalpha():
                return a_ch
            return "_"

        def _ch0() -> str:
            if len(file_title) > 0:
                return _cleanse_path(file_title[0])
            return "_"

        def _ch1() -> str:
            if len(file_title) > 1:
                return _cleanse_path(file_title[1])
            return "_"

        def _ch2() -> str:
            if len(file_title) > 2:
                return _cleanse_path(file_title[2])
            return "_"

        rel_path = f"resources/cache/{self._cache_name}\\{_ch0()}\\{_ch1()}\\{_ch2()}"

        abs_path = os.path.normpath(
            os.path.join(os.environ["PROJECT_BASE"],
                         rel_path))

        if make_dirs and not os.path.exists(abs_path):
            os.makedirs(abs_path)

        return os.path.join(abs_path,
                            f"{file_title}.json")
