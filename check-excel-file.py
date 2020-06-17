import xlrd
from xlrd import open_workbook, XLRDError


def test_file(excel_file):
    try:
        xlrd.open_workbook(excel_file)

    except XLRDError as e:
        return e
    else:
        return "File is clean"


path = input()  # input file path
message = test_file(path)
print(message)
