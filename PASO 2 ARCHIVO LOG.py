import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem

class LogViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Formulario.ui", self)
        self.setupDB()
        self.setupConnections()

    def setupDB(self):
        self.conexion = sqlite3.connect("logs.db")
        self.cursor = self.conexion.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Logs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                fecha TEXT,
                                nivel TEXT,
                                origen TEXT,
                                mensaje TEXT
                              )''')
        self.conexion.commit()

    def setupConnections(self):
        self.btnCargarLog.clicked.connect(self.cargarLog)
        self.btnFiltrar.clicked.connect(self.filtrarLogs)
        self.btnEstadisticas.clicked.connect(self.mostrarEstadisticas)

    def cargarLog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Cargar Archivo de Log", "", "Archivos de Texto (*.txt);;Todos los Archivos (*)", options=options)
        if filePath:
            with open(filePath, 'r') as file:
                for line in file:
                    parts = line.strip().split('|')
                    if len(parts) == 4:
                        fecha, nivel, origen, mensaje = parts
                        self.cursor.execute('INSERT INTO Logs (fecha, nivel, origen, mensaje) VALUES (?, ?, ?, ?)', (fecha, nivel, origen, mensaje))
                self.conexion.commit()
            self.cargarLogs()
#hola

    def cargarLogs(self, query='SELECT fecha, nivel, origen, mensaje FROM Logs', params=()):
        self.tableViewLogs.setModel(QStandardItemModel())
        model = self.tableViewLogs.model()
        model.setHorizontalHeaderLabels(['Fecha', 'Nivel', 'Origen', 'Mensaje'])
        self.cursor.execute(query, params)
        for row in self.cursor.fetchall():
            items = [QStandardItem(field) for field in row]
            model.appendRow(items)
        self.tableViewLogs.resizeColumnsToContents()

    def filtrarLogs(self):
        date_filter = self.dateEdit.text()
        severity_filter = self.comboBoxSeveridad.currentText()
        origin_filter = self.lineEditOrigen.text()
        query = 'SELECT fecha, nivel, origen, mensaje FROM Logs WHERE 1=1'
        params = []
        if date_filter:
            query += ' AND fecha=?'
            params.append(date_filter)
        if severity_filter and severity_filter != "Todos":
            query += ' AND nivel=?'
            params.append(severity_filter)
        if origin_filter:
            query += ' AND origen LIKE ?'
            params.append(f'%{origin_filter}%')
        self.cargarLogs(query, params)

    def mostrarEstadisticas(self):
        estadisticas = "Estadísticas:\n\n"
        self.cursor.execute('SELECT nivel, COUNT(*) FROM Logs GROUP BY nivel')
        niveles = self.cursor.fetchall()
        estadisticas += "Cantidad de logs por nivel de severidad:\n"
        for nivel, count in niveles:
            estadisticas += f"{nivel}: {count}\n"
        estadisticas += "\nCantidad de logs por origen:\n"
        self.cursor.execute('SELECT origen, COUNT(*) FROM Logs GROUP BY origen')
        origenes = self.cursor.fetchall()
        for origen, count in origenes:
            estadisticas += f"{origen}: {count}\n"
        self.textBrowserEstadisticas.setText(estadisticas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = LogViewer()
    viewer.show()
    sys.exit(app.exec_())
