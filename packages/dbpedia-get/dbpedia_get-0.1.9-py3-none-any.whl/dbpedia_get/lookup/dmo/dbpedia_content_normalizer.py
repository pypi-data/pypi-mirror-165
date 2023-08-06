#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from baseblock import BaseObject

from fast_sentence_segment import Segmenter


class DBPediaContentNormalizer(BaseObject):
    """ Normalize the DBPedia Content Section """

    def __init__(self):
        """ Change Log

        Created:
            14-Jul-2022
            craigtrim@gmail.com
            *   https://github.com/craigtrim/dbpedia/issues/1
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    # TODO: replace with 'from fast_sentence_segment import segment_text'
    def _segment_text(input_text, flatten: bool = False) -> list:
        segment = Segmenter().input_text

        results = segment(input_text)

        if flatten:
            flat = []
            [[flat.append(y) for y in x] for x in results]
            return flat

        return results

    def _process(self,
                 content: list) -> list:

        def _split() -> list:
            master = []

            for item in content:
                for line in item.split('\n'):
                    master.append(line)

            master = [line.strip() for line in master if line]
            master = [line for line in master if line and len(line)]

            return master

        def _sentencize(lines: list) -> list:

            master = []
            for line in lines:
                while '  ' in line:
                    line = line.replace('  ', ' ')

                [master.append(x) for x in
                 self._segment_text(line, flatten=True)]

            master = [line.strip() for line in master if line]
            master = [line for line in master if line and len(line)]

            return master

        return _sentencize(_split())

    def process(self,
                content: list) -> list:
        return self._process(content)
