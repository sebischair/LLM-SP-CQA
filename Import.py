import pandas as pd
import numpy as np
import random
import json
import os
import pathlib
from typing import List
from Entity_Resolver import resolve_entities
from Export import export_dataframe_to_csv


def _sort_paths(path):
    # Split the path into directory and filename
    directory, filename = os.path.split(path)
    # Extract the numeric part of the folder & file name (i.e. "QA_2" -> 2)
    folder_number = int(directory.split("/")[-1].split("_")[1])
    file_number = int(filename.split("_")[1].split(".")[0])
    return folder_number, file_number


def get_file_paths(input_path: str) -> List[str]:
    ''' Create flat list of all files contained in a folder and its subfolders (root is input_path) '''
    file_paths = [os.path.join(r,file) for r,d,f in os.walk(input_path) for file in f]
    return sorted(file_paths, key=_sort_paths)


def _sort_paths_pathlib(path: pathlib.Path):
    # Split the path into directory and filename
    directory = path.parent.name
    filename = path.stem
    # Extract the numeric part of the folder & file name (i.e. "QA_2" -> 2)
    folder_number = int(directory.split("_")[1])
    file_number = int(filename.split("_")[1])
    return folder_number, file_number


def get_file_paths_pathlib(input_path: pathlib.Path) -> List[pathlib.Path]:
    ''' Create flat list of all files contained in a folder and its subfolders (root is input_path) '''
    file_paths = [os.path.join(r,file) for r,d,f in os.walk(input_path) for file in f]

    paths = [pathlib.Path(path) for path in file_paths]

    return sorted(paths, key=_sort_paths_pathlib)


def get_text_from_file(file_path: str) -> str:
  ''' Returns the content of the given file '''
  with open(file_path,encoding='utf-8') as f:
    text = f.read()
    return text


def get_turnID(input_folder_path: str, folder: str, file: str, turn: int) -> str:
    turnID = ""
    # input_folder_path contains train
    if input_folder_path.endswith('train'):
        turnID += 'train#'
    elif input_folder_path.endswith('valid'):
        turnID += 'valid#'
    elif input_folder_path.endswith('test'):
        turnID += 'test#'

    turnID += f"{folder}#"
    turnID += f"{file.split('.')[0]}#"
    turnID += f"{turn}"
    
    return turnID


def handle_file(input_folder_path: str, output_folder_path: str, folder: str, file: str):
    dataframe = pd.DataFrame(columns=['turnID', 'question_type_id', 'question_type', 'description', 'speaker', 'entities_in_utterance', 'relations', 'type_list', 'utterance', 'all_response_entities', 'sparql_query'])
    data_set = json.loads(get_text_from_file(f"{input_folder_path}/{folder}/{file}"))
    # Turn starts at 0 and is the same for question and answer
    turn = 0
    for i in range(len(data_set)):
        if i % 2 == 0 and i != 0:
            turn += 1

        new_row = pd.Series({
            'turnID': get_turnID(input_folder_path, folder, file, turn),
            'question_type_id': data_set[i].get('ques_type_id', np.nan),
            'question_type': data_set[i].get('question-type', ''),
            'description': data_set[i].get('description', ''),
            'speaker': data_set[i]['speaker'],
            'entities_in_utterance': resolve_entities(data_set[i]['entities_in_utterance']) if 'entities_in_utterance' in data_set[i] else {},
            'relations': resolve_entities(data_set[i]['relations']) if 'relations' in data_set[i] else {},
            'type_list': resolve_entities(data_set[i]['type_list']) if 'type_list' in data_set[i] else {},
            'utterance': data_set[i]["utterance"],
            'all_response_entities': resolve_entities(data_set[i]['all_entities']) if 'all_entities' in data_set[i] else {},
            'sparql_query': data_set[i].get('sparql', '')
            }
        , index=dataframe.columns)
        dataframe = pd.concat([dataframe, pd.DataFrame([new_row])], ignore_index=True)
    export_dataframe_to_csv(dataframe, f'{output_folder_path}/{folder}', file.split('.')[0])
    print(f"File {file} in folder {folder} done")


def handle_files(input_folder_path: str, output_folder_path: str, folder: str, start_file_id: int, stop_file_id: int):
    for i in range(start_file_id, stop_file_id + 1):
        try:
            file = f"QA_{i}.json"

            # check if file exists
            if os.path.isfile(f"{input_folder_path}/{folder}/{file}"):
                handle_file(input_folder_path, output_folder_path, folder, file)
        except Exception as e:
            print(f"Error importing file {file} in folder {folder}: {e}")


def create_spice_csv(input_folder_path: str, output_folder_path: str, start_folder_id: int, stop_folder_id: int, start_file_id: int, stop_file_id: int):
    for i in range(start_folder_id, stop_folder_id + 1):
            folder = f"QA_{i}"

            # check if folder exists
            if os.path.exists(f"{input_folder_path}/{folder}"):
                 handle_files(input_folder_path, output_folder_path, folder, start_file_id, stop_file_id)
                 print(f"Folder {folder} done")


def create_spice_csv_random(input_folder_path: str, output_folder_path:str, number_of_files: int):
    for i in range(number_of_files):
        # select a random folder in base_path
        folder = random.choice(os.listdir(input_folder_path))
        
        # select a random file in the folder
        file = random.choice(os.listdir(f"{input_folder_path}/{folder}"))

        try:
            # Check if this file is already processed
            if os.path.isfile(f"{output_folder_path}/{folder}/{file.split('.')[0]}.csv"):
                # If yes, choose another file
                i -= 1
                continue

            handle_file(input_folder_path, output_folder_path, folder, file)
        except Exception as e:
            i -= 1
            print(f"Error importing file {file} in folder {folder}: {e}")
