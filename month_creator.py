 #crea el mes a partir de inputs (mes, año, feriados), colocar cada dia en su lista correspondiente

import calendar
import datetime
import locale
from re import M
from day_creator import Day

locale.setlocale(locale.LC_TIME, '')


class MesDeGuardia:
  guardias = dict()

  def __init__(self, year, month, feriados):
    self.year = year
    self.month = month
    self.feriados = feriados
    self.cal = calendar.Calendar()
    self.month_days = self.cal.itermonthdates(self.year, self.month)
    self.dias_de_semana = []
    self.fin_de_semana = []
    self.get_month_days()

  
  def get_month_days(self):
    for day in self.month_days:
      day = Day(day.year,day.month,day.day)

      if day.month == self.month and day.weekday() not in [5, 6] and day not in self.feriados:
        self.dias_de_semana.append(day)
      
      if day.month == self.month and day.weekday() in [5, 6] and day not in self.feriados:
        self.fin_de_semana.append(day)
  
  def add_feriados(self):
    if self.feriados:
      for day in self.feriados:
        self.guardias[day] = self.feriados[day]
        
  def __len__(self):
    return len(self.dias_de_semana) + len(self.fin_de_semana) + len(self.feriados)

  def dias_habiles(self):
    return len(self.dias_de_semana)

  def horas_de_trabajo(self,):
    return len(self.dias_de_semana) * 7

  def __str__(self):
    return self.month.strftime("%m")

  def get_median_ratio(self, agentes):
    ratio_sum = 0
    for agente in agentes:
      ratio_sum += agente.get_ratio_hours(self)

    median = ratio_sum/len(agentes)

    return median
  
  def get_guardias_median_ratio(self, agentes):
    ratio_sum = 0
    agentes_guardia = 0
    for agente in agentes:
      if agente.hace_guardia == True:
        ratio_sum += agente.get_ratio_hours(self)
        agentes_guardia +=1

    median = ratio_sum/agentes_guardia

    return median
