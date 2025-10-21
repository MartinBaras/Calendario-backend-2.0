import requests
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget, QLabel
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor
from PyQt5.QtCore import QDate

api_key = "Iwk14tHROHVo2ypCU1EsTfHfuWCAldET"
pais = "AR"
año = 2025

class Calendario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendario")
        self.resize(400, 300)

        layout = QVBoxLayout()
        self.calendario = QCalendarWidget()
        layout.addWidget(self.calendario)
        
        #INTERFAZ
        self.label = QLabel("Selecciona una fecha\n")
        layout.addWidget(self.label)

        self.setLayout(layout)
        
        #MAIN
        self.feriados = self.obtener_feriados()

        self.marcar_feriados()

        self.calendario.clicked.connect(self.mostrar_fecha)

    def obtener_feriados(self):
        url = 'https://calendarific.com/api/v2/holidays'
        parametros = {
            "api_key": api_key,
            "country": pais,
            "year": año
        }

        response = requests.get(url, params=parametros)
        data = response.json()

        feriados = []
        
        for feriado in data['response']['holidays']:
            fecha = feriado['date']['datetime']
            razon = feriado['description'] #obtener descripcion de los dias feriados
            feriados.append((fecha['year'], fecha['month'], fecha['day'], razon)) #agregar a la lista feriados cada feriado con; año,mes,dia,descripcion

        return feriados
    
    def marcar_feriados(self):
        formato = QTextCharFormat()
        formato.setBackground(QBrush(QColor("lightcoral"))) #Color de los dias marcados como feriado en el calendario

        for year, month, day, _ in self.feriados:
            fecha = QDate(year, month, day)
            self.calendario.setDateTextFormat(fecha, formato)

    def mostrar_fecha(self, date):
        festividad = ""

        for year, month, day, razon in self.feriados:
            if year == date.year() and month == date.month() and day == date.day():
                festividad = f"Festividad: {razon}"
                break

        self.label.setText(f"Fecha seleccionada: {date.toString()}\n{festividad}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ventana = Calendario()
    ventana.show()

    sys.exit(app.exec_())
