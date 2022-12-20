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
import tracemalloc
import datetime as dt

# Tamaño de campos de lectura csv aumentado
csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de 

def init():
    control = model.newcatalog()
    return control

# Funciones para la carga de datos

def loaddata(control,size):
    file1 = cf.data_dir + "Speedruns\game_data_utf-8-" + size + ".csv"
    file2 = cf.data_dir + "Speedruns\category_data_utf-8-" + size + ".csv"
    inputfile1 = csv.DictReader(open(file1, encoding="utf-8"),delimiter=",")
    inputfile2 = csv.DictReader(open(file2, encoding="utf-8"),delimiter=",")
    for item1 in inputfile1:
        for item2 in inputfile2:
            item2["Time_0"]=float(item2["Time_0"])
            item2["Num_Runs"]=int(item2["Num_Runs"])
            if item2["Record_Date_0"]!="":
                item2["Record_Date_0"]=dt.datetime.strptime(item2["Record_Date_0"],"%Y-%m-%dT%H:%M:%SZ")
            else: 
                item2["Record_Date_0"]=dt.datetime(1,1,1,0,0,0)
            if item2["Time_1"]!="":
                item2["Time_1"]=float(item2["Time_1"])
            if item2["Record_Date_1"]!="":
                item2["Record_Date_1"]=dt.datetime.strptime(item2["Record_Date_1"],"%Y-%m-%dT%H:%M:%SZ")
            if item2["Time_2"]!="":
                item2["Time_2"]=float(item2["Time_2"])
            if item2["Record_Date_2"]!="":
                item2["Record_Date_2"]=dt.datetime.strptime(item2["Record_Date_2"],"%Y-%m-%dT%H:%M:%SZ")
            model.addcategory(control,item2)
            if item1["Game_Id"] == item2["Game_Id"]:
                for key in item2.keys():
                    value = item2[key]
                    item1[key] = value
        item1["Release_Date"]=dt.datetime.strptime(item1["Release_Date"],"%y-%m-%d")
        model.addgame(control,item1)
    return control

# Requerimiento 1

def findbplt(datesup, dateinf, control, platform, criteria="Platforms"):
    list,size = model.find_in_range_date(datesup,dateinf,control,platform,criteria)
    return list,size

# Requerimiento 2

def findply(player,control):
    return model.find_by_player(player,control)

# Requerimiento 3

def findbnr(runsup,runinf,control):
    return model.find_in_range_num(runsup,runinf,control)

# Requerimiento 4

def findbd0(datesup,dateinf,control):
    return model.find_in_range_WOCrit(datesup,dateinf,control)

# Requerimiento 5

def firbt0(timesup,timeinf,control):
    return model.find_in_range_times(timesup,timeinf,control)  

# Requerimiento 6

def hist(lim_sup,lim_inf,n,x,propiedad,control):
    return model.histograma(lim_sup,lim_inf,n,x,propiedad,control) 

# Requerimiento 7

def findtop(platform,N,control):
    return model.find_top(platform,N,control)