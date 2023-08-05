#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Validate Tokens against the dbPedia Dictionaries """


from pprint import pformat
from typing import Callable
from wsgiref import validate

from baseblock import Stopwatch
from baseblock import BaseObject

from dbpedia_ent import Finder


class SlidingWindowValidate(BaseObject):
    """ Validate Tokens against the dbPedia Dictionaries """

    def __init__(self,
                 candidates: list,
                 entity_exists: Callable):
        """
        Created:
            24-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._candidates = candidates
        self._entity_exists = entity_exists

    def _process(self) -> list:

        normalized = []

        for candidate in self._candidates:

            def get_entity() -> str:
                if type(candidate) == list:
                    return ' '.join(candidate)
                return candidate

            entity = get_entity()
            if len(entity) < 3:
                continue

            if self._entity_exists(entity):
                normalized.append(entity)

        return normalized

    def process(self) -> list:
        sw = Stopwatch()

        results = self._process()

        if self.isEnabledForDebug:

            self.logger.debug('\n'.join([
                "Sliding Window Validation Completed",
                f"\tTotal Tokens: {len(results)}",
                f"\tTotal Time: {str(sw)}"]))

            if self._candidates != results:
                self.logger.debug('\n'.join([
                    "Sliding Window Validation Results",
                    f"\tTokens: {pformat(results, indent=4)}"]))

        return results
