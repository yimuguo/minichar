__author__ = 'YG'
import openpyxl
import re
import csv
import os
import glob

# LVCMOS33 = 0 LVCMOS25 = 1 LVCMOS18 = 2 HCSL = 3 LVDS33/25 = 4 LVDS18 = 5 LVPECL = 6

os.chdir('./')


class SummaryConfig(object):
    output_type = []
    output_vdd = []
    output_freq = []
    cfg_enable = [0]

    def __init__(self, cfgnum):
        self.cfgnum = cfgnum
        try:
            for file in glob.glob("*summary*.txt"):
                filename = file
        except RuntimeError:
            os.error('No Summary File Here!')
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
