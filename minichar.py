__author__ = 'YG'
import sys
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
def summary_output_type():
    with open()


def m1_output_type():
    type_list_char = []
    type_list = []
    i = 0
    while i < 21:
        i += 1
        type_list_char.append(worksheet.cell_value(16, i))
    for x in type_list_char:
        if 'LVCMOS3.3' in x:
            type_list.append(0)
        elif 'LVCMOS2.5' in x:
            type_list.append(1)
        elif 'LVCMOS1.8' in x:
            type_list.sppend(2)
        elif 'HCSL' in x:
            type_list.append(3)
        elif ('LVDS3.3' or 'LVDS2.5') in x:
            type_list.append(4)
        elif 'LVDS1.8' in x:
            type_list.append(5)
        elif 'LVPECL' in x:
            type_list.append(6)
        else:
            sys.exit('Did not Find Output Type, please check form')
    return type_list

class FindLimits:
    def __init__(self, output_type, spec, rownum):
        self.spec = spec
        self.rownum = rownum
        self.name = output_type

    def minima(self, colnum):
        minlist = worksheet.cell_value(self.spec, colnum)
        return minlist


cell_value = worksheet.cell_value(15, 7)
print(cell_value)
