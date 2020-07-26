from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget


class StatWidget(QWidget):

    def __init__(self, parent=None, result=None):
        super().__init__(parent)

        self._result = result

        self._ui = uic.loadUi('statwidget.ui', self)

        self._ui.texteditStat.setPlainText('')

    @pyqtSlot()
    def on_btnExportExcel_clicked(self):
        self._exportExcel()

    @property
    def stats(self):
        return self._ui.texteditStat.plainText()

    @stats.setter
    def stats(self, text):
        self._ui.texteditStat.setPlainText(text)


    def _exportExcel(self):
        print('exporting')
