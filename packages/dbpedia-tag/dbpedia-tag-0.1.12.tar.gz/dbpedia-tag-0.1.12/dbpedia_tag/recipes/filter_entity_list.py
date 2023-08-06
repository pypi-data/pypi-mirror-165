
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Orchestrate dbPedia Filtering of Input Entities """


from dbpedia_tag.bp import Tagger
import logging

components = [
    'dbpedia_tag.dmo.candidate_fuzzy_match',
    'dbpedia_tag.dmo.sliding_window_blacklist',
    'dbpedia_tag.dmo.sliding_window_validate',
    'dbpedia_tag.dmo.sliding_window_match',
    'dbpedia_tag.svc.find_exact_matches',
    'dbpedia_tag.svc.perform_text_replacement',
]

[logging.getLogger(x).setLevel(logging.INFO) for x in components]


tagger = Tagger().process


def filter_entity_list(entities: list) -> dict:

    d_tags = {}
    for entity in entities:
        d_result = tagger(entity)
        d_canons = d_result['events'][0]['data']['canons']
        d_tags[entity] = list(d_canons.values())

    return d_tags
