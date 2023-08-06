#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Transform the list of Categories """


from baseblock import BaseObject


class TransformCategories(BaseObject):
    """ Transform the list of Categories 

    Sample Input:
        1919 establishments in California
        1967 mergers and acquisitions
        1970 mergers and acquisitions
        2002 mergers and acquisitions
        2011 mergers and acquisitions
        All articles needing examples
        All articles with unsourced statements
        Articles needing examples from April 2022
        Articles with short description
        Articles with unsourced statements from August 2022
        Articles with unsourced statements from February 2015
        Articles with unsourced statements from March 2019
        Commons category link is on Wikidata
        Companies based in Lexington, Kentucky
        Drive-in restaurants
        Fast-food chains of the United States
        Fast-food franchises
        Fast-food hamburger restaurants
        Hot dog restaurants
        Official website different in Wikidata and Wikipedia
        Privately held companies based in Kentucky
        Restaurant chains in the United States
        Restaurants established in 1919
        Root beer stands
        Short description matches Wikidata
        Use mdy dates from October 2021
        Wikipedia articles needing clarification from April 2022'

    Sample Output:
            1919 establishments in California
            1967 mergers and acquisitions
            1970 mergers and acquisitions
            2002 mergers and acquisitions
            2011 mergers and acquisitions
            All articles needing examples
            All articles with unsourced statements
            Articles needing examples from April 2022
            Articles with short description
            Articles with unsourced statements from August 2022
            Articles with unsourced statements from February 2015
            Articles with unsourced statements from March 2019
            Commons category link is on Wikidata
            Companies based in Lexington, Kentucky
        Drive-in restaurants
        Fast-food chains of the United States
        Fast-food franchises
        Fast-food hamburger restaurants
        Hot dog restaurants
            Official website different in Wikidata and Wikipedia
            Privately held companies based in Kentucky
        Restaurant chains in the United States
            Restaurants established in 1919
        Root beer stands
            Short description matches Wikidata
            Use mdy dates from October 2021
            Wikipedia articles needing clarification from April 2022'


    """

    __stop_phrases = [
        'establishments in',
        'mergers and acquisitions',
        'articles',
        'wikidata',
        'wikipedia',
        'based in',
        'mdy dates',
        'established in',
        'needing clarification',
        'of the united states',
        'in the united states',
    ]

    def __init__(self):
        """ Change Log

        Created:
            25-Aug-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)

    def _has_stop_phrase(self,
                         category: str) -> bool:
        category = category.lower().strip()
        for phrase in self.__stop_phrases:
            if phrase in category.lower():
                return True

        return False

    def process(self,
                entity_name: str) -> list or None:

        def get_article() -> str:
            from dbpedia_get import find_article
            return find_article(entity_name)

        d_page = get_article()
        if not d_page:
            return None
        if 'categories' not in d_page:
            return None

        categories = [x for x in d_page['categories']
                      if not self._has_stop_phrase(x)]

        categories = sorted(set(categories),
                            key=len, reverse=False)

        return categories
