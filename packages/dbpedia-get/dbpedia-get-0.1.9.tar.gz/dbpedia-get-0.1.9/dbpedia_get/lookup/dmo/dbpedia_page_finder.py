#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from wikipedia import page as wiki_page
from wikipedia.exceptions import PageError
from wikipedia.exceptions import WikipediaException
from wikipedia.exceptions import DisambiguationError

from baseblock import BaseObject
from dbpedia_get.lookup.dto import WikipediaPageStatus


class DBpediaPageFinder(BaseObject):
    """ make a wire call to dbPedia to find a page 

    *** API LIMITS ***
        -   There is no hard and fast limit on read requests, but be considerate 
            and try not to take a site down. 
        -   Most system administrators reserve the right to unceremoniously block you 
            if you do endanger the stability of their site.
        -   https://www.mediawiki.org/wiki/API:Etiquette """

    __d_disambiguation = {}

    def __init__(self,
                 auto_suggest: bool = False):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)
        self._auto_suggest = auto_suggest

        self.logger.debug('\n'.join([
            "Instantiated DBPediaPageFinder",
            f"\tAuto Suggest: {self._auto_suggest}"]))

    def _page_error(self,
                    title: str) -> tuple:
        self.logger.error('\n'.join([
            "Lookup Failed (Page Error)",
            f"\tTitle: {title}"]))

        if not title.islower():
            _title = title.lower()
            self.logger.debug('\n'.join([
                "Forced Lookup",
                f"\tOriginal Term: {title}",
                f"\tDisambiguation: {_title}"]))
            return DBpediaPageFinder(self._auto_suggest).process(_title)

        return None, WikipediaPageStatus.FAIL_PAGE_ERROR

    def _disambiguation_error(self,
                              title: str) -> tuple:
        if title in self.__d_disambiguation:
            _title = self.__d_disambiguation[title]
            self.logger.debug('\n'.join([
                "Forced Disambiguation",
                f"\tOriginal Term: {title}",
                f"\tDisambiguation: {_title}"]))
            return DBpediaPageFinder(self._auto_suggest).process(_title)

        self.logger.error('\n'.join([
            "Disambiguation Error",
            f"\tTitle: {title}"]))

        return None, WikipediaPageStatus.FAIL_DISAMBIGUATION_ERROR

    def _wikipedia_error(self,
                         title: str) -> tuple:
        self.logger.error('\n'.join([
            "Wikipedia Error",
            f"\tTitle: {title}"]))

        return None, WikipediaPageStatus.FAIL_WIKIPEDIA_ERROR

    def _key_error(self,
                   title: str) -> tuple:
        self.logger.error('\n'.join([
            "Lookup Failed (Key Error)",
            f"\tTitle: {title}"]))

        return None, WikipediaPageStatus.FAIL_KEY_ERROR

    def _os_error(self,
                  title: str) -> tuple:
        self.logger.error('\n'.join([
            "OS Error (Likely a bad Filename)",
            f"\tTitle: {title}"]))

        return None, WikipediaPageStatus.FAIL_OS_ERROR

    def process(self,
                title: str) -> tuple:

        if not title or not len(title):
            return None, WikipediaPageStatus.FAIL_INVALID_INPUT

        # if no ascii character input exists, don't bother moving forward
        if sum([ch.isascii() for ch in title]) == 0:
            return None, WikipediaPageStatus.FAIL_INVALID_INPUT

        try:

            page = wiki_page(title=title,
                             pageid=None,
                             preload=True,
                             redirect=True,
                             auto_suggest=self._auto_suggest)

            return page, WikipediaPageStatus.PASS

        except KeyError as e:
            self.logger.exception(e)
            return self._key_error(title)

        except OSError as e:
            self.logger.exception(e)
            return self._os_error(title)

        except PageError as e:
            self.logger.exception(e)
            return self._page_error(title)

        except DisambiguationError as e:
            self.logger.exception(e)
            return self._disambiguation_error(title)

        except WikipediaException as e:
            self.logger.exception(e)
            return self._wikipedia_error(title)

        return None, WikipediaPageStatus.FAIL_OTHER
