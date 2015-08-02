__author__ = 'YG'
import sys
import xlrd
import re
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
# minichardata = sys.argv[0]
workbook = xlrd.open_workbook('.\data\\5P49V5901A689NLGI_AK652C-008_MiniChar.xls')
worksheet = workbook.sheet_by_name('Mini char ')

# LVCMOS33 = 0 LVCMOS25 = 1 LVCMOS18 = 2 HCSL = 3 LVDS33/25 = 4 LVDS18 = 5 LVPECL = 6
def summary_output_type(summary_file):
    output_type = []
    search_for = ['CLK0', 'CLK1', 'CLK2', 'CLK3', 'CLK4']   # Search for it in summary txt file
    for line in open(summary_file):
        if any(x in line for x in search_for):
            line = re.split("\s+", line)
            if 'LVCMOS' in line[2]:
                if line[3] == '3.3':
                    output_type.append(0)
                elif line[3] == '2.5':
                    output_type.append(1)
                elif line[3] == '1.8':
                    output_type.append(2)
                else:
                    sys.exit('CMOS OUTPUTS HAS NO VDD')
            elif 'HCSL' in line[2]:
                output_type.append(3)
            elif 'LVDS' in line[2]:
                if line[3] == '3.3':
                    output_type.append(4)
                elif line[3] == '2.5':
                    output_type.append(4)
                elif line[3] == '1.8':
                    output_type.append(5)
                else:
                    sys.exit('LVDS OUTPUTS HAS NO VDD')
            elif 'LVPECL' in line[2]:
                output_type.append(6)
            else:
                output_type.append('N')
    return output_type

def m1_output_type():
    type_list_char = []
    type_list = []
    i = 5
    k = 0
    while k < 4:
        while i < 10:
            i += 1
            type_list_char.append(worksheet.cell_value(16, i))
        k += 43
    for x in type_list_char:
        if 'LVCMOS3.3' in x:
            type_list.append(0)
        elif 'LVCMOS2.5' in x:
            type_list.append(1)
        elif 'LVCMOS1.8' in x:
            type_list.append(2)
        elif 'HCSL' in x:
            type_list.append(3)
        elif ('LVDS3.3' or 'LVDS2.5') in x:
            type_list.append(4)
        elif 'LVDS1.8' in x:
            type_list.append(5)
        elif 'LVPECL' in x:
            type_list.append(6)
        else:
            type_list.append('N')
    return type_list

class FindLimits:
    def __init__(self, output_type, spec, rownum):
        self.spec = spec
        self.rownum = rownum
        self.name = output_type

    def values(self, colnum):

        value_list.append(worksheet.cell_value(self.spec, colnum))
        return value_list

filename = ".\data\\5P49V5901_20150401_045742_05212015_summary.txt"
output_types = summary_output_type(filename)
output_types_from_m1 = m1_output_type()
cell_value = worksheet.cell_value(15, 7)
print(cell_value)
