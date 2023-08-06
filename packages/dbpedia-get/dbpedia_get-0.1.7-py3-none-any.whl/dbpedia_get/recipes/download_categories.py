#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Recipe for Downloading Categories from a Page """


from baseblock import BaseObject

from dbpedia_get.lookup.dmo import PageCacheReader
from dbpedia_get.lookup.bp import LookupOrchestrator
from dbpedia_get.transform.bp import TransformOrchestrator


class DownloadCategories(BaseObject):
    """ Recipe for Downloading Categories from a Page """

    def __init__(self):
        """ Change Log

        Created:
            25-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._find_categories = TransformOrchestrator().categories

    def process(self,
                entity_name: str):
        categories = self._find_categories(entity_name)
        print (categories)
        
        # #for category in categories:
        # print (self._find_categories(f"Category:Fast-food_hamburger_restaurants"))
