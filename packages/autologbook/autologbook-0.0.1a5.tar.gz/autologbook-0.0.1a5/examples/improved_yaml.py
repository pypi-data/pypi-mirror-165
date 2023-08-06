# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 20:34:44 2022

@author: Antonio
"""

import yaml
from PyQt5.QtWidgets import QApplication, QPlainTextEdit, QTextEdit
from yaml.representer import SafeRepresenter


class literal_str(str):
    pass


def change_style(style, representer):
    def new_representer(dumper, data):
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer


represent_literal_str = change_style('|', SafeRepresenter.represent_str)
yaml.add_representer(literal_str, represent_literal_str)


app = QApplication(['test'])
editor = QPlainTextEdit()
editor.setPlainText('#Header1')
editor.appendPlainText('##Header2')
editor.appendPlainText('Normal text')


print(editor.document().toPlainText())
print('-------------')


doc = editor.document()
block_list = []
for blockIndex in range(doc.blockCount()):
    block = doc.findBlockByNumber(blockIndex)
    if block.isValid():
        block_list.append(block.text())

block_list = list(filter(None, block_list))

j = '\n'.join(block_list)
print(j)

dic = {
    'html': literal_str(doc.toHtml()),
    'l': literal_str(j),
    'num': 5
}
dic['added'] = literal_str(doc.toPlainText())

print(yaml.dump(dic))
print(doc.toPlainText())
