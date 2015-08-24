__author__ = 'YG'
import sys
import xlrd
import re
import csv
import os
import glob
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
# workbook = xlrd.open_workbook('.\data\\5P49V5901A689NLGI_AK652C-008_MiniChar.xls')
# worksheet = workbook.sheet_by_name('Mini char ')

# LVCMOS33 = 0 LVCMOS25 = 1 LVCMOS18 = 2 HCSL = 3 LVDS33/25 = 4 LVDS18 = 5 LVPECL = 6

os.chdir('./')


class SummaryConfig(object):
    output_type = []
    output_vdd = []
    output_freq = []
    cfg_enable = [0]

    def __init__(self, cfgnum):
        self.cfgnum = cfgnum
        for file in glob.glob("*summary*.txt"):
            filename = file
        search_for = ['CLK0', 'CLK1', 'CLK2', 'CLK3', 'CLK4']  # Search for it in summary txt file

        for line in open(filename):
            if any(x in line for x in search_for):
                line = re.split("\s+", line)
                self.output_type.append(line[2])
                self.output_vdd.append(line[3])
                self.output_freq.append(line[1])

    def config_enable(self):
        for x in range(4 * self.cfgnum + self.cfgnum, 4 * self.cfgnum + self.cfgnum + int(len(self.output_freq) / 4)):
            if self.output_freq[x] != '-----':
                self.cfg_enable = 1
                break


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


m1_data = '.\\newminichar\\newminichar.csv'

config1 = SummaryConfig(1)
config1.config_enable()
print(config1.cfg_enable)
print(config1.output_vdd)
print(config1.output_type)
# output_types_from_m1 = m1_output_type()
# cell_value = worksheet.cell_value(15, 7)
# print(cell_value)
