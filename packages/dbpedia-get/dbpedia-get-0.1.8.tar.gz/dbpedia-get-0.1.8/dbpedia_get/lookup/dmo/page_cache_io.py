#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import os

from baseblock import FileIO
from baseblock import BaseObject

from dbpedia_get.lookup.dto import WikipediaPageStatus


class PageCacheIO(BaseObject):
    """ I/O Operations for a DBpedia page from disk (cache) """

    def __init__(self):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)

    def read(self,
             title_path: str) -> dict or None:

        if not os.path.exists(title_path):
            if self.isEnabledForDebug:
                self.logger.debug('\n'.join([
                    "DBpedia Article Not Cached",
                    f"\tPath: {title_path}"]))
            return None

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Reading DBpedia Article from File",
                f"\tPath: {title_path}"]))

        return FileIO.read_json(title_path)

    def write_fail(self,
                   title_path: str,
                   entity_type: str,
                   entity_name: str,
                   entity_label: str,
                   status: WikipediaPageStatus) -> str:
        """ This method writes an empty file to the cache
            This prevents the system from continually requesting a page that does not exist

        Args:
            title_path (str): the path of the local copy
            entity_type (str): the type of entity
                e.g.,   the object in an rdfs:subClass relationship
            entity_name (str): the name of the entity
                e.g.,   the subject of an rdf:type relationship
            entity_label (str): the human readable label for the entity
                e.g.,   the object of an rdfs:label relationship
            status (WikipediaPageStatus): the status of the request

        Returns:
            str: the title path
        """

        d_page = {
            "is_empty": True,
            "status": status.name,
            "entity": {
                "type": entity_type,
                "name": entity_name,
                "label": entity_label
            }
        }

        FileIO.write_json(data=d_page,
                          file_path=title_path)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Wrote Empty Entity to File",
                f"\tPath: {title_path}"]))

        return title_path

    def write(self,
              d_page: dict,
              title_path: str) -> str:

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Caching DBpedia Article to File",
                f"\tPath: {title_path}"]))

        FileIO.write_json(data=d_page,
                          file_path=title_path)

        return title_path
