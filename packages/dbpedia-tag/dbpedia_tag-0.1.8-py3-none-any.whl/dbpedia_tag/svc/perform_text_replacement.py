#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Sliding Window Extraction for Candidate Synonym Swapping """


from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import TextMatcher

from fast_sentence_tokenize import Tokenizer


class PerformTextReplacement(BaseObject):
    """ Perform Sliding Window Extraction for Candidate Synonym Swapping """

    def __init__(self,
                 original_text: str):
        """ Change Log:

        Created:
            26-Aug-2022
            craigtrim@gmail.com
            *   refactor sliding window algorithm
                https://github.com/craigtrim/dbpedia-tag/issues/2
        """
        BaseObject.__init__(self, __name__)
        self._tokenize = Tokenizer().input_text
        self._original_text = original_text
        self._d_coords = {}
        self._d_canons = {}

    def coords(self) -> dict:
        return self._d_coords

    def canons(self) -> dict:
        return self._d_canons

    # TODO: baseblock.TextMatcher (0.1.14+)

    @staticmethod
    def replace(input_text: str,
                old_value: str,
                new_value: str,
                case_sensitive: bool = False,
                recursive: bool = False) -> bool:
        """ Check for the existence of a value in input text

        Args:
            input_text (str): any text string to search in
            old_value (str): the value that must exist in the input text
            new_value (str): the value that will replace 'old value' within the input text
            case_sensitive (bool): True if case sensitivity matters
            recursive (bool): if True, then apply method recursively until all changes are made

        Returns:
            bool: True if the value exists in the input text
        """

        if not case_sensitive:
            old_value = old_value.lower()
            input_text = input_text.lower()

        if old_value == input_text:
            return new_value

        original_text = input_text

        match_lr = f" {old_value} "
        if match_lr in input_text:
            input_text = input_text.replace(match_lr, f" {new_value} ")

        match_l = f" {old_value}"
        if input_text.endswith(match_l):
            input_text = input_text.replace(match_lr, f" {new_value}")

        match_r = f"{old_value} "
        if input_text.startswith(match_r):
            input_text = input_text.replace(match_lr, f"{new_value} ")

        if recursive and original_text != input_text:
            return TextMatcher.replace(
                input_text=input_text,
                old_value=old_value,
                new_value=new_value,
                case_sensitive=case_sensitive)

        return input_text

    @staticmethod
    def get_coords(value: str,
                   input_text: str,
                   case_sensitive: bool = False) -> bool:
        """ Find the X,Y coords (if any) for a given value in the supplied input text

        Args:
            input_text (str): any text string to search in
            value (str): the value to find coords for
            case_sensitive (bool): True if case sensitivity matters

        Returns:
            bool: True if the value exists in the input text
        """

        if not case_sensitive:
            value = value.lower()
            input_text = input_text.lower()

        if value == input_text:
            return 0, len(value)

        match_lr = f" {value} "
        if match_lr in input_text:
            x = input_text.index(match_lr)
            return x, x + len(value)

        match_l = f" {value}"
        if input_text.endswith(match_l):
            return len(input_text) - len(value), len(input_text)

        match_r = f"{value} "
        if input_text.startswith(match_r):
            return 0, len(value)

        # not found
        return None, None

    def _process(self,
                 entities: list,
                 input_text: str) -> dict:

        # tokens = [x.strip() for x in self._tokenize(input_text)]
        # tokens = [x for x in tokens if not x.startswith('entity_')]

        for entity in entities:

            key = f"entity_{entity.replace(' ', '_').lower()}"

            x, y = self.get_coords(value=entity,
                                   input_text=input_text,
                                   case_sensitive=False)

            self._d_coords[key] = [x, y]
            self._d_canons[key] = entity

            input_text = self.replace(input_text=input_text,
                                      old_value=entity,
                                      new_value=key,
                                      case_sensitive=False,
                                      recursive=False)

            input_text = input_text.replace(entity, key)

        return input_text

    def process(self,
                entities: list,
                input_text: str) -> list:

        sw = Stopwatch()

        output_text = self._process(entities=entities,
                                    input_text=input_text)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Text Replacement Completed",
                f"\tInput Text: {input_text}",
                f"\tOutput Text: {output_text}",
                f"\tTotal Time: {str(sw)}"]))

        return output_text
