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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """
from re import L
import numpy as np
import config as cf
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from unicodedata import category
from datetime import datetime
import datetime as datetime
from DISClib.Algorithms.Sorting import selectionsort as selection
import operator as operator
from itertools import chain
from main_adts import Hash, lista, rbt, Heap
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def new_catalog()->hash:
    catalogo=Hash(6, "PROBING", 0.5, None)
    catalogo.put("game", Hash(6, "PROBING", 0.5, None))
    game = catalogo.get_value("game")
    game.put("plataformas", Hash(6, "PROBING", 0.5, None))
    game.put("plataformas7", Hash(6, "PROBING", 0.5, None))
       
    game.put("plataformas_req1", Hash(6, "PROBING", 0.5, None))
    
    game.put("total", lista("ARRAY_LIST"))

    game.put("release_date", Hash(6, "PROBING", 0.5, None))
    game.put("game_id", Hash(6, "PROBING", 0.5, None))
    game.put("release_date2", rbt(cmp_date2)) #luego ver si lo borro
    
    catalogo.put("category", Hash(6, "PROBING", 0.5, None))
    categoria=catalogo.get_value("category")
    categoria.put("jugadores", Hash(5000, "CHAINING", 0.7, None))
    categoria.put("jugadoresreq2", Hash(5000, "CHAINING", 0.7, None))
    categoria.put("num_records", rbt(cmp_runs))
    categoria.put("plataformas", Hash(6, "PROBING", 0.5, None))
    
    categoria.put("año", rbt(cmp_date2)) 
       

    categoria.put("ARRAY_LIST", Hash(6, "PROBING", 0.5, None))
    categoria.put("total", lista("ARRAY_LIST"))
    categoria.put("recors", rbt(cmp_record0))
    categoria.put("time0", rbt(cmp_time0))
    categoria.put("release2", rbt(cmp_date2))
    categoria.put("release", Hash(6, "PROBING", 0.5, None))
    categoria.put("release_map", Hash(6, "PROBING", 0.5, None))

    categoria.put("Game_Id", Hash(5000, "CHAINING", 0.7, None))
    return catalogo 

# Funciones para agregar informacion al catalogo
cmp_time0=lambda a, b: 1 if float(a)>float(b) else 0 if float(a)==float(b) else -1
cmp_record0=lambda a, b: 1 if a<b else 0 if a==b else -1


def cmp_game2(x, y):
    if x["date"]<y["date"]:
        return 1
    else:
        return -1
def add_game(catalog:Hash, game:dict)->None:
    
    games=catalog.get_value("game")
    game_id=games.get_value("game_id")
    game_id.put(int(game["Game_Id"]), game)
    
    plataformas1=catalog.get_value("game").get_value("plataformas_req1")
    add_category_hash2(plataformas1, game, "Platforms", cmpgame)
    
    plataformas=catalog.get_value("game").get_value("plataformas")
    add_req1(plataformas, game, "Platforms", cmp_1)

    plataformas2=catalog.get_value("game").get_value("plataformas7")
    add_category_hash(plataformas2, game, "Platforms", cmpgame)

    plataformas=catalog.get_value("game").get_value("release_date")
    add_category_hash(plataformas, game, "Release_Date", cmpgame)

    tree_release = games.get_value("release_date2")
    add_category_trees(tree_release, game, "Release_Date", cmp1)
    
    
def add_req1(mapa:Hash, game:dict, by:str, cmpf):
    time=str(datetime.datetime.strptime(game['Release_Date'],'%y-%m-%d'))

    game["date"]=time[:time.find(" ")]

    for i in game[by].split(", "):
        if mapa.contains(i):
            arbol=mapa.get_value(i)

            arbol.put(game, game)

            mapa.put(i, arbol)
        else:
            arbol=rbt(cmpf)
            arbol.put(game, game)
            mapa.put(i, arbol)

def sep_players(players:dict)->list:
    jugadores=[]
    base={a:b for a,b in players.items() if a[-1] not in "012"}
    for i in range(3):
        a, b = players[f"Players_{i}"],players[f"Country_{i}"]
        if a!="" and b!="":
            for c,d in zip(a.split(","), b.split(",")):
                dic=base.copy()
                temp={f"Players_{i}":c, f"Country_{i}":d, f"Record_Date_{i}":players[f"Record_Date_{i}"], f"Time_{i}":players[f"Time_{i}"]}
                dic.update(temp)
                jugadores.append(dic)
    return jugadores


def add_hash_by_some(mapa:Hash,content, key, cmpf)->None:
    for dato in content[key].split(", "):
        if dato=="":
            dato="Unknown"
        if mapa.contains(dato):
            heap=mapa.get_value(dato)
            if heap is None:
                heap=Heap(cmpf)
            heap.insert(content)
            mapa.put(content[key], heap)
        else:
            heap=Heap(cmpf)
            heap.insert(content)
            mapa.put(content[key], heap)

def add_category(catalog:Hash, speedrun:dict)->None:
    categoria=catalog.get_value("category")
    players=categoria.get_value("jugadores")
    # add_hash_by_release(players, speedrun ,"Players_0", cmp_times)
 
    map_num_runs= categoria.get_value("num_records")
    add_category_trees(map_num_runs, speedrun, "Num_Runs", cmp1)
   
    tree_time0= categoria.get_value("time0")
    add_hash_by_some(tree_time0, speedrun,"Time_0",  cmpf_req5)

    prueba= categoria.get_value("recors")
    add_hash_by_some(prueba, speedrun,"Record_Date_0",  cmpf_req4)

    plataformas=catalog.get_value("category").get_value("plataformas")
    add_category_hash(plataformas, speedrun, "Platforms", cmpgame)

    fechas=catalog.get_value("category").get_value("release")
    add_category_hash(fechas, speedrun, "date", cmpgame)

    fechas2 = categoria.get_value("release2")
    add_category_trees(fechas2, speedrun, "date", cmp_game2)

    game=catalog.get_value("category").get_value("Game_Id")
    add_category_hash(game, speedrun, "Game_Id", cmpgame)   

    add_players(players, speedrun)

    map_time=categoria.get_value("release_map")
    add_map(map_time, speedrun)
    
    año=categoria.get_value("año")
    add_category_trees(año, speedrun, "año", cmp_game2)
    # add_category_hash(map_time, speedrun, "Game_Id", cmpgame)
    
    carol=categoria.get_value("jugadoresreq2")
    add_category_hashcarol(carol, speedrun, "Players_0", cmpgame) 
    
       

def add_players(players:Hash, content:dict):
    for player, country, date in zip(content["Players_0"].split(","), content["Country_0"].split(","), content["Record_Date_0"].split(",")):
        dictt={a: b for a, b in content.items() if not a[-1].isdigit()} 
        if player == "Nami":
            print("Namii")
        dictt["Players_0"]=player
        dictt["Country_0"]=country
        dictt["Record_Date_0"]=date
        dictt["Time_0"]=content["Time_0"]
        try:
            if players.contains(player):
                value=players.get_value(player)
                if value.contains(dictt["Time_0"]):
                    heap=value.get_value(dictt["Time_0"])
                    heap.insert(dictt)
                    value.put(dictt["Time_0"], heap)
                    players.put(player, value)

                else:
                    heap=Heap(cmp3_1)
                    heap.insert(dictt)
                    value.put(dictt["Time_0"], heap)
                    players.put(player, value)
            else:
                tree=rbt(cmp3)
                heap=Heap(cmp3_1)
                heap.insert(dictt)
                tree.put(dictt["Time_0"], heap)
                players.put(player, tree)
        except Exception as err:
                if players.contains(player):
                    value=players.get_value(player)
                    if value.contains(dictt["Time_0"]):
                        heap=value.get_value(dictt["Time_0"])
                        heap.insert(dictt)
                        value.put(dictt["Time_0"], heap)
                        players.put(player, value)

                    else:
                        heap=Heap(cmp3_1)
                        heap.insert(dictt)
                        value.put(dictt["Time_0"], heap)
                        players.put(player, value)
                else:
                    tree=rbt(cmp3)
                    heap=Heap(cmp3_1)
                    heap.insert(dictt)
                    tree.put(dictt["Time_0"], heap)
                    players.put(player, tree)

def cmpf_map(elem1, elem2):
    if float(elem1["Time_0"]) > float(elem2["Time_0"]):
        return True
    elif float(elem1["Time_0"]) < float(elem2["Time_0"]):
        return -1
    else:
        return 0

def cmpf_map2(elem1, elem2):
    if float(elem1) > float(elem2):
        return True
    elif float(elem1) < float(elem2):
        return -1
    else:
        return 0

def add_map(mapa:Hash, speedrun):
    for date in speedrun["date"].split(","):
        date=date[:4]
        
        if mapa.contains(date):
            arbol=mapa.get_value(date)
            if arbol.contains(speedrun["Time_0"]):
                heap=arbol.get_value(speedrun["Time_0"])
                heap.insert(speedrun)
                arbol.put(speedrun["Time_0"], heap)
                mapa.put(date, arbol)
            else:
                heap=Heap(cmpf_map)
                heap.insert(speedrun)
                arbol.put(speedrun["Time_0"], heap)
                mapa.put(date, arbol)
        else:
            arbol=rbt(cmpf_map2)
            heap=Heap(cmpf_map)
            heap.insert(speedrun)
            arbol.put(speedrun["Time_0"], heap)
            mapa.put(date, arbol)
        
       
           

def new_entry_function(speedrun):
    
    entry = lista("ARRAY_LIST")
    entry.add_last(speedrun)
    
    return entry

def new_entry_funcion2(sppedrun):
    entry = rbt(cmp7)
    entry.put(sppedrun["date"], lista("ARRAY_LIST"))
    y=sppedrun["date"]
    x=entry.get_value(sppedrun["date"])
    x.add_last(sppedrun)
    
    return entry
def new_entry_funcioncarol(sppedrun):
    entry = rbt(cmpf=cmp77)
    entry.put(sppedrun["Time_0"], lista("ARRAY_LIST"))
    y=sppedrun["Time_0"]
    x=entry.get_value(sppedrun["Time_0"])
    x.add_last(sppedrun)
    
    return entry


def add_category_trees(map_category, speedrun:dict, category, cmp)->None:
    category_info=speedrun[category]
    entry = map_category.get(category_info)
   
    if entry is None:
        new_entry = new_entry_function(speedrun)
        map_category.put(category_info, new_entry)
    else:
        entry= me.getValue(entry)
        entry.add_last(speedrun)
 
def add_category_hash(hash_category, speedrun:dict, category, cmp)->None:
    categoryinf=speedrun[category]
    
    for category_info in categoryinf.split(", "):
        entry = hash_category.contains(category_info)
    
        if entry is False:
            new_entry = new_entry_function(speedrun)
            hash_category.put(category_info, new_entry)
        else:
            entry= hash_category.get_value(category_info)
            entry.add_last(speedrun)
            
def add_category_hash3(hash_category, speedrun:dict, category, cmp)->None:
    categoryinf=speedrun[category]
    
    for category_info in categoryinf.split(","):
        entry = hash_category.contains(category_info)
    
        if entry is False:
            new_entry = new_entry_function(speedrun)
            hash_category.put(category_info, new_entry)
        else:
            entry= hash_category.get_value(category_info)
            entry.add_last(speedrun)           
            
def add_category_hash2(hash_category, speedrun:dict, category, cmp)->None:
    
    categoryinf=speedrun[category]
    
    for category_info in categoryinf.split(", "):
        entry = hash_category.contains(category_info)
    
        if entry is False:
            new_entry = new_entry_funcion2(speedrun)
            hash_category.put(category_info, new_entry)
        else:
            entry= hash_category.get_value(category_info)
            u=speedrun["date"]
            y=entry.get_value(u)
            if y != None:
                y.add_last(speedrun)
            else:
                entry.put(speedrun["date"], lista("ARRAY_LIST"))
                w=entry.get_value(u)
                w.add_last(speedrun)

def add_category_hashcarol(hash_category, speedrun:dict, category, cmp)->None:
    
    categoryinf=speedrun[category]
    
    for category_info in categoryinf.split(","):
        entry = hash_category.contains(category_info)
    
        if entry is False:
            new_entry = new_entry_funcioncarol(speedrun)
            hash_category.put(category_info, new_entry)
        else:
            entry= hash_category.get_value(category_info)
            u=speedrun["Time_0"]
            y=entry.get_value(u)
            if y != None:
                y.add_last(speedrun)
            else:
                entry.put(speedrun["Time_0"], lista("ARRAY_LIST"))
                w=entry.get_value(u)
                w.add_last(speedrun)

def rentabilidad(juego, datos, plataformai):


    antiguedad_data=antiguedad(juego)
    popularidad_data=popularidad(juego, datos)
    lista_promedio_data, promedio_data=promedio(juego, datos)
    
    revenue=0
    for elementos in lista_promedio_data.iterator():
        revenue += ((popularidad_data)*(elementos/60))/antiguedad_data
    
   
    share_data=marketshare(juego, datos, plataformai)

    streamrevenue = share_data*revenue
    #Hacer el streamrenevue para cada uno, el revenue se calcula solo para uno  
    juego["Time_Avg"]=round(promedio_data, 2)
    juego["Market_Share"]=round(share_data,2)
    juego["Stream_Revenue"]=round(streamrevenue,2)
        
    return juego


def antiguedad(juego):
    antiguedad=juego["Release_Date"]
    
    split=antiguedad.split("-")
    if int(split[0]) > 22:
        split[0]="19"+split[0]
    else:
         split[0]="20"+split[0]       
    antiguedad=int(split[0])
    
    if antiguedad>=2018:
        resultado=antiguedad-2017
    elif antiguedad>1998 and antiguedad<2018:
        resultado=(-1/5)*antiguedad+404.6
    else:
        resultado=5
    return resultado

def popularidad(juego, datos):
    return np.log(int(juego["Total_Runs"]))

def promedio(juego, datos):
    total=datos.get_value("category").get_value("Game_Id").get_value(juego["Game_Id"])
    x1=0
    listaa=lista("ARRAY_LIST")
    suma1=0

    for juegos in total.iterator():
        
        misc=juegos["Misc"]
        if misc == "False":
         
            suma=0
            x=0
            if (juegos["Time_0"]) != "":
                x+= float(juegos["Time_0"])
                suma+=1
            if (juegos["Time_1"]) != "":
                x+=float(juegos["Time_1"])
                suma+=1
            if (juegos["Time_2"]) != "":
                x+=float(juegos["Time_2"])
                suma+=1
            x1+=1
            promedio=x/suma
            listaa.add_last(promedio)
            suma1+=promedio
            
    if suma1!=0:
        return listaa, suma1/x1
    else:
        return listaa, 0

def marketshare(juego, datos, plataformai):

    count=0
    cc=0
 
    data_plataforma=datos.get_value("category").get_value("plataformas").get_value(plataformai)
    for elementos in data_plataforma.iterator():
            if elementos["Misc"]=="False":    
                count+=1
                
                
    count2=datos.get_value("category").get_value("Game_Id").get_value(juego["Game_Id"])
    
    for datos in count2.iterator():
        if datos["Misc"]=="False":
            cc+=1
    
    return cc/count

def req11(datos, inferior, superior, plataforma):
    lst=datos.get_value("game").get_value("plataformas_req1").get_value(plataforma)
    r=lst.values_range(superior, inferior)
    return r
     
    
# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def date(juego):
    antiguedad=juego["Release_Date"]

    split=antiguedad.split("-")
    if int(split[0]) > 22:
        split[0]="19"+split[0]
    else:
         split[0]="20"+split[0]
    return  "-".join(split)


def cmp_game(obj1:int, obj2:int)->bool:
    if int(obj1) > int(obj2):
        return 1
    else:
        return -1     

def cmp_times(time1:dict, time2:dict):
    if float(time1["Time_0"])>float(time2["Time_0"]):
        return 1
    elif float(time1["Time_0"])<float(time2["Time_0"]):
        return -1
    else:
        if time1["Record_Date_0"]>time2["Record_Date_0"]:
            return 1
        elif time1["Record_Date_0"]<time2["Record_Date_0"]:
            return -1
        else:
            return 0
def cmp_date2(run1, run2)->bool:
    """funcion de comparacion para el arbol basado en las fechas de lanzamiento
    ---------------------------------------------------------------------
    Args:
        data1 = Diccionario con la informacion del juego 1
        data2 = Diccionario con la informacion del juego 2
    ---------------------------------------------------------------------
    Return: 
        1 si la fecha 1 es menor, 0 si es igual y -1 si es mayor
    """


    if ((run1) == (run2)):
        return 0
    elif ((run1) > (run2)):
        return 1
    else:
        return -1
    
def cmp_date(time1, time2)->bool:
    """funcion de comparacion para el arbol basado en las fechas de lanzamiento
    ---------------------------------------------------------------------
    Args:
        data1 = Diccionario con la informacion del juego 1
        data2 = Diccionario con la informacion del juego 2
    ---------------------------------------------------------------------
    Return: 
        1 si la fecha 1 es menor, 0 si es igual y -1 si es mayor
    """

    if (time1["Release_Date"])>(time2["Release_Date"]):
        return 1
    elif (time1["Release_Date"])<(time2["Release_Date"]):
        return -1
    else:
        if time1["Abbreviation"]>time2["Abbreviation"]:
            return 1
        elif time1["Abbreviation"]<time2["Abbreviation"]:
            return -1
        else:
            return 0
def cmpgame(x, y):
    if x["Name"]>y["Name"]:
        return 1
    else:
        return -1



def cmp_runs(run1, run2)->bool:
    """funcion de comparacion para el arbol basado en el numero de runs
    ---------------------------------------------------------------------
    Args:
        data1 = Diccionario con la informacion del juego 1
        data2 = Diccionario con la informacion del juego 2
    ---------------------------------------------------------------------
    Return: 
        1 si run 1 es mayor, 0 si es igual y -1 si es menor
    """

    if (int(run1) == int(run2)):
        return 0
    elif (int(run1) > int(run2)):
        return 1
    else:
        return -1

def cmpf_req5(elem1, elem2):
    if elem1["Record_Date_0"] > elem2["Record_Date_0"]:
        return 1
    elif elem1["Record_Date_0"] < elem2["Record_Date_0"]:
        return 0
    else:
        if elem1["Num_Runs"] > elem2["Num_Runs"]:
            return 1
        elif elem1["Num_Runs"] < elem2["Num_Runs"]:
            return 0
        else:
            if elem1["Name"] > elem2["Name"]:
                return 1
            elif elem1["Name"] < elem2["Name"]:
                return 0

def cmp1(x,y):

    if ((x["Release_Date"]) > (y["Release_Date"]))==True:
        return True
    elif ((x["Release_Date"]) > (y["Release_Date"]))==False:
        return False
    else:
        if ((x["Abbreviation"]) < (y["Abbreviation"]))==True:
            return True
        elif ((x["Abbreviation"]) < (y["Abbreviation"]))==False:
            return False
        else:
            return False
def cmp3(x,y):

    if (float(x) > float(y)):
        return True
    elif (float(x) < float(y)):
        return False
    return 0

def cmp3_1(x, y):
    if (float(x["Time_0"]) > float(y["Time_0"])):
        return True
    elif (float(x["Time_0"]) < float(y["Time_0"])):
        return False
    else:
        if ((x["Record_Date_0"]) > (y["Record_Date_0"])):
            return True
        elif ((x["Record_Date_0"]) < (y["Record_Date_0"])):
            
            return False 
        else:
            if x["Name"] > y["Name"]:
                return True
            else:
                return False
                    
def cmp7(run1, run2):

    if ((run1) == (run2)):
        return 0
    elif ((run1) < (run2)):
        return 1
    else:
        return -1
def cmp77(run1, run2):

    if (float(run1) > float(run2)):
        return 1
    elif (float(run1) < float(run2)):
        return -1
    elif float(run1) == float(run2):
        return 0
# Laura requerimientos: ------------------------------------------------------------------------------------------------------------------------

def cmp_1(elem1, elem2)->bool:

    if elem1["date"] < elem2["date"]:
        return True
    elif elem1["date"] > elem2["date"]:
        return False
    else:
        if elem1["Abbreviation"] < elem2["Abbreviation"]:
            return True
        elif elem1["Abbreviation"] > elem2["Abbreviation"]:
            return False
        else:
            if elem1["Name"] < elem2["Name"]:
                return True
            elif elem1["Name"] > elem2["Name"]:
                return False


def cmpf_req4(elem1, elem2):
    if elem1["Time_0"] > elem2["Time_0"]:
        return 1
    elif elem1["Time_0"] < elem2["Time_0"]:
        return 0
    else:
        if elem1["Num_Runs"] > elem2["Num_Runs"]:
            return 1
        elif elem1["Num_Runs"] < elem2["Num_Runs"]:
            return 0
        else:
            if elem1["Name"] > elem2["Name"]:
                return 1
            elif elem1["Name"] < elem2["Name"]:
                return 0


def cmp6(time1, time2):
    
    if float(time1["Resultado"] < time2["Resultado"]):
        return True
    
    else:
        return False

def requerimiento4(catalogo, inferior, superior):
    times=catalogo.get_value("category").get_value("recors")
    lst = times.values_range(superior,inferior)
    for heaps in lst.iterator():
        heaps.heapsort()
    return lst


def req1(catalogo, inferior, superior, plataforma):
    ayuda=catalogo.get_value("game").get_value("plataformas").get_value(plataforma)
    contador = ayuda.size()
    ayuda=ayuda.values_range({"date":superior},{"date":inferior})
    listica = ayuda

    respuesta = lista("ARRAY_LIST")
    respuesta.insertElement(contador, 0)
    respuesta.insertElement(listica, 1)
    return respuesta

def req6(catalogo, inferior, superior, opcion):
    listica = catalogo.get_value("category").get_value("año")
    fechas = listica.values_range(inferior, superior)

    resultado = lista("ARRAY_LIST")
    

    for listas in fechas.iterator():

        for videojuegos in listas.iterator():

            if opcion == 4:

                tiempos = []
                if videojuegos["Time_0"] != "":
                    tiempos.append(float(videojuegos["Time_0"]))
                if videojuegos["Time_1"] != "":
                    tiempos.append(float(videojuegos["Time_1"]))
                if videojuegos["Time_2"] != "":
                    tiempos.append(float(videojuegos["Time_2"]))

                resultado.add_last({"Resultado":round(sum(tiempos)/len(tiempos),2)})

            if opcion == 1:

                if videojuegos["Time_0"] != "":
                    resultado.add_last({"Resultado": round(float(videojuegos["Time_0"]))})

            if opcion == 2:
                if videojuegos["Time_1"] != "":
                    resultado.add_last({"Resultado": round(float(videojuegos["Time_1"]))})

            if opcion == 3:
                if videojuegos["Time_2"] != "":
                    resultado.add_last({"Resultado": round(float(videojuegos["Time_2"]))})

            if opcion ==5:

                if videojuegos["Num_Runs"] != "":
                    resultado.add_last({"Resultado": int(videojuegos["Num_Runs"])})
    ordenar = resultado.merge_sort(cmp6)
    return ordenar