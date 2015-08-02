__author__ = 'yguo'
import sys
import re
#filename = sys.argv[0]
import xml.etree.cElementTree as ET

# Read Summary File
filename = ".\\example\\Summary-046_updated_final.txt"
SummaryFile = open(filename, 'r')

conf_string = []
conf = []
output_freq = []
conf_enable = [1, 1, 1, 1]
search_for = ['CLK0', 'CLK1', 'CLK2', 'CLK3', 'CLK4']
for line in SummaryFile:
    if any(x in line for x in search_for):      # Read Frequency Across Configs
        enable_flag = 0
        line = re.split('\s+', line)
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
if output_freq[0] == '-----' == output_freq[1] == output_freq[2] == output_freq[3] == output_freq[4]:
    conf_enable[0] = 0
if output_freq[5] == '-----' == output_freq[6] == output_freq[7] == output_freq[8] == output_freq[9]:
    conf_enable[1] = 0
if output_freq[10] == '-----' == output_freq[11] == output_freq[12] == output_freq[13] == output_freq[14]:
    conf_enable[2] = 0
if output_freq[15] == '-----' == output_freq[16] == output_freq[17] == output_freq[18] == output_freq[19]:
    conf_enable[3] = 0

if conf[0][:2] == '61':
    i2c_add = '0x6a'
elif conf[0][:2] == '60':
    i2c_add = '0x68'
else:
    sys.exit('Configuration Strings Read Error of First Byte')

# Write Config Strings to Aardvark XML Batch File
root = ET.Element("aardvark")
ET.SubElement(root, "Configure", i2c="1", spi="0", gpio="0", tpower="0", pullups="1")
ET.SubElement(root, "i2c_bitrate", khz="100")
ET.SubElement(root, "sleep", ms="500")
for x in range(0, 4):
    if conf_enable[x] == 1:
        if x == 0:
            ET.SubElement(root, "i2c_write", addr="0x6A", count="1", radix="16", nostop="0").text = conf[x]
        else:
            ET.SubElement(root, "i2c_write", addr="%s" % i2c_add, count="1", radix="16", nostop="0").text = conf[x]
        ET.SubElement(root, "i2c_write", addr="%s" % i2c_add, count="1", radix="16", nostop="0").text = "6F 30 00 60 F0 00 4E 34 E1 00 00"
        ET.SubElement(root, "sleep", ms="100")
        ET.SubElement(root, "i2c_write", addr="%s" % i2c_add, count="1", radix="16", nostop="0").text = "72 F8"
        ET.SubElement(root, "sleep", ms="900")
        ET.SubElement(root, "i2c_write", addr="%s" % i2c_add, count="1", radix="16", nostop="0").text = "72 F0"
        ET.SubElement(root, "sleep", ms="5")

ET.ElementTree(root).write("Aardvark Burn All Configs.xml")
