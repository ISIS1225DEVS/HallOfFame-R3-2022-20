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
import time
...
csv.field_size_limit(2147483647)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer, pct):
    analyzer = loadDataGame(analyzer, pct)
    analyzer = loadDataCategory(analyzer, pct)
    return analyzer
    
def loadDataCategory(analyzer, pct):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    Categoryfile = cf.data_dir + 'category_data_utf-8-' + pct +".csv"
    input_file = csv.DictReader(open(Categoryfile, encoding="utf-8"),
                                delimiter=",")
    for category in input_file:
        model.addCategory(analyzer, category)
    return analyzer

def loadDataGame(analyzer, pct):
    Gamesfile = cf.data_dir + 'game_data_utf-8-' + pct +".csv"
    input_file = csv.DictReader(open(Gamesfile, encoding="utf-8"),
                                delimiter=",")
    for game in input_file:
        model.addGame(analyzer, game)
    return analyzer

# Funciones de ordenamiento
def sortByReleaseDate(title):
    return model.sortByReleaseDate(title)

def sortByTime(title):
    return model.sortByTime(title)

# Funciones de consulta sobre el catálogo4

def getSix(list):
    return model.getSix(list)

#=====================================
#Requerimiento 1
#=====================================

def gamesInRange(analyzer, platform, rangesup, rangeinf):
    total, lst, totalgames = model.gamesInRange(analyzer, platform, rangesup, rangeinf)
    return total, lst, totalgames


#=====================================
#Requerimiento 2
#=====================================

def registroJugador(analyzer, jugador):
    return model.registroJugador(analyzer, jugador)

#=====================================
#Requerimiento 3
#=====================================

def numInRangemap(analyzer, limiteinf, limitesup):
    starttime= getTime()
    limiteinf=int(limiteinf)
    limitesup=int(limitesup)
    lst= model.numInRangemap(analyzer, limiteinf, limitesup)
    stroptime= getTime()
    deltatime= deltaTime(stroptime, starttime)
    return lst, deltatime

#=====================================
#Requerimiento 4
#=====================================

def slowInRange(analyzer, rangesup, rangeinf):
    return model.slowInRange(analyzer, rangesup, rangeinf)

#=====================================
#Requerimiento 5
#=====================================

def rangeTime(analyzer, rangesup, rangeinf):
    return model.rangeTime(analyzer, rangesup, rangeinf)

#=====================================
#Requerimiento 6
#=====================================

def propertyHistogram(analyzer, rangeinf, rangesup, num_segmentos, num_niveles, propiedad):
    return model.propertyHistogram(analyzer, rangeinf, rangesup, num_segmentos, num_niveles, propiedad)
#=====================================
#Requerimiento 7
#=====================================

def topNmasrentables(analyzer, platform, top):
    return  model.topNmasrentables(analyzer, platform, top)


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
