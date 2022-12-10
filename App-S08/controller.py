"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from datetime import datetime
from DISClib.ADT import list as lt
import config as cf
import math
import model
import csv
import time

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
def init():
    analyzer = model.newAnalyzer()
    return analyzer


def loadData(analyzer, gamesfile, categoryfile):
    """
    Carga datos de archivos CSV
    """
    gamesfile = cf.data_dir + gamesfile
    categoryfile = cf.data_dir + categoryfile

    input_gamefile = csv.DictReader(open(gamesfile,encoding="utf-8"),delimiter=",")
    input_registerfile = csv.DictReader(open(categoryfile,encoding="utf-8"),delimiter=",")
    ids = lt.newList("ARRAY_LIST", cmpfunction=None)
    miscs = lt.newList("ARRAY_LIST", cmpfunction=None)


    for game in input_gamefile:
        for key,value in game.items():
            if value == "":
                game[key] = "Unknown"
        lt.addLast(ids, {"Game_Id":game["Game_Id"],"value":game})
        model.addGame(analyzer,game)


    for register in input_registerfile:
        for key,value in register.items():
            if value == "":
                register[key] = "Unknown"
        for dt in lt.iterator(ids):
            if register["Game_Id"] == dt["Game_Id"]:
                register["Name"] = dt["value"]["Name"]
                register["Platforms"] = dt["value"]["Platforms"]
                register["Genres"] = dt["value"]["Genres"]
                register["Release_Date"] = dt["value"]["Release_Date"]
                
                count = 0
                time_0 = register["Time_0"]
                if time_0 == "Unknown":
                    time_0 = 0
                else:
                    time_0 = float(register["Time_0"])
                    count+=1


                time_1 = register["Time_1"]
                if time_1 == "Unknown":
                    time_1 = 0
                else:
                    time_1 = float(register["Time_1"])
                    count+=1

                time_2 = register["Time_2"]
                
                if time_2 == "Unknown":
                    time_2 = 0
                else:
                    time_2 = float(register["Time_2"])
                    count+=1

                register["Time_average"] = ((time_0+time_1+time_2)/count)
                register["Time_average1"] = ((time_0+time_1+time_2)/3)



        if register["Num_Runs"] != 0:            
            model.addRegister(analyzer,register)
        
    
    
    
    return analyzer



#Requerimiento 1
def gamesinRange(cont,date_lo,date_hi,plataforma):
    start_time = getTime()
    totalgamesplatform,lstgames = model.gamesinRange(cont,date_lo,date_hi,plataforma)
    end_time = getTime()
    delta_time = deltaTime(end_time,start_time)

    return delta_time,totalgamesplatform,lstgames

#Requerimiento 2
def fastestRecordsPlayer(cont,player):
    start_time = getTime()
    totalregistersplayer,lstregisters = model.fastestRecordsPlayer(cont,player)
    end_time = getTime()
    delta_time = deltaTime(end_time,start_time)
    return delta_time,totalregistersplayer,lstregisters

#Requerimiento 3
def registrosVeloces(cont,run_lo,run_hi):
    start_time = getTime()
    size,lstregisters = model.registrosVeloces(cont,run_lo,run_hi)
    end_time = getTime()
    delta_time = deltaTime(end_time,start_time)
    return delta_time,size,lstregisters
    
#Requerimiento 4
def registrosLentos(cont,date_lo,date_hi):
    start_time = getTime()
    size,lstregisters = model.registrosLentos(cont,date_lo,date_hi)
    end_time = getTime()
    delta_time = deltaTime(end_time,start_time)
    return delta_time,size,lstregisters

#Requerimiento 5
def registrosRecientes(cont,time_lo,time_hi):
    start_time = getTime()
    size,lstregisters = model.registrosRecientes(cont,time_lo,time_hi)
    end_time = getTime()
    delta_time = deltaTime(end_time,start_time)
    return delta_time,size,lstregisters

#Requerimiento 6
def diagramarHistograma(cont,anio_lo,anio_hi,segmentos,niveles,op):
    start_time = getTime()
    lowest_value, max_value, tamanio, dt_intervalos = model.diagramarHistograma(cont,anio_lo,anio_hi,segmentos,niveles,op)
    end_time = getTime()
    delta_time = deltaTime(end_time,start_time)
    return delta_time,lowest_value, max_value, tamanio, dt_intervalos

#Requerimiento 7
def calcularRentabilidad(analyzer,plataforma,top):
    start_time = getTime()
    tamanio,lista_rentabilidad = model.calcularRentabilidad(analyzer,plataforma,top)
    end_time = getTime()
    delta_time = deltaTime(end_time,start_time)
    return delta_time,tamanio,lista_rentabilidad

#Requerimiento 8
def graficar(cont,date,time_lo,time_hi):
    start_time = getTime()
    size,mapa = model.graficar(cont,date,time_lo,time_hi)
    end_time = getTime()
    delta_time = deltaTime(end_time,start_time)
    return delta_time,size,mapa


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)

def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo


