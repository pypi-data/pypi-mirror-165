#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" dbPedia Orchestrator for Transforming Wikipedia Content """


from baseblock import BaseObject


from dbpedia_get.transform.svc import TransformCategories


class TransformOrchestrator(BaseObject):
    """ dbPedia Orchestrator for Transforming Wikipedia Content """

    def __init__(self):
        """ Change Log

        Created:
            25-Aug-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)
        self._transform = TransformCategories().process

    def categories(self,
                   entity_name: str) -> list or None:
        return self._transform(entity_name)
