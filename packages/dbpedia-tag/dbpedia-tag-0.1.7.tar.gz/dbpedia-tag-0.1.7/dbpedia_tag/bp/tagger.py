
#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from pprint import pprint

from baseblock import Enforcer
from baseblock import Stopwatch
from baseblock import BaseObject
from baseblock import ServiceEventGenerator

from fast_sentence_tokenize import Tokenizer

from dbpedia_ent.bp import Finder
from dbpedia_tag.svc import ExactMatchFinder
from dbpedia_tag.svc import FuzzyMatchFinder


class Tagger(BaseObject):
    """ Orchestrate Taxonomy Generation """

    def __init__(self):
        """ Change Log:

        Created:
            24-Aug-2022
            craigtrim@gmail.com
        """
        BaseObject.__init__(self, __name__)
        finder = Finder()
        self._entity_exists = finder.exists
        self._tokenize = Tokenizer().input_text

        self._generate_event = ServiceEventGenerator().process
        self._fuzzy_matcher = FuzzyMatchFinder(finder.find).process

    def _tag_exact(self,
                   d_coords: dict,
                   d_canons: dict,
                   input_text: str,
                   original_text: str):

        for i in reversed(range(1, 4)):

            tokens = [x.strip() for x in self._tokenize(input_text)]
            tokens = [x for x in tokens if not x.startswith('entity_')]

            svc = ExactMatchFinder(gram_size=i,
                                   entity_exists=self._entity_exists)

            d_finder = svc.process(tokens)
            if not d_finder:
                continue

            if d_finder['validated']:
                for item in d_finder['validated']:

                    key = f"entity_{item.replace(' ', '_').lower()}"

                    x = original_text.lower().index(item)
                    y = x + len(item)

                    d_coords[key] = [x, y]
                    d_canons[key] = item

                    input_text = input_text.replace(item, key)
                    print(input_text)
                    print('\n'*2)

                tokens = [x.strip() for x in self._tokenize(input_text)]
                tokens = [x for x in tokens if not x.startswith('entity_')]

            if d_finder['unmatched']:

                d_fuzzy = self._fuzzy_matcher(d_finder['unmatched'])
                d_fuzzy = {k: d_fuzzy[k] for k in d_fuzzy if d_fuzzy[k]}

                for k in d_fuzzy:
                    if not d_fuzzy[k]:
                        continue

                    key = f"Fuzzentity_{d_fuzzy[k].replace(' ', '_').lower()}"

                    x = original_text.lower().index(k)
                    y = x + len(k)

                    d_coords[key] = [x, y]
                    d_canons[key] = d_fuzzy[k]

                    input_text = input_text.replace(k, key)

        return input_text

    def process(self,
                input_text: str):

        sw = Stopwatch()
        output_events = []

        d_canons = {}
        d_coords = {}

        original_text = input_text
        input_text = input_text.lower().strip()

        input_text = self._tag_exact(
            d_coords=d_coords,
            d_canons=d_canons,
            input_text=input_text,
            original_text=original_text)

        # input_text = self._tag(d_coords=d_coords,
        #                        d_canons=d_canons,
        #                        input_text=input_text,
        #                        original_text=original_text,
        #                        tag_bucket='validated')

        output_events.append(self._generate_event(
            service_name=self.component_name(),
            event_name='tagger',
            stopwatch=sw,
            data={
                'input_text': original_text,
                'output_text': input_text,
                'canons': d_canons,
                'coords': d_coords,
            }))

        return {
            'text': input_text,
            'events': output_events
        }
