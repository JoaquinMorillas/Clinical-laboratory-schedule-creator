import json
import datetime
from datetime import timedelta
import locale
locale.setlocale(locale.LC_TIME, '')



class Agente:
    """
    Custom object that defines the behaviour of the agents that work in the laboratory
    """
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
        """
        Return the formated string of the agent
        """
        return f"{self.apellido.upper()} {self.nombre.upper()}"


       
    def convert_int(self):
        """
        Convert the keys type from str to int

        Return : dict
        """
        output_dict = {}
        for key, value in self.dias_de_trabajo.items():
            output_dict[int(key)] = [int(item) for item in value]
        return output_dict

    #calcula las horas en días de semana sin contar las guardias
    def get_week_hours(self, month):
        """
        Calculates the worked hours without the guards

        Return : int
        """
        week_hours = 0
        month.get_month_days()
        
        for day in month.dias_de_semana:
           
            if day.weekday() in self.dias_de_trabajo and day not in self.licencias:
                hours = self.dias_de_trabajo[day.weekday()][1] - self.dias_de_trabajo[day.weekday()][0]
                week_hours += hours

        return week_hours

    def trabaja_al_siguiente_dia(self, dia):
        """
        Checks if the agent work the next day that is passed to the function

        Return : bool
        """
        delta = timedelta(days=1)
        mañana = dia + delta
        if mañana.weekday() in self.dias_de_trabajo and self.dias_de_trabajo[mañana.weekday()][0] < 14:
            return True
        return False
    
    def get_guardia_hours(self, month):
        """
        Calculates the total guard's hours worked

        Return : int
        """
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
        """
        Returns the total worked hours in the month passed to the function
        """
        return self.get_guardia_hours(month) + self.get_week_hours(month)

    def corrected_horas_de_trabajo(self, month):
        """
        Returns the hours that the agent has to work in the month passed to
        the function
        
        """
        horas_de_trabajo = month.horas_de_trabajo()

        for day in month.dias_de_semana:
            horas_de_trabajo -= self.reduccion_horaria

        for day in self.licencias:
            if day.weekday() not in [5,6]:
                horas_de_trabajo -= 7

        return horas_de_trabajo

    def get_ratio_hours(self, month):
        """
        Returns the the divition between the the hours worked and the 
        hours expected to work
        """
        if self.corrected_horas_de_trabajo(month) == 0:
            return 1.0
        return self.get_total_hours(month)/self.corrected_horas_de_trabajo(month)
