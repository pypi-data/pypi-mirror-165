# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 16:38:48 2022

@author: elog-admin
"""

import sys
from pathlib import Path

from PyQt5 import Qt, QtCore, QtGui
from PyQt5.Qt import QItemSelection, QModelIndex, QStandardItem, QStandardItemModel
from PyQt5.QtGui import QPixmap
#from protocol_editor_ui import  Ui_tree_viewer_dialog
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot
#import watchdog.events
#import watchdog.observers


def check_child(item):
    print(item.text())
    if item.hasChildren():
        for row in range(item.rowCount()):
            child_item = item.child(row)
            check_child(child_item)


treeModel = QStandardItemModel()
rootNode = treeModel.invisibleRootItem()

for i in range(3):
    item = QStandardItem()
    item.setText(f'{i}')
    for k in range(3):
        subitem = QStandardItem()
        subitem.setText(f'{i}_{k}')
        # for j in range(5):
        #     ssubitem = QStandardItem()
        #     ssubitem.setText(f'{i}_{k}_{j}')
        #     subitem.appendRow(ssubitem)
        item.appendRow(subitem)
    rootNode.appendRow(item)

# for i in range(treeModel.rowCount()):
#     item = treeModel.item(i)
#     print(item.hasChildren())
print('---prima---')
for i in range(treeModel.rowCount()):
    item = treeModel.item(i)
    check_child(item)

text = '2_1'
items = treeModel.findItems(
    text, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)

new_text = f'{text} porca vaccaaaa**'
print('---------------')
print(f'aggiungo {new_text}')
if len(items) == 1:
    new_item = QStandardItem()
    new_item.setText(f'{new_text}')
    items[0].appendRow(new_item)
for i in range(treeModel.rowCount()):
    item = treeModel.item(i)
    check_child(item)

text = '1_2'
print('------------')
print(f'rimuovo {text}')
items = treeModel.findItems(
    text, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
if not len(items):
    print(f'non trovato {text}')
for item in items:
    print(f'trovato {item.text()}')
if len(items) == 1:
    item = items[0]
    if not isinstance(item.parent(), QStandardItem):
        parent_index = 0
        item.model().removeRow(item.row())
    else:
        parent_index = item.parent().index()
        item.model().removeRow(item.row(), parent_index)

else:
    print('ops trovati troppi items')


items = treeModel.findItems(
    text, QtCore.Qt.MatchExactly or QtCore.Qt.MatchRecursive, 0)
for i in range(treeModel.rowCount()):
    item = treeModel.item(i)
    check_child(item)
if not len(items):
    print(f'non trovato {text}')
for item in items:
    print(f'trovato {item.text()}')
