"""
https://is20-2019.susu.ru/utkinaea/2021/03/15/obrabotka-baz-dannyh-sql-s-pomoshhyu-pyqt-osnovy/
"""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView


class Contacts(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("QTableView Example")
        self.resize(800, 600)
        # Set up the model
        self.model = QSqlTableModel(self)
        self.model.setTable("flower")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnFieldChange)
        self.model.setHeaderData(0, Qt.Orientation.Horizontal, "datanew")
        self.model.setHeaderData(1, Qt.Orientation.Horizontal, "dataedit")
        self.model.setHeaderData(2, Qt.Orientation.Horizontal, "idul")
        self.model.setHeaderData(3, Qt.Orientation.Horizontal, "idfl")
        self.model.setHeaderData(4, Qt.Orientation.Horizontal, "cnamefl")
        self.model.setHeaderData(5, Qt.Orientation.Horizontal, "width")
        self.model.setHeaderData(6, Qt.Orientation.Horizontal, "dlina")
        self.model.setHeaderData(7, Qt.Orientation.Horizontal, "radius")
        self.model.setHeaderData(8, Qt.Orientation.Horizontal, "height")
        self.model.setHeaderData(9, Qt.Orientation.Horizontal, "square")
        self.model.select()
        # Set up the view
        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.resizeColumnsToContents()
        self.setCentralWidget(self.view)


def createConnection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("street.sqlite")
    if not con.open():
        QMessageBox.critical(None, "QTableView Example - Error!", "Database Error: %s" % con.lastError().databaseText(), )
        return False
    return True


app = QApplication(sys.argv)
if not createConnection():
    sys.exit(1)
win = Contacts()
win.show()
sys.exit(app.exec())
