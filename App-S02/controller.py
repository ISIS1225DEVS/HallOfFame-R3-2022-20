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

import config as cf
import model
import csv
import datetime
from datetime import datetime as dt
import time
import tracemalloc
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos
def loadData(catalog, id):
    start_time = getTime()

    

    registerfile = cf.data_dir + "Speedruns//category_data_urf-8-{}.csv".format(id)
    gamesfile = cf.data_dir + "Speedruns//game_data_utf-8-{}.csv".format(id)
    inputreg_file = csv.DictReader(open(registerfile, encoding="utf-8"),
                                    delimiter=",")
    inputgame_file = csv.DictReader(open(gamesfile, encoding="utf-8"),
                                    delimiter=",")
    for register in inputreg_file:
        model.addObservation(catalog,register, "register")
    
    for game in inputgame_file:
        model.addObservation(catalog, game, "games")
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)

    return catalog

def getRegName(catalog, reg):
    return model.getRegName(catalog, reg) 

def indexHeight(catalog):
    return model.indexHeight(catalog)


def indexSize(catalog):
    return model.indexSize(catalog)


def minKey(catalog):
    return model.minKey(catalog)


def maxKey(catalog):
    return model.maxKey(catalog)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def cons_catalog_findSize(catalog,identifier):
    return model.cons_catalog_findSize(catalog,identifier)

def getGamesByRange(catalog, idate, fdate, platform, memflag): 
    formato = "%{}/%m/%Y".format("d")
    start_time = getTime()
    #try: 
    if memflag is True:
        tracemalloc.start()
        start_memory = getMemory()
    idate = datetime.datetime.strptime(idate,formato)
    fdate = datetime.datetime.strptime(fdate,formato)
    titulos = model.getGamesByRange(catalog, idate,fdate, platform)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    if memflag is True:
        stop_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(stop_memory, start_memory)
        return titulos, delta_time, delta_memory
    else:
        return titulos, delta_time
    #except:
    #    print("Introduzca fechas válidas")

def req2(catalog,player):
    return model.req2(catalog,player)

def req5(catalog,l_inf,l_sup):
    return model.req5(catalog,l_inf,l_sup)

def req8(catalog,anio,l_inf,l_sup):
    return model.req8(catalog,anio,l_inf,l_sup)


def getRegisterByRange(catalog, iDate, fDate):
    return model.getRegisterByRange(catalog, iDate, fDate)

def ordenarReq4(catalog, iDate, fDate):
    formato = "%Y-%m-%dT%H:%M:%S%z"
    iDate = datetime.datetime.strptime(iDate, formato)
    fDate = datetime.datetime.strptime(fDate, formato)
    lst = getRegisterByRange(catalog, iDate, fDate)
    return model.ordenarReq4(lst)

def getIdByPlatform(catalog, platform):
    map = catalog['platforms']
    return model.getIdByPlatform(map, platform)

def getRegsByPlatform(catalog, lst): 
    map = catalog['GameReg']
    return model.getRegsByPlatform(map, lst)

def calculosreq7(lst, catalog, datos, platform):
    return model.calculosreq7(lst, catalog, datos, platform)

def ordenarReq7(lst):
    return model.ordenarReq7(lst)

def getRunsbyRange(catalog,iRuns,fRuns):
    return model.getRunsbyRange(catalog,iRuns,fRuns)
    
def ordernarReg3(catalog,iRuns,fRuns):
    lst = getRunsbyRange(catalog,iRuns,fRuns)
    return model.ordenarReg3(catalog,lst)

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


# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

def getReq6(catalog, iDate, fDate):
    return model.getRequerimiento6(catalog, iDate, fDate)

def ordenarReq6Time_0(lst):
    return model.ordenarReq6Time_0(lst)


def ordenarReq6Prom(lst):
    return model.ordenarReq6Prom(lst)

def ordenarReq6Num(lst):
    return model.ordenarReq6Num(lst)