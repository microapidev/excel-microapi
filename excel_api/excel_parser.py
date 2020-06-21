import pandas as pd
import xlrd
from typing import List, Dict, Union
import time
import xlrd.biffh
#import xlsxwriter

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


def parse_excel_file(file_bytes_object: bytes, sheet_name=0) -> Dict[str, Union[str, float]]:
    """
    Parses and Excel Bytes Object

    Args:
        file_bytes_object (bytes): A bytes representation of the Excel File
        sheet_name Union[str, List]: A column name, or a list of the columns we are interested in

    Returns:
        List: A list of the Excel File contentsn
    """
    process_time = None
    data = None
    result = None
    try:
        start_time = start_timer()
        df = pd.read_excel(file_bytes_object, sheet_name=sheet_name, parse_dates=False)

        end_time = start_timer()
        process_time = round(end_time - start_time, 2)
        data = df.to_dict(orient="records")
        result = {"data": data, "process_time": process_time}


    except xlrd.biffh.XLRDError as e:
        print("Unable to parse, corrupt Excel file or unsupported type")
        result = {"responseMessage": "Unable to parse, corrupt Excel file or unsupported type"}
        print(e)

    except Exception as e:
        result = {"responseMessage": "Unable to parse, corrupt Excel file or unsupported type"}
        print(e)
    return result


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






def get_duplicates_excel(file_bytes_obj: bytes) -> Dict:
    results = {"columns": None}
    try:
       
        df = pd.read_excel(file_bytes_obj)
        results = {'columns': []}
        df_columns = df.columns
        for col in df_columns:
            results['columns'].append({str(col): dict(df[str(col)].value_counts())})     
    except Exception as e:
        print(e)
    return results

def save_duplicates_excel(file_bytes_obj: bytes):
    result = {}
    duplicates_dict = get_duplicates_excel(file_bytes_obj=file_bytes_obj)
    df = pd.read_excel(file_bytes_obj, sheet_name=0, parse_dates=False)
    df = df.drop_duplicates()

    data = str(df.to_dict(orient="records"))
    result = {"duplicates" : duplicates_dict, "data": data}
    return result



def print_duplicates(file_bytes_obj: bytes) -> Dict:
    results ={"columns": []}
    try:

        df = pd.read_excel(file_bytes_obj)
        results = {'columns': []}
        df_columns = df.columns
        for col in df_columns:
            results['columns'].append({str(col): dict(df[str(col)].value_counts())})     
    except Exception as e:
        print(e)
    return results

    wb = xlrd.open_workbook(file_bytes_obj)
    sheet = wb.sheet_by_index(0)
    numcols = sheet.ncols
    write_colummn = numcols + 1
    
    df = pd.DataFrame(results)

    writer = pd.ExcelWriter(file_bytes_obj, engine='xlsxwriter')


    df.to_excel(writer, sheet_name='Sheet1', startcol=write_colummn, index=False)

    writer.save()


    

#def create_new_file(file_bytes_obj: bytes):
 #   new = request.data.get('result')

  #  newWorkbook = pd.Workbook('new.xlsx')
   # outputSheet = newWorkbook.add_worksheet()

    #df = pd.DataFrame(new)

    #print(df[['Duplicates']])

    #outputSheet.write('A1', 'Duplicates')
    












