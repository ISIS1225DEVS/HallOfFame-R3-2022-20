# -*- coding: utf-8 -*-

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
from time import sleep
from types import FunctionType
from App.main_adts import lista
from model import add_category, add_game
import config as cf
import model as md
import tracemalloc
from timeit import default_timer as timer
from datetime import datetime
import datetime as datetime
import csv
import pandas as pd 
from main_adts import Hash, lista, rbt, Heap
from DISClib.Algorithms.Sorting import mergesort as merge

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""
csv.field_size_limit(2147483647)
castBoolean=lambda x: True if x in ('True', 'true', 'TRUE', 'T', 't', '1', "Si", "SI", "Sí", "si", "Yes, YES") else False

#decorador manejo de tiempos y memoria
def deltaMemory(stop_memory:tracemalloc.Snapshot, start_memory:tracemalloc.Snapshot)->float:
    """Devuelve la diferencia en memoria en KB entre dos Snapshots
    ---------------------------------------------------------------------
    Args:
        start_memory: Snapshot inicial
        stop_memory: Snapshot final
    ---------------------------------------------------------------------
    Return: 
        Diferencia de uso de memoria en KB"""
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    delta_memory = delta_memory/1024.0
    return delta_memory

def printLoadDataAnswer(answer:...)->str:
    """Valida y retorna los tiempos y/o memoria
    ---------------------------------------------------------------------
    Args:
        answer: información con los tiempos y/o memoria
    ---------------------------------------------------------------------
    Return: 
        String con el tiempo y/o memoria de ejecución"""
    if isinstance(answer, (list, tuple)) is True:
        return("Tiempo [ms]: "+ f"{answer[0]:.3f}"+ "||"+
            "Memoria [kB]: "+ f"{answer[1]:.3f}")
    else:
        return("Tiempo [ms]: "+ f"{answer:.3f}")


def timer_y_mem(func:FunctionType)->tuple:
    """Decorador para medir tiempos y memoria
    ---------------------------------------------------------------------
    Args:
        func: función a medir tiempo
    ---------------------------------------------------------------------
    Return: 
        Tupla con el resultado de la función y los tiempos/memoria"""
    def new_func(*args:...)->tuple:
        """Función para medir tiempos y memoria
        ---------------------------------------------------------------------
        Args:
            *args: argumentos para llamar a la función
        ---------------------------------------------------------------------
        Return: 
            Tupla con el resultado de la función y los tiempos/memoria"""
        print("¿Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        start_time = timer()
        if mem is True:
            tracemalloc.start()
            start_memory = tracemalloc.take_snapshot()

        fun=func(*args)

        stop_time = timer()
        delta_time = (stop_time-start_time)*1000

        if mem is True:
            stop_memory = tracemalloc.take_snapshot()
            tracemalloc.stop()
            delta_memory = deltaMemory(stop_memory, start_memory)
            exec_time= delta_time, delta_memory
        else:
            exec_time= delta_time
        
        return fun, printLoadDataAnswer(exec_time)
    return new_func


# Inicialización del Catálogo de libros
def catalog_init()->hash:
    """Inicializa el catalogo/donde se manejan los datos po
    ---------------------------------------------------------------------
    Args:
        None
    ---------------------------------------------------------------------
    Return: 
        DISC.ADT: Hash map para almacenar la información"""
    catalog = md.new_catalog()
    return catalog 

# Funciones para la carga de datos
@timer_y_mem
def cargar_datos(catalog:hash,size_lt:str)->None:
    """Inicializa el catalogo/donde se manejan los datos po
    ---------------------------------------------------------------------
    Args:
        None
    ---------------------------------------------------------------------
    Return: 
        DISC.ADT: Hash map para almacenar la información
    ---------------------------------------------------------------------
    Exceptions:
        Imprime por pantalla el error sucedido en la ejecución"""
    path_file1=cf.data_dir + f"category_data_utf-8-{size_lt}.csv"
    path_file2=cf.data_dir + f"game_data_utf-8-{size_lt}.csv"
    file1=csv.DictReader(open(path_file1, encoding="utf-8"))
    file2=csv.DictReader(open(path_file2, encoding="utf-8"))
    totalgame=catalog.get_value("game").get_value("total")
    totalcontent=catalog.get_value("category").get_value("total")
    for game in file2:
            
            game["date"]=md.date(game)
            totalgame.add_last(game)
            add_game(catalog, game)
            
    for content in file1:
            game=content["Game_Id"]
            
            name=catalog.get_value("game").get_value("game_id")
            x=name.get_value(int(game))
            content["Name"]=x["Name"]
            content["Platforms"]=x["Platforms"]
            content["Genres"]=x["Genres"]
            content["Release_Date"]= x['Release_Date']
            content["date"]= x['date']
            content["año"]=content["date"].split("-")[0]
            content["Total_Runs"]=x["Total_Runs"]
            totalcontent.add_last(content)
            add_category(catalog, content)

    return catalog

 
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
@timer_y_mem
def requerimiento5(datos, inferior, superios):
    times=datos.get_value("category").get_value("time0")
    lst = times.values_range(inferior,superios)
    for heaps in lst.iterator():
        heaps.heapsort()
    return lst, times.size()

@timer_y_mem
def reqerimiento3(datos, inferior, superios):
    records=datos.get_value("category").get_value("num_records")
    lst = records.values_range(inferior, superios)
    
    for juegos in lst.iterator():
        juegos.merge_sort(md.cmp3_1)

    return lst

@timer_y_mem   
def requerimiento2carol(datos, jugador):
    data=datos.get_value("category").get_value("jugadoresreq2").get_value(jugador)
    return data.values()
    
@timer_y_mem    
def reqeurimiento7(datos, plataformai):
    arbol=rbt(md.cmp7)
    x=0
    plataforma=datos.get_value("game").get_value("plataformas7").get_value(plataformai)
    for juegos in plataforma.iterator():
        juego=md.rentabilidad(juegos, datos, plataformai)
        arbol.put(juego["Stream_Revenue"], juego)
        if juegos["Platforms"]==plataformai:
            x+=1
    return arbol.values(), x
#Funciones de impresion 
@timer_y_mem
def requerimiento4(catalogo, inferior, superior):
    return md.requerimiento4(catalogo, inferior, superior)

def requerimiento1laura(catalogo, inferior, superior, plataforma):
    return md.req1(catalogo, inferior, superior, plataforma)

@timer_y_mem
def req1(datos, inferior, superior, plataforma):
    lst=md.req11(datos, inferior, superior, plataforma)
    return lst

@timer_y_mem
def requerimiento6(catalogo, inferior, superior, opcion):
    return md.req6(catalogo, inferior, superior, opcion)
def req6(catalogo, inferior, superior):
    return md.requ6(catalogo, inferior, superior)

@timer_y_mem
def requerimiento8(catalogo,anio ,inferior, superior):
    mapa=catalogo.get_value("category").get_value("release_map")
    arbol=mapa.get_value(anio)
    rango=arbol.values_range( inferior, superior)
    return hash_by_country(rango)


def hash_by_country(rango:md.lista):
    mapa=Hash(200, "PROBING", 1, None)
    for heap in rango.iterator():
        for element in heap.iterator():
            for country in element["Country_0"].split(","):
                if mapa.contains(country):
                    value=mapa.get_value(country)
                    value.insert(element)
                    mapa.put(country, value)
                else:
                    lst = Heap(lambda a, b : len(a)>len(b))
                    lst.insert(element)
                    mapa.put(country, lst)
    return mapa
