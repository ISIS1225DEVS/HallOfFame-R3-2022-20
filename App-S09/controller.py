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
from datetime import datetime
import datetime as datetime
import time
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
# Inicialización del Catálogo de libros

def newController():
    analyzer={
        "model":None
    }
    analyzer["model"]=model.NewCatalog()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer,muestra): 
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    loadDatas(analyzer,muestra)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return analyzer,(delta_time,delta_memory)
    



def loadDatas(catalog,muestra):
    opcion=['5pct','10pct','20pct','30pct','50pct','80pct','large','small']
    gamesfile2= cf.data_dir + 'Speedruns/game_data_utf-8-'+ opcion[muestra-1] +'.csv'
    input_file2= csv.DictReader (open(gamesfile2, encoding='utf-8'))
    for game in input_file2:  
        game['Release_Date'] = str(datetime.datetime.strptime(game['Release_Date'],'%y-%m-%d'))[:10]
        model.AddGameData(catalog['model'], game)
    gamesfile1= cf.data_dir + 'Speedruns/category_data_urf-8-'+ opcion[muestra-1] +'.csv'
    input_file1= csv.DictReader (open(gamesfile1, encoding='utf-8'))
    for game in input_file1:  
        name = model.getId(catalog['model'],game['Game_Id'])
        game['Name']=name['Name']
        game['Lanzamiento'] = name['AnioLanzamiento']
        game['plataforma'] = name['plataforma']
        model.AddCategorys(catalog['model'], game)



# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def GetRangodeFechas(catalogo,plataforma,limite_inf,limite_max):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado = model.GetRangodeFechas(catalogo['model'],plataforma,limite_inf,limite_max)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return resultado,(delta_time,delta_memory)

def GetTiemposLentos(catalogo,limite_inf,limite_max):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado =  model.GetTiemposPequeños(catalogo['model'],limite_inf,limite_max)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return resultado,(delta_time,delta_memory)

def GetTiemposRecord(catalogo, limite_superior, limite_inferior): 
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado =  model.getRegistrosRecientes(catalogo['model'], limite_inferior, limite_superior)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)    
    return resultado,(delta_time,delta_memory)

def getRangodeIntentos(catalog,plataforma,intento1,intento2):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado = model.getRangodeIntentos(catalog["model"],plataforma,intento1,intento2)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return resultado,(delta_time,delta_memory)

def getTiemposVeloces(catalog,intento1,intento2):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado = model.getTiemposVeloces(catalog["model"],intento1,intento2)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return resultado,(delta_time,delta_memory)

def getPlayers(catalogo,nombre):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado = model.getPlayersTimes(catalogo['model'],nombre)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return resultado,(delta_time,delta_memory)

def getHistogram(catalog,inferior,mayor,opcion):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado =  model.getAverageYears(catalog['model'],inferior,mayor,opcion)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return resultado,(delta_time,delta_memory)

def getMapa(catalog,anio,lim_inf,lim_sup):
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado =  model.MapaInteractivoInformacion(catalog['model'],anio,lim_inf,lim_sup)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return resultado,(delta_time,delta_memory)

def getPlataforma(catalogo, plataforma): 
    start_time = getTime()
    tracemalloc.start()
    start_memory = getMemory()
    resultado = model.getPlataforma(catalogo['model'], plataforma)
    stop_time = getTime()
    delta_time = deltaTime(stop_time, start_time)
    stop_memory = getMemory()
    tracemalloc.stop()
    delta_memory = deltaMemory(stop_memory, start_memory)
    return resultado,(delta_time,delta_memory)

#Funciones de tiempo y memoria
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