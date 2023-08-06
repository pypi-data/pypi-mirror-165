#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Match Tokens against the dbPedia Dictionaries """


from typing import Callable

from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject


class SlidingWindowMatch(BaseObject):
    """ Match Tokens against the dbPedia Dictionaries """

    def __init__(self,
                 entity_exists: Callable):
        """ Change Log

        Created:
            24-Aug-2022
            craigtrim@gmail.com
        Updated:
            26-Aug-2022
            craigtrim@gmail.com

        Args:
            entity_exists (Callable): callback to the dbpedia-ent function
        """
        BaseObject.__init__(self, __name__)
        self._entity_exists = entity_exists

    def _process(self,
                 candidates: list) -> list:

        normalized = []

        for candidate in candidates:
            if self._entity_exists(candidate):
                normalized.append(candidate)

        return normalized

    def process(self,
                candidates: list) -> list:
        sw = Stopwatch()

        results = self._process(candidates)

        if self.isEnabledForDebug:
            if results and len(results):
                Enforcer.is_list_of_str(results)
            removed = set(candidates).difference(set(results))

            self.logger.debug('\n'.join([
                "Sliding Window Location Completed",
                f"\tRemoved Tokens: {list(removed)}",
                f"\tRetained Tokens: {results}",
                f"\tTotal Time: {str(sw)}"]))

        return results
