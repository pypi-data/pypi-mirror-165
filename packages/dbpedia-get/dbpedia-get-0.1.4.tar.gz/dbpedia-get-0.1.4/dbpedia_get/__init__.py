from .recipes import *
from .transform import *
from .lookup import *
from .lookup.bp.lookup_orchestrator import LookupOrchestrator

import os


# this is where the dbpedia pages are downloaded into
if 'CACHE_NAME' not in os.environ:
    os.environ['CACHE_NAME'] = 'default'


lookup_orchestration = LookupOrchestrator().process


def find_article(entity_label: str,
                 entity_type: str = None,
                 entity_name: str = None) -> dict or None:
    """ Find a dbPedia Article

    Args:
        entity_label (str): the string label of the entity
            Sample: "Network Protocol"
        entity_type (str, optional): the type of the entity. Defaults to None.
            Sample: "Protocol"
            This is only required for disambiguation purposes.  
            if you are searching for (entity_label=pandas) dbPedia will return pandas/animal
            but if you want the python software, then you should supply an entity_type of either "python" or "software"
            and this will assist the lookup engine in returning the correct page
        entity_name (str, optional): the entity form. Defaults to None.
            Sample: "network_protocol"

    Returns:
        dict or None: the dbPedia page (if any)
    """

    if not entity_label or not len(entity_label):
        return None

    def get_entity_type() -> str:
        if entity_type:
            return entity_type
        return entity_label.lower().replace(' ', '_')

    def get_entity_name() -> str:
        if entity_name:
            return entity_name
        return entity_label.lower().replace(' ', '_')

    return lookup_orchestration(
        entity_type=get_entity_type(),
        entity_name=get_entity_name(),
        entity_label=entity_label)
