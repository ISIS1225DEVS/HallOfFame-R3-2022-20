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
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mer
from datetime import datetime
import math
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    analyzer = {"games": None,
                "categories": None,
                "video_games": None,
                "platforms": None,
                "players_0": None,
                "games_map": None,
                "records": None,
                "time_0": None,
                "num_runmap": None,
                "records_release_date": None,
                "platforms_games": None
                }

    analyzer["games"] = lt.newList("SINGLE_LINKED", compareIds)
    analyzer["categories"]= lt.newList("SINGLE_LINKED", compareIds)
    analyzer["video_games"] = om.newMap(comparefunction = compareIds)
    analyzer["platforms"] = mp.newMap(100,
                                    maptype='PROBING',
                                    loadfactor=0.5)
    analyzer['players_0'] = om.newMap(omaptype='RBT')
    analyzer['time_0'] = om.newMap(omaptype='RBT')
    analyzer["games_map"] = mp.newMap(1000, maptype='PROBING',
                                    loadfactor=0.5)
    analyzer["records"] = om.newMap(comparefunction = compareIds)

    analyzer["num_runmap"]=om.newMap(omaptype="RBT",
                                        comparefunction=compareIds)
    analyzer["records_release_date"] = om.newMap(comparefunction = cmpReleaseDate)
    analyzer['platforms_games'] = mp.newMap(100,
                                    maptype='PROBING',
                                    loadfactor=0.5)
    return analyzer

# Funciones para agregar informacion al catalogo

def addCategory(analyzer, category):
    
    if category['Game_Id'] != '':
        category['Game_Id'] = int(category['Game_Id'])
    else:
        category['Game_Id'] = 9999
    if category['Subcategory_Id'] != '':
        category['Category_Id'] = int(category['Category_Id'])
    else:
        category['Category_Id'] = 9999
    if category['Subcategory_Id'] != '':
        category['Subcategory_Id'] = int(category['Subcategory_Id'])
    else:
        category['Subcategory_Id'] = 9999
    category['Num_Runs'] = int(category['Num_Runs'])
    if category['Subcategory'] == '':
        category['Subcategory'] = ['Unknown']
    else:
        category['Subcategory'] = category['Subcategory'].split(',')
    if category['Time_0'] != 0:
        category['Time_0'] = float(category['Time_0'])
    if category['Country_0'] != '':
        category['Country_0'] = category['Country_0'].split(',')
    if category['Players_0'] != '':
        category['Players_0'] = category['Players_0'].split(',')
    if category['Record_Date_0'] != '':
        category['Record_Date_0'] = datetime.fromisoformat(category['Record_Date_0'].replace('Z', ''))
    else:
        category['Record_Date_0'] = datetime.strptime("0001", "%Y")
    if category['Time_1'] != '':
        category['Time_1'] = float(category['Time_1'])
    if category['Country_1'] != '':
        category['Country_1'] = category['Country_1'].split(',')
    if category['Players_1'] != '':
        category['Players_1'] = category['Players_1'].split(',')
    if category['Record_Date_1'] != '':
        category['Record_Date_1'] = datetime.fromisoformat(category['Record_Date_1'].replace('Z', ''))
    if category['Time_2'] != '':
        category['Time_2'] = float(category['Time_2'])
    if category['Country_2'] != '':
        category['Country_2'] = category['Country_2'].split(',')
    if category['Players_2'] != '':
        category['Players_2'] = category['Players_2'].split(',')
    if category['Record_Date_2'] != '':
        category['Record_Date_2'] = datetime.fromisoformat(category['Record_Date_2'].replace('Z', ''))
    if category['Misc'] == 'False':
        category['Misc'] = False
    else:
        category['Misc'] = True
    
    """Agregar categoria a la lista categories"""

    lt.addLast(analyzer['categories'], category)

    """Agregar categoria al videojuego correspondiente en el arbol"""

    game = me.getValue(om.get(analyzer['video_games'], category['Game_Id']))
    lt.addLast(game['categories'], category)
    om.put(analyzer['video_games'], category['Game_Id'], game)

    """Agregar jugador al mapa de players_0"""
    for jugador in category['Players_0']:
        addPlayer(analyzer, jugador.strip(), category)

    """Agregar tiempo al mapa Time_0"""
    addTime(analyzer, category['Time_0'], category)

    if om.contains(analyzer["records"], category["Record_Date_0"]):
        entry = om.get(analyzer["records"], category["Record_Date_0"])
        record = me.getValue(entry)

    else:

        record = lt.newList()
        om.put(analyzer["records"], category["Record_Date_0"], record)

    lt.addLast(record, category)
    
    """Agregar registro al árbol ordenado por Release_Date"""
    
    entry = mp.get(analyzer["games_map"],category["Game_Id"])
    game = me.getValue(entry)

    category["Release_Date"] = game["Release_Date"]

    om.put(analyzer["records_release_date"], category, True)

    """Agregar numero de intentos al mapa Num_Runs"""
    updateNumindex(analyzer, category["Num_Runs"], category)

    return analyzer

def addGame(analyzer, game):

    game['Game_Id'] = int(game['Game_Id'])
    game['Platforms'] = game['Platforms'].split(',')
    game['Total_Runs'] = int(game['Total_Runs'])
    if game['Release_Date'] != '':  
        game["Release_Date"] = datetime.strptime(game["Release_Date"], "%y-%m-%d")
    else:
        game['Release_Date'] = datetime.strptime("0001", "%Y")

    """Agregar videojuego a la lista games"""
    lt.addLast(analyzer['games'], game)

    mp.put(analyzer['games_map'], game["Game_Id"], game)
    
    """Crear nuedo nodo en el arbol de videojuegos"""
    entry = newGameEntry(game)
    om.put(analyzer['video_games'], game['Game_Id'], entry)
    
    """Agregar videojuego al mapa de plataformas"""
    for platform in game['Platforms']:
        addPlatform(analyzer, platform.strip(), game)
        addPlatformGames(analyzer, platform.strip(), game)
    return analyzer

# Funciones para creacion de datos

def newGameEntry(game):

    entry = {'info':None,
            'categories': None}

    entry['info'] = game
    entry['categories'] = lt.newList()
    return entry

def addPlatform(analyzer, platformname, game):

        platforms = analyzer['platforms']
        existsplatforms = mp.contains(platforms, platformname)

        if existsplatforms:
            entry = mp.get(platforms, platformname)
            platform=me.getValue(entry)

        else:
            platform = newplatform()
            mp.put(platforms, platformname, platform)

        addReleaseDate(platform['releaseDate'], game['Release_Date'], game)
        platform['total'] += 1

def addReleaseDate(platform, releasename, game):
        existsrelease = om.contains(platform, releasename)

        if existsrelease:
            entry = om.get(platform, releasename)
            release=me.getValue(entry)

        else:
            release = newrelease()
            om.put(platform, releasename, release)
        lt.addLast(release['games'], game)
        sortByReleaseDate(release['games'])

def newplatform():
    entry = {'releaseDate': None,
            'total': 0}

    entry['releaseDate'] = om.newMap(omaptype="RBT")
    return entry

def newrelease():
    entry = {'games': None,
            'total': 0}

    entry['games'] = lt.newList('SINGLE_LINKED',
                                cmpfunction=cmpGamesByReleaseDate)
    return entry

def addPlayer(analyzer, playername, category):
        players = analyzer['players_0']
        existsplayers = om.contains(players, playername)

        if existsplayers:
            entry = om.get(players, playername)
            player=me.getValue(entry)

        else:
            player = newplayer()
            om.put(players, playername, player)
        
        lt.addLast(player['games'], category)
        player['total'] += 1

def newplayer():
    entry = {'games': None,
            'total': 0}

    entry['games'] = lt.newList()
    return entry

def addTime(analyzer, timename, category):
    times = analyzer['time_0']
    existstime = om.contains(times, timename)

    if existstime:
        entry = om.get(times, timename)
        time = me.getValue(entry)
    else:
        time = newTime(timename)
        om.put(times, timename, time)

    lt.addLast(time['registros'], category)
    time['total'] += 1
    
def newTime(time):
    entry = {'time': None,
            'registros': None,
            'total': 0}
    entry['time'] = time
    entry['registros'] = lt.newList()
    return entry

def updateNumindex(analyzer, numname, category): 
   
    nums  = analyzer["num_runmap"]
    existenum = om.contains(nums, numname)

    if existenum: 
        entry = om.get(nums,numname)
        num = me.getValue(entry)
    
    else: 
        num = newnum(numname)
        om.put(nums,numname,num)
    
    lt.addLast(num["registros"], category)
    num["total"]+= 1


def newnum(num):

    entry = {'num': None,
            "registros": None,
            "total": 0}

    entry["num"]= num  
    entry['registros'] = lt.newList()
    return entry 

def addPlatformGames(analyzer, platformname, game):

        platforms = analyzer['platforms_games']
        existsplatforms = mp.contains(platforms, platformname)

        if existsplatforms:
            entry = mp.get(platforms, platformname)
            platform=me.getValue(entry)

        else:
            platform = newplatform2()
            mp.put(platforms, platformname, platform)
        games = newGameEntry(game)
        lst = me.getValue(om.get(analyzer['video_games'], game['Game_Id']))
        games['categories'] = lst['categories']
        lt.addLast(platform['games'], games)
        platform['total'] += 1

def newplatform2():
    entry = {'games': None,
            'total': 0}

    entry['games'] = lt.newList()
    return entry

# Funciones de consulta

def getSix(list):
    if lt.size(list)>= 6: 
        first = lt.subList(list, 1, 3)
        last = lt.subList(list, lt.size(list) - 2, 3)
        six = lt.newList('ARRAY_LIST')
        for elem in lt.iterator(first):
            lt.addLast(six, elem)
        for elem in lt.iterator(last):
            lt.addLast(six, elem)
    else:
        six = list
    return six

#=====================================
#Requerimiento 1
#=====================================

def gamesInRange(analyzer, platform, rangesup, rangeinf):
    platforms = analyzer['platforms']
    info_platform = me.getValue(mp.get(platforms, platform))
    lst = om.values(info_platform['releaseDate'], rangeinf, rangesup)
    totalgames = 0
    for date in lt.iterator(lst):
        totalgames += lt.size(date['games'])
    return info_platform['total'], lst, totalgames

#=====================================
#Requerimiento 2
#=====================================

def registroJugador(analyzer, jugador):
    registros = me.getValue(om.get(analyzer['players_0'], jugador))
    games=lt.newList()
    for registro in lt.iterator(registros['games']):
        dicct = {}
        game = me.getValue(om.get(analyzer['video_games'], registro['Game_Id']))
        dicct['game'] = game
        dicct['registro'] = registro
        lt.addLast(games,dicct)
    return games

#=====================================
#Requerimiento 3
#=====================================

def numInRangemap(analyzer, limiteinf, limitesup):
    nums = analyzer["num_runmap"]
    lst = om.values(nums, limiteinf, limitesup)
    registros= lt.newList()
    for registro in lt.iterator(lst):
        x ={"Num_Runs": registro["num"],
            "Count": registro["total"],
            "Details": lt.newList()}

        for category in lt.iterator(registro["registros"]):
            dicct = {}
            game = me.getValue(om.get(analyzer["video_games"], category["Game_Id"]))
            dicct["game"]= game
            dicct["registro"]= category
            lt.addLast(x["Details"], dicct)
        lt.addLast(registros, x)

    return registros

#=====================================
#Requerimiento 4
#=====================================

def slowInRange(analyzer, rangesup, rangeinf):

    records = analyzer["records"]
    rango = om.values(records, rangeinf, rangesup)
    size = om.size(rango)
    rango = getSix(rango)

    for fecha_registro in lt.iterator(rango):
        for registro in lt.iterator(fecha_registro):
            entry = mp.get(analyzer["games_map"], registro["Game_Id"])
            game = me.getValue(entry)
            registro["Release_Date"] = game["Release_Date"]
            registro["Name"] = game["Name"]
            registro["Platforms"] = game["Platforms"]
            registro["Genres"] = game["Genres"]
        mer.sort(fecha_registro, compareTime)

    return rango, size

#=====================================
#Requerimiento 5
#=====================================

def rangeTime(analyzer, rangesup, rangeinf):
    times = analyzer['time_0']
    lst = om.values(times, rangeinf, rangesup)
    registros = lt.newList()
    for registro in lt.iterator(lst):
        x = {'Time_0' : registro['time'],
            'Count': registro['total'],
            'Details': lt.newList()
        }
        for category in lt.iterator(registro['registros']):
            dicct = {}
            game = me.getValue(om.get(analyzer['video_games'], category['Game_Id']))
            dicct['game'] = game
            dicct['registro'] = category
            lt.addLast(x['Details'],dicct)
        lt.addLast(registros,x)
    return registros

#=====================================
#Requerimiento 6
#=====================================

def propertyHistogram(analyzer, rangeinf, rangesup, num_segmentos, num_niveles, propiedad):

    records = analyzer["records_release_date"]
    categories = om.keys(records, {"Release_Date": datetime.strptime(rangeinf, "%Y")}, {"Release_Date": datetime.strptime(rangesup + "-12-31 23:59:59", "%Y-%m-%d %H:%M:%S")})
    total = lt.size(categories)

    for i in range(1, lt.size(categories)+1):
        record = lt.getElement(categories, i)

        if propiedad == "Time_Avg":
            times = ["Time_0", "Time_1", "Time_2"]
            suma = 0
            count = 0

            for time in times:
                if record[time] != "":
                    suma += record[time]
                    count += 1
            
            record["Time_Avg"] = suma/count

        elif not record[propiedad]:
            lt.deleteElement(categories, i)

    histogram_count = lt.size(categories)
    mer.sort(categories, index_cmp[propiedad])

    min = lt.getElement(categories, 1)[propiedad]
    max = lt.getElement(categories, lt.size(categories))[propiedad]

    tam = (max - min) / num_segmentos
    tabla = []
    count = 0
    high = min + tam
    pos = 1

    for i in range(num_segmentos):
        record = lt.getElement(categories, pos)

        while record[propiedad] < high:
            pos += 1
            record = lt.getElement(categories, pos)
            count += 1

        if i == num_segmentos-1:
        
            count += lt.size(categories) - (pos-1)

        tabla.append({"bin": "("+ str(round(min + i*tam, 2))+", "+ str(round(min + ((i+1) * tam),2)) + "]",
            "count" : count,
            "lvl" : count//num_niveles,
            "mark":  "*" * (count//num_niveles)})

        count = 0
        
        high += tam
    
    return tabla, total, histogram_count, min, max

#=====================================
#Requerimiento 7
#=====================================

def antiquity(game):
    game=int(game)

    if game >= 2018:
        rlsy = game - 2017
    elif game < 2018 and game > 1998:
        rlsy = (game/-5)+404.6
    else:
        rlsy = 5
    return rlsy

def popularity(game):
    return math.log(game)

def misc(game):
    new_list = lt.newList()
    for x in lt.iterator(game):
        if x['Misc'] == False:
            lt.addLast(new_list, x)
    return new_list

def time_avg(game):
    total = 0
    for x in lt.iterator(game):
        total_tiempo = 0
        pos = 0
        if x['Time_0'] != '':
            total_tiempo+=x['Time_0']
            pos += 1
        if x['Time_1'] != '':
            total_tiempo+=x['Time_1']
            pos += 1
        if x['Time_2'] != '':
            total_tiempo+=x['Time_2']
            pos += 1
        total += total_tiempo/pos
    return round(total,2)

def revenue(game,timeavg):
    popular = popularity(game['info']['Total_Runs'])
    date = game['info']['Release_Date']
    date = date.strftime('%Y')
    antiqui = antiquity(date)
    return (popular*timeavg)/antiqui

def marketshare(game, games):
    total = 0
    for x in lt.iterator(games):
        y = misc(x['categories'])
        total += lt.size(y)
    return round(lt.size(game)/total,2)

def streamrevenue(game,timeavg, marketshare):
    reve = revenue(game,timeavg)
    return reve*marketshare

def topNmasrentables(analyzer, platform, top):
    info = me.getValue(om.get(analyzer['platforms_games'], platform))
    games = info['games']
    new_list= lt.newList()
    for game in lt.iterator(games):
        game_cate = misc(game['categories'])
        timeavg = time_avg(game_cate)
        market = marketshare(game_cate, games)
        stream = streamrevenue(game, timeavg, market)
        dicct = {'Name': game['info']['Name'],
                'Release_Date': game['info']['Release_Date'],
                'Platforms': game['info']['Platforms'],
                'Genres': game['info']['Genres'],
                'Stream_Revenue': stream,
                'Market_Share': market,
                'Time_Avg': timeavg,
                'Total_Runs': game['info']['Total_Runs']}
        lt.addLast(new_list, dicct)
    new_list = sortByStream(new_list)
    topN = lt.subList(new_list, 1, top)
    return topN

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def sortByReleaseDate(title):
    return mer.sort(title, cmpGamesByReleaseDate)

def sortByTime(title):
    return mer.sort(title, cmpRegistroTime)

def sortByStream(title):
    return mer.sort(title, cmpStream)

# Funciones de comparacion 

def cmpGamesByReleaseDate(game1, game2):
    if game1['Release_Date'] == game2['Release_Date']:
        if game1['Abbreviation'] == game2['Abbreviation']:
            return game1['Name'] < game2['Name']
        return game1['Abbreviation'] < game2['Abbreviation']
    return game1['Release_Date'] > game2['Release_Date']

def cmpRegistroTime(reg1, reg2):
    if reg1['Time_0'] == reg2['Time_0']:
        if reg1['Record_Date_0'] == reg2['Record_Date_0']:
            return reg1['Name'] < reg2['Name']
        return reg1['Record_Date_0'] > reg2['Record_Date_0']
    return reg1['Time_0'] < reg2['Time_0']

def cmpReleaseDate(registro1, registro2):

    if registro1["Release_Date"] < registro2["Release_Date"]:
        res = -1
    elif registro1["Release_Date"] > registro2["Release_Date"]:
        res = 1
    else:
        res = 0

    if res != 0: return res

    if registro1["Category_Id"] < registro2["Category_Id"]:
        res = -1
    elif registro1["Category_Id"] > registro2["Category_Id"]:
        res = 1
    else:
        res = 0
    
    if res != 0: return res
    
    if registro1["Game_Id"] < registro2["Game_Id"]:
        res =  -1
    elif registro1["Game_Id"] > registro2["Game_Id"]:
        res =  1
    else:
        res =  0
    
    if res != 0: return res

    if registro1["Subcategory_Id"] < registro2["Subcategory_Id"]:
        return  -1
    elif registro1["Subcategory_Id"] > registro2["Subcategory_Id"]:
        return  1
    else:
        return  0
    
def cmpStream(game1, game2):
    return game1['Stream_Revenue'] > game2['Stream_Revenue']

    

def compareIds(id1, id2):
    
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareTime(registro1, registro2):
    if registro1["Time_0"] == registro2["Time_0"]:
        if registro1["Num_Runs"] == registro2["Num_Runs"]:
            return registro1["Name"] < registro2["Name"]
        return registro1["Num_Runs"] < registro2["Num_Runs"]
    return registro1["Time_0"] < registro2["Time_0"]


def cmpTime0(registro1,  registro2):
    return registro1["Time_0"] < registro2["Time_0"]

def cmpTime1(registro1,  registro2):
    return registro1["Time_1"] < registro2["Time_1"]

def cmpTime2(registro1,  registro2):
    return registro1["Time_2"] < registro2["Time_2"]

def cmpTimeAvg(registro1,  registro2):
    return registro1["Time_Avg"] < registro2["Time_Avg"]

def cmpNumRuns(registro1,  registro2):
    return registro1["Num_Runs"] < registro2["Num_Runs"]

index_cmp = {
    "Time_0": cmpTime0,
    "Time_1": cmpTime1,
    "Time_2": cmpTime2,
    "Time_Avg": cmpTimeAvg,
    "Num_Runs": cmpNumRuns
}
