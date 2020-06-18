import pandas as pd


def myFunc(file_path, column_name):
    excel_data = pd.read_excel(file_path, 'Sheet1')
    excel_data.fillna(value="No Data Found", inplace=True)
    return excel_data[column_name].sum()

filename = input()
columnname = input()
print(myFunc(filename, columnname))

