#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from baseblock import EnvIO


from dbpedia_get.recipes import download_links


def main():

    entity_type = EnvIO.str_or_exception('ENTITY_TYPE')
    entity_name = EnvIO.str_or_exception('ENTITY_NAME')
    entity_label = EnvIO.str_or_exception('ENTITY_LABEL')

    download_links(entity_type=entity_type,
                   entity_name=entity_name,
                   entity_label=entity_label)


if __name__ == "__main__":
    main()
