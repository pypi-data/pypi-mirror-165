#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Blacklist certain Tokens from the sliding window result """


from baseblock import EnvIO
from baseblock import TextUtils
from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject

from dbpedia_tag.dto import stopwords


MIN_LEN_THRESHOLD = EnvIO.int_or_default('MIN_LEN_THRESHOLD', 4)


class SlidingWindowBlacklist(BaseObject):
    """ Blacklist certain Tokens from the sliding window result """

    def __init__(self):
        """
        Created:
            24-Aug-2022
            craigtrim@gmail.com
        Updated:
            26-Aug-2022
            craigtrim@gmail.com
            *   refactor filtering into multiple methods
        """
        BaseObject.__init__(self, __name__)

    def _length_check(self,
                      candidates: list) -> list:

        normalized = []
        for candidate in candidates:

            len_of_candidate = len(candidate)
            if len_of_candidate < MIN_LEN_THRESHOLD:
                continue

            # count the length minus the spaces
            if len_of_candidate - candidate.count(' ') < MIN_LEN_THRESHOLD:
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

    def _stopword_filter(self,
                         candidates: list) -> list:
        """ Stopword Filtering removes low-value phrases and words

        Architectural Decisions:
            https://github.com/craigtrim/dbpedia-tag/issues/3
            Net Net: We can't remove all low-value words; this has to be a consumer strategy

        Args:
            candidates (list): the incoming candidates

        Returns:
            list: the potentially filtered candidates
        """

        normalized = []
        for candidate in candidates:

            if candidate in stopwords:
                continue

            # avoid any n-grams where even a single gram is a stopwrd
            grams = candidate.split()
            if not len([x for x in grams if x in stopwords]):
                normalized.append(candidate)

        return normalized

    def _process(self,
                 candidates: list) -> list:

        candidates = self._stopword_filter(candidates)
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
