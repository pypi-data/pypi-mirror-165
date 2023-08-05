#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Blacklist certain Tokens from the sliding window result """


from typing import Text
from baseblock import TextUtils
from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from dbpedia_tag.dto import stopwords


class SlidingWindowBlacklist(BaseObject):
    """ Blacklist certain Tokens from the sliding window result """

    def __init__(self):
        """
        Created:
            24-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)

    def _length_check(self,
                      candidates: list) -> list:

        normalized = []
        for candidate in candidates:

            len_of_candidate = len(candidate)
            if len_of_candidate < 5:
                continue

            # count the length minus the spaces
            if len_of_candidate - candidate.count(' ') < 5:
                continue

            normalized.append(candidate)

        return normalized

    def _punkt_check(self,
                     candidates: list) -> list:

        normalized = []
        for candidate in candidates:

            if ' ' not in candidate:
                normalized.append(candidate)
                continue

            # avoid any n-grams where a single gram is only punctuation
            grams = candidate.split()
            if not len([x for x in grams if TextUtils.is_punctuation(x)]):
                normalized.append(candidate)

        return normalized

    def _process(self,
                 candidates: list) -> list:

        candidates = [x for x in candidates
                      if x not in stopwords]

        candidates = self._length_check(candidates)
        candidates = self._punkt_check(candidates)

        return candidates

    def process(self,
                candidates: list) -> list:
        sw = Stopwatch()

        results = self._process(candidates)

        if self.isEnabledForDebug:
            if results:
                Enforcer.is_list_of_str(results)

            removed = set(candidates).difference(set(results))

            self.logger.debug('\n'.join([
                "Sliding Window Blacklist Completed",
                f"\tRemoved Tokens: {list(removed)}",
                f"\tRetained Tokens: {results}",
                f"\tTotal Time: {str(sw)}"]))

        return results
