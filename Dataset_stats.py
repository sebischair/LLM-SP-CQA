import json
import pandas as pd
import pathlib
from typing import Dict, List, Callable
from Import import get_file_paths_pathlib, get_text_from_file, get_file_paths
from Models import *


def list_question_types_with_categories(input_path: str) -> Dict[str, List[str]]:
    ''' Returns a dictionary with all question types and their corresponding categories '''
    question_types = {}
    file_paths = get_file_paths(input_path)

    # Loop through all files in the given folders
    for file_path in file_paths:
        data_set = json.loads(get_text_from_file(file_path))
        # Loop through all questions in the file and add extract the question type id, question type and description
        for i in range(len(data_set)):
            question_type = data_set[i].get('question-type', '')
            question_description = data_set[i].get('description', '')

            if question_type == '':
                continue

            if question_type not in question_types:
                question_types[question_type] = []

            if question_description not in question_types[question_type]:
                question_types[question_type].append(question_description)

    # Return the dictionary sorted by question types
    return dict(sorted(question_types.items(), key=lambda item: item[0]))


def list_question_types(input_path: str) -> List[str]:
    ''' Returns a list of all question types '''
    question_types = []
    file_paths = get_file_paths(input_path)

    # Loop through all files in the given folders
    for file_path in file_paths:
        data_set = json.loads(get_text_from_file(file_path))
        # Loop through all questions in the file and add extract the question type
        for i in range(len(data_set)):
            question_type = data_set[i].get('question-type', '')

            if question_type != '' and question_type not in question_types:
                question_types.append(question_type)

    return question_types


def list_question_type_ids(input_path: str) -> List[str]:
    ''' Returns a list of all question types '''
    question_type_ids = []
    file_paths = get_file_paths(input_path)

    # Loop through all files in the given folders
    for file_path in file_paths:
        data_set = json.loads(get_text_from_file(file_path))
        # Loop through all questions in the file and add extract the question type
        for i in range(len(data_set)):
            question_type_id = data_set[i].get('ques_type_id', '')

            if question_type_id != '' and question_type_id not in question_type_ids:
                question_type_ids.append(question_type_id)

    return question_type_ids


def count_instances_of_each_question_type(input_path: str) -> Dict[str, int]:
    ''' Returns a dictionary with all question types and the number of instances of each question type '''
    question_type_instances = {}
    file_paths = get_file_paths(input_path)

    # Loop through all files in the given folders
    for file_path in file_paths:
        data_set = json.loads(get_text_from_file(file_path))
        # Loop through all questions in the file and add extract the question type id and question type
        for i in range(len(data_set)):
            question_type = f"{data_set[i].get('question-type', '')}"
            if question_type == '':
                continue
            if question_type not in question_type_instances:
                question_type_instances[question_type] = 0
            question_type_instances[question_type] += 1

    # Return the dictionary sorted by the question type id
    return dict(sorted(question_type_instances.items(), key=lambda item: item[0]))


def count_instances_of_question_subtypes_for_files(file_paths: List[pathlib.Path]) -> Dict[str, int]:
    ''' Returns a dictionary with all question subtypes and the number of instances of each question subtype '''
    question_subtype_instances = {}

    # Loop through all files in the given folders
    for file_path in file_paths:
        data_set = json.loads(get_text_from_file(str(file_path)))
        # Loop through all questions in the file and add extract the question type and description
        for i in range(len(data_set)):
            question_type = data_set[i].get('question-type', '')
            question_description = data_set[i].get('description', '')

            if question_type == '':
                continue

            if question_description != '':
                question_type += f" [{question_description}]"

            if question_type not in question_subtype_instances:
                question_subtype_instances[question_type] = 0

            question_subtype_instances[question_type] += 1

    # Return the dictionary sorted number of instances
    return dict(sorted(question_subtype_instances.items(), key=lambda item: item[1], reverse=True))


def count_instances_of_question_subtypes(input_path: pathlib.Path) -> Dict[str, int]:
    ''' Returns a dictionary with all question subtypes and the number of instances of each question subtype '''
    file_paths = get_file_paths_pathlib(input_path)

    return count_instances_of_question_subtypes_for_files(file_paths)


def calculate_percentage_for_each_question_type(question_type_instances: Dict[str, int], sort_key: Callable, sort_reverse: bool = False) -> Dict[str, float]:
    ''' Returns a dictionary with all question type ids and the percentage of instances of each question type id '''
    question_type_percentages = {}
    total_instances = sum(question_type_instances.values())

    # Loop through all question types
    for question_type in question_type_instances:
        question_type_percentages[question_type] = question_type_instances[question_type] / total_instances * 100
        # Round to 2 decimal places
        question_type_percentages[question_type] = round(question_type_percentages[question_type], 4)

    # Return the dictionary sorted by the question type id
    return dict(sorted(question_type_percentages.items(), key=sort_key, reverse=sort_reverse))


def get_required_samples_for_each_question_type(sample_size: int, question_type_percentages: Dict[str, float], sort_key: Callable, reverse: bool = False) -> Dict[str, int]:
    ''' Returns a dictionary with all question type ids and the required number of samples for each question type id '''
    required_samples_rounded = {}
    required_samples = {}

    # Loop through all question types
    for question_type in question_type_percentages:
        required_samples_rounded[question_type] = round(sample_size / 100 * question_type_percentages[question_type])
        required_samples[question_type] = sample_size / 100 * question_type_percentages[question_type]

    sum_rounded = sum(required_samples_rounded.values())
    missing_values = sample_size - sum_rounded

    # Correct rounding errors
    # Find all values that have been rounded down
    rounded_down = {key: value % 1 for key, value in required_samples.items() if value % 1 <= 0.5}
    
    # sort them by value and take the first missing_values number of values
    rounded_down = dict(sorted(rounded_down.items(), key=lambda item: item[1], reverse=True)[:missing_values])

    # Add 1 to each of these rounded down values
    for key, value in rounded_down.items():
        if key in required_samples_rounded:
            required_samples_rounded[key] += 1
        else:
            required_samples_rounded[key] = 1

    # Return the dictionary sorted dictionary
    return dict(sorted(required_samples_rounded.items(), key=sort_key, reverse=reverse))


def count_instances_of_question_subtypes_csv_files(file_paths: List[str], sort_key: Callable, reverse: bool = False) -> Dict[str, int]:
    ''' Returns a dictionary with all question subtypes and the number of instances of each question subtype '''
    question_subtype_instances = {}

    # Loop through all files in the given folders
    for file_path in file_paths:
        dataframe = pd.read_csv(file_path)
        # Loop through all questions in the dataframe and add extract the question type and description
        for index, row in dataframe.iterrows():
            question_type = row['question_type']
            question_description = row['description']

            # Check if question_type is not string or empty string
            if type(question_type) != str or question_type == '':
                if index % 2 == 0:
                    print(f"Question type is not string or empty string in file: {file_path}, at index: {index}")
                continue

            if type(question_description) == str and question_description != '':
                question_type += f" [{question_description}]"

            if question_type not in question_subtype_instances:
                question_subtype_instances[question_type] = 0

            question_subtype_instances[question_type] += 1

    # Return the dictionary sorted number of instances
    return dict(sorted(question_subtype_instances.items(), key=sort_key, reverse=reverse))


def count_instances_of_question_subtypes_csv(input_path: str, sort_key: Callable, reverse: bool = False) -> Dict[str, int]:
    ''' Returns a dictionary with all question subtypes and the number of instances of each question subtype '''
    file_paths = get_file_paths(input_path)

    return count_instances_of_question_subtypes_csv_files(file_paths, sort_key, reverse)


def count_difference_of_required_samples_and_available_samples(required_samples: Dict[str, int], available_samples: Dict[str, int], sort_key: Callable, reverse: bool = False, include_sufficient_samples: bool = True) -> Dict[str, int]:
    ''' Returns number of missing samples for each question (sub)type '''
    missing_samples = {}

    for question_type in required_samples:
        available_sample = available_samples[question_type] if question_type in available_samples else 0
        missing_samples[question_type] = required_samples[question_type] - available_sample
    
    if not include_sufficient_samples:
        missing_samples = {key: value for key, value in missing_samples.items() if value > 0}
    
    return dict(sorted(missing_samples.items(), key=sort_key, reverse=reverse))


def count_missing_predictions_per_subcategory(sample_size: int, distribution_path: str, output_path: str, model: ModelType, prompt_type: str):
    file_paths = get_file_paths(output_path)
    # Exclude all file paths that do not contain the model name and promtp type
    file_paths = [file_path for file_path in file_paths if model.value in file_path and f"{prompt_type}.csv" in file_path]
    existing_predictions = count_instances_of_question_subtypes_csv_files(file_paths, lambda item: item[1], False)

    # Get the required number of prediction for each question category
    question_type_instances = count_instances_of_question_subtypes(distribution_path)
    question_type_percentages = calculate_percentage_for_each_question_type(question_type_instances, sort_key= lambda item: item[1])
    required_samples = get_required_samples_for_each_question_type(sample_size, question_type_percentages, sort_key= lambda item: item[1], reverse = False)

    return count_difference_of_required_samples_and_available_samples(required_samples, existing_predictions, sort_key= lambda item: item[1], include_sufficient_samples= True)


def count_required_predictions_per_subcategory(sample_size: int, distribution_path: pathlib.Path):
    # Get the required number of prediction for each question category
    question_type_instances = count_instances_of_question_subtypes(distribution_path)
    question_type_percentages = calculate_percentage_for_each_question_type(question_type_instances, sort_key= lambda item: item[1])
    required_samples = get_required_samples_for_each_question_type(sample_size, question_type_percentages, sort_key= lambda item: item[1], reverse = False)

    return required_samples
