#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Blacklist certain Tokens from the sliding window result """


from pprint import pformat

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

    def _process(self,
                 candidates: list) -> list:
        for candidate in candidates:
            print (candidate)
            if type(candidate) == list:
                raise ValueError
        return [x for x in candidates if x not in stopwords]

    def process(self,
                candidates: list) -> list:
        sw = Stopwatch()

        results = self._process(candidates)

        if self.isEnabledForDebug:

            self.logger.debug('\n'.join([
                "Sliding Window Blacklist Completed",
                f"\tTotal Tokens: {len(candidates)}",
                f"\tTotal Time: {str(sw)}"]))

            if candidates != results:
                self.logger.debug('\n'.join([
                    "Sliding Window Blacklist Completed",
                    f"\tTokens: {pformat(candidates, indent=4)}"]))

        return candidates
