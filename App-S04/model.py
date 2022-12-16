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
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import quicksort as qui
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Trees import traversal as tr
import datetime
import time
import math 
from geopy.geocoders import Nominatim
import folium
from folium.plugins import MarkerCluster

assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    analyzer = {"games": None,
                "category": None,
                }

    analyzer["games"] = lt.newList("SINGLE_LINKED")
    analyzer["category"] = lt.newList("SINGLE_LINKED")
    analyzer["gamesByPlatform"] = om.newMap(omaptype="RBT")
    analyzer["gamesbyDate"] = om.newMap(omaptype="RBT")
    analyzer["gamesbyPlayer"] = om.newMap(omaptype="RBT")
    analyzer["gamesbyTime"] = om.newMap(omaptype="RBT")
    analyzer['gamesByRelease_Date'] = om.newMap(omaptype="RBT")
    analyzer["gamesbyReleaseYear"]=om.newMap(omaptype="RBT")
    analyzer["gamesbyId"]=om.newMap(omaptype="RBT")

    
    return analyzer

# Funciones para agregar informacion al catalogo

def addGame(catalog, gamesfile):
    catalog["games"] = lt.newList(datastructure="ARRAY_LIST",
                                  filename=gamesfile)
    return catalog

def addCategory(catalog, categoryfile):
    catalog["category"] = lt.newList(datastructure="ARRAY_LIST",
                                  filename=categoryfile)
    return catalog


def addGamestotal(catalog):
    for i in range(0, len(catalog[0]['games']['elements'])): 
        addGamesByPlatfom(catalog, catalog[0]['games']['elements'][i])
        addGamesByRelease_Date(catalog, catalog[0]['games']['elements'][i])
        addGameByReleaseDate(catalog, catalog[0]["games"]["elements"][i])
    return catalog
        
        
def addCategorytotal(catalog):
    for i in range(0, len(catalog[1]['games']['elements'])):
        addRecordsByDate(catalog, catalog[1]['games']['elements'][i])
        addRecordsByPlayer(catalog, catalog[1]['games']['elements'][i])
        addRecordsByTime(catalog, catalog[1]['games']['elements'][i])
    return catalog


def addGamesByPlatfom(catalog, game):

    map = catalog[0]['gamesByPlatform']
    plataforma = game["Platforms"].split(', ')
    for pos in plataforma:
        entry = om.get(map, pos)    
        if entry is None:
            platform_search = lt.newList(datastructure = "ARRAY_LIST")
            om.put(map, pos, platform_search)
        else:
            platform_search = me.getValue(entry)
        lt.addLast(platform_search, game)
    return catalog

def addRecordsByDate(catalog, category):

    map = catalog[0]['gamesbyDate']
    date = category['Record_Date_0']
    entry = om.get(map, date)    
    if entry is None:
        date_search = lt.newList(datastructure = "ARRAY_LIST")
        om.put(map, date, date_search)
    else:
        date_search = me.getValue(entry)
    lt.addLast(date_search, category)

    return catalog

def addRecordsByPlayer(catalog, category):
    map = catalog[0]['gamesbyPlayer']
    player = category['Players_0']
    entry = om.get(map, player)    
    if entry is None:
        player_search = lt.newList(datastructure = "ARRAY_LIST")
        om.put(map, player, player_search)
    else:
        player_search = me.getValue(entry)
    lt.addLast(player_search, category)

    return catalog


def addRecordsByTime(catalog, category):

    map = catalog[0]['gamesbyTime']
    time = category['Time_0']
    entry = om.get(map, time)    
    if entry is None:
        time_search = lt.newList(datastructure = "ARRAY_LIST")
        om.put(map, time, time_search)
    else:
        time_search = me.getValue(entry)
    lt.addLast(time_search, category)

    return catalog

def addGamesByRelease_Date(catalog, game):
    map = catalog[0]['gamesByRelease_Date']
    date = game['Release_Date']
    entry = om.get(map, date)    
    if entry is None:
        date_search = lt.newList(datastructure = "ARRAY_LIST")
        om.put(map, date, date_search)
    else:
        date_search = me.getValue(entry)
    lt.addLast(date_search, game)

    return catalog

def addGameByReleaseDate(catalog, game):
    mapa=catalog[0]["gamesbyReleaseYear"]
    game1=game["Release_Date"]
    for i in range(0, len(catalog[0]["games"]["elements"])):
        date=(str(game1)+"-"+str(i))
    entry=om.get(mapa, date)
    if entry is None:
        date_search=lt.newList(datastructure="ARRAY_LIST")
        om.put(mapa, date, date_search)
    else: 
        date_search=me.getValue(entry)
    lt.addLast(date_search, game)
    return catalog


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

# Funciones para creacion de datos

# Funciones de consulta

#REQUERIMIENTO 1

def gamesByPlarformAndDate(catalog, platform, date1, date2):
    map = catalog[0]['gamesByPlatform']
    listafinal = lt.newList(datastructure='ARRAY_LIST')
    listabuscar = om.get(map, platform)
    totalplataforma = len(listabuscar['value']['elements'])
    for i in range(0, len(listabuscar['value']['elements'])):
        elemento = listabuscar['value']['elements'][i]['Release_Date']
        year = int(elemento[0:2])
        if year > 22: 
            year = int("19"+str(year))
        else: 
            if len(str(year)) == 1:
                year = ("0"+str(year))
                year = int("20"+str(year))
            else:
                year = int("20"+str(year))
        if int(year) >= int(date1[0:4]) and int(year) <= int(date2[0:4]):
            if int(elemento[3:5]) >= int(date1[5:7]) and int(elemento[3:5]) <= int(date2[5:7]):
                if int(elemento[6:8]) >= int(date1[8:10]) and int(elemento[6:8]) <= int(date2[8:10]):
                    lt.addLast(listafinal, listabuscar['value']['elements'][i])

    sortShellBig(listafinal)
    
    return listafinal, totalplataforma

#REQUERIMIENTO 2


def gamesbyPlayer(catalog, player):
    map = catalog[0]['gamesbyPlayer']
    listabuscar = om.get(map, player)
    listafinal = listabuscar['value']
    sortShellDates(listafinal)


    listagames = catalog[0]['games']

    for i in range(0, len(listafinal['elements'])):
        gameid = listafinal['elements'][i]['Game_Id']
        for j in range(0, len(listagames['elements'])):
            juegoid = listagames['elements'][j]['Game_Id']
            if gameid == juegoid:
                listafinal['elements'][i]['Name'] = listagames['elements'][j]['Name']
    
    return listafinal
    
#REQUERIMIENTO 3

def RegistersbyTimeandTrials(catalog, trial_inferior, trial_superior):
    inicial= getTime()
    map = catalog[0]['gamesbyTime']
    lt_final = lt.newList(datastructure='ARRAY_LIST')
    listausar = tr.inorder(map)
    for i in range(0, len(listausar['elements'])):
        for j in range(0, len(listausar['elements'][i]['elements'])):
            elemento = listausar['elements'][i]['elements'][j]['Num_Runs']
            if int(elemento) > int(trial_inferior) and int(elemento) < int(trial_superior):
                lt.addLast(lt_final, listausar['elements'][i]['elements'][j])

    sortShellDates(lt_final)
    final=getTime()
    dif = deltaTime(final,inicial)

    return lt_final, dif

#REQUERIMIENTO 4

def dateCategory(catalog, start, end):
    inicial=getTime()
    mapa=catalog[0]["gamesbyDate"]
    listacompleta=lt.newList(datastructure="ARRAY_LIST")
    listaordenada=tr.inorder(mapa)
    for i in range(0, len(listaordenada["elements"])):
       elemento=listaordenada["elements"][i]
       if(str(elemento["elements"][0]["Record_Date_0"])>=str(start) and str(elemento["elements"][0]["Record_Date_0"])<=str(end)):
            lt.addLast(listacompleta, elemento["elements"][0])
    sortShellDates(listacompleta)
    final=getTime()
    dif=deltaTime(final, inicial)
    return listacompleta, dif

#REQUERIMIENTO 5

def RegistersByTimeandDate(catalog, time1, time2):
    map = catalog[0]['gamesbyDate']
    listafinal = lt.newList(datastructure='ARRAY_LIST')
    listausar = tr.inorder(map)
    for i in range(0, len(listausar['elements'])):
        for j in range(0, len(listausar['elements'][i]['elements'])):
            elemento = listausar['elements'][i]['elements'][j]['Time_0']
            if float(elemento) > float(time1) and float(elemento) < float(time2):
                lt.addLast(listafinal, listausar['elements'][i]['elements'][j])

    sortShellDates(listafinal)

    listagames = catalog[0]['games']

    for i in range(0, len(listafinal['elements'])):
        gameid = listafinal['elements'][i]['Game_Id']
        for j in range(0, len(listagames['elements'])):
            juegoid = listagames['elements'][j]['Game_Id']
            if gameid == juegoid:
                listafinal['elements'][i]['Name'] = listagames['elements'][j]['Name']


    return listafinal

#REQUERIMIENTO 6

def rangeofYears(catalog, year1, year2, segmentos, niveles, consulta):
    inicial=getTime()
    mapa=catalog[0]["gamesbyReleaseYear"]
    listacompleta=lt.newList(datastructure="ARRAY_LIST")
    listaordenada=tr.inorder(mapa)
    for i in range(0, len(listaordenada["elements"])):
        elemento=listaordenada["elements"][i]
        if str(elemento["elements"][0]["Release_Date"][:2])>=year1 and str(elemento["elements"][0]["Release_Date"][:2])<=year2:
            lt.addLast(listacompleta, elemento["elements"][0])

    #Tiempo 0, Tiempo 1, Tiempo 2
    if consulta==str(1):
        lista_tiempos012=lt.newList(datastructure="ARRAY_LIST")
        lista=catalog[1]["games"]["elements"]
        for i in range(0, len(listacompleta["elements"])):
            idgame_listacompleta=listacompleta["elements"][i]["Game_Id"]
            for j in range(0, len(catalog[1]["games"]["elements"])):
                idgame_lista=lista[j]["Game_Id"]
                if idgame_listacompleta==idgame_lista:
                    if lista[j]["Time_0"] != "":
                        lt.addLast(lista_tiempos012, float(lista[j]["Time_0"]))
                    if lista[j]["Time_1"] != "":
                        lt.addLast(lista_tiempos012, float(lista[j]["Time_1"]))
                    if lista[j]["Time_2"] != "":
                        lt.addLast(lista_tiempos012, float(lista[j]["Time_2"]))
        sortCmpmenoramayor_tiempo(lista_tiempos012)
        
        Histograma(lista_tiempos012["elements"], segmentos, niveles)

    #Tiempo promedio 
    if consulta==str(2): 
        lista_tiempospromedios=lt.newList(datastructure="ARRAY_LIST")
        lista=catalog[1]["games"]["elements"]
        for i in range(0, len(listacompleta["elements"])):
            idgame_listacompleta=listacompleta["elements"][i]["Game_Id"]
            for j in range(0, len(catalog[1]["games"]["elements"])):
                idgame_lista=lista[j]["Game_Id"]
                count=0
                tiempo_promedio=0
                if idgame_listacompleta==idgame_lista:
                    if lista[j]["Time_0"] != "" :
                        tiempo_promedio=tiempo_promedio+float(lista[j]["Time_0"])
                        count=count+1
                    if lista[j]["Time_1"] != "":
                        tiempo_promedio=tiempo_promedio+float(lista[j]["Time_1"])
                        count=count+1
                    if lista[j]["Time_2"] != "":
                        tiempo_promedio=tiempo_promedio+float(lista[j]["Time_2"])
                        count=count+1
                    tiempofinal=tiempo_promedio/count
                    lt.addLast(lista_tiempospromedios, tiempofinal)
        sortCmpmenoramayor_tiempo(lista_tiempospromedios)  
        
        Histograma(lista_tiempospromedios["elements"], segmentos, niveles)

        


    #Numero de intentos 
    if consulta==str(3):
        lista_numerointentos=lt.newList(datastructure="ARRAY_LIST")
        lista=catalog[1]["games"]["elements"]
        for i in range(0, len(listacompleta["elements"])):
            idgame_listacompleta=listacompleta["elements"][i]["Game_Id"]
            for j in range(0, len(catalog[1]["games"]["elements"])):
                idgame_lista=lista[j]["Game_Id"]
                if idgame_listacompleta==idgame_lista:
                    if lista[j]["Num_Runs"] != "" :
                        lt.addLast(lista_numerointentos, lista[j]["Num_Runs"])
        sortCmpmenoramayor_intentos(lista_numerointentos)
       
        Histograma(lista_numerointentos["elements"], segmentos, niveles)

    final=getTime()
    dif=deltaTime(final, inicial)
    return dif

def Histograma(lista, segmentos, niveles):
    lista_niveles=lt.newList(datastructure="ARRAY_LIST")
    lista_segmentos=lt.newList(datastructure="ARRAY_LIST")
    valor_menor=lista[0]
    lista_len=len(lista)
    valor_mayor=lista[int(lista_len-1)]
    diferencia=float(valor_mayor)-float(valor_menor)
    segmentos_def=float(diferencia)/float(segmentos)
    segmentos_def=round(segmentos_def, 3)
    primervalor=valor_menor

    
    for i in range(0, int(segmentos)):
        segundovalor=float(primervalor)+float(segmentos_def)
        segundovalor=round(segundovalor, 1)
        lt.addLast(lista_segmentos, primervalor)
        contador=0

        for j in range(0, len(lista)):
            if float(lista[j])>=float(primervalor) and float(lista[j])<=float(segundovalor):
                contador=contador+1
        lt.addLast(lista_niveles, contador)
        primervalor=segundovalor

    lt.addLast(lista_segmentos, segundovalor)
    lista_marcas=lt.newList(datastructure="ARRAY_LIST")
    for n in range(0, len(lista_niveles["elements"])):
        cantidad=float(lista_niveles["elements"][n])/float(niveles)
        if cantidad==0.5:
            cantidad_def=1
        else: 
            cantidad_def=round(cantidad)
        lt.addLast(lista_marcas, cantidad_def)
    print("El numero de valores: "+ str(len(lista)))
    print("El valor menor: "+ str(valor_menor))
    print("El valor mayor: "+ str(valor_mayor))
    print("bin                     |count     |lvl   |mark        ")
    print("-------------------------------------------------------")
     

    for m in range(0, int(segmentos)): 
        if (len(str(lista_segmentos["elements"][m]))+len(str(lista_segmentos["elements"][m+1])))<40: 
            largo=40-(len(str(lista_segmentos["elements"][m]))+len(str(lista_segmentos["elements"][m+1]))) 
            print("("+ str(round(lista_segmentos["elements"][m], 1))+ ", "+ str(round(lista_segmentos["elements"][m+1], 1))+"] "+ (" "*largo)+  str(lista_niveles["elements"][m])+"      |"+ str(lista_marcas["elements"][m]) + "       |"  + str("*"*lista_marcas["elements"][m])) 

        else: 
            largo=1 
            print("("+ str(round(lista_segmentos["elements"][m], 1))+ ", "+ str(round(lista_segmentos["elements"][m+1], 1))+"] "+ (" "*largo)+  str(lista_niveles["elements"][m])+"      |"+ str(lista_marcas["elements"][m]) + "       |"  + str("*"*lista_marcas["elements"][m])) 

    return lista_niveles

#REQUERIMIENTO 7
    
def rentability(catalog, platform, n):
    map = catalog[0]['gamesByPlatform']
    listafinal = lt.newList(datastructure='ARRAY_LIST')
    listabuscar = om.get(map, platform)
    contadorbig = 0
    for i in range(0, len(listabuscar['value']['elements'])):
        year = int(listabuscar['value']['elements'][i]["Release_Date"][0:2])
        if year > 22: 
            year = int("19"+str(year))
        else: 
            if len(str(year)) == 1:
                year = ("0"+str(year))
                year = int("20"+str(year))
                
            else:
                year = int("20"+str(year))
    #ANTIGUEDAD
        if year >= 2018:
            antiquity = year - 2017
        elif year < 2018 and year > 1998: 
            antiquity = ((-1/5)*year) + 404.6
        elif year < 1998:
            antiquity = 5
    #POPULARIDAD
        runs = int(listabuscar['value']['elements'][i]["Total_Runs"])
        popularity = math.log(runs)
        
    #TIEMPOS
        idjuego = listabuscar['value']['elements'][i]["Game_Id"]
        listacatalogo = catalog[1]['games']['elements']
        sumatiempos = lt.newList(datastructure="ARRAY_LIST")
        for j in range(0, len(catalog[1]['games']['elements'])):
            gameid = listacatalogo[j]["Game_Id"]
            if idjuego == gameid: 
                if listacatalogo[j]["Time_0"] != '':
                    lt.addLast(sumatiempos, float(listacatalogo[j]["Time_0"]))
                    
                if listacatalogo[j]["Time_1"] != '':
                    lt.addLast(sumatiempos, float(listacatalogo[j]["Time_1"]))
                if listacatalogo[j]["Time_2"] != '':
                    lt.addLast(sumatiempos, float(listacatalogo[j]["Time_2"]))
                sumafinal = 0
                for k in range(0, len(sumatiempos['elements'])):
                    sumafinal = sumafinal + sumatiempos['elements'][k]
                average = sumafinal/len(sumatiempos['elements'])
            
    
    #REVENUE 
        revenue = round((popularity*average)/antiquity, 2)
        listabuscar['value']['elements'][i]["Revenue"]=revenue

    #MARKETSHARE
        gameid = listabuscar['value']['elements'][i]['Game_Id']
        
        for j in range(0, len(listacatalogo)):
            idjuego = listacatalogo[j]["Game_Id"]
            if idjuego == gameid:
                contadorbig = contadorbig + 1
    for i in range(0, len(listabuscar['value']['elements'])): 
        listacatalogo = catalog[1]['games']['elements']
        gameid = listabuscar['value']['elements'][i]['Game_Id'] 
        contadorsingle = 0
        for k in range(0, len(listacatalogo)):
            idjuego = listacatalogo[k]["Game_Id"]
            if idjuego == gameid:
                contadorsingle = contadorsingle + 1
        marketshare = round(contadorsingle/contadorbig,2)
        listabuscar['value']['elements'][i]["MarketShare"]=marketshare

    for i in range(0, len(listabuscar['value']['elements'])):
        revenue = listabuscar['value']['elements'][i]["Revenue"]
        marketshare = listabuscar['value']['elements'][i]['MarketShare']
        streamrevenue = revenue * marketshare
        listabuscar['value']['elements'][i]["StreamRevenue"]=round(streamrevenue,2)

    listafinal = listabuscar['value']

    sortQuickRentability(listafinal)


    listaend = lt.newList(datastructure='ARRAY_LIST')

    for i in range(0,int(n)):
        lt.addLast(listaend, listabuscar['value']['elements'][i])
    
    return listaend


#REQUERIMIENTO 8
def RegistersByTimeandYear(catalog, year, time1, time2):
    inicial= getTime()
    map = catalog[0]['gamesbyTime']
    map2 = catalog[0]['gamesByRelease_Date']
    lista_gameid = lt.newList(datastructure='ARRAY_LIST')

    listabuscar = tr.inorder(map2)
    listausar = tr.inorder(map)
    lista_paises = lt.newList(datastructure='ARRAY_LIST')
    m = folium.Map(location=[44, -73], zoom_start=2)
    marker_cluster = MarkerCluster().add_to(m)

    for i in range(0, len(listabuscar['elements'])):
        year_evaluar = int(listabuscar['elements'][i]['elements'][0]['Release_Date'][0:2])
        if year_evaluar > 22: 
            year_evaluar = int("19"+str(year_evaluar))
        else: 
            if len(str(year_evaluar)) == 1:
                year_evaluar = ("0"+str(year_evaluar))
                year_evaluar = int("20"+str(year_evaluar))
                
            else:
                year_evaluar = int("20"+str(year_evaluar))

        if int(year_evaluar) == int(year):
            lt.addLast(lista_gameid, listabuscar['elements'][i]['elements'][0]["Game_Id"])
    contador = 0
    for y in range(0, len(lista_gameid['elements'])):
        for i in range(0, len(listausar['elements'])):
            for j in range(0, len(listausar['elements'][i]['elements'])):
                tiempoaevaluar = listausar['elements'][i]['elements'][j]['Time_0']
                nuevo_id = listausar['elements'][i]['elements'][j]['Game_Id']
                if int(lista_gameid['elements'][y]) == int(nuevo_id) and float(tiempoaevaluar) > float(time1) and float(tiempoaevaluar) < float(time2):
                    contador+=1
                    lt.addLast(lista_paises, listausar['elements'][i]['elements'][j]['Country_0'])
    
    geolocator = Nominatim(user_agent="location script")
    for city in lista_paises['elements']:
        city=city.split(",")
        if str(city[0]) == str('U.S. Minor Outlying Islands'):
            coordinate_long = -159.55
            coordinate_lat = -0.374
            folium.Marker(location=[coordinate_long,coordinate_lat], popup="Ubicación de juego",icon=folium.Icon(color="green", icon="ok-sign"),).add_to(marker_cluster)
            m.save("mapa.html")
        else:
            location = geolocator.geocode(city[0])
            coordinate = (location.longitude,location.latitude)
            coordinate_long = coordinate[1]
            coordinate_lat = coordinate[0]
            folium.Marker(location=[coordinate_long,coordinate_lat], popup="Ubicación de juego",icon=folium.Icon(color="green", icon="ok-sign"),).add_to(marker_cluster)
            m.save("mapa.html")
    print("    ")
    
    print(" El número total de registros de speedrun en dicho año y rango es de: "+ str(contador))

    final=getTime()
    dif = deltaTime(final,inicial)

    return "--- Ya puede visualizar el mapa, este se encuentra como un archivo html ---", dif

# Funciones utilizadas para comparar elementos dentro de una lista

def cmpDates(record1, record2):
    if float(record1["Time_0"]) != float(record2["Time_0"]):
        if float(record1["Time_0"]) < float(record2["Time_0"]):
            return True
    elif record1["Num_Runs" ] != record2["Num_Runs"]:
        if record1["Num_Runs"] < record2["Num_Runs"]:
            return True

def cmpGamesBig(record1, record2):
    if record1["Release_Date"] != record2["Release_Date"]:
        if record1["Release_Date"] < record2["Release_Date"]:
            return True
    elif record1["Abbreviation"] != record2["Abbreviation"]:
        if record1["Abbreviation"] < record2["Abbreviation"]:
            return True
    elif record1["Name"] != record2["Name"]:
        if record1["Name"] < record2["Name"]:
            return True    

def cmpGamesbyRentability(record1, record2):
        if float(record1["StreamRevenue"]) != float(record2["StreamRevenue"]):
            if float(record1["StreamRevenue"]) > float(record2["StreamRevenue"]):
                return True

def Cmpmenoramayor_tiempo(tiempo1, tiempo2):
    if tiempo1 != tiempo2:
        if tiempo1<tiempo2:
            return True
def Cmpmenoramayor_intentos(intento1, intento2):
    if intento1!=intento2:
        if intento1<intento2:
            return True

def CmpRecordDate(RecordDate1, RecordDate2):
    if RecordDate1["Record_Date_0"] != RecordDate2["Record_Date_0"]:
        if RecordDate1["Record_Date_0"] > RecordDate2["Record_Date_0"]:
            return True

# Funciones de ordenamiento
def sortShellDates(lista):
    sort = sa.sort(lista, cmpDates)
    return sort

def sortShellBig(lista):
    sort = sa.sort(lista, cmpGamesBig)
    return sort

def sortQuickRentability(lista):
    sort=qui.sort(lista, cmpGamesbyRentability)
    return sort

def sortCmpmenoramayor_tiempo(lista):
    sort=qui.sort(lista, Cmpmenoramayor_tiempo)
    return sort
def sortCmpmenoramayor_intentos(lista):
    sort=qui.sort(lista, Cmpmenoramayor_intentos)
    return sort
def sortCmpRecordDate(lista):
    sort=qui.sort(lista, CmpRecordDate)
