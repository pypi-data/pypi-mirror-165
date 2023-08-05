#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Extract Tokens using a Sliding Window Algorithm """


from pprint import pformat

from baseblock import Stopwatch
from baseblock import BaseObject


class SlidingWindowExtract(BaseObject):
    """ Extract Tokens using a Sliding Window Algorithm """

    def __init__(self,
                 tokens: list,
                 gram_size: int):
        """
        Created:
            24-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        self._tokens = tokens
        self._gram_size = gram_size

    @staticmethod
    def _normalize(results: list) -> list:
        normalized = []
        for result in results:

            output = result
            if type(result) == list:
                output = ' '.join(result).strip()

            normalized.append(output.replace('  ', ' ').strip())

        return normalized

    def _process(self) -> list:
        results = []
        tokens = self._tokens

        if self._gram_size == len(tokens):
            return self._normalize(tokens)

        if self._gram_size == 1:
            return self._normalize(tokens)

        x = 0
        y = x + self._gram_size

        while y <= len(tokens):
            results.append(tokens[x: y])

            x += 1
            y = x + self._gram_size

        normalized = []
        for result in results:
            output = ' '.join(result).strip()
            output = output.replace('  ', ' ')
            normalized.append(output)

        return normalized

    def process(self) -> list:
        sw = Stopwatch()

        results = self._process()

        if self.isEnabledForDebug:

            self.logger.debug('\n'.join([
                "Sliding Window Extract Completed",
                f"\tGram Size: {self._gram_size}",
                f"\tTotal Tokens: {len(results)}",
                f"\tTotal Time: {str(sw)}"]))

            if self._tokens != results:
                self.logger.debug('\n'.join([
                    "Sliding Window Extract Results",
                    f"\tTokens: {pformat(results, indent=4)}"]))

        return results
