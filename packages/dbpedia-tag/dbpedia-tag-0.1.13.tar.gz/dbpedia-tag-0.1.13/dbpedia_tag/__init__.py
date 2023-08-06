from .bp.tagger import Tagger
from .bp import *
from .svc import *
from .dmo import *
from .dto import *

from .recipes import *
from .recipes.filter_entity_list import filter_entity_list

import logging


components = [
    'dbpedia_tag.dmo.candidate_fuzzy_match',
    # 'dbpedia_tag.dmo.sliding_window_blacklist',
    # 'dbpedia_tag.dmo.sliding_window_validate',
]

[logging.getLogger(x).setLevel(logging.INFO) for x in components]


tagapi = Tagger()


def dbpedia_tag(input_text) -> dict:
    return tagapi.process(input_text)
