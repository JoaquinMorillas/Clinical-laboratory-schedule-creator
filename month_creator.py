 #crea el mes a partir de inputs (mes, año, feriados), colocar cada dia en su lista correspondiente

import calendar
import datetime
import locale
from re import M
from day_creator import Day

locale.setlocale(locale.LC_TIME, '')


class MesDeGuardia:
  """
  Creates the month object where the day_creator.Day objects will be stored
  """
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
    """
    Creates the day_creator.Day objects and instert them into two lists according
    if the Day is a weekday or not

    Return : None
    """
    for day in self.month_days:
      day = Day(day.year,day.month,day.day)

      if day.month == self.month and day.weekday() not in [5, 6] and day not in self.feriados:
        self.dias_de_semana.append(day)
      
      if day.month == self.month and day.weekday() in [5, 6] and day not in self.feriados:
        self.fin_de_semana.append(day)
  
  def add_feriados(self):
    """
    Instert the holidays in a list

    Return : None
    """
    if self.feriados:
      for day in self.feriados:
        self.guardias[day] = self.feriados[day]
        
  def __len__(self):
    """
    Returns the total number of days in the month
    """
    return len(self.dias_de_semana) + len(self.fin_de_semana) + len(self.feriados)

  def dias_habiles(self):
    """
    Returns the total number of workable days in the month
    """
    return len(self.dias_de_semana)

  def horas_de_trabajo(self,):
    """
    Returns the total number of workable hours in the month
    """
    return len(self.dias_de_semana) * 7

  def __str__(self):
    """
    Retruns the formated string representation of the month
    """
    return self.month.strftime("%m")

  def get_median_ratio(self, agentes):
    """
    Returns the median hours worked of the agents in the month
    """
    ratio_sum = 0
    for agente in agentes:
      ratio_sum += agente.get_ratio_hours(self)

    median = ratio_sum/len(agentes)

    return median
  
  def get_guardias_median_ratio(self, agentes):
    """
    Returns the median hours worked of the agents that are able to do guards
    """
    ratio_sum = 0
    agentes_guardia = 0
    for agente in agentes:
      if agente.hace_guardia == True:
        ratio_sum += agente.get_ratio_hours(self)
        agentes_guardia +=1

    median = ratio_sum/agentes_guardia

    return median
