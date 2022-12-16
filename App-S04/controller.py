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

from unicodedata import category
import config as cf
import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadGame(filename):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    analyzer = model.newAnalyzer()
    gamesfile = os.path.join(cf.data_dir, filename)
    catalog = model.addGame(analyzer, gamesfile)
    return catalog


def loadCategory(filename):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    analyzer = model.newAnalyzer()
    categoryfile = os.path.join(cf.data_dir, filename)
    catalog = model.addGame(analyzer, categoryfile)
    return catalog

def loadData(filename):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    
    analyzer = model.newAnalyzer()
    games = loadGame(analyzer, filename)
    category = loadCategory(analyzer, filename)


    return games, category

def addGamesTotal(catalog):
    return model.addGamestotal(catalog)

def addCatedoryTotal(catalog):
    return model.addCategorytotal(catalog)

def gamesByPlarformAndDate(catalog, platform, date1, date2):
    return model.gamesByPlarformAndDate(catalog, platform, date1, date2)

def gamesbyPlayer(catalog, player):
    return model.gamesbyPlayer(catalog, player)

def RegistersByTimeandDate(catalog, time1, time2):
    return model.RegistersByTimeandDate(catalog, time1, time2)

def rentability(catalog, platform, n):
    return model.rentability(catalog, platform, n)

def RegistersbyTimeandTrials(catalog, trial_inferior, trial_superior):
    return model.RegistersbyTimeandTrials(catalog, trial_inferior, trial_superior)

def RegistersByTimeandYear(catalog, year, time1, time2):
    return model.RegistersByTimeandYear(catalog, year, time1, time2)
    
def dateCategory(catalog, start, end):
    return model.dateCategory(catalog, start, end)

def rangeofYears(catalog, year1, year2, segmentos, niveles, consulta):
    return model.rangeofYears(catalog, year1, year2,  segmentos, niveles, consulta)


# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
