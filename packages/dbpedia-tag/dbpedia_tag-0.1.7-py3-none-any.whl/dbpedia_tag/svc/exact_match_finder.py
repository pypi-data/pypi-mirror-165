#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Sliding Window Extraction for Candidate Synonym Swapping """


from typing import Callable

from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from dbpedia_tag.dmo import SlidingWindowExtract
from dbpedia_tag.dmo import SlidingWindowBlacklist
from dbpedia_tag.dmo import SlidingWindowValidate


class ExactMatchFinder(BaseObject):
    """ Perform Sliding Window Extraction for Candidate Synonym Swapping """

    def __init__(self,
                 gram_size: int,
                 entity_exists: Callable):
        """
        Created:
            24-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._gram_size = gram_size
        self._entity_exists = entity_exists

    def _process(self,
                 tokens: list) -> dict:

        candidates_1 = SlidingWindowExtract(
            tokens=tokens,
            gram_size=self._gram_size).process()

        if not candidates_1 or not len(candidates_1):
            return None

        candidates_2 = SlidingWindowBlacklist().process(candidates_1)

        candidates_3 = SlidingWindowValidate(
            candidates=candidates_2,
            entity_exists=self._entity_exists).process()

        unmatched = [x for x in candidates_2 if x not in candidates_3]
        if not unmatched or not len(unmatched):
            return None

        return {
            'input': tokens,
            'extracted': candidates_1,
            'validated': candidates_3,
            'unmatched': unmatched
        }

    def process(self,
                tokens: list) -> list:
        sw = Stopwatch()

        d_results = self._process(tokens)

        if self.isEnabledForInfo:

            def total_results() -> int:
                if d_results:
                    return len(d_results)
                return 0

            if self.isEnabledForInfo:
                self.logger.info('\n'.join([
                    "Sliding Window Completed",
                    f"\tGram Size: {self._gram_size}",
                    f"\tTotal Results: {total_results()}",
                    f"\tTotal Time: {str(sw)}"]))

        if self.isEnabledForDebug and d_results:
            Enforcer.keys(d_results, 'input', 'extracted',
                          'validated', 'unmatched')

        return d_results
