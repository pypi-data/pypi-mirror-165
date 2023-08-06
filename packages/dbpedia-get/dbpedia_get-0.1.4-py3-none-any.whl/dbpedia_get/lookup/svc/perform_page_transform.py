#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from wikipedia import WikipediaPage

from baseblock import BaseObject

from dbpedia_get.lookup.dmo import DBPediaContentNormalizer


class PerformPageTransform(BaseObject):
    """ for a given dbPedia page, create a JSON structure """

    def __init__(self,
                 ):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)
        self._normalize_page = DBPediaContentNormalizer().process

    def _normalized(self,
                    content: list or str) -> list:
        if type(content) == str:
            content = [content]

        return self._normalize_page(content)

    def _summary(self,
                 page: WikipediaPage) -> list:
        return self._normalized(page.summary)

    def _content(self,
                 page: WikipediaPage) -> list:
        return self._normalized(page.content)

    def process(self,
                title: str,
                page: WikipediaPage) -> dict:
        """_summary_

        Args:
            title (str): _description_
            page (WikipediaPage): _description_

        Returns:
            dict: _description_
        """

        def _references():
            try:
                return page.references
            except Exception as e:
                self.logger.error(e)

        def _categories():
            try:
                return page.categories
            except Exception as e:
                self.logger.error(e)

        def _sections():
            try:
                return page.sections
            except Exception as e:
                self.logger.error(e)

        def _parent_id():
            try:
                return str(page.parent_id)
            except Exception as e:
                self.logger.error(e)

        def _page_id():
            try:
                return str(page.pageid)
            except Exception as e:
                self.logger.error(e)

        def _revision_id():
            try:
                return str(page.revision_id)
            except Exception as e:
                self.logger.error(e)

        def _url():
            try:
                return page.url
            except Exception as e:
                self.logger.error(e)

        def _links():
            try:
                return page.links
            except Exception as e:
                self.logger.error(e)

        def _title():
            try:
                return page.title
            except Exception as e:
                self.logger.error(e)

        def _original_title():
            try:
                return page.original_title
            except Exception as e:
                self.logger.error(e)

        return {"key": title,
                "url": _url(),
                "title": _title(),
                "links": _links(),
                "content": self._content(page),
                "page_id": _page_id(),
                "summary": self._summary(page),
                "sections": _sections(),
                "parent_id": _parent_id(),
                "categories": _categories(),
                "references": _references(),
                "revision_id": _revision_id(),
                "original_title": _original_title()}
