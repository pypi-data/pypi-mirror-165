#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Token Candidate Fuzzy Matching """


from enum import Enum
from typing import Callable
from collections import defaultdict

from baseblock import Stopwatch
from baseblock import TextUtils
from baseblock import BaseObject


class MatchType(Enum):  # debug codes
    TYPE_00 = 0
    TYPE_10 = 10
    TYPE_11 = 11
    TYPE_12 = 12
    TYPE_20 = 20
    TYPE_21 = 21
    TYPE_30 = 30
    TYPE_31 = 31
    TYPE_40 = 40
    TYPE_41 = 41
    TYPE_50 = 50
    TYPE_51 = 51


class CandidateFuzzyMatch(BaseObject):
    """ Perform Token Candidate Fuzzy Matching """

    def __init__(self,
                 entity_finder: Callable):
        """
        Created:
            24-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._entity_finder = entity_finder

    @staticmethod
    def _trie_exclusion(token: str,
                        candidates: list) -> list:
        """ Progressively narrow down tokens

        Args:
            token (str): the token to match
            candidates (list): the incoming candidates

        Returns:
            list: the remaining candidates
        """

        token = token.replace(' ', '_').lower()

        for i in range(4, len(token) - 1):

            if len(token) < i:
                return candidates
            if len(candidates) <= 3:
                return candidates

            candidates = [candidate for candidate in candidates
                          if i < len(candidate) and
                          candidate[i-1] == token[i-1]]

            if len(candidates) == 1:
                score = TextUtils.jaccard_similarity(token, candidates[0])
                if score >= 0.90:
                    return candidates
                return []

        return candidates

    @staticmethod
    def _length_filter(token: str,
                       candidates: list) -> list:
        """ Exclude Candidates to Short or too Long to be useful matches

        Heuristic:
            Narrow candidates down to +/- 2
            this covers suffixes such as the gerund form (e.g., "<word>ing" => "<word>")

        Args:
            token (str): the token to match
            candidates (list): the incoming candidates

        Returns:
            list: the remaining candidates
        """
        x = len(token) - 3
        y = len(token) + 3
        return [candidate for candidate in candidates
                if len(candidate) >= x and len(candidate) <= y]

    @staticmethod
    def _suffix_match(token: str,
                      candidates: list) -> str or None:
        """ Search Candidate for Common Suffixes

        e.g.,   if the token is 'Restaurants' and there exists a candidate 'Restaurant'
                then use this

        Args:
            token (str): the token to match
            candidates (list): the incoming candidates

        Returns:
            str: the closest candidate (if any)
        """

        suffixes = ['s', 'ies', 'ing', 'ed', 'ly']
        for suffix in suffixes:
            if token.endswith(suffix):
                candidates = [candidate for candidate in candidates
                              if token[:-len(suffix)] == candidate]
                if len(candidates) == 1:
                    return candidates[0]

    def _similarity_match(self,
                          token: str,
                          candidates: list) -> str or None:
        """ Use Jaccard Similarity to find the closest match

        Args:
            token (str): the token to match
            candidates (list): the incoming candidates

        Returns:
            str: the closest candidate (if any)
        """

        d_score = defaultdict(list)
        for candidate in candidates:
            token = token.replace(' ', '_').lower()
            score = TextUtils.jaccard_similarity(token, candidate)

            if self.isEnabledForDebug:
                self.logger.debug('\n'.join([
                    "Similarity Score Completed",
                    f"\tToken: {token}",
                    f"\tCandidate: {candidate}",
                    f"\tScore: {score}"]))

            if score >= 0.90:
                d_score[score].append(candidate)

        if not len(d_score):
            return None

        # find the values with the highest score
        # there may be more than 1
        values = d_score[max(d_score)]

        # find the values with the minimum length
        # it seems unlikely there would be more than 1, since this would imply duplicate values
        d_values = {len(value): value for value in values}

        return d_values[min(d_values)]

    def _process(self,
                 token: str) -> tuple or None:

        if len(token) < 3:
            return None, MatchType.TYPE_00.name

        candidates = self._entity_finder(token)

        if not candidates or not len(candidates):
            return None, MatchType.TYPE_10.name
        if token in candidates:
            return token, MatchType.TYPE_11.name
        if len(candidates) == 1:
            return candidates[0], MatchType.TYPE_12.name

        candidates = self._length_filter(token, candidates)
        if not len(candidates):
            return None, MatchType.TYPE_20.name
        if len(candidates) == 1:
            return candidates[0], MatchType.TYPE_21.name

        candidates = self._trie_exclusion(token, candidates)
        if not len(candidates):
            return None, MatchType.TYPE_30.name
        if len(candidates) == 1:
            return candidates[0], MatchType.TYPE_31.name

        candidate = self._suffix_match(token, candidates)
        if candidate:
            return candidate, MatchType.TYPE_40.name

        candidate = self._similarity_match(token, candidates)
        if candidate:
            return candidate, MatchType.TYPE_50.name

        return None, MatchType.TYPE_51.name

    def process(self,
                token: str) -> str or None:
        sw = Stopwatch()

        result, reason = self._process(token)

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                "Fuzzy Match Completed",
                f"\tUnknown Token: {token}",
                f"\tFuzzy Token: {result}",
                f"\tMatch Type: {reason}",
                f"\tTotal Time: {str(sw)}"]))

        return result
