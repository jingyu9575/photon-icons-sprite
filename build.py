import xml.etree.ElementTree as ET
from pathlib import Path
import re
from collections import defaultdict

ET.register_namespace('', 'http://www.w3.org/2000/svg')
sprite = ET.XML('<svg><defs/></svg>')
defs = sprite.find('defs')

sizes = defaultdict(int)
for svg in Path('.').glob('photon-icons/icons/desktop/*.svg'):
    id = re.sub(r'-\d+', '', svg.stem)
    size_match = re.search(r'-(\d+)', svg.stem)
    size = int(size_match[1]) if size_match else 0
    if sizes[id] > size:
        continue
    sizes[id] = size
    
    symbol = ET.parse(svg).getroot()
    symbol.tag = 'symbol'
    symbol.set('id', id)
    del symbol.attrib['height']
    del symbol.attrib['width']
    
    for element in symbol.findall('*') + [symbol]:
        if element.get('fill') is not None:
            element.set('fill', element.get('fill').replace('context-fill', 'currentColor'))
        if element.get('stroke') is not None:
            element.set('stroke', element.get('stroke').replace('context-fill', 'currentColor'))
        if element.get('fill-opacity') is not None:
            element.set('fill-opacity', element.get('fill-opacity').replace('context-fill-opacity', ''))
    defs.append(symbol)

comment = ET.Comment('''
    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.
''')
sprite.insert(0, comment) 

Path('dist').mkdir(exist_ok=True)
ET.ElementTree(element=sprite).write('dist/photon-icons.svg',
                                     encoding='utf-8', xml_declaration=True)

