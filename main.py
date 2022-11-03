import json
import datetime
from datetime import timedelta
import locale
import calendar
from re import M
from month_creator import MesDeGuardia
from agent_creator import Agente
from day_creator import Day
#import pandas as pd
locale.setlocale(locale.LC_TIME, '')


def get_licenses(agentes,year, month):
    """
    Asks the user to select agents and assing them leave days

    Return : None 
    """
    while True:
        print("Selecciona al agente que dispone de licencias('q' para salir): ")
        for idx, agente in enumerate(agentes):
            print(f"Para seleccionas al agente {agente}, ingresar {idx}")

        seleccion = input("")
        if seleccion.lower() == "q":
            break
        while True:
            print(f"elegiste a {agentes[int(seleccion)]}")
            agente = agentes[int(seleccion)]
            dia_1 = input("para regresar pulsa 'q', ingreasar el primer dia de licencia: ")
            if dia_1.lower() == "q":
                break

            dia_2 = input("para regresar pulsa 'q', ingreasar el ultimo dia de licencia: ")
            if dia_2.lower() == "q":
                break
            for day in range(int(dia_1), int(dia_2) +1):
                agente.licencias.append(Day(year, month, int(day)))
            break
                    
def get_dias_pedidos(agentes, year, month):
    """
    Asks the user to select agents and assing them days in wich the agents
    has asked not to do a guard

    Return : None
    """
    while True:
        print("Selecciona al agente que ha solicitado no hacer guardia un dia('q' para salir): ")
        for idx, agente in enumerate(agentes):
            print(f"Para seleccionas al agente {agente}, ingresar {idx}")

        seleccion = input("")
        if seleccion.lower() == "q":
            break
        print(f"elegiste a {agentes[int(seleccion)]}")
        agente = agentes[int(seleccion)]

        while True:
            dia = input("para regresar pulsa 'q', ingreasar el dia solicitado: ")
            if dia.lower() == "q":
                break

            agente.dias_pedidos.append(Day(year, month, int(dia)))   

def prints(agentes,year, month, mes):
    """
    Prints out all the information relevant for the user
    """
    
    for dia in sorted(mes.guardias.keys()):
        print(dia, ":")
        for idx, agente in enumerate(mes.guardias[dia]):
            if idx != len(mes.guardias[dia])-1:
                print(str(agente), end=",")
            else:
                print(str(agente))

    for agente in sorted(agentes, key= lambda x : x.get_ratio_hours(mes)):            
        print(agente, "week", agente.get_week_hours(mes),
        "guardias", agente.get_guardia_hours(mes), 
        f"horas totales/horas del mes: {agente.get_total_hours(mes)}/{agente.corrected_horas_de_trabajo(mes)}",
        "ratio", agente.get_ratio_hours(mes))


    print("media = ", mes.get_median_ratio(agentes))
    

def main(agentes,year, month, mes):
    """
    Calls all the relevant functions to complete the work schedule

    Return : None
    """

    for dia in mes.dias_de_semana:
       
        dia.get_agentes_de_guarida_weekday(agentes, mes, lenth = 2) 
        print(dia)
        
    for dia in mes.fin_de_semana:
        
        current = dia.get_agentes_de_guarida_weekend(agentes, mes, lenth = 3)
        print(dia, current) 
        if current == False:
            print("recalculando")
            mes.guardias = {}
            main(agentes,year, month, mes)
    prints(agentes,year, month, mes)    

with open("agentes.json") as file:
    json_string = file.read()
    json_data = json.loads(json_string) # Loads the json file that contains the agents

agentes_dict = json_data["agentes"]
agentes = []

for agente in agentes_dict: #Creates the agents
    a = Agente(agente["nombre"], agente["apellido"], agente["rol"],
    agente["dias_de_trabajo"], agente["dias_de_guardia"], agente["hace_guardia"], 
    agente["licencias"], agente["reduccion_horaria"])
    agentes.append(a)


agentes = sorted(agentes, key = lambda x: x.apellido)
feriados= {}
month = int(input("mes: "))
year = int(input("año: "))

while True:
    feriado = input("feriado(q para salir): ")
    if feriado.lower() == "q":
        break
   
    print("Selecciona a los 3 agentes que hacen guardia este feriado")
    for idx, agente in enumerate(agentes):
        print(f"Para seleccionas al agente {agente}, ingresar {idx}") 
   
    agente_1=int(input("Agente 1: "))
    agente_2=int(input("Agente 2: "))
    agente_3=int(input("Agente 3: "))

    feriados[Day(year, month, int(feriado))] = [agentes[agente_1], agentes[agente_2], agentes[agente_3]]

mes = MesDeGuardia(year, month, feriados)
mes.get_month_days()
mes.add_feriados()

get_dias_pedidos(agentes,year,  month)
get_licenses(agentes, year, month)

main(agentes, year,  month, mes)

      