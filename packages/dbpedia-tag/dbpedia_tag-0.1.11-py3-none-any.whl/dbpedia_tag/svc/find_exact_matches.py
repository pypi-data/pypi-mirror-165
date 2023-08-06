#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Sliding Window Extraction for Candidate Synonym Swapping """


from typing import Callable

from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from dbpedia_tag.dmo import SlidingWindowExtract
from dbpedia_tag.dmo import SlidingWindowBlacklist
from dbpedia_tag.dmo import SlidingWindowMatch


class FindExactMatches(BaseObject):
    """ Perform Sliding Window Extraction for Candidate Synonym Swapping """

    def __init__(self,
                 entity_exists: Callable):
        """ Change Log:

        Created:
            24-Aug-2022
            craigtrim@gmail.com
        Updated:
            26-Aug-2022
            craigtrim@gmail.com
            *   refactor sliding window algorithm
                https://github.com/craigtrim/dbpedia-tag/issues/1

        Args:
            entity_exists (Callable): _description_
        """
        BaseObject.__init__(self, __name__)
        self._entity_exists = entity_exists

        self._extract_candidates = SlidingWindowExtract().process
        self._blacklist_candidates = SlidingWindowBlacklist().process
        self._match_candidates = SlidingWindowMatch(
            self._entity_exists).process

    def _process(self,
                 gram_size: int,
                 tokens: list) -> dict:

        candidates = self._extract_candidates(
            candidates=tokens,
            gram_size=gram_size)

        if not candidates or not len(candidates):
            return None

        candidates = self._blacklist_candidates(candidates)
        matched = self._match_candidates(candidates)

        unmatched = [x for x in candidates if x not in matched]

        return {
            'input': tokens,
            'candidates': candidates,
            'matched': matched,
            'unmatched': unmatched
        }

    def process(self,
                gram_size: int,
                tokens: list) -> list:

        sw = Stopwatch()

        d_results = self._process(tokens=tokens,
                                  gram_size=gram_size)

        if self.isEnabledForInfo:

            def total_results() -> int:
                if d_results:
                    return len(d_results)
                return 0

            if self.isEnabledForInfo:
                self.logger.info('\n'.join([
                    "Sliding Window Completed",
                    f"\tGram Size: {gram_size}",
                    f"\tTotal Results: {total_results()}",
                    f"\tTotal Time: {str(sw)}"]))

        if self.isEnabledForDebug and d_results:
            Enforcer.keys(d_results,
                          'input', 'candidates', 'matched', 'unmatched')

        return d_results
