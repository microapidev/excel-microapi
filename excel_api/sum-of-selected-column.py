import pandas as pd


def myFunc(file_path, sheet, column_name):
    excel_data = pd.read_excel(file_path, sheet)
    excel_data.fillna(value="No Data Found", inplace=True)
    return excel_data[column_name].sum()

filename = input()
sheetname = input()
columnname = input()
print(myFunc(filename, sheetname, columnname))
