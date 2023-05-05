# The Diorisis xml files in orig/ are in beta code, and must be converted to unicode.
# This is a command line script for the conversion.

# Run this script with "python3 diorisis_beta_to_unicode.py tlgxxx.xml" where 
# tlgxxx.xml is a file in plato-texts/orig/diorisis with a three digit code instead
# of the xxx, e.g. tlg001.xml

# imports

import xml.etree.ElementTree as ET
from pathlib import Path
import betacode.conv
import sys, re

# Check for a suitable file and get its XML tree

args = sys.argv[1:]
if not args:
    print("Error: provide a file to convert")
    exit()
file = args[0]

regex = r"tlg\d{3}.xml"
if not re.match(regex, file):
    print("Error: file name must be of the form 'tlgxxx.xml' where x is a digit")
    exit()

new_file = file[:6] + "u" + file[6:] # tlg001.xml -> tlg001u.xml

path = Path(__file__).parent.parent.resolve() # project directory
old_xml_path = path / "orig" / "diorisis" / file
new_xml_path = path / "orig" / "diorisis" / new_file

try:
    tree = ET.parse(old_xml_path)
except (FileNotFoundError, PermissionError, OSError):
    print(f"Error opening file {old_xml_path}")
    exit()
root = tree.getroot()

# Convert the words from beta code to unicode

words = root.findall(".//word")
for word in words:
    beta_form = word.attrib["form"]
    unicode_form = betacode.conv.beta_to_uni(beta_form)
    word.set("form", unicode_form)

# Save to a new file

try:
    with open(new_xml_path,"w") as xml_file:
        try:
            tree.write(xml_file,"unicode")
            print(f"New file: {new_file}")
        except (IOError, OSError):
            print("Error writing to file")
            exit()
except (FileNotFoundError, PermissionError, OSError):
    print("Error opening new file")
    exit()