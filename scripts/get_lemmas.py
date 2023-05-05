# This script 

import xml.etree.ElementTree as ET
from pathlib import Path
import re
from greek_normalisation.normalise import Normaliser

PROPER_NOUNS = {
    "Σώκρατες": "Σώκρατες",
    "Μέλητον": "Μέλητον",
    "Ἡράκλεις": "Ἡράκλεις",
    "Εὐθύφρων": "Εὐθύφρων",
}
normalise = Normaliser(proper_nouns=PROPER_NOUNS).normalise

path = Path(__file__).parent.parent.resolve() # project directory
xml_file = path / "orig" / "diorisis" / "tlg001u.xml"

try:
    tree = ET.parse(xml_file)
except (FileNotFoundError, PermissionError, OSError):
    print(f"Error opening file {xml_file}")
    exit()

root = tree.getroot()

sentences = root.findall(".//sentence")

txt_lines = []
with open(path / "text" / "euthyphro.txt") as txt_file:
    for line in txt_file:
        if re.match(r"\d{3}.00", line[:6]):
            continue
        words = []
        words.clear()
        for word in line.split():
            if re.match(r"\d{3}.\d{2}", word):
                continue
            if re.match(r"\{.+\}", word):
                continue
            if re.match(r"—", word):
                continue
            words.append(word)
        txt_lines.append(words)

with open("euthyphro_lemmas.csv", "w") as csv_file:
    for sentence in sentences:
        words = sentence.findall(".//word")
        for word in words:
            id = f"{int(sentence.attrib['id']):03}.{int(word.attrib['id']):02}"
            txt_line = txt_lines[int(sentence.attrib["id"])-1]
            text = txt_line[int(word.attrib["id"])-1]
            token = word.attrib["form"]
            normal_form = normalise(token)[0]
            lemma = word.find("./lemma").attrib["entry"]
        csv_file.write(f"{id}\t {text}\t {token}\t {normal_form}\t {lemma}\n")