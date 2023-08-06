# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 09:53:56 2022

@author: elog-admin
"""
import sys
from pathlib import Path

import watchdog.events
import watchdog.observers
from protocol_editor_ui import Ui_tree_viewer_dialog
from PyQt5 import Qt, QtCore, QtGui
from PyQt5.Qt import QItemSelection, QModelIndex, QStandardItem, QStandardItemModel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMainWindow

import autologbook

Signal = QtCore.pyqtSignal
Slot = QtCore.pyqtSlot

# module variables.
# their value can be overwritten from the configuration file
#
elog_user = 'log-robot'
elog_password = 'IchBinRoboter'
elog_hostname = 'https://10.166.16.24'
elog_port = 8080
item_type = QtCore.Qt.UserRole + 1
description_role = QtCore.Qt.UserRole + 2
extra_role = QtCore.Qt.UserRole + 3
image_role = QtCore.Qt.UserRole + 4
pic_id_role = QtCore.Qt.UserRole + 10
caption_role = QtCore.Qt.UserRole + 11
description_role = QtCore.Qt.UserRole + 12
extra_role = QtCore.Qt.UserRole + 13


class TextItem(QStandardItem):

    def __init__(self, txt=''):
        super().__init__()
        self.setText(txt)
        self.setData('Text', item_type)


class SectionItem(TextItem):
    def __init__(self, txt=''):
        super().__init__(txt=txt)
        self.setData('Section', item_type)


class NavPicItem(TextItem):

    def __init__(self, txt='', img_link=''):
        super().__init__(txt=txt)
        self.setData('NavPic', item_type)
        self.setData(img_link, image_role)


class MicroPicItem(TextItem):

    def __init__(self, txt='', img_id=0, img_link=''):
        super().__init__(txt=txt)
        self.setData('MicroPic', item_type)
        self.setData(img_id, pic_id_role)
        self.setData(img_link, image_role)

    def getDataFromYAML(self, yamlDict):
        pic_id = int(self.data(pic_id_role))
        if pic_id in yamlDict.keys():
            pass
        elif int(pic_id) in yamlDict.keys():
            pic_id = int(pic_id)
        else:
            return
        self.setData(yamlDict[pic_id]['Caption'], caption_role)
        self.setData(yamlDict[pic_id]['Description'], description_role)
        self.setData(yamlDict[pic_id]['Extra'], extra_role)


class ProtocolEditor(QDialog, Ui_tree_viewer_dialog):
    def __init__(self, parent=None, autolog=None):
        super().__init__(parent)
        self.autolog = autolog
        self.setupUi(self)
        self.autolog_tree_viewer.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()

        rootNode.appendRow(SectionItem('Introduction'))
        navcam_section = SectionItem('Navigation images')
        for navpic in self.autolog.navcamimages:
            navpic_item = NavPicItem(Path(navpic).name, str(Path(navpic)))
            navcam_section.appendRow(navpic_item)
        rootNode.appendRow(navcam_section)

        sample_section = SectionItem('Samples')
        for name, sample in self.autolog.samples.items():
            entry = TextItem(txt=sample.name)
            for key, image in sample.images.items():
                pic = MicroPicItem(
                    Path(key).name, image.getID(), image.thumbfilename)
                pic.getDataFromYAML(autolog.yamlDict)
                entry.appendRow(pic)
            sample_section.appendRow(entry)
        rootNode.appendRow(sample_section)

        self.autolog_tree_viewer.setModel(treeModel)
        self.autolog_tree_viewer.selectionModel().currentRowChanged.connect(self.get_values)

    @Slot()
    def caption_updated(self):
        new_caption = self.caption_field.text()
        model = self.autolog_tree_viewer.currentIndex().model()
        index = self.autolog_tree_viewer.currentIndex()
        model.setData(index, new_caption, caption_role)

    @Slot()
    def description_updated(self):
        new_text = self.description_input.document().toPlainText()
        model = self.autolog_tree_viewer.currentIndex().model()
        index = self.autolog_tree_viewer.currentIndex()
        model.setData(index, new_text, description_role)

    @Slot()
    def extra_updated(self):
        new_text = self.extrainfo_input.document().toPlainText()
        model = self.autolog_tree_viewer.currentIndex().model()
        index = self.autolog_tree_viewer.currentIndex()
        model.setData(index, new_text, extra_role)

    @Slot(QModelIndex)
    def get_values(self, index):
        if index.data(item_type) == 'NavPic':
            self.image_preview.setPixmap(
                QPixmap(index.data(image_role)).scaledToWidth(390, 1))
            self.caption_field.setEnabled(True)
            self.caption_field.setText(index.data(caption_role))
            self.description_input.setPlainText(index.data(description_role))
            self.extrainfo_input.setPlainText(index.data(extra_role))
        elif index.data(item_type) == 'MicroPic':
            self.image_preview.setPixmap(
                QPixmap(index.data(image_role)).scaledToWidth(390, 1))
            self.caption_field.setEnabled(True)
            self.caption_field.setText(index.data(caption_role))
            self.description_input.setPlainText(index.data(description_role))
            self.extrainfo_input.setPlainText(index.data(extra_role))
        elif index.data(item_type) == 'Text':
            self.image_preview.setText(
                'Image preview not available for this element')
            self.caption_field.clear()
            self.caption_field.setEnabled(False)
            self.description_input.setPlainText(index.data(description_role))
            self.extrainfo_input.setPlainText(index.data(extra_role))
        elif index.data(item_type) == 'Section':
            self.image_preview.setText(
                'Image preview not available for this element')
            self.caption_field.clear()
            self.caption_field.setEnabled(False)
            self.description_input.setPlainText(index.data(description_role))
            self.extrainfo_input.setPlainText(index.data(extra_role))


def main():
    app = QApplication(sys.argv)
    path = Path('R:\\A226\\Results\\2022\\12456-RADCAS-Bulgheroni')
    autolog = autologbook.QuattroELOGProtocol(
        path, elog_hostname, elog_port, elog_user, elog_password)
    autologEventHandler = autologbook.QuattroELOGProtocolEventHandler(autolog)
    observer = watchdog.observers.Observer()
    observer.schedule(autologEventHandler, path, recursive=True)
    autologEventHandler.setQueueReference(observer.event_queue)
    autologEventHandler.processAlreadyExistingItems()

    win = ProtocolEditor(autolog=autolog)
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
