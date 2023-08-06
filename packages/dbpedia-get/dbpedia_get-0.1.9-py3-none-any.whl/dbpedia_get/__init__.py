from .recipes import *
from .transform import *
from .transform.bp.transform_orchestrator import TransformOrchestrator
from .lookup import *
from .lookup.bp.lookup_orchestrator import LookupOrchestrator

import os


# this is where the dbpedia pages are downloaded into
if 'CACHE_NAME' not in os.environ:
    os.environ['CACHE_NAME'] = 'default'


lookup_orchestration = LookupOrchestrator().process
transform_orchestrator = TransformOrchestrator()


def extract_categories(entity_name: str) -> list:
    return transform_orchestrator.categories(entity_name)


def find_article(entity_name: str) -> dict or None:
    """ Find a dbPedia Article

    Args:
        entity_name (str): the string label of the entity
            Sample: "Network Protocol"

    Returns:
        dict or None: the dbPedia page (if any)
    """

    if not entity_name or not len(entity_name):
        return None

    def get_entity_type() -> str:
        return entity_name.lower().replace(' ', '_')

    def get_entity_name() -> str:
        return entity_name.lower().replace(' ', '_')

    return lookup_orchestration(
        entity_type=get_entity_type(),
        entity_name=get_entity_name(),
        entity_label=entity_name)
