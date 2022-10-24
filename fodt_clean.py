"""
USAGE: fodt_clean.py  path/to/file.fodt
"""

import sys
import lxml.etree as et
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit(__doc__)

filename = Path(sys.argv[1])
tree = et.fromstring(filename.read_bytes())

for binary_data in tree.xpath("//office:binary-data", namespaces=tree.nsmap):
    draw_image = binary_data.getparent()
    draw_image.getparent().remove(draw_image)  

xml_str = et.tostring(tree, pretty_print=True, encoding="unicode")
with filename.open("wt") as fp:
    fp.write('<?xml version="1.0" encoding="UTF-8"?>\n\n')
    fp.write(xml_str)
