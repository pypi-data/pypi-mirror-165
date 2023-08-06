#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from baseblock import TextUtils
from baseblock import BaseObject

from dbpedia_get.lookup.dto import WikipediaPageStatus


class PageCacheEntry(BaseObject):
    """ Create an Entry in the Page Cache """

    def __init__(self):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        Updated:
            24-Aug-2022
            craigtrim@gmail.com
            *   replace 'lev-ratio' with jaccard sim from baseblock
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def _summary(d_page: dict,
                 threshold: int = 100) -> str:
        tokens = []
        for sentence in d_page['summary']:

            for sentoken in sentence.split(' '):
                tokens.append(sentoken)

                if len(''.join(tokens)) > threshold:
                    return f"{' '.join(tokens)} ..."

        return f"{' '.join(tokens)} ..."

    # @staticmethod
    # def _lev_ratio(entity_label: str,
    #                title: str) -> int:
    #     """ Purpose
    #     Derive the Levenstein Ratio between
    #     Entity Label and Wikipedia Entry Title """

    #     title = title.lower().replace('_', ' ')
    #     entity_label = entity_label.lower().replace('_', ' ')

    #     lev_ratio = lev.ratio(entity_label, title)

    #     if lev_ratio == 1:
    #         return 100
    #     if lev_ratio == 0:
    #         return 0

    #     return int(round(lev_ratio * 100, 0))

    def process(self,
                d_page: dict,
                status: WikipediaPageStatus) -> dict:

        def title() -> str or None:
            if d_page:
                return d_page['title']

        title = title()

        def summary() -> str or None:
            if d_page:
                return self._summary(d_page)

        def url() -> str or None:
            if d_page:
                return d_page["url"]

        def ratio() -> str:
            if d_page:
                score = TextUtils.jaccard_similarity(
                    title, d_page["entity"]["label"])
                score = int(round(score * 100, 0))
                return score
                # return self._lev_ratio(title=title,
                #                        entity_label=d_page["entity"]["label"])
            return 0

        return {
            "URL": url(),
            "Title": title,
            "Ratio": ratio(),
            "Summary": summary(),
            "Status": status.name,
            "entity": {
                "type": d_page["entity"]["type"],
                "name": d_page["entity"]["name"],
                "label": d_page["entity"]["label"],
            },
        }
