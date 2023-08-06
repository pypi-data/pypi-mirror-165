#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from baseblock import EnvIO
from baseblock import Stopwatch
from baseblock import BaseObject

from dbpedia_get.lookup.dmo import PageCacheReader

from dbpedia_get.lookup.svc import PerformPageTransform
from dbpedia_get.lookup.svc import PerformPageLookup


class LookupOrchestrator(BaseObject):
    """ dbPedia Orchestrator for Wikipedia Lookup """

    def __init__(self):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)
        auto_suggest = EnvIO.exists_as_true('AUTO_SUGGEST')

        self._find_page = PerformPageLookup(
            auto_suggest=auto_suggest,
            transform_page=PerformPageTransform().process).process

    def process(self,
                entity_type: str,
                entity_name: str,
                entity_label: str) -> dict:
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
            dict: the JSON rendering of the dbPedia page
        """

        sw = Stopwatch()

        d_results = PageCacheReader().process()

        if entity_name in d_results:
            if self.isEnabledForDebug:
                self.logger.debug('\n'.join([
                    "Entity Exists in Cache",
                    f"\tEntity Type: {entity_type}",
                    f"\tEntity Name: {entity_name}",
                    f"\tEntity Label: {entity_label}"]))
            return d_results[entity_name]

        d_page, status = self._find_page(
            entity_type=entity_type,
            entity_name=entity_name,
            entity_label=entity_label)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Lookup Orchestration Completed",
                f"\tTotal Time: {str(sw)}",
                f"\tStatus: {status}",
                f"\tEntity Type: {entity_type}",
                f"\tEntity Name: {entity_name}",
                f"\tEntity Label: {entity_label}"]))

        return d_page
