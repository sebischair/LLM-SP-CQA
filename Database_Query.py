from typing import Tuple
import requests
import xmltodict
import json
from Result_Type import *

def query_blazegraph(query: str) -> Tuple[bool, str]:
    try:
        url = 'http://localhost:9999/blazegraph/namespace/wd/sparql'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'query': query}
        timeout = 10
        was_successful = False

        response = requests.post(url, headers=headers, params=params, timeout=timeout)

        if response.status_code >= 200 & response.status_code < 300:
            was_successful = True
            response_dict = xmltodict.parse(response.text)
            json_result = json.dumps(response_dict)

            return (was_successful, json_result)
        else:
            response = f"Request was not successful: {response.status_code} - {response.text}"
            return (was_successful, response)
    except Exception as e:
        return (False, f"Error: {e}")


def extract_db_query_result(input: str) -> Tuple[Result_Type, str]:
    ''' Extracts the result from the given input string (dictionary) and returns it as a tuple of Result_Type and str '''
    input.replace("null", "None")
    result = json.loads(input)

    # Check if result contains boolean
    if 'boolean' in result['sparql']:
        result_bool = result['sparql']['boolean']
        return (Result_Type.BOOLEAN, result_bool)

    elif 'results' not in result['sparql'] or result['sparql']['results'] is None:
        return (Result_Type.NULL, "No results found")

    elif 'result' not in result['sparql']['results']:
        return (Result_Type.NULL, "No result found")

    # Check if result contains list of entities
    elif isinstance(result['sparql']['results']['result'], list) and ['uri' in x['binding'] for x in result['sparql']['results']['result']]:
        result_list = [x['binding']['uri'] for x in result['sparql']['results']['result']]
        result_entities = [x.split('/')[-1] for x in result_list]
        return (Result_Type.ENTITIES, result_entities)

    elif 'binding' not in result['sparql']['results']['result']:
        return (Result_Type.NULL, "No binding")

    # Check if result contains entity uri
    elif 'uri' in result['sparql']['results']['result']['binding']:
        result_cleaned = result['sparql']['results']['result']['binding']['uri']
        result_entity = result_cleaned.split('/')[-1]
        return (Result_Type.ENTITY, result_entity)

    # Check if result contains entity literal
    elif 'literal' in result['sparql']['results']['result']['binding'] and '#text' in result['sparql']['results']['result']['binding']['literal']:
        result_count = result['sparql']['results']['result']['binding']['literal']['#text']
        return (Result_Type.COUNT, result_count)
    
    return (Result_Type.NULL, "No result found")
