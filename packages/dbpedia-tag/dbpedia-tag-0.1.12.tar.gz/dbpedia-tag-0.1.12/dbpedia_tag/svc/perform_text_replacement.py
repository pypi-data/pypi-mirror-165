#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Perform Sliding Window Extraction for Candidate Synonym Swapping """


from typing import Callable

from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import TextMatcher
from baseblock import TextUtils

from fast_sentence_tokenize import Tokenizer


class PerformTextReplacement(BaseObject):
    """ Perform Sliding Window Extraction for Candidate Synonym Swapping """

    def __init__(self,
                 original_text: str,
                 find_canon: Callable):
        """ Change Log:

        Created:
            26-Aug-2022
            craigtrim@gmail.com
            *   refactor sliding window algorithm
                https://github.com/craigtrim/dbpedia-tag/issues/2
        """
        BaseObject.__init__(self, __name__)
        self._tokenize = Tokenizer().input_text
        self._find_canon = find_canon
        self._original_text = original_text
        self._d_coords = {}
        self._d_canons = {}

    def coords(self) -> dict:
        return self._d_coords

    def canons(self) -> dict:
        return self._d_canons

    # TODO: baseblock.TextMatcher (0.1.14+)

    # @staticmethod
    # def replace(input_text: str,
    #             old_value: str,
    #             new_value: str,
    #             case_sensitive: bool = False,
    #             recursive: bool = False) -> bool:
    #     """ Check for the existence of a value in input text

    #     Args:
    #         input_text (str): any text string to search in
    #         old_value (str): the value that must exist in the input text
    #         new_value (str): the value that will replace 'old value' within the input text
    #         case_sensitive (bool): True if case sensitivity matters
    #         recursive (bool): if True, then apply method recursively until all changes are made

    #     Returns:
    #         bool: True if the value exists in the input text
    #     """

    #     if not case_sensitive:
    #         old_value = old_value.lower()
    #         input_text = input_text.lower()

    #     if old_value == input_text:
    #         return new_value

    #     original_text = input_text

    #     match_lr = f" {old_value} "
    #     if match_lr in input_text:
    #         input_text = input_text.replace(match_lr, f" {new_value} ")

    #     match_l = f" {old_value}"
    #     if input_text.endswith(match_l):
    #         input_text = input_text.replace(match_l, f" {new_value}")

    #     match_r = f"{old_value} "
    #     if input_text.startswith(match_r):
    #         input_text = input_text.replace(match_r, f"{new_value} ")

    #     if recursive and original_text != input_text:
    #         return TextMatcher.replace(
    #             input_text=input_text,
    #             old_value=old_value,
    #             new_value=new_value,
    #             case_sensitive=case_sensitive)

    #     return input_text

    # @staticmethod
    # def get_coords(value: str,
    #                input_text: str,
    #                case_sensitive: bool = False) -> bool:
    #     """ Find the X,Y coords (if any) for a given value in the supplied input text

    #     Args:
    #         input_text (str): any text string to search in
    #         value (str): the value to find coords for
    #         case_sensitive (bool): True if case sensitivity matters

    #     Returns:
    #         bool: True if the value exists in the input text
    #     """

    #     if not case_sensitive:
    #         value = value.lower()
    #         input_text = input_text.lower()

    #     if value == input_text:
    #         return 0, len(value)

    #     match_lr = f" {value} "
    #     if match_lr in input_text:
    #         x = input_text.index(match_lr)
    #         return x, x + len(value)

    #     match_l = f" {value}"
    #     if input_text.endswith(match_l):
    #         return len(input_text) - len(value), len(input_text)

    #     match_r = f"{value} "
    #     if input_text.startswith(match_r):
    #         return 0, len(value)

    #     # not found
    #     return None, None

    def _process(self,
                 input_text: str,
                 d_entity_map: dict) -> dict:

        for original_entity in d_entity_map:

            canon = d_entity_map[original_entity]

            # ensure we are dealing with a true canonical form
            # and not the variant form ...
            canon = self._find_canon(canon)

            print(">>> canon: ", canon)
            print(">>> original entity: ", original_entity)

            key = f"entity_{canon.replace(' ', '_').lower()}"

            x, y = TextMatcher.coords(value=original_entity,
                                      input_text=input_text,
                                      case_sensitive=False)

            if x is None or y is None:
                continue

            self._d_coords[key] = [x, y]
            self._d_canons[key] = original_entity

            input_text = TextMatcher.replace(input_text=input_text,
                                             old_value=original_entity,
                                             new_value=key,
                                             case_sensitive=False,
                                             recursive=False)

        return input_text

    def process(self,
                d_entity_map: dict,
                input_text: str) -> str:
        """ Entry Point

        Args:
            d_entity_map (dict): maps original form to canonical form
                e.g., 
                {
                    'a&w restaurant': 'a&w_restaurants'
                }
            input_text (str): the input text in which original forms will be replaced with canonical forms
                e.g.,       "let's go to the a&w restaurant"
                becomes     "let's go to the entity_a&w_restaurants"          

        Returns:
            str: the modified text
        """

        sw = Stopwatch()

        output_text = self._process(input_text=input_text,
                                    d_entity_map=d_entity_map)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                "Text Replacement Completed",
                f"\tInput Text: {input_text}",
                f"\tOutput Text: {output_text}",
                f"\tTotal Time: {str(sw)}"]))

        return output_text
