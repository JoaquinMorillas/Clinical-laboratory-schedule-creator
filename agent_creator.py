import json
import datetime
from datetime import timedelta
import locale
locale.setlocale(locale.LC_TIME, '')



class Agente:
    cantidad_de_agentes = 0
    
    def __init__(self, nombre, apellido, 
    rol, dias_de_trabajo, dias_de_guardia, hace_guardia, licencias, reduccion_horaria):
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol
        self.dias_de_trabajo = dias_de_trabajo
        self.dias_de_guardia = dias_de_guardia
        self.hace_guardia = hace_guardia
        self.licencias = licencias
        self.dias_de_trabajo = self.convert_int()
        self.reduccion_horaria = reduccion_horaria
        self.dias_pedidos = []
        Agente.cantidad_de_agentes +=1

    def __str__(self):
        return f"{self.apellido.upper()} {self.nombre.upper()}"


    #convierte a int las llaves de dias de trabajo    
    def convert_int(self):
        output_dict = {}
        for key, value in self.dias_de_trabajo.items():
            output_dict[int(key)] = [int(item) for item in value]
        return output_dict

    #calcula las horas en días de semana sin contar las guardias
    def get_week_hours(self, month):
        week_hours = 0
        month.get_month_days()
        
        for day in month.dias_de_semana:
           
            if day.weekday() in self.dias_de_trabajo and day not in self.licencias:
                hours = self.dias_de_trabajo[day.weekday()][1] - self.dias_de_trabajo[day.weekday()][0]
                week_hours += hours

        return week_hours

    def trabaja_al_siguiente_dia(self, dia):
        delta = timedelta(days=1)
        mañana = dia + delta
        if mañana.weekday() in self.dias_de_trabajo and self.dias_de_trabajo[mañana.weekday()][0] < 14:
            return True
        return False
    
    def get_guardia_hours(self, month):
        guardia_hours = 0
        for day, agents in month.guardias.items():
            if self in agents:
                if len(agents) == 2:
                    if self.apellido == "lanza":
                        guardia_hours += 19
                    else:
                        guardia_hours += 12
                else:
                    if agents[-1] == self:
                        guardia_hours += 12
                    else:
                        guardia_hours += 24
        return guardia_hours

    def get_total_hours(self, month):

        return self.get_guardia_hours(month) + self.get_week_hours(month)

    def corrected_horas_de_trabajo(self, month):
        horas_de_trabajo = month.horas_de_trabajo()

        for day in month.dias_de_semana:
            horas_de_trabajo -= self.reduccion_horaria

        for day in self.licencias:
            if day.weekday() not in [5,6]:
                horas_de_trabajo -= 7

        return horas_de_trabajo

    def get_ratio_hours(self, month):

        if self.corrected_horas_de_trabajo(month) == 0:
            return 1.0
        return self.get_total_hours(month)/self.corrected_horas_de_trabajo(month)
