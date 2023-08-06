#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os

from wikipedia import WikipediaPage

from baseblock import BaseObject

from dbpedia_get.lookup.dmo import PageCacheIO
from dbpedia_get.lookup.dmo import PageTitlePath
from dbpedia_get.lookup.dmo import PageCacheReader
from dbpedia_get.lookup.dmo import DBpediaPageFinder
from dbpedia_get.lookup.svc import PerformPageTransform


class FollowPageLinks(BaseObject):
    """ For a given page, download all the linked pages """

    def __init__(self):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)

        auto_suggest = os.environ['AUTO_SUGGEST'].lower() == 'true'

        self._cache = PageCacheIO()
        self._pathr = PageTitlePath().process
        self._finder = DBpediaPageFinder(auto_suggest)

    @staticmethod
    def _page_exists(d_page: dict) -> bool:
        if d_page is not None and "content" in d_page and len(d_page["content"]):
            return d_page

    def _page(self,
              entity_name: str) -> dict or None:
        d_page = self._cache.read(entity_name)
        if self._page_exists(d_page):
            return d_page

        self.logger.error('\n'.join([
            "Entity Page Not Found",
            f"\tEntity Name: {entity_name}"]))

        raise ValueError

    def _links(self,
               d_page: dict) -> dict:

        if "links" not in d_page:  # normal; empty page
            if self.isEnabledForInfo:
                self.logger.info('\n'.join([
                    "Empty Page",
                    "Entity Was Not Found in WikiPedia",
                    f"\tEntity Name: {d_page['entity']['name']}"]))
            return []

        links = d_page['links']

        links = [link for link in links
                 if 'list of' not in link.lower()]

        d_links = {link: self._cache.read(link)
                   for link in links}

        d_links = {link: d_links[link]
                   for link in d_links if d_links[link] is None}

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Retrieved Cached Page",
                f"\tEntity Name: {d_page['entity']['name']}",
                f"\tTotal Links: {len(links)}",
                f"\tTotal Uncached Links: {len(d_links)}"]))

        return d_links

    def _master_page(self,
                     entity_name: str) -> dict:
        if entity_name == "random":
            return PageCacheReader().random()

        return self._page(self._pathr(entity_name))

    def process(self,
                entity_type: str,
                entity_name: str,
                entity_label: str) -> tuple:

        d_master_page = self._master_page(entity_name)
        d_links = self._links(d_master_page)

        for link in d_links:
            title_path = self._pathr(title=link,
                                     make_dirs=True)
            w_page, status = self._finder.process(link)

            if not w_page:
                # we are spidering known Wikipedia Links,
                # so this should not happen (but it does...)
                self._cache.write_fail(status=status,
                                       title_path=title_path,
                                       entity_type=entity_type,
                                       entity_name=entity_name,
                                       entity_label=entity_label)
                if self.isEnabledForWarning:
                    self.logger.warning('\n'.join([
                        "Page Not Found",
                        f"\tEntity Name: {link}"]))
                continue

            svc_transform = PerformPageTransform(title=link,
                                                 page=w_page)

            d_page = svc_transform.process()
            if d_page is None or not len(d_page):
                self._cache.write_fail(status=status,
                                       title_path=title_path,
                                       entity_type=entity_type,
                                       entity_name=entity_name,
                                       entity_label=entity_label)
                if self.isEnabledForWarning:
                    self.logger.warning('\n'.join([
                        "Page Transformation Failed",
                        f"\tEntity Name: {link}"]))
                continue

            # we have no entity information;
            # these pages exist outside the CL KB
            d_page["entity"] = {
                "type": None,
                "name": None,
                "label": None}

            self._cache.write(d_page=d_page,
                              title_path=title_path)

            # persist twice if the link is actually a redirect to the primary page
            if link != d_page["title"]:
                self._cache.write(d_page=d_page,
                                  title_path=title_path)

        if entity_name == "random":
            self.process(entity_type="*",
                         entity_name="random",
                         entity_label="*")  # infinite recursion
