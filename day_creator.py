from datetime import datetime
from datetime import timedelta
import random
import locale

#from month_creator import MesDeGuardia
locale.setlocale(locale.LC_TIME, '')


class Day(datetime):
    """
    Custom day object that inherit from datetime
    """
    def __init__(self, *args, **kargs):
        super().__init__()
        # self.week_day = self.is_week_day()
        self.agentes_de_guardia = []

    def __str__(self):
        """
        Return the formated string of the Day object
        """
        return self.strftime("%A %d")

    # def is_week_day(self):

    #     if self.weekday() not in [5, 6]:
    #         return True
    #     return False

    def get_agents(self, agentes):
        """
        Returns the agents that work this day
        """
        agentes_del_dia = {}
        for agente in agentes:
            if self.weekday() in agente.dias_de_trabajo:
                agentes_del_dia[str(
                    agente)] = agente.dias_de_trabajo[self.weekday()]

        return agentes_del_dia

    def get_agentes_de_guarida_weekday(self, agentes, mes, lenth):
        """
        Picks the agents that will do the guards in this day
        this functions is used for weekdays

        Return : bool
        """
        delta = timedelta(days=1)
        
        previous_day = self - delta
        next_day = self + delta
        previous_week = self- (delta*7)
        roles = []
        random.shuffle(agentes)
        shuf = agentes[:]
        for agente in agentes:
            if str(self.weekday()) in agente.dias_de_guardia and self not in agente.licencias:
                self.agentes_de_guardia.append(agente)
                roles.append(agente.rol)

        if self.weekday() == 4:
            agente = self.guardia_viernes(agentes, mes)
            if agente in mes.guardias.get(previous_week, []):
                agente = self.guardia_viernes(agentes, mes)
            self.agentes_de_guardia.append(agente)
            roles.append(agente.rol)
            
        while len(self.agentes_de_guardia) < lenth:
            while len(shuf) > 0:
                agente = shuf.pop()

                if (agente.trabaja_al_siguiente_dia(self) or 
                agente in mes.guardias.get(previous_day, []) or 
                str(next_day.weekday()) in agente.dias_de_guardia or
                agente in self.agentes_de_guardia or
                agente.hace_guardia == False or
                agente.get_ratio_hours(mes) > mes.get_median_ratio(agentes) or
                self in agente.licencias or
                self in agente.dias_pedidos):

                    break

                else:
                    self.agentes_de_guardia.append(agente)
                    roles.append(agente.rol)

                if len(self.agentes_de_guardia) == lenth:
                    break
            if len(shuf) == 0:
                return False        
        if "bioquimico" not in roles:
            self.agentes_de_guardia = []
            roles = []
            self.get_agentes_de_guarida_weekday(agentes, mes, lenth)

        mes.guardias[self] = self.agentes_de_guardia
        return True
        

    # def get_agentes_de_guarida_weekend(self, agentes, mes, lenth, roles=None):
    #     delta = timedelta(days=1)
    #     previous_day = self - delta
    #     next_day = self + delta
        
    #     agents_ratios= []
    #     if roles == None:
    #         roles = []
        
    #     for agente in agentes:
    #         agents_ratios.append(tuple((agente, agente.get_ratio_hours(mes))))
        
    #     agentes_sort = sorted(agents_ratios, key = lambda x: x[1], reverse = True)
        
    #     while len(self.agentes_de_guardia) < lenth:
    #         while True:
    #             agente = agentes_sort.pop()[0]
    #             #print(str(agente))
    #             if (agente.trabaja_al_siguiente_dia(self) or 
    #             agente in mes.guardias.get(previous_day, []) or 
    #             str(next_day.weekday()) in agente.dias_de_guardia or
    #             agente in self.agentes_de_guardia or
    #             agente.hace_guardia == False or
    #             agente in mes.guardias.get(next_day, [])):

    #                 break

    #             else:
    #                 self.agentes_de_guardia.append(agente)
    #                 roles.append(agente.rol)

    #             if len(self.agentes_de_guardia) == lenth:
    #                 break

    #     if "bioquimico" not in roles[:-1]:

    #         self.agentes_de_guardia = [self.agentes_de_guardia[0]]
            
    #         self.get_agentes_de_guarida_weekend(agentes[:-1], mes, lenth, roles=[self.agentes_de_guardia[0].rol])
        
    #     print(self, roles)
    #     mes.guardias[self] = self.agentes_de_guardia


    def get_agentes_de_guarida_weekend(self, agentes, mes, lenth):
        """
        Picks the agents that will do the guards in this day
        this functions is used for weekends

        Return : bool
        """
        delta = timedelta(days=1)
        previous_day = self - delta
        next_day = self + delta
        roles = []
        random.shuffle(agentes)
        shuf = agentes[:]
        while len(self.agentes_de_guardia) < lenth:
            while len(shuf) > 0:
                agente = shuf.pop()
                

                if (agente.trabaja_al_siguiente_dia(self) or 
                agente in mes.guardias.get(previous_day, []) or 
                str(next_day.weekday()) in agente.dias_de_guardia or
                agente in self.agentes_de_guardia or
                agente.hace_guardia == False or
                agente in mes.guardias.get(next_day, []) or
                agente.get_ratio_hours(mes) > mes.get_median_ratio(agentes) or
                self in agente.licencias or
                self in agente.dias_pedidos):

                    break

                else:
                    self.agentes_de_guardia.append(agente)
                    roles.append(agente.rol)

                if len(self.agentes_de_guardia) == lenth:
                    break
            if len(shuf) == 0:
                return False   

        if "bioquimico" not in roles[:-1]:

            self.agentes_de_guardia = []
            roles = []
            self.get_agentes_de_guarida_weekend(agentes, mes, lenth)
        
       
        mes.guardias[self] = self.agentes_de_guardia
        return True
        
    def guardia_viernes(self, agentes, mes):
        """
        Picks the agents that will do the guards in this day
        this functions is used for fridays

        Return : bool
        """
        agents = []
        for agente in agentes:
            if agente.apellido in ["gauna", "lanza"]:
                agents.append(agente)
        
    
        agent = random.choice(agents)

        return agent
        
