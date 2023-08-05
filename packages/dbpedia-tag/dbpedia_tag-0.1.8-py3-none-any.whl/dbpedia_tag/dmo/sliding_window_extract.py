#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Tokens using a Sliding Window Algorithm """


from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject


class SlidingWindowExtract(BaseObject):
    """ Extract Tokens using a Sliding Window Algorithm """

    def __init__(self):
        """ Change Log

        Created:
            24-Aug-2022
            craigtrim@gmail.com
        Updated:
            26-Aug-2022
            craigtrim@gmail.com
            *   ensure consistency of output
                https://github.com/craigtrim/dbpedia-tag/issues/1
        """
        BaseObject.__init__(self, __name__)

    @staticmethod
    def _normalize(results: list) -> list:
        normalized = []
        for result in results:

            output = result
            if type(result) == list:
                output = ' '.join(result).strip()

            normalized.append(output.replace('  ', ' ').strip())

        return normalized

    def _process(self,
                 gram_size: int,
                 candidates: list) -> list:
        results = []

        if gram_size == len(candidates):
            return [' '.join(candidates).strip()]

        if gram_size == 1:
            return self._normalize(candidates)

        x = 0
        y = x + gram_size

        while y <= len(candidates):
            results.append(candidates[x: y])

            x += 1
            y = x + gram_size

        normalized = []
        for result in results:
            output = ' '.join(result).strip()
            output = output.replace('  ', ' ')
            normalized.append(output)

        return normalized

    def process(self,
                gram_size: int,
                candidates: list) -> list:
        """ Entry Point

        Args:
            gram_size (int): the gram size to execute the sliding window at
            candidates (list): the incoming tokens to run the sliding window against

        Returns:
            list: extraction of candidates by gram level
        """
        sw = Stopwatch()

        results = self._process(gram_size=gram_size,
                                candidates=candidates)

        if self.isEnabledForDebug:
            if results:
                Enforcer.is_list_of_str(results)

            self.logger.debug('\n'.join([
                "Sliding Window Extraction Completed",
                f"\tGram Size: {gram_size}",
                f"\tExtracted Tokens: {results}",
                f"\tTotal Time: {str(sw)}"]))

        return results
