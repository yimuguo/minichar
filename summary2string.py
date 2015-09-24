__author__ = 'yguo'
import re
import glob
import os

# Read Summary File
# os.chdir("./")
# for file in glob.glob("*Summary*.txt"):
#     filename = file
# try:
#     SummaryFile = open(filename, 'r')
# except:
#     os.exit('no summary')
SummaryFile = open(".\\example\\Summary-046_updated_final.txt", 'r')

# Read Hex Strings from Summary File
conf_string = []
conf = []
output_freq = []
conf_enable = [1, 1, 1, 1]
search_for = ['CLK0', 'CLK1', 'CLK2', 'CLK3', 'CLK4']
output_num = 4
output_vdd = []
output_type = []
for line in SummaryFile:
    if any(x in line for x in search_for):      # Read Frequency Across Configs
        line = re.split('\s+', line)
        output_type.append(line[2])
        output_vdd.append(line[3])
        output_freq.append(line[1])
    elif ("Configuration" in line) and (len(line) > 20):
        line = re.split('\s+', line)            # Read Config Hex Strings and Correct I2C Address for Timing Commander
        if line[2] == 'E0':
            line[2] = '60'
        elif line[2] == 'E1':
            line[2] = '61'
        line = line[2:]
        conf_string = ' '.join(line)
        conf.append(conf_string)

# Determine if Configs are active
for i in range(0, 4):
    conf_enable[i] = 0
    for x in range(int(len(output_freq) / 4)*i, 4*i + int(len(output_freq) / 4)):
        if output_freq[x] != '-----':
            conf_enable[i] = 1
            break

if conf[0][:2] == '61':
    i2c_add = 'D4'
elif conf[0][:2] == '60':
    i2c_add = 'D0'
else:
    os.exit('Configuration Strings Read Error of First Byte')

print(i2c_add)
print(output_freq)
print(output_type)
print(output_vdd)
print(conf_enable)