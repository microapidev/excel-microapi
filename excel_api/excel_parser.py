import pandas as pd
import xlrd
from typing import List, Dict, Union
import time


def get_file_name(file_bytes_object: bytes) -> str:
    """
    Gets the filename of the Uploaded file
    Args:
        file_bytes_object (bytes): A bytes representation of the Excel File

    Returns:
        str: name of the uploaded file
    """
    excel_file_title = file_bytes_object.name
    return excel_file_title


def parse_excel_file(file_bytes_object: bytes, sheet_name=None) -> Dict[str, Union[str, float]]:
    """
    Parses and Excel Bytes Object

    Args:
        file_bytes_object (bytes): A bytes representation of the Excel File

    Returns:
        List: A list of the Excel File contents
    """
    process_time = None
    data = None
    try:
        start_time = start_timer()
        df = pd.read_excel(file_bytes_object, sheet_name=sheet_name)
        end_time = start_timer()
        process_time = round(end_time - start_time, 2)
        data = df.to_json(orient="records")
    except Exception as e:
        print("Error ->", e)

    return {"data": data, "process_time": process_time}


def start_timer() -> float:
    """
    Parses and Excel Bytes Object

    Args:
        file_bytes_object (bytes): A bytes representation of the Excel File

    Returns:
        float: A float object with the time started
    """
    start_time = time.time()
    return start_time
