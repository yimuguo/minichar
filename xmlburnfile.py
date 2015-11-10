__author__ = 'yguo'

import re
import xml.etree.cElementTree as ET
import xml.dom.minidom
import glob
import os

# Read Summary File
os.chdir("./")
try:
    for file in glob.glob("*summary*.txt"):
        filename = file
        SummaryFile = open(filename, 'r')
        break
except (RuntimeError, TypeError, NameError):
    os.error('No Summary Txt File Present')
# filename = ".\\example\\Summary-046_updated_final.txt"

# Read Hex Strings from Summary File
conf_string = []
conf = []
output_freq = []
conf_enable = [0, 0, 0, 0]
search_for = ['CLK0', 'CLK1', 'CLK2', 'CLK3', 'CLK4']
output_num = 4
for line in SummaryFile:
    if any(x in line for x in search_for):      # Read Frequency Across Configs
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
for i in range(0, 4):
    for x in range(int(len(output_freq) / 4)*i, (1+i)*int(len(output_freq) / 4)):
        if output_freq[x] != '-----':
            conf_enable[i] = 1
            break

if conf[0][:2] == '61':
    i2c_add = '0x6a'
elif conf[0][:2] == '60':
    i2c_add = '0x68'
else:
    os.error('Configuration Strings Read Error of First Byte')

# Write Config Strings to Aardvark XML Batch File
root = ET.Element("aardvark")
ET.SubElement(root, "Configure", i2c="1", spi="0", gpio="0", tpower="0", pullups="1")
ET.SubElement(root, "i2c_bitrate", khz="100")
ET.SubElement(root, "sleep", ms="500")
OTPAddress = ['6F 30 00 60 F0 00 4E 34 E1 00 00', '6F 30 00 60 F0 35 4E 61 E1 10 10', '6F 30 00 60 F0 62 4E 8E E1 10 10', '6F 30 00 60 F0 8F 4E BB E1 10 10']
for x in range(0, 4):
    if conf_enable[x] == 1:
        if x == 0:
            ET.SubElement(root, "i2c_write", addr="0x6A", count="1", radix="16", nostop="0").text = '00 ' + conf[x]
        else:
            ET.SubElement(root, "i2c_write", addr="%s" % i2c_add, count="1", radix="16", nostop="0").text = '00 ' + conf[x]
        
        ET.SubElement(root, "i2c_write", addr="%s" % i2c_add, count="1", radix="16", nostop="0").text = "%s" % OTPAddress[x]
        ET.SubElement(root, "sleep", ms="100")
        ET.SubElement(root, "i2c_write", addr="%s" % i2c_add, count="1", radix="16", nostop="0").text = "72 F8"
        ET.SubElement(root, "sleep", ms="900")
        ET.SubElement(root, "i2c_write", addr="%s" % i2c_add, count="1", radix="16", nostop="0").text = "72 F0"
        ET.SubElement(root, "sleep", ms="5")

# ET.ElementTree(root).write("Aardvark Burn All Configs.xml")

XMLFile = open("Aardvark Burn All Configs.xml", 'w+')
PrintXML = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml()
XMLFile.write(PrintXML)
