import json
import requests
from typing import Dict, List

entity_cache = {}

def retriev_wikidata_entity(entity: str) -> str:
    if entity in entity_cache:
        return entity_cache[entity]

    url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity}.json"
    response = requests.get(url)
    ## Get only "en" label of json
    json_data = json.loads(response.text)
    entities = json_data['entities']

    # In rare instances the entity number in the response differes from the requested entity
    for entry in entities:
        label = json_data['entities'][entry]['labels']['en']['value']
        break

    # Add to inmemory cache
    entity_cache[entity] = label
    return label

def resolve_entities(entities: List[str]) -> Dict[str, str]:
    resolved_entities = {}
    for entity in entities:
        entity_label = retriev_wikidata_entity(entity)
        resolved_entities[entity] = entity_label
    return resolved_entities

