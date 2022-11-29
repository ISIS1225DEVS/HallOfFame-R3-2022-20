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
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import datetime
import math

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog = { "games":None,
                "register": None,
                }
    catalog['games'] = lt.newList("ARRAY_LIST", compareGame)
    catalog['register'] = lt.newList("ARRAY_LIST", compareReg)
    catalog['dateIndex'] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    catalog['game_id'] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    catalog['release_dates'] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    catalog['players'] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    catalog['regDates'] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    catalog['GameReg'] = mp.newMap(10000,
                                   maptype= "PROBING",
                                   loadfactor= 0.5,
                                   comparefunction=compareIDS)
    catalog['platforms'] = mp.newMap(10000,
                                   maptype= "PROBING",
                                   loadfactor= 0.5,
                                   comparefunction=comparePlat)
    catalog['RegGames'] = mp.newMap(10000,
                                   maptype= "PROBING",
                                   loadfactor= 0.5,
                                   comparefunction=comparePlat)
    catalog['regId'] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    catalog['regRuns'] = om.newMap(omaptype="RBT",
                                      comparefunction=compareDates)
    
    return catalog

# Funciones para agregar informacion al catalogo

def addObservation(catalog,observation,type):
    '''En el catalog[type] se guarda la observación observation.
    type es un str en el siguiente conjunto {"games","register"}, donde:
    games: corresponde a la adición a los juegos
    register: corresponde a la adición a los registros de tiempos'''
    lt.addLast(catalog[type], observation)
    if type == 'games':
        updateDateIndex(catalog['dateIndex'], observation)
        updateGameId(catalog['game_id'], observation)
        updateReleaseDate(catalog['release_dates'], observation)
        addNewPlatform(catalog['platforms'], observation)
    else:
        #print(observation)
        updatePlayers(catalog,catalog['players'], observation)
        updateRegDates(catalog['regDates'], observation)
        addNewGameReg(catalog['GameReg'], observation)
        updateRegRuns(catalog["regRuns"],observation)
        addNewId(catalog['regId'], observation) 
        

    return catalog
def updateRegRuns(map,reg):
    key = reg["Num_Runs"]
    entry = om.get(map,key)
    if entry is None:
        lst=lt.newList()
        lt.addLast(lst,reg)
        om.put(map,key,lst)
    else:
        lst=me.getValue(entry)
        lt.addLast(lst,reg)
        om.put(map,key,lst)
    return map

def updateGameId(map, game):
    id = game['Game_Id']
    entry = om.get(map, id)
    if entry is None:
        om.put(map, id, game)
    return map

def updateDateIndex(map, game):
    formato = "%y-%m-%{}".format("d")
    date = datetime.datetime.strptime(game['Release_Date'],formato)
    entry = om.get(map, date)
    if entry is None:
        datentry = newDateEntry(game)
        om.put(map, date, datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, game)
    #return map

def updateReleaseDate(map, game):
    key = int(game['Release_Date'].split("-")[0])
    if key > 22:
        key += 1900
    else:
        key += 2000
    entry = om.get(map, key)
    if entry is None:
        lst = lt.newList()
        lt.addLast(lst, game['Game_Id'])
        om.put(map, key, lst)
    else:
        lst = me.getValue(entry)
        lt.addLast(lst, game['Game_Id'])
        om.put(map, key, lst)

def updatePlayers(catalog,map, game):
    id = game['Players_0']
    entry = om.get(map, id)
    #print(game['Game_Id'],type(game['Game_Id']))
    #adicionar = {'Game':getRegName(catalog,game)}
    #adicionar = {}
    #for i in ['Game_Id','Category','Subcategory','Num_Runs','Players_0','Country_0','Time_0','Record_Date_0']:
    #    adicionar[i] = game[i]
    if entry is None:
        lst = lt.newList(datastructure="ARRAY_LIST",cmpfunction=Orden_Player)
        adicionar = game
        lt.addLast(lst, adicionar)
        om.put(map, id, lst)
    else:
        lst = me.getValue(entry)
        adicionar = game
        lt.addLast(lst,adicionar)
        om.put(map,id,lst)
    return map

def addDateIndex(datentry, game):
    #lst = datentry['games']
    #lt.addLast(lst, game)
    platformIndex = datentry['platform']
    games = game['Platforms'].split(',')
    for g in games:
        g = g.strip()
        platentry = mp.get(platformIndex, g)
        if platentry is None:
            entry = newPlatformEntry(g, game)
            #lt.addLast(entry["lstgames"], game)
            mp.put(platformIndex, g, entry)
        else:
            entry = me.getValue(platentry)
            lt.addLast(entry['lstgames'], game)
    return datentry

def newDateEntry(game):
    entry = {"games": None, "platform" : None}
    entry['games'] = lt.newList("SINGLE_LINKED", compareDates)
    entry['platform'] = mp.newMap(numelements=30,
                                     maptype="PROBING",
                                     comparefunction=comparePlatform)
    lt.addLast(entry['games'], game)
    return entry

def newPlatformEntry(g, game):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    plentry = {"lstgames": None}
    plentry["lstgames"] = lt.newList("SINGLE_LINKED", comparePlatform)
    lt.addLast(plentry["lstgames"], game)
    return plentry

def addNewId(map, reg):
    key = reg['Game_Id']
    entry = mp.contains(map, key)
    if not entry :
        lst = lt.newList()
        lt.addLast(lst, reg)
        mp.put(map, key, lst)
    else:
        lst = me.getValue(mp.get(map, key))
        lt.addLast(lst, reg)
        mp.put(map, key, lst)
    return map

def addGame(catalog, game):
    lt.addLast(catalog["games"], game)
    return catalog

def addRegister(catalog, register):
    lt.addLast(catalog["register"], register)
    return catalog

def getRegName(catalog, reg):
    games = catalog['game_id']
    game = me.getValue(om.get(games, reg['Game_Id']))
    return game['Name']

#Requerimiento 4
def updateRegDates(map, reg): #carga util para req 4
    formato = "%Y-%m-%dT%H:%M:%S%z"
    if reg['Record_Date_0'] != "":
        key = datetime.datetime.strptime(reg['Record_Date_0'], formato)
        entry = om.get(map, key)
        if entry is None:
            lst = lt.newList()
            lt.addLast(lst, reg)
            om.put(map, key, lst)
        else:
            lst = me.getValue(entry)
            lt.addLast(lst, reg)
            om.put(map, key, lst)
        return map

def getRegisterByRange(catalog, iDate, fDate): #req4
    lugar = catalog['regDates']
    return om.values(lugar, iDate, fDate)

def ordenarReq4(lst): #req4
    lista = lt.newList()
    for i in lt.iterator(lst):
        for element in lt.iterator(i):
            lt.addLast(lista, element)
    lista1 = sa.sort(lista, compareReq4)
    return lista1

def ordenarReg3(catalog,lst): 
    lista = lt.newList()
    for i in lt.iterator(lst):
        for reg in lt.iterator(i):
            name = getRegName(catalog,reg)
            reg["name"] = name
            lt.addLast(lista,reg)
        #sa.sort(i,compareReg3)
    sa.sort(lista,compareReg3)
    return lista

#Requerimiento 7
def addNewPlatform(map, game): #carga de datos - estructura para req7
    
    platforms = [i.strip() for i in game['Platforms'].split(",")] 
    for plat in platforms:
        if not mp.contains(map, plat):
            lst = lt.newList()
            lt.addLast(lst, game)
            mp.put(map, plat, lst)
        else:
            lst = me.getValue(mp.get(map, plat))
            lt.addLast(lst, game)
            mp.put(map, plat, lst)


def addNewGameReg(map, reg): #CARGA USADA PARA req7
    
    key = int(reg['Game_Id'])
    #entry = mp.contains(map, key)
    if not mp.contains(map, key):
        lst = lt.newList()
        lt.addLast(lst, reg)
        mp.put(map, key, lst)
    else:
        #entry = mp.get(map, key)
        lst = me.getValue(mp.get(map, key))
        lt.addLast(lst, reg)
        mp.put(map, key, lst)
    return map 


def getIdByPlatform(map, platform): #devuelve la lista de Games para un plataforma - req7
    #print(mp.keySet(map))
    return me.getValue(mp.get(map, platform)) 

def getRegsByPlatform(map, lst): #guarda en una tabla de hash cuantos registros hay por juego, tomando como llave el Id del juego y además devuelve el número de registros total para la plataforma
    regtotal = 0                    #req7 map es GameReg
    mapareg = mp.newMap(10000,
                        maptype= "PROBING",
                        loadfactor= 0.5,
                        comparefunction=compareIDS)
    for game in lt.iterator(lst):
        size = 0
        id = int(game['Game_Id'])

        reg = mp.get(map, id)
        if reg:
            reg= me.getValue(reg)
            size = lt.size(reg)
        regtotal += size
        mp.put(mapareg, id, size)
    return mapareg, regtotal

def calculosreq7(lst, catalog, datos, platform): #lst es la lista de juegos, map es GameReg, datos es regs,
    map = catalog['GameReg']
    antiquity(lst)
    popularity(lst)
    time_avg(lst, map)
    revenue(lst)
    marketshare(catalog, datos, platform)
    streamrevenue(catalog, platform)


def antiquity(lst): #req7
    for game in lt.iterator(lst):
        key = int(game['Release_Date'].split("-")[0])
        if key > 22:
            key += 1900
        else:
            key += 2000
        if key >= 2018:
            key = key -2017
        elif key > 1998 and key < 2018:
            key = (-1/5)*key + 404.6
        else:
            key = 5
        key = round(key, 2)
        game['antiquity'] = key

def popularity(lst): #req7
    for game in lt.iterator(lst):
        popularity = int(game['Total_Runs'])
        popularity = math.log(popularity)
        popularity = round(popularity, 2)
        game['popularity'] = popularity

def time_avg(lst, map): #req7
    for game in lt.iterator(lst):
        id = int(game['Game_Id'])
        lista2 = me.getValue(mp.get(map, id))
        sumat = 0
        contador = 0
        for reg in lt.iterator(lista2):
            count = 1
            suma = float(reg['Time_0'])

            if reg['Time_1'] != None and reg['Time_1'] != "" :
                time_1 = float(reg['Time_1'])
                suma += time_1
                count += 1
            if reg['Time_2'] != None and reg['Time_2'] != "":
                time_2 = float(reg['Time_2'])
                suma += time_2
                count += 1
            mean = suma/count
            sumat += mean
            contador += 1
        avg = sumat/contador
        avg = round(avg, 2)
        game['time_average'] = avg


def revenue(lst): #req7
    for game in lt.iterator(lst):
        revenue = (float(game['popularity'])* float(game['time_average']))/ float(game['antiquity'])
        revenue = round(revenue, 2)
        game['revenue'] = revenue

def marketshare(catalog, datos, platform): #req7
    mapareg = datos[0]
    regtotal = datos[1]
    plataforma = me.getValue(mp.get(catalog['platforms'], platform))
    for game in lt.iterator(plataforma):
        #print(game)
        gt = me.getValue(mp.get(mapareg, int(game['Game_Id'])))
        
        mshare = float(gt)/regtotal
        mshare = round(mshare, 2)
        game['marketshare'] = mshare

def streamrevenue(catalog, platform): #req7
    plataforma = me.getValue(mp.get(catalog['platforms'], platform))
    for game in lt.iterator(plataforma):
        revenue = float(game['revenue'])
        mshare = float(game['marketshare'])
        streamrev = revenue * mshare
        streamrev = round(streamrev, 2)
        game['streamrevenue'] = streamrev

def ordenarReq7(lst):
    return sa.sort(lst, compareReq7)

# Funciones para creacion de datos

def getRequerimiento6(catalog, iDate, fDate): #req6
    lstId = getIdByRange(catalog, int(iDate), int(fDate))
    nueva = lt.newList()
    for lst in lt.iterator(lstId):
        for id in lt.iterator(lst):
            valor = me.getValue(mp.get(catalog['regId'], id)) 
            for reg in lt.iterator(valor):
                lt.addLast(nueva, reg)
    contador = 1
    for i in lt.iterator(nueva):
        promedio = float(i["Time_0"])
        if i["Time_1"] != "":
            contador += 1
            promedio += float(i["Time_1"])
        if i["Time_2"] != "":
            contador += 1
            promedio += float(i["Time_2"])
        fpromedio = float(promedio)/float(contador)
        i["Promedio"]=fpromedio
        
        #contador2= 0 
        #if i["Num_Runs"]>=0:
        #    contador2 +=1
        #i["Intentos"]=contador2
    return nueva 

def ordenarReq6Time_0(lst):
    return sa.sort(lst, compareTime)

def ordenarReq6Prom(lst):
    return sa.sort(lst, compareAvg)

def ordenarReq6Num(lst):
    return sa.sort(lst, compareNum)

# Funciones de consulta

def cons_catalog_findSize(catalog,identifier):
    return lt.size(catalog[identifier])

def getGamesByRange(catalog, initialDate, finalDate, platform):
    llaves = om.keys(catalog['dateIndex'], initialDate, finalDate)
    lst = lt.newList('ARRAY_LIST')

    for llave in lt.iterator(llaves):
        valor = (me.getValue(om.get(catalog['dateIndex'], llave)))['platform']
        #print('v',valor)
        juegos = mp.get(valor, platform)
        #print("j",juegos)
        if juegos:
            game = me.getValue(juegos)['lstgames']
            #game = lt.getElement(game, 1)
            lt.addLast(lst, game)
    return lst

def getIdByRange(catalog, iDate, fDate):
    lugar = catalog['release_dates']
    return om.values(lugar, iDate, fDate)

def indexHeight(catalog):
    return om.height(catalog["dateIndex"])

def indexSize(catalog):
    return om.size(catalog["dateIndex"])

def minKey(catalog):
    return om.minKey(catalog["dateIndex"])

def maxKey(catalog):
    return om.maxKey(catalog["dateIndex"])

def req2(catalog,player):
    info = om.get(catalog['players'],player)
    if info is None:
        print('\nEl jugador NO tiene registros\n')
        return None
    else:
        listado = me.getValue(info)
        listado = sa.sort(listado,Orden_Player)
        to_show = list(lt.iterator(listado))
        for i in to_show:
            i['Name'] = getRegName(catalog,i)
        return to_show

def req5(catalog,l_inf,l_sup):
    listado = catalog['register']
    lista = lt.newList()
    for i in lt.iterator(listado):
        if float(i['Time_0'])>=l_inf:
            if float(i['Time_0'])<=l_sup:
                i['Name'] = getRegName(catalog,i)
                lt.addLast(lista,i)
    lista = sa.sort(lista,Orden_Player)
    lista = list(lt.iterator(lista))
    #print(lista)
    return lista

def req8(catalog,anio,l_inf,l_sup):
    listado = catalog['register']
    lista = lt.newList()
    for i in lt.iterator(listado):
        if float(i['Time_0'])>=l_inf:
            if float(i['Time_0'])<=l_sup:
                f_inf = int(anio)
                if i['Record_Date_0']!='':
                    rev_fecha = convertidor_fechas(i['Record_Date_0'],True)
                    #print(f_inf,rev_fecha.year)
                    #rev_fecha = datetime.datetime.strptime(i['Record_Date_0'],"%Y-%m-%d%XZ")
                    if f_inf==(rev_fecha.year):
                        i['Name'] = getRegName(catalog,i)
                        lt.addLast(lista,i)
    lista = sa.sort(lista,Orden_Player)
    lista = list(lt.iterator(lista))
    print(lista)
    return lista

def getRunsbyRange(catalog,iRuns,fRuns):
    lugar = catalog["regRuns"]
    return om.values(lugar,iRuns,fRuns)



# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def compareReg(reg1, reg2):
    if (reg1 == reg2):
        return 0
    elif reg1 > reg2:
        return 1
    else:
        return -1

def compareGame(game1, game2):
    if (game1 == game2):
        return 0
    elif game1 > game2:
        return 1
    else:
        return -1

def compareDates(date1, date2):
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def comparePlatform(plat1, plat2):
    """
    Compara dos tipos de crimenes
    """
    platform = me.getKey(plat2)
    if (plat1 == platform):
        return 0
    elif (plat1 > platform):
        return 1
    else:
        return -1

def Orden_Player(game1,game2):
    T1 = float(game1['Time_0'])
    T2 = float(game2['Time_0'])
    if (T1>T2) or (T1<T2):
        return T1<T2
    else:
        RD1 = game1['Record_Date_0'].replace('T',' ').replace('Z','')
        RD2 = game2['Record_Date_0'].replace('T',' ').replace('Z','')
        if (RD1=='') or (RD2==''):
            if (RD1!=''):
                return True
            elif (RD2!=''):
                return False
            else:
                return True
        else:
            RD1 = datetime.datetime.strptime(RD1,"%Y-%m-%{} %H:%M:%S".format('d')) 
            RD2 = datetime.datetime.strptime(RD2,"%Y-%m-%{} %H:%M:%S".format('d'))
            if RD1 != RD2:
                return RD1<RD2
            else:
                N1 = game1['Name']
                N2 = game2['Name']
                return N1<=N2

def convertidor_fechas(fecha,mode):
    if mode:
        #print(fecha,type(fecha))
        #date = str((fecha.split('T'))[0]).replace(' ','')
        date = (fecha).replace('T',' ').replace('Z','')
        #print(date,type(date))
        date = datetime.datetime.strptime(date,"%Y-%m-%{} %H:%M:%S".format('d'))
        #print(date,type(date))
        return date
    else:
        date = datetime.datetime.strptime('{}-01-01'.format(fecha),"%Y-%m-%{}".format('d'))
        return date

def compareReq4(reg1, reg2):
    formato = "%Y-%m-%dT%H:%M:%S%z"
    key1 = datetime.datetime.strptime(reg1['Record_Date_0'], formato)
    key2 = datetime.datetime.strptime(reg2['Record_Date_0'], formato)
    if key1 < key2:
        return key1 < key2
    elif key1 == key2:
        return float(reg1['Time_0']) > float(reg2['Time_0'])
    elif float(reg1['Time_0']) == float(reg2['Time_0']):
        return reg1['Num_Runs'] > reg2['Num_Runs']

def compareReq7(g1, g2):
    if g1['streamrevenue'] > g2['streamrevenue']:
        return g1['streamrevenue'] > g2['streamrevenue']

def compareIDS(id, id1):
    identry = me.getKey(id1)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def comparePlat(nombreactor, actor):
    '''O(1)'''
    authentry = me.getKey(actor) 
    if nombreactor == authentry:
        return 0 
    elif nombreactor > authentry:
        return 1
    else:
        return -1

def compareTime(reg1, reg2):
    if reg1['Time_0'] < reg2['Time_0']:
        return reg1['Time_0'] < reg2['Time_0']
    elif reg1['Time_0'] == reg2['Time_0']:
        return reg1['Time_1'] < reg2['Time_1']
    elif reg1['Time_1'] == reg2['Time_1']:
        return reg1['Time_2'] < reg2['Time_2']

def compareAvg(reg1, reg2):
    if reg1['Promedio'] < reg2['Promedio']:
        return reg1['Promedio'] < reg2['Promedio']

def compareNum(reg1, reg2):
    if reg1['Num_Runs'] < reg2['Num_Runs']:
        return reg1['Num_Runs'] < reg2['Num_Runs']

def compareReg3(reg1,reg2):
    if reg1["Num_Runs"] < reg2["Num_Runs"]:
        return reg1["Num_Runs"] < reg2["Num_Runs"]
    elif reg1["Num_Runs"] == reg2["Num_Runs"]:
        return float(reg1["Time_0"]) > float(reg2["Time_0"])
    elif float(reg1["Time_0"]) == float(reg2["Time_0"]):
        return reg1["Record_Date_0"] > reg2["Record_Date_0"]
    elif reg1["Record_Date_0"] == reg2["Record_Date_0"]:
        return reg1["name"] > reg2["name"] 
