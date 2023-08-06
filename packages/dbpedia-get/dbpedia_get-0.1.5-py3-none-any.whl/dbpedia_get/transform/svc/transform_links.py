#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Transform the External References list of Links """


from pprint import pprint

from baseblock import BaseObject




class TransformLinks(BaseObject):
    """ Transform the External References list of Links """

    def __init__(self):
        """ Change Log

        Created:
            25-Aug-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)

    def process(self,
                entity_name: str) -> list or None:
        from dbpedia_get import find_article
        d_page = find_article(entity_name)
        pprint(d_page)
