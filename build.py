import xml.etree.ElementTree as ET
from pathlib import Path
import re
from collections import defaultdict

ET.register_namespace('', 'http://www.w3.org/2000/svg')
sprite = ET.XML('<svg><defs/></svg>')
defs = sprite.find('defs')

ids = {}
for svg in Path('.').glob('photon-icons/icons/desktop/*.svg'):
    id = re.sub(r'-\d+', '', svg.stem)
    if id in ids:
        continue
    ids[id] = True
    
    symbol = ET.parse(svg).getroot()
    symbol.tag = 'symbol'
    symbol.set('id', id)
    del symbol.attrib['height']
    del symbol.attrib['width']
    
    has_context_fill = False
    for element in symbol.findall('*') + [symbol]:
        for attr in ['fill', 'stroke']:
            if element.get(attr) is not None:
                if 'context-fill' in element.get(attr):
                    has_context_fill = True
                element.set(attr, element.get(attr).replace('context-fill', 'currentColor'))
        if element.get('fill-opacity') is not None:
            element.set('fill-opacity', element.get('fill-opacity').replace('context-fill-opacity', ''))
    
    if not has_context_fill:
        for element in symbol.findall('*'):
            try:
                del element.attrib['fill']
            except KeyError:
                pass
        symbol.set('fill', 'currentColor')

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

