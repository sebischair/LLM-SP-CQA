import os
import pathlib
import pandas as pd
from Models import *

def export_dataframe_to_csv(dataframe: pd.DataFrame, path: str, file_name: str):
    ''' Exports the given dataframe to a csv file '''

    # Check if folder exists and create it if not
    if not os.path.exists(path):
        os.makedirs(path)

    # If path does not end with a slash, add one
    if not path.endswith("/"):
        path = f"{path}/"

    dataframe.to_csv(f"{path}{file_name}.csv", index=False)


def append_to_dataframe_and_export(dataframe: pd.DataFrame, index: int, prediction: str, execution_time: float, model: ModelType, prompt_type: str, output_path: str, file_name: str):
    header = False

    # check if ouput_path exists and create it if it doesn't
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # check if file exists
    if not os.path.isfile(f"{output_path}/{file_name}_{model.value}_{prompt_type}.csv"):
        header = True

    # add prediction and execution time to the dataframe columns at index
    dataframe.loc[index, f"prediction_{model.value}"] = prediction
    dataframe.loc[index, f"execution_time_{model.value}"] = execution_time    

    # append the dataframe row at index to the csv file
    dataframe.iloc[[index]].to_csv(f"{output_path}/{file_name}_{model.value}_{prompt_type}.csv", mode='a', header=header, index=False)


def append_to_dataframe_and_export_pathlib(dataframe: pd.DataFrame, index: int, prediction: str, execution_time: float, model: ModelType, prompt_type: str, output_path: pathlib.Path, file_name: str):
    header = False

    # check if ouput_path exists and create it if it doesn't
    output_path.mkdir(exist_ok=True, parents=True)

    # check if file exists
    file_path = output_path.joinpath(f"{file_name}_{model.value}_{prompt_type}.csv")
    if not file_path.exists():
        header = True

    # add prediction and execution time to the dataframe columns at index
    dataframe.loc[index, f"prediction_{model.value}"] = prediction
    dataframe.loc[index, f"execution_time_{model.value}"] = execution_time    

    # append the dataframe row at index to the csv file
    dataframe.iloc[[index]].to_csv(file_path, mode='a', header=header, index=False)
