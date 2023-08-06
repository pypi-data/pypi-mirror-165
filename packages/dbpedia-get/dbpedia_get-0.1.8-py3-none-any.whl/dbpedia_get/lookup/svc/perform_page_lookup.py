#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" for a given input find the associated dbPedia entry """


from typing import Callable

from baseblock import BaseObject

from dbpedia_get.lookup.dmo import DBpediaPageFinder
from dbpedia_get.lookup.dmo import PageCacheIO
from dbpedia_get.lookup.dmo import PageTitlePath
from dbpedia_get.lookup.dto import WikipediaPageStatus


class PerformPageLookup(BaseObject):
    """ for a given input find the associated dbPedia entry """

    def __init__(self,
                 auto_suggest: bool,
                 transform_page: Callable):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1

        Args:
            auto_suggest (bool): _description_
        """
        BaseObject.__init__(self, __name__)
        self._transform_page = transform_page
        self._pathr = PageTitlePath().process
        self._finder = DBpediaPageFinder(auto_suggest)

        cache = PageCacheIO()
        self._read = cache.read
        self._write = cache.write
        self._write_fail = cache.write_fail

    def process(self,
                entity_type: str,
                entity_name: str,
                entity_label: str) -> tuple:
        """ Lookup a dbPedia Page for the provided information

        Args:
            entity_type (str): the type of entity
                e.g.,   the object in an rdfs:subClass relationship
            entity_name (str): the name of the entity
                e.g.,   the subject of an rdf:type relationship
            entity_label (str): the human readable label for the entity
                e.g.,   the object of an rdfs:label relationship

        Sample Usage:
            to look up the dbPedia page for 'network topology' use the following parameters:
                bp.process(
                    entity_type='topology',
                    entity_name='network_topology',
                    entity_label='network topology')

            The most important parameter is entity_name; but entity_type and entity_label are both useful
                when there is a need to differentiate an ambigous entity_name
                e.g.,   if you want the dbpedia page for the 'pandas' software package
                        an entity_type of 'software' will help you differentiate from pandas as an animal

        Returns:
            dict: _description_
        """

        title_path = self._pathr(
            title=entity_name,
            make_dirs=True)

        d_page = self._read(title_path)
        if d_page is not None and "content" in d_page and len(d_page["content"]):
            return d_page, WikipediaPageStatus.FROM_CACHE

        w_page, status = self._finder.process(entity_label)
        if not w_page:
            self._write_fail(status=status,
                             title_path=title_path,
                             entity_type=entity_type,
                             entity_name=entity_name,
                             entity_label=entity_label)
            return None, status

        d_page = self._transform_page(page=w_page,
                                      title=entity_name)
        if d_page is None or not len(d_page):
            return None, WikipediaPageStatus.FAIL_TRANSFORM

        d_page["entity"] = {
            "type": entity_type,
            "name": entity_name,
            "label": entity_label
        }

        self._write(d_page=d_page,
                    title_path=title_path)

        return d_page, status
