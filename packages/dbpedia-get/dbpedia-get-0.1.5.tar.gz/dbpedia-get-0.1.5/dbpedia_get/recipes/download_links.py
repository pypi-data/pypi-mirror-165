#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" API for dbPedia Recipes """


from baseblock import BaseObject

from dbpedia_get.lookup.dmo import PageCacheReader
from dbpedia_get.lookup.bp import LookupOrchestrator


class DownloadLinks(BaseObject):
    """ API for dbPedia Recipes """

    def __init__(self):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/3
        Updated:
            25-Aug-2022
            craigtrim@gmail.com
            *   expose functions outside of class
        """
        BaseObject.__init__(self, __name__)
        self._lookup = LookupOrchestrator().process

    def _download_named_link(self,
                             link_name: str) -> dict:
        """ Download the dbPedia page corresponding to a named link

        Args:
            link_name (str): the link name

        Returns:
            dict: the corresponding dbPedia page
        """
        entity_type = link_name
        entity_name = link_name.replace(' ', '_').lower()
        entity_label = link_name

        return self._lookup(
            entity_type=entity_type,
            entity_name=entity_name,
            entity_label=entity_label)

    def download_all_links(self) -> None:
        """ Download the Links for all Cached Pages """
        d_results = PageCacheReader().process()

        for key in d_results:
            [self._download_named_link(x) for x in d_results[key]['links']]

    def download_links(self,
                       entity_type: str,
                       entity_name: str,
                       entity_label: str) -> int:
        """ Download the Links for a given Entity

        Args:
            entity_type (str): the type of entity
                e.g.,   the object in an rdfs:subClass relationship
            entity_name (str): the name of the entity
                e.g.,   the subject of an rdf:type relationship
            entity_label (str): the human readable label for the entity
                e.g.,   the object of an rdfs:label relationship

        Returns:
            int: the number of links accessed
        """
        d_page = self._lookup(
            entity_type=entity_type,
            entity_name=entity_name,
            entity_label=entity_label)

        if 'links' not in d_page:
            return 0

        [self._download_named_link(x) for x in d_page['links']]

        return len(d_page['links'])


downloader = DownloadLinks()


def download_all_links() -> None:
    downloader.download_all_links()


def download_links(entity_type: str,
                   entity_name: str,
                   entity_label: str) -> int:
    return downloader.download_links(
        entity_type=entity_type,
        entity_name=entity_name,
        entity_label=entity_label)
