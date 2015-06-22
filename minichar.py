__author__ = 'YG'
# import sys
# from openpyxl import *
# minichardata = sys.argv[0]
import xlrd

workbook = xlrd.open_workbook('test.xls')
worksheet = workbook.sheet_by_name('Minichar')
# num_rows = worksheet.nrows - 1
# num_cells = worksheet.ncols - 1
# curr_row = -1
# while curr_row < num_rows:
#     curr_row += 1
#     row = worksheet.row(curr_row)
#     print('Row:', curr_row)
#     curr_cell = -1
#     while curr_cell < num_cells:
#         curr_cell += 1
#         # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
#         cell_type = worksheet.cell_type(curr_row, curr_cell)
#         cell_value = worksheet.cell_value(curr_row, curr_cell)
#         print('	', cell_type, ':', cell_value)
class SummaryType:
    def __init__(self, output_type, vdd):
        self.output_type = output_type
        self.vdd = vdd

    def risetime(self, column):
        minvals = worksheet.cell_values(20, column)
        return minvals

cell_value = worksheet.cell_value(15, 7)
print(cell_value)
