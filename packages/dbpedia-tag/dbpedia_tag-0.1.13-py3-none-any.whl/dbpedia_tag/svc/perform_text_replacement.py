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
        self._d_map = {}

    def map(self) -> dict:
        return self._d_map

    def _process(self,
                 input_text: str,
                 d_entity_map: dict) -> dict:

        for original_entity in d_entity_map:

            canon = d_entity_map[original_entity]

            # ensure we are dealing with a true canonical form
            # and not the variant form ...
            canon = self._find_canon(canon)

            key = f"entity_{canon.replace(' ', '_').lower()}"

            x, y = TextMatcher.coords(value=original_entity,
                                      input_text=input_text,
                                      case_sensitive=False)

            if x is None or y is None:
                continue

            self._d_map[key] = {
                'canon': canon,
                'coords': [x, y],
                'original': original_entity
            }

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
