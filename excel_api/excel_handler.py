import xlrd
from xlrd import open_workbook, XLRDError
import pandas as pd


def test_file(excel_file):
    try:
        pd.read_excel(excel_file, sheet_name='Sheet1', parse_dates=False)

    except XLRDError as e:
        return e
    else:
        return "File is clean"
    
    
def column_sum(file_path, sheet, column_name):
    excel_data = pd.read_excel(file_path, sheet)
    excel_data.fillna(value="No Data Found", inplace=True)
    return excel_data[column_name].sum()
