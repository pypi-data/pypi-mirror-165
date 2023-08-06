#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Recipe for Downloading Categories from a Page """

from dbpedia_get.recipes import DownloadCategories

process = DownloadCategories().process


def download_categories(entity_name: str) -> None:
    process(entity_name)


def main(entity_name):
    download_categories(entity_name)


if __name__ == "__main__":
    import plac
    plac.call(main)
