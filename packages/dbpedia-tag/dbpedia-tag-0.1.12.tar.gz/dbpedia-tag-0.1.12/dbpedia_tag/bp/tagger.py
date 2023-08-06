
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate dbPedia Tagging on Input Text """


from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import ServiceEventGenerator

from fast_sentence_tokenize import Tokenizer

from dbpedia_ent.bp import Finder
from dbpedia_tag.svc import FindExactMatches
from dbpedia_tag.svc import FindFuzzyMatches
from dbpedia_tag.svc import PerformTextReplacement


class Tagger(BaseObject):
    """ Orchestrate dbPedia Tagging on Input Text """

    def __init__(self):
        """ Change Log:

        Created:
            24-Aug-2022
            craigtrim@gmail.com
        Updated:
            30-Aug-2022
            craigtrim@gmail.com
            *   integrate find-canon
        """
        BaseObject.__init__(self, __name__)
        finder = Finder()
        self._entity_exists = finder.exists
        self._find_canon = finder.find_canon
        self._tokenize = Tokenizer().input_text

        self._generate_event = ServiceEventGenerator().process
        self._fuzzy_matcher = FindFuzzyMatches(finder.find).process
        self._exact_matcher = FindExactMatches(self._entity_exists).process

    def _process(self,
                 input_text: str,
                 original_text: str):

        replace_text = PerformTextReplacement(original_text=original_text,
                                              find_canon=self._find_canon)

        tokens = [x.strip() for x in self._tokenize(input_text)]
        tokens = [x for x in tokens if not x.startswith('entity_')]

        for i in reversed(range(1, 4)):

            d_match_results = self._exact_matcher(
                gram_size=i, tokens=tokens)
            if not d_match_results:
                continue

            if d_match_results['matched']:
                # need to induce a structure to fit the service
                d_exact = {k: k for k in d_match_results['matched']}
                input_text = replace_text.process(
                    d_entity_map=d_exact,
                    input_text=input_text)

            if d_match_results['unmatched']:
                d_fuzzy = self._fuzzy_matcher(
                    d_match_results['unmatched'])

                d_fuzzy = {k: d_fuzzy[k] for k in d_fuzzy if d_fuzzy[k]}

                input_text = replace_text.process(
                    d_entity_map=d_fuzzy,
                    input_text=input_text)

            tokens = [x.strip() for x in self._tokenize(input_text)]
            tokens = [x for x in tokens if not x.startswith('entity_')]

        return {
            'input_text': original_text,
            'output_text': input_text,
            'coords': replace_text.coords(),
            'canons': replace_text.canons()
        }

    def process(self,
                input_text: str):

        sw = Stopwatch()

        output_events = []
        d_result = self._process(
            input_text=input_text.lower().strip(),
            original_text=input_text)

        output_events.append(self._generate_event(
            service_name=self.component_name(),
            event_name='tagger',
            stopwatch=sw,
            data=d_result))

        return {
            'text': input_text,
            'events': output_events
        }
