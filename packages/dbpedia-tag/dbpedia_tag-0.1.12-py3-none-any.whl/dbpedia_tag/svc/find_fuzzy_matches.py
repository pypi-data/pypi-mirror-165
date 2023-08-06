#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Fuzzy Matching on unmatched tokens """


from typing import Callable

from baseblock import Stopwatch
from baseblock import BaseObject

from dbpedia_tag.dmo import CandidateFuzzyMatch


class FindFuzzyMatches(BaseObject):
    """ Perform Fuzzy Matching on Tokens that don't have an exact match to the dbpedia tries """

    def __init__(self,
                 entity_finder: Callable):
        """
        Created:
            24-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._fuzzy_match = CandidateFuzzyMatch(entity_finder).process

    def _process(self,
                 tokens: list) -> dict:

        d_fuzzy = {}

        for token in tokens:
            if type(token) == list:
                token = ' '.join(token)
            d_fuzzy[token] = self._fuzzy_match(token)

        return d_fuzzy

    def process(self,
                tokens: list) -> list:
        sw = Stopwatch()

        d_fuzzy = self._process(tokens)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Sliding Window Completed",
                f"\tTotal Time: {str(sw)}",
                f"\tResults: {d_fuzzy}"]))

        return d_fuzzy
