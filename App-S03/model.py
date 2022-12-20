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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as omp
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as sa
assert cf
import datetime as dt
from tabulate import tabulate
import time
import math as ma

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newcatalog():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los juegos y categorías 
    se crean indices (Maps) por los siguientes criterios:
    - Platforms
    - Players
    - Num runs
    - Record dates
    - Record times
    - Release dates


    Retorna el analizador inicializado.
    """
    catalog = {"Games": None,
               "Games mp":None,
               "Categories": None,
               "Categories mp": None,
               "Platforms": None,
               "Players": None,
               "Num runs": None,
               "Record dates": None,
               "Record times": None,
               "Times 1":None,
               "Times 2":None,
               "Release dates": None,
               "Countries":None}

    catalog["Games"]= lt.newList("ARRAY_LIST",cmpfunction=compareIds)
    catalog["Categories"]= lt.newList("ARRAY_LIST",cmpfunction=compareIds)

    catalog["Platforms"]=mp.newMap(100,maptype="PROBING")
    catalog["Players"]=mp.newMap(25400,maptype="PROBING")
    catalog["Countries"]=mp.newMap(25400,maptype="PROBING")
    catalog["Categories mp"]=mp.newMap(200,maptype="PROBING")
    catalog["Games mp"]=mp.newMap(25000,maptype="PROBING")

    catalog["Num runs"]=omp.newMap()
    catalog["Record dates"]=omp.newMap()
    catalog["Record times"]=omp.newMap()
    catalog["Release dates"]=omp.newMap()
    catalog["Times 1"]=omp.newMap()
    catalog["Times 2"]=omp.newMap()

    return catalog

# Funciones para creacion de datos

def createnew(game,plt):
    platform = {"key":None,"elements":None}
    platform["key"]=plt
    platform["elements"]=lt.newList("ARRAY_LIST")
    lt.addLast(platform["elements"],game)
    return platform

# Funciones para agregar informacion al catalogo

def addgame(catalog,game):
    lt.addLast(catalog["Games"],game)
    mp.put(catalog["Games mp"],game["Game_Id"],game)
    addplatform(catalog["Platforms"],game)
    addreldates(catalog["Release dates"],game)
    return catalog

def addcategory(catalog,category):
    lt.addLast(catalog["Categories"],category)
    mp.put(catalog["Categories mp"],category["Game_Id"],category)
    addplayers(catalog["Players"],category)
    addnumruns(catalog["Num runs"],category)
    omp.put(catalog["Record dates"],category["Record_Date_0"],category)
    omp.put(catalog["Record times"],category["Time_0"],category)
    if category["Time_1"]!= "":
        omp.put(catalog["Times 1"],category["Time_1"],category)
    if category["Time_2"]!= "":
        omp.put(catalog["Times 2"],category["Time_2"],category)
    addcountries(catalog["Countries"],category)
    return catalog 

def addplatform(map,game):
    platforms = game["Platforms"].split(",")
    for plt in platforms:
        plt=plt.strip()
        entry=mp.get(map,plt)
        if entry is None:
            platform=createnew(game,plt)
            mp.put(map,plt,platform)
        else:
            pltvalue=me.getValue(entry)
            lt.addLast(pltvalue["elements"],game)
    return map

def addplayers(map,game):
    players = game["Players_0"].split(",")
    for ply in players:
        ply = ply.strip()
        entry=mp.get(map,ply)
        if entry is None:
            player=createnew(game,ply)
            mp.put(map,ply,player)
        else:
            plyvalue=me.getValue(entry)
            lt.addLast(plyvalue["elements"],game)
    return map

def addnumruns(map,game):
    num = int(game["Num_Runs"])
    entry = omp.get(map,num)
    if entry is None: 
        number = createnew(game,num)
        omp.put(map,num,number)
    else:
        numvalue=me.getValue(entry)
        lt.addLast(numvalue["elements"],game)
    return map

"""def addrecdates(map,game):
    dt = game["Record_Date_0"]
    entry = omp.get(map,dt)
    if entry is None: 
        date = createnew(game,dt)
        omp.put(map,dt,date)
    else:
        dtvalue=me.getValue(entry)
        lt.addLast(dtvalue["elements"],game)
    return map

def addrectimes(map,game):
    t = game["Time_0"]
    entry = omp.get(map,t)
    if entry is None: 
        time = createnew(game,t)
        omp.put(map,t,time)
    else:
        tvalue=me.getValue(entry)
        lt.addLast(tvalue["elements"],game)
    return map"""

def addreldates(map,game):
    dt = game["Release_Date"]
    entry = omp.get(map,dt)
    if entry is None: 
        date = createnew(game,dt)
        omp.put(map,dt,date)
    else:
        dtvalue=me.getValue(entry)
        lt.addLast(dtvalue["elements"],game)
    return map

def addcountries(map,game):
    ct = game["Country_0"]
    entry=mp.get(map,ct)
    if entry is None:
        country=createnew(game,ct)
        mp.put(map,ct,country)
    else:
        ctvalue=me.getValue(entry)
        lt.addLast(ctvalue["elements"],game)
    return map


# Requerimiento 1

def find_in_range_date(lim_sup,lim_inf,catalog,critwanted,criteria):
    mapa = catalog[criteria]
    list = lt.newList("ARRAY_LIST")
    entry = mp.get(mapa,critwanted)
    if entry != None: 
        entryvalue = me.getValue(entry)
        size = entryvalue["elements"]["size"]
        for i in range(size):
            if entryvalue["elements"]["elements"][i]["Release_Date"] < lim_sup and entryvalue["elements"]["elements"][i]["Release_Date"] >lim_inf:
                lt.addLast(list,entryvalue["elements"]["elements"][i])
    list=sa.sort(list,cmp_date_abb_name)
    return list,size

# Requerimiento 2

def find_by_player (player,catalog):
    mapa=catalog["Players"]
    entry=mp.get(mapa,player)
    list=None
    if entry != None: 
        entryvalue= me.getValue(entry)
        list=sa.sort(entryvalue["elements"],cmp_time_num_name)
    return list

# Requerimiento 3

def find_in_range_num (sup,inf,catalog):
    mapa=catalog["Num runs"]
    lst = omp.values(mapa,inf,sup)
    return lst

# Requerimiento 4

def find_in_range_WOCrit (sup,inf,catalog):
    mapa=catalog["Record dates"]
    lst=omp.values(mapa,inf,sup)
    return sa.sort(lst,cmp_rdate)

# Requerimiento 5

def find_in_range_times(sup,inf,catalog):
    mapa=catalog["Record times"]
    lst=omp.values(mapa,inf,sup)
    return lst

# Requerimiento 6

def histograma(lim_sup,lim_inf,n,x,propiedad,catalog):
    if propiedad == 1:
        datos1 = omp.values(catalog["Release dates"],lim_inf,lim_sup)
        datos = lt.newList("ARRAY_LIST")
        for i in range(datos1["size"]):
            for j in range(datos1["elements"][i]["elements"]["size"]):
                key = datos1["elements"][i]["elements"]["elements"][j]["Game_Id"]
                entry = mp.get(catalog["Categories mp"],key)
                if entry != None:
                    lt.addLast(datos,me.getValue(entry))

        min = float(omp.minKey(catalog["Record times"]))
        max = float(omp.maxKey(catalog["Record times"]))
        ratio = round((max-min)/n,2)
        categories = lt.newList("ARRAY_LIST")
        for i in range(n+1):
            if i<n:
                lt.addLast(categories,(min+i*ratio,min+(i+1)*ratio))
            else:
                lt.addLast(categories,(min+i*ratio,max))
        counter = lt.newList("ARRAY_LIST")
        lvl = lt.newList("ARRAY_LIST")
        for i in range(n):
            c=0
            low = categories["elements"][i][0]
            high = categories["elements"][i][1]
            for j in range(datos["size"]):
                if datos["elements"][j]["Time_0"]!="":
                    if datos["elements"][j]["Time_0"]<high and datos["elements"][j]["Time_0"]>low:
                        c+=1
            lt.addLast(counter,c)
        for i in range(n):
            lt.addLast(lvl,counter["elements"][i]//x)
        return min,max,categories,counter,lvl
    elif propiedad == 2:
        datos1 = omp.values(catalog["Release dates"],lim_inf,lim_sup)
        datos = lt.newList("ARRAY_LIST")
        for i in range(datos1["size"]):
            for j in range(datos1["elements"][i]["elements"]["size"]):
                key = datos1["elements"][i]["elements"]["elements"][j]["Game_Id"]
                entry = mp.get(catalog["Categories mp"],key)
                if entry != None:
                    lt.addLast(datos,me.getValue(entry))
        min = float(omp.minKey(catalog["Time 1"]))
        max = float(omp.maxKey(catalog["Time 1"]))
        ratio = round((max-min)/n,2)
        categories = lt.newList("ARRAY_LIST")
        for i in range(n+1):
            if i<n:
                lt.addLast(categories,(min+i*ratio,min+(i+1)*ratio))
            else:
                lt.addLast(categories,(min+i*ratio,max))
        counter = lt.newList("ARRAY_LIST")
        lvl = lt.newList("ARRAY_LIST")
        for i in range(n):
            c=0
            low = categories["elements"][i][0]
            high = categories["elements"][i][1]
            for j in range(datos["size"]):
                if datos["elements"][j]["Time_1"]!="":
                    if datos["elements"][j]["Time_1"]<high and datos["elements"][j]["Time_1"]>low:
                        c+=1
            lt.addLast(counter,c)
        for i in range(n):
            lt.addLast(lvl,counter["elements"][i]//x)
        return min,max,categories,counter,lvl
    elif propiedad == 3:
        datos1 = omp.values(catalog["Release dates"],lim_inf,lim_sup)
        datos = lt.newList("ARRAY_LIST")
        for i in range(datos1["size"]):
            for j in range(datos1["elements"][i]["elements"]["size"]):
                key = datos1["elements"][i]["elements"]["elements"][j]["Game_Id"]
                entry = mp.get(catalog["Categories mp"],key)
                if entry != None:
                    lt.addLast(datos,me.getValue(entry))
        min = float(omp.minKey(catalog["Time 2"]))
        max = float(omp.maxKey(catalog["Time 2"]))
        ratio = round((max-min)/n,2)
        categories = lt.newList("ARRAY_LIST")
        for i in range(n+1):
            if i<n:
                lt.addLast(categories,(min+i*ratio,min+(i+1)*ratio))
            else:
                lt.addLast(categories,(min+i*ratio,max))
        counter = lt.newList("ARRAY_LIST")
        lvl = lt.newList("ARRAY_LIST")
        for i in range(n):
            c=0
            low = categories["elements"][i][0]
            high = categories["elements"][i][1]
            for j in range(datos["size"]):
                if datos["elements"][j]["Time_2"]!="":
                    if datos["elements"][j]["Time_2"]<high and datos["elements"][j]["Time_2"]>low:
                        c+=1
            lt.addLast(counter,c)
        for i in range(n):
            lt.addLast(lvl,counter["elements"][i]//x)
        return min,max,categories,counter,lvl
    elif propiedad == 4:
        datos1 = omp.values(catalog["Release dates"],lim_inf,lim_sup)
        datos = lt.newList("ARRAY_LIST")
        for i in range(datos1["size"]):
            for j in range(datos1["elements"][i]["elements"]["size"]):
                key = datos1["elements"][i]["elements"]["elements"][j]["Game_Id"]
                entry = mp.get(catalog["Categories mp"],key)
                if entry != None:
                    lt.addLast(datos,me.getValue(entry))
        promedios = lt.newList("ARRAY_LIST")
        for i in range(datos["size"]):
            sum = datos["elements"][i]["Time_0"]
            tot = 1
            if datos["elements"][i]["Time_1"]!="":
                sum += datos["elements"][i]["Time_1"]
                tot += 1
            if datos["elements"][i]["Time_2"]!="":
                sum += datos["elements"][i]["Time_2"]
                tot += 1
            prom = round(sum/tot,2)
            lt.addLast(promedios,prom)
        promedios = sa.sort(promedios,cmp_min)
        min = float(lt.firstElement(promedios))
        max = float(lt.lastElement(promedios))
        categories = lt.newList("ARRAY_LIST")
        ratio = max-min
        for i in range(n+1):
            if i<n:
                lt.addLast(categories,(min+i*ratio,min+(i+1)*ratio))
            else:
                lt.addLast(categories,(min+i*ratio,max))
        counter = lt.newList("ARRAY_LIST")
        lvl = lt.newList("ARRAY_LIST")
        for i in range(n):
            c=0
            low = categories["elements"][i][0]
            high = categories["elements"][i][1]
            for j in range(promedios["size"]):
                if promedios["elements"][j]<high and promedios["elements"][j]>low:
                    c+=1
            lt.addLast(counter,c)
        for i in range(n):
            lt.addLast(lvl,counter["elements"][i]//x)
        return min,max,categories,counter,lvl
    elif propiedad == 5:
        datos1 = omp.values(catalog["Release dates"],lim_inf,lim_sup)
        datos = lt.newList("ARRAY_LIST")
        for i in range(datos1["size"]):
            for j in range(datos1["elements"][i]["elements"]["size"]):
                key = datos1["elements"][i]["elements"]["elements"][j]["Game_Id"]
                entry = mp.get(catalog["Categories mp"],key)
                if entry != None:
                    lt.addLast(datos,me.getValue(entry))
        min = omp.minKey(catalog["Num runs"])
        max = omp.maxKey(catalog["Num runs"])
        ratio = round((max-min)/n,2)
        categories = lt.newList("ARRAY_LIST")
        for i in range(n+1):
            if i<n:
                lt.addLast(categories,(min+i*ratio,min+(i+1)*ratio))
            else:
                lt.addLast(categories,(min+i*ratio,max))
        counter = lt.newList("ARRAY_LIST")
        lvl = lt.newList("ARRAY_LIST")
        for i in range(n):
            c=0
            low = categories["elements"][i][0]
            high = categories["elements"][i][1]
            for j in range(datos["size"]):
                if datos["elements"][j]["Num_Runs"]<high and datos["elements"][j]["Num_Runs"]>low:
                    c+=1
            lt.addLast(counter,c)
        for i in range(n):
            lt.addLast(lvl,counter["elements"][i]//x)
        return min,max,categories,counter,lvl


# Requerimiento 7

def find_top(plat,N,catalog):
    mapa=catalog["Platforms"]
    entry = mp.get(mapa,plat)
    lit = lt.newList("ARRAY_LIST")
    if entry:
        list_data = me.getValue(entry)
        size = list_data["elements"]["size"]
        value = lt.newList("ARRAY_LIST")
        for i in range(size):
            key = list_data["elements"]["elements"][i]["Game_Id"]
            entry = mp.get(catalog["Categories mp"],key)
            if entry != None:
                lt.addLast(value,me.getValue(entry))
        for i in range(value["size"]):
            if value["elements"][i]["Misc"] != True:
                lanzm = list_data["elements"]["elements"][i]["Release_Date"]
                year = int(lanzm.year)
                antiquity = 5
                if year >= 2018:
                    antiquity = year - 2017
                elif 2018 > year and year > 1998:
                    antiquity = 404.6 - (year/5)
                tries = list_data["elements"]["elements"][i]["Total_Runs"]
                popularity = ma.log(float(tries))
                time0 = 0
                time1 = 0
                time2 = 0
                if value["elements"][i]["Time_0"]:
                    time0 = value["elements"][i]["Time_0"]
                if value["elements"][i]["Time_1"]:
                    time1 = value["elements"][i]["Time_1"]
                if value["elements"][i]["Time_2"]:
                    time2 = value["elements"][i]["Time_2"]
                t_time = (float(time0)+float(time1)+float(time2))
                revenue = (popularity*t_time)/antiquity
                marketshared = marketshare(plat,list_data["elements"]["elements"][i]["Name"],catalog)
                streamrevenue = revenue*marketshared
                value["elements"][i]["stream"]=streamrevenue
                lt.addLast(lit,value["elements"][i])
    return sa.sort(lit,cmp_stream)

def marketshare(plat,name,catalog):
    mapa=catalog["Platforms"]
    entry = mp.get(mapa,plat)
    pt = 1
    gt = 1
    if entry:
        list_data = me.getValue(entry)
        size = list_data["elements"]["size"]
        value = lt.newList("ARRAY_LIST")
        for i in range(size):
            key = list_data["elements"]["elements"][i]["Game_Id"]
            entry = mp.get(catalog["Categories mp"],key)
            if entry != None:
                lt.addLast(value,me.getValue(entry))
        for i in range(value["size"]):
            if value["elements"][i]["Misc"] != True:
                if value["elements"][i]["Time_2"] != "":
                    pt += 3
                elif value["elements"][i]["Time_1"] != "":
                    pt += 2
                elif value["elements"][i]["Time_0"] != "":
                    pt += 1
            if name == list_data["elements"]["elements"][i]["Name"]:
                if value["elements"][i]["Time_2"] != "":
                    gt += 3
                elif value["elements"][i]["Time_1"] != "":
                    gt += 2
                elif value["elements"][i]["Time_0"] != "":
                    gt += 1
    return gt/pt


# Funciones utilizadas para comparar elementos dentro de una lista

def cmp_date_abb_name(game1,game2):
    if game1["Release_Date"]!=game2["Release_Date"]:
        return game1["Release_Date"]>game2["Release_Date"]
    elif game1["Abbreviation"].lower()!=game2["Abbreviation"].lower():
        return game1["Abbreviation"].lower()>game2["Abbreviation"].lower()
    elif game1["Name"].lower()!=game2["Name"].lower():
        return game1["Name"].lower()>game2["Name"].lower()

def cmp_time_num_name (game1,game2):
    if game1["Time_0"]!=game2["Time_0"]:
        return game1["Time_0"]<game2["Time_0"]
    elif game1["Num_Runs"]!=game2["Num_Runs"]:
       return game1["Num_Runs"]>game2["Num_Runs"] 
    elif game1["Name"].lower()!=game2["Name"].lower():
        return game1["Name"].lower()>game2["Name"].lower()

def cmp_rdate (game1,game2):
    return game1["Record_Date_0"]>game2["Record_Date_0"]

def cmp_min (dato1,dato2):
    return dato1<dato2

def cmp_stream(data1,data2):
    return data1["stream"]>data2["stream"]

# Funciones de ordenamiento
def compareIds(id1, id2):
    
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1