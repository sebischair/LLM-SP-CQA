from typing import Dict, List
import pandas as pd
from Entity_Resolver import *

def _get_system_prompt() -> str:
    return "Generate a SPARQL query that answers the given 'Input question:'. Use 'Entities:', 'Relations:' and 'Types:' specified in the prompt to generate the query. The SPARQL query should be compatible with the Wikidata knowledge graph. Prefixes like 'wdt' and 'wd' have already been defined. No language tag is required. Use '?x' as variable name in the SPARQL query. Remember to provide only a SPARQL query in the response without any notes, comments, or explanations."

def get_zero_shot_chat_prompt(input_question: str, entities: Dict[str, str], relations: Dict[str, str], type_list: Dict[str, str], system_message: bool = False) -> List[dict]:
    ''' Returns the template for a prompt that converts a user question into a sparl query'''
    message = []

    if system_message:
        message.append({"role": "system", "content": f"{_get_system_prompt()}"})
    
    message.append({"role": "user", "content": f"""Input question: {input_question}
Entities: {entities}
Relations: {relations}
Types: {type_list}"""})
    return message


def get_zero_shot_chat_history_prompt(dataframe: pd.DataFrame, index: int, system_message: bool = False) -> List[dict]:
    ''' Returns the template for a prompt that converts a user question into a sparl query'''
    message = []
    current_row = dataframe.iloc[index]
    conversation_history = create_conversation_history(dataframe, index)

    if system_message:
        message.append({"role": "system", "content": f"{_get_system_prompt()}"})
    
    message.append({"role": "user", "content": f"""{conversation_history}Input question: {current_row['utterance']}
Entities: {current_row['entities_in_utterance']}
Relations: {current_row['relations']}
Types: {current_row['type_list']}"""})
    return message


def get_few_shot_chat_prompt(input_question: str, entities: Dict[str, str], relations: Dict[str, str], type_list: Dict[str, str], system_message: bool = False) -> List[dict]:
    ''' Returns the template for a prompt that converts a user question into a sparl query'''
    message = []

    if system_message:
        message.append({"role": "system", "content": f"{_get_system_prompt()}"})
    
    message.append({"role": "user", "content": f"""{_get_input_question_01()}
{_get_entities_01()}
{_get_relations_01()}
{_get_types_01()}"""})
    message.append({"role": "assistant", "content": f"{_get_sparql_01()}"})
    message.append({"role": "user", "content": f"""{_get_input_question_02()}
{_get_entities_02()}
{_get_relations_02()}
{_get_types_02()}"""})
    message.append({"role": "assistant", "content": f"{_get_sparql_02()}"})
    message.append({"role": "user", "content": f"""{_get_input_question_04()}
{_get_entities_04()}
{_get_relations_04()}
{_get_types_04()}"""})
    message.append({"role": "assistant", "content": f"{_get_sparql_04()}"})
    message.append({"role": "user", "content": f"""Input question: {input_question}
Entities: {entities}
Relations: {relations}
Types: {type_list}"""})
    return message


def get_few_shot_chat_history_prompt(dataframe: pd.DataFrame, index: int, system_message: bool = False) -> List[dict]:
    ''' Returns the template for a prompt that converts a user question into a sparl query'''
    message = []
    current_row = dataframe.iloc[index]
    conversation_history = create_conversation_history(dataframe, index)

    if system_message:
        message.append({"role": "system", "content": f"{_get_system_prompt()}"})
    
    message.append({"role": "user", "content": f"""{_get_input_question_01()}
{_get_entities_01()}
{_get_relations_01()}
{_get_types_01()}"""})
    message.append({"role": "assistant", "content": f"{_get_sparql_01()}"})
    message.append({"role": "user", "content": f"""{_get_input_question_02()}
{_get_entities_02()}
{_get_relations_02()}
{_get_types_02()}"""})
    message.append({"role": "assistant", "content": f"{_get_sparql_02()}"})
    message.append({"role": "user", "content": f"""{_get_conversation_history_03()}{_get_input_question_03()}
{_get_entities_03()}
{_get_relations_03()}
{_get_types_03()}"""})
    message.append({"role": "assistant", "content": f"{_get_sparql_03()}"})
    message.append({"role": "user", "content": f"""{conversation_history}Input question: {current_row['utterance']}
Entities: {current_row['entities_in_utterance']}
Relations: {current_row['relations']}
Types: {current_row['type_list']}"""})
    return message


def create_conversation_history(dataframe: pd.DataFrame, question_index: int) -> str:
    conversation_history = ""

    if question_index == 0:
        return conversation_history

    # Use at most the last three turns of the conversation history -> 6 rows
    conversation_turns = 6
    for i in range(question_index, 0, -1):
        conversation_turn = i - 1
        if conversation_turn < 0 or conversation_turn < question_index - conversation_turns:
            break

        current_turn = dataframe.iloc[conversation_turn]
        speaker = current_turn['speaker']
        
        if speaker == "USER":
            conversation_history = f"{speaker}: {current_turn['utterance']}\n" + conversation_history
        else:
            response_entities = _get_first_values_of_dict(current_turn['entities_in_utterance'])
            if len(response_entities) > 0:
                conversation_history = f"{speaker}: {response_entities}\n" + conversation_history
            else:
                conversation_history = f"{speaker}: {current_turn['utterance']}\n" + conversation_history

    return f"Conversation history:\n{conversation_history}\n"


def _get_first_values_of_dict(entities: str) -> Dict[str, str]:
    # Get the first 3 values of the dictionary
    result = {}
    dictionary = eval(entities)

    for i, (key, value) in enumerate(dictionary.items()):
        if i == 3:
            break
        result[key] = value
    return result


def _get_input_question_01() -> str:
    return "Input question: Is New York City the place of death of Cirilo Villaverde ?"

def _get_entities_01() -> str:
    return "Entities: {'Q727043': 'Cirilo Villaverde', 'Q60': 'New York City'}"

def _get_relations_01() -> str:
    return "Relations: {'P20': 'place of death'}"

def _get_types_01() -> str:
    return "Types: {'Q56061': 'administrative territorial entity'}"

def _get_sparql_01() -> str:
    return "SPARQL query: ASK { wd:Q727043 wdt:P20 wd:Q60 .  }"

def _get_input_question_02() -> str:
    return "Input question: How many works of art express Michael Jordan or pain ?"

def _get_entities_02() -> str:
    return "Entities: {'Q41421': 'Michael Jordan', 'Q81938': 'pain'}"

def _get_relations_02() -> str:
    return "Relations: {'P180': 'depicts'}"

def _get_types_02() -> str:
    return "Types: {'Q838948': 'work of art'}"

def _get_sparql_02() -> str:
    return "SPARQL query: SELECT (COUNT(DISTINCT ?x) AS ?count) WHERE { { ?x wdt:P180 wd:Q41421 . ?x wdt:P31 wd:Q838948 .  } UNION { ?x wdt:P180 wd:Q81938 . ?x wdt:P31 wd:Q838948 .  } }"

def _get_conversation_history_03() -> str:
    return """Conversation history:
USER: Which administrative territory is the native country of Cirilo Villaverde ?
SYSTEM: {'Q241': 'Cuba'}

"""

def _get_input_question_03() -> str:
    return "Input question: Which is the national anthem of that administrative territory ?"

def _get_entities_03() -> str:
    return "Entities: {'Q241': 'Cuba'}"

def _get_relations_03() -> str:
    return "Relations: {'P85': 'anthem'}"

def _get_types_03() -> str:
    return "Types: {'Q484692': 'hymn'}"

def _get_sparql_03() -> str:
    return "SPARQL query: SELECT ?x WHERE { wd:Q241 wdt:P85 ?x . ?x wdt:P31 wd:Q484692 .  }"

def _get_input_question_04() -> str:
    return "Input question: Which administrative territory was Pavel Astakhov born in ?"

def _get_entities_04() -> str:
    return "Entities: {'Q4071605': 'Pavel Astakhov'}"

def _get_relations_04() -> str:
    return "Relations: {'P19': 'place of birth'}"

def _get_types_04() -> str:
    return "Types: {'Q56061': 'administrative territorial entity'}"

def _get_sparql_04() -> str:
    return "SPARQL query: SELECT ?x WHERE { wd:Q4071605 wdt:P19 ?x . ?x wdt:P31 wd:Q56061 .  }"
