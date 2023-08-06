#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from dbpedia_get.lookup.bp import LookupOrchestrator

from baseblock import EnvIO


def main():

    entity_type = EnvIO.str_or_exception('ENTITY_TYPE')
    entity_name = EnvIO.str_or_exception('ENTITY_NAME')
    entity_label = EnvIO.str_or_exception('ENTITY_LABEL')

    bp = LookupOrchestrator()
    bp.process(entity_type=entity_type,
               entity_name=entity_name,
               entity_label=entity_label)


if __name__ == "__main__":
    main()
