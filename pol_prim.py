import sqlite3 as mdb
import sys

from PyQt5 import QtSql, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout, QTableView, QAbstractItemView
from PyQt5.QtWidgets import QWidget


class sqlite_conect(object):
    def sqlite_conect(self, find_text, find_function):
        self.connection = mdb.connect('imenik.db')
        self.cursor = self.connection.cursor()
        self.find_text1 = "%" + find_text + "%"

        db = QtSql.QSqlDatabase.addDatabase("SQLITE3");

        ok = db.open()


def createConnection():
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("imenik.db")
    if not db.open():
        QtWidgets.QMessageBox.critical(None, "Cannot open database",
                                       "Unable to establish a database connection.\n"
                                       "This example needs SQLite support. Please read "
                                       "the Qt SQL driver documentation for information how "
                                       "to build it.\n\n"
                                       "Click Cancel to exit.", QtWidgets.QMessageBox.Cancel)
        return False
    return True


class Glavni_prozor(QWidget):
    def __init__(self):
        super(Glavni_prozor, self).__init__()
        self.setFixedSize(1024, 768)

        self.edit_window = edit_window(self)

        layout = QVBoxLayout(self)

        self.tabelaEditovanje = QTableView()
        self.tabelaEditovanje.setGeometry(50, 50, 300, 200)
        self.tabelaEditovanje.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabelaEditovanje.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabelaEditovanje.doubleClicked.connect(self.select_id)
        self.tabelaEditovanje.doubleClicked.connect(self.prikazi_drugi)

        layout.addWidget(self.tabelaEditovanje)

        # pravi promjenjivu za pretragu baze podataka
        self.model = QtSql.QSqlQueryModel()

        ## ---
        ##self.model.setQuery("SELECT Lokacija,Kancelarija,Prezime,Ime,Telefon,Lokal,Fax,Oblast FROM telImenik")
        # +++ id, !!!
        self.model.setQuery("""SELECT 
                                   id,                
                                   Lokacija,
                                   Kancelarija,
                                   Prezime,
                                   Ime,
                                   Telefon,
                                   Lokal,
                                   Fax,
                                   Oblast 
                               FROM telImenik""")

        # upisuje rezultate pretrage baze u self.tableView
        self.tabelaEditovanje.setModel(self.model)

        # ---
        ## odredjuje sirinu kolona u self.tableView-u prva kolona je 0-nulta,id nema potrebe dodavati jer ga sam odredjuje
        ##for i, width in enumerate([150, 65, 100, 80, 90, 40, 80, 340]):
        ##    self.tabelaEditovanje.setColumnWidth(i, width)

        # +++
        for i, width in enumerate([10, 150, 65, 100, 80, 90, 40, 80, 340]):
            self.tabelaEditovanje.setColumnWidth(i, width)
        # Если hide True/верно, данный столбец будет скрыт; в противном случае это будет показано.
        self.tabelaEditovanje.setColumnHidden(0, True)  # id не показываем!!!

    def prikazi_drugi(self):
        self.edit_window.show()

    def close(self):
        self.edit_window.close()
        super(Glavni_prozor, self).close()

    # --- +++
    def select_id(self, index):

        # ---        id_read=index.row()+1
        # ---        print(id_read)
        # ---        konekcija = sqlite_conect()
        # ---        konekcija.sqlite_conect("", "")
        # ---        konekcija.cursor.execute("SELECT * FROM telImenik WHERE id= '%s'" % (id_read))
        # ---        row = konekcija.cursor.fetchone()
        # ---        print(row)

        # +++
        row = index.row()
        self.id_db = self.model.record(row).value("id")
        print("row->`{}`, id_db->`{}`".format(row, self.id_db))

        self.edit_window.le_prezime.setText(self.model.record(row).value("Prezime"))
        self.edit_window.le_ime.setText(self.model.record(row).value("Ime"))
        self.edit_window.le_telefon.setText(self.model.record(row).value("Telefon"))
        self.edit_window.le_lokal.setText(self.model.record(row).value("Lokal"))
        self.edit_window.le_fax.setText(self.model.record(row).value("Fax"))
        self.edit_window.le_oblast.setText(self.model.record(row).value("Oblast"))

    # +++
    def clickedBtnSave(self):
        prezime = self.edit_window.le_prezime.text()
        ime = self.edit_window.le_ime.text()
        telefon = self.edit_window.le_telefon.text()
        lokal = self.edit_window.le_lokal.text()
        fax = self.edit_window.le_fax.text()
        oblast = self.edit_window.le_oblast.text()

        self.editDb(self.id_db, prezime, ime, telefon, lokal, fax, oblast)

    # +++
    def editDb(self, id_db, prezime, ime, telefon, lokal, fax, oblast):
        self.edit_window.hide()
        q = QtSql.QSqlQuery(""" UPDATE telImenik 
                                   SET Prezime = '{}',
                                       Ime     = '{}',
                                       Telefon = '{}',
                                       Lokal   = '{}',
                                       Fax     = '{}',
                                       Oblast  = '{}'
                                 WHERE id =  '{}'
                            """.format(prezime, ime, telefon, lokal, fax, oblast, id_db))

        result = q.exec_()
        if result:
            self.model.query().exec_()
            print("Ok!!!")
        else:
            print("Error ->", self.model.query().lastError().text())
        return result

    # +++
    def clickedBtnCancel(self):
        self.edit_window.hide()


class edit_window(QWidget):
    def __init__(self, parent):
        super(edit_window, self).__init__()

        edit_window.setWindowTitle(self, 'Izmjena podataka postojećeg korisnika')
        self.setFixedSize(500, 400)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.groupBox = QtWidgets.QGroupBox()
        self.groupBox.setGeometry(QtCore.QRect(190, 20, 421, 231))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle('Edit Contact')
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 391, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText('Izmjena postojećeg kontakta')

        self.le_prezime = QtWidgets.QLineEdit(self.groupBox)
        self.le_prezime.setGeometry(QtCore.QRect(160, 130, 150, 20))
        self.le_prezime.setObjectName("le_prezime")
        self.le_ime = QtWidgets.QLineEdit(self.groupBox)
        self.le_ime.setGeometry(QtCore.QRect(160, 160, 150, 20))
        self.le_ime.setObjectName("le_ime")
        self.le_telefon = QtWidgets.QLineEdit(self.groupBox)
        self.le_telefon.setGeometry(QtCore.QRect(160, 190, 150, 20))
        self.le_telefon.setObjectName("le_telefon")
        self.le_lokal = QtWidgets.QLineEdit(self.groupBox)
        self.le_lokal.setGeometry(QtCore.QRect(160, 220, 150, 20))
        self.le_lokal.setObjectName("le_lokal")
        self.le_fax = QtWidgets.QLineEdit(self.groupBox)
        self.le_fax.setGeometry(QtCore.QRect(160, 250, 150, 20))
        self.le_fax.setObjectName("le_fax")
        self.le_oblast = QtWidgets.QLineEdit(self.groupBox)
        self.le_oblast.setGeometry(QtCore.QRect(160, 280, 150, 20))
        self.le_oblast.setObjectName("le_oblast")
        self.lbl_prezime = QtWidgets.QLabel(self.groupBox)
        self.lbl_prezime.setGeometry(QtCore.QRect(0, 130, 150, 20))
        self.lbl_prezime.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_prezime.setObjectName("lbl_prezime")
        self.lbl_prezime.setText('Prezime')
        self.lbl_ime = QtWidgets.QLabel(self.groupBox)
        self.lbl_ime.setGeometry(QtCore.QRect(0, 160, 150, 20))
        self.lbl_ime.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_ime.setObjectName("lbl_ime")
        self.lbl_ime.setText('Ime')
        self.lbl_telefon = QtWidgets.QLabel(self.groupBox)
        self.lbl_telefon.setGeometry(QtCore.QRect(0, 190, 150, 20))
        self.lbl_telefon.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_telefon.setObjectName("lbl_telefon")
        self.lbl_telefon.setText('Telefon')
        self.lbl_lokal = QtWidgets.QLabel(self.groupBox)
        self.lbl_lokal.setGeometry(QtCore.QRect(0, 220, 150, 20))
        self.lbl_lokal.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_lokal.setObjectName("lbl_lokal")
        self.lbl_lokal.setText('Lokal')
        self.lbl_fax = QtWidgets.QLabel(self.groupBox)
        self.lbl_fax.setGeometry(QtCore.QRect(0, 250, 150, 20))
        self.lbl_fax.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_fax.setObjectName("lbl_fax")
        self.lbl_fax.setText('Fax')
        self.lbl_oblast = QtWidgets.QLabel(self.groupBox)
        self.lbl_oblast.setGeometry(QtCore.QRect(0, 280, 150, 20))
        self.lbl_oblast.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lbl_oblast.setObjectName("lbl_oblast")
        self.lbl_oblast.setText('Oblast')

        # ---    self.btn_save = QtWidgets.QPushButton(self.groupBox)
        # +++
        self.btn_save = QtWidgets.QPushButton(self.groupBox, clicked=parent.clickedBtnSave)

        self.btn_save.setGeometry(QtCore.QRect(140, 340, 80, 25))
        self.btn_save.setObjectName("btn_save")
        self.btn_save.setText('Snimi izmjene')

        # ---    self.btn_cancel = QtWidgets.QPushButton(self.groupBox)
        # +++
        self.btn_cancel = QtWidgets.QPushButton(self.groupBox, clicked=parent.clickedBtnCancel)

        self.btn_cancel.setGeometry(QtCore.QRect(230, 340, 80, 25))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.setText('Odustani')

        self.layout.addWidget(self.groupBox)

    def select_id(self, index):
        id_read = index() + 1
        print(id_read)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not createConnection():
        sys.exit(-1)
    mw = Glavni_prozor()
    mw.show()
    sys.exit(app.exec_())
