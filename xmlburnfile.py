__author__ = 'yguo'
import sys
#filename = sys.argv[0]
import xml

filename = ".\example\Summary-046_updated_final.txt"
SummaryFile = open(filename, 'r')
conf = []
LineNumberConf = []
for line in SummaryFile:
    if "CLK0" in SummaryFile:
        LineNumberConf.append = SummaryFile.index("CLK0")
    if ("Configuration" in line) and (len(line) > 20):
        line = line[17:]
        conf.append(line)
i = 0

for x in range(0,3):


aarvark = xml.etree.cElementTree.Element("aarvark")
configure = xml.etree.cElementTree.SubElement(aarvark, "configure")

xml.etree.cElementTree.SubElement(configure, "1", name="blah").text = "some value1"
xml.etree.cElementTree.SubElement(configure, "field2", name="asdfasd").text = "some vlaue2"

tree = xml.etree.cElementTree.ElementTree(root)
tree.write("Aardvark Burn All Configs.xml")

for line in conf:
    print (line)