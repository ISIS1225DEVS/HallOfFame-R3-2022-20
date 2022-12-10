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


from doctest import ELLIPSIS_MARKER
from itertools import filterfalse
from lzma import FILTER_LZMA2
from platform import platform, release
from unicodedata import category
from xml.dom import registerDOMImplementation
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.DataStructures import rbtnode as rbtn
from DISClib.Algorithms.Trees import traversal as tv
from DISClib.Algorithms.Sorting import shellsort as sa, mergesort as ms
from DISClib.ADT import orderedmap as om
from datetime import date, datetime
import math
import folium
import pandas
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
assert cf
import webbrowser
geolocator = Nominatim(user_agent="reto")

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos

def newAnalyzer():
    analyzer = {"games":None,
                "registers":None,
                "release_dates":None}

    analyzer["games"] = lt.newList("SINGLE_LINKED",compareIds)
    analyzer["registers"] = lt.newList("SINGLE_LINKED",compareIds)
    analyzer["release_dates"] = om.newMap("RBT",cmpReleaseDates)
    analyzer["times"] = om.newMap("RBT",cmpTimes)
    analyzer["years"] = om.newMap("RBT",cmpYears)
    analyzer["platforms"] = om.newMap("RBT",cmpYears)
    analyzer["dates"] = om.newMap("RBT",cmpReleaseDates)
    analyzer["releases"] = om.newMap("RBT",cmpReleaseDates)
    analyzer["times_0"] = om.newMap("RBT", cmpTimes)
    analyzer["num_runs"] = om.newMap("RBT", cmpRuns)


    return analyzer


def addGame(analyzer,game):
    lt.addLast(analyzer["games"],game)
    updateDate(analyzer["release_dates"],game)
    updatePlatform(analyzer["platforms"],game)
    return analyzer

def addRegister(analyzer,register):
    lt.addLast(analyzer["registers"],register)
    updateTime(analyzer["times"],register)
    updateYear(analyzer["years"],register)
    updateDateRegister(analyzer["dates"],register)
    updateTime0(analyzer["times_0"],register)
    updateNumRuns(analyzer["num_runs"],register)
    updateReleases(analyzer["releases"],register)
    return analyzer



def updateDate(map,game):
    occurrdate = game["Release_Date"]
    release_date = datetime.strptime(occurrdate,"%y-%m-%d")
    release_date = release_date.date()
    release_date = datetime.strftime(release_date, "%Y-%m-%d")

    entry = om.get(map,release_date)
    if entry is None:
        dataentry = newDataEntry(game)
        om.put(map,release_date,dataentry)
    else:
        dataentry = me.getValue(entry)
    
    platforms = game["Platforms"].split(",")

    for platform in platforms:
        addPlatform(dataentry,game,platform.strip())


    return map

def updateTime(map,register):
    occurrtime = float(register["Time_0"])
    
    entry = om.get(map,occurrtime)
    if entry is None:
        dataentry = newDataEntryTime(register)
        om.put(map,occurrtime,dataentry)
    else:
        dataentry = me.getValue(entry)
    

    players = register["Players_0"].split(",")
    for player in players:
        addPlayer(dataentry,register,player.strip())
        
    return map

def updateYear(map,register):
    release_year = register["Release_Date"]
    release_year = datetime.strptime(release_year,"%y-%m-%d").date()
    release_year = datetime.strftime(release_year,"%Y")


    entry = om.get(map, int(release_year))

    if entry is None:
        dataentry = lt.newList("ARRAY_LIST",cmpfunction=None)
        lt.addLast(dataentry,register)
        om.put(map, int(release_year), dataentry)
    else:
        dataentry = me.getValue(entry)
        lt.addLast(dataentry,register)
        om.put(map, int(release_year), dataentry)
    
    #addTime(dataentry, register, register["Time_0"])
    return map
    
def updatePlatform(map,game):
    platforms = game["Platforms"].split(",")

    for platform in platforms:
        platform = platform.strip()
        entry = om.get(map,platform)
        if entry is None:
            dataentry = lt.newList("ARRAY_LIST",cmpfunction=None)
            lt.addLast(dataentry,game)
            om.put(map,platform,dataentry)
        else:
            dataentry = me.getValue(entry)
            lt.addLast(dataentry,game)
            om.put(map, platform, dataentry)

    return map

#Update Requerimiento 3
def updateNumRuns(map,register):
    num_runs = float(register["Num_Runs"])


    entry = om.get(map,num_runs)
    if entry is None:
        dataentry = newRunsEntry(register,num_runs)
        om.put(map,num_runs,dataentry)
    else:
        dataentry = me.getValue(entry)

    addTime0(dataentry,register,register["Time_0"])

    return entry

#Update Requerimiento 4
def updateDateRegister(map,register):
    record_date = register["Record_Date_0"]


    entry = om.get(map,record_date)
    if entry is None:
        dataentry = newDateEntry(register,record_date)
        om.put(map,record_date,dataentry)
    else:
        dataentry = me.getValue(entry)

    addTime(dataentry,register,register["Time_0"])

    return entry

#Update Requerimiento 5
def updateTime0(map, register):
    record_time = float(register["Time_0"])

    entry = om.get(map, record_time)
    if entry is None:
        dataentry = newTime0(register,record_time)
        om.put(map, record_time, dataentry)
    else:
        dataentry = me.getValue(entry)
    
    addDate(dataentry, register, register["Record_Date_0"])

    return map

def updateReleases(map,register):
    release_year = register["Release_Date"]
    release_year = datetime.strptime(release_year,"%y-%m-%d").date()
    release_year = datetime.strftime(release_year,"%Y")

    entry = om.get(map, int(release_year))

    if entry is None:
        dataentry = newTimeMap(register)
        om.put(map, int(release_year), dataentry)
    else:
        dataentry = me.getValue(entry)

    addTimes(dataentry,register,float(register["Time_0"]))
    return map






def newDataEntry(game):
    entry = {"platforms": None,"lstgames":None}
    entry["platforms"] = mp.newMap(numelements=700,
                                    maptype="PROBING",
                                    comparefunction=comparePlatformMap)

    entry["lstgames"] = lt.newList("SINGLE_LINKED", compareIds)
    lt.addLast(entry["lstgames"],game)
    return entry

def newDataEntryTime(register):
    entry = {"players":None,"lstregisters":None}
    entry["players"] = mp.newMap(numelements=1200,
                                    maptype="PROBING",
                                    comparefunction=comparePlayersMap)
    entry["lstregisters"] = lt.newList("SINGLE_LINKED", compareIds)
    lt.addLast(entry["lstregisters"],register)
    return entry

def newDataEntryYear(register):
    entry = {"lstyearstodo":None}
    entry["lstyearstodo"] = lt.newList("ARRAY_LIST",compareIds)
    lt.addLast(entry["lstyearstodo"],register)
    return entry

#Requerimiento 3
def newRunsEntry(register,num_runs):
    entry = {"times":None,"lstregisters":None,"Num_Runs":None}
    entry["times"] = om.newMap("RBT",cmpTimes)
    entry["lstregisters"] = lt.newList("ARRAY_LIST",compareIds)
    entry["Num_Runs"] = num_runs

    lt.addLast(entry["lstregisters"],register)
    return entry

#Requerimiento 4
def newDateEntry(register,release_date):
    entry = {"times":None,"lstregisters":None,"date":None}
    entry["times"] = om.newMap("RBT",cmpTimes)
    entry["lstregisters"] = lt.newList("ARRAY_LIST",compareIds)
    entry["date"] = release_date

    lt.addLast(entry["lstregisters"],register)
    return entry

#newTime Requerimiento 5
def newTime0(register,record_time):
    entry = {"dates":None,"lstregisters":None,"times":None}
    entry["dates"] = om.newMap("RBT", cmpRecordDate)
    entry["lstregisters"] = lt.newList("ARRAY_LIST",compareIds)
    entry["times"] = record_time

    lt.addLast(entry["lstregisters"],register)
    return entry


def newTimeMap(register):
    entry = {"times":None,"lstregisters":None}
    entry["times"] = om.newMap("RBT", cmpTimes)
    entry["lstregisters"] = lt.newList("ARRAY_LIST",compareIds)

    lt.addLast(entry["lstregisters"],register)
    return entry




def addPlatform(dataentry,game,platform):
    lst = dataentry["lstgames"]
    #lt.addLast(lst,game)

    platformmap = dataentry["platforms"]
    platformentry = mp.get(platformmap,platform)
    if platformentry is None:
        entry = newPlatformEntry(platform,game)
        lt.addLast(entry["lstgames"],game)
        mp.put(platformmap,platform,entry)
    else:
        entry = me.getValue(platformentry)
        lt.addLast(entry["lstgames"],game)
    
    return dataentry

def addPlayer(dataentry,register,players):
    lst = dataentry["lstregisters"]
    playermap = dataentry["players"]

    playermapentry = mp.get(playermap,players)
    if playermapentry is None:
        entry = newPlayerEntry(players,register)
        lt.addLast(entry["lstregisters"],register)
        mp.put(playermap,players,entry)
    else:
        entry = me.getValue(playermapentry)
        lt.addLast(entry["lstregisters"],register)
        
    return dataentry

#Requerimiento 3
def addTime0(dataentry,register,time):
    lst = dataentry["lstregisters"]
    num_runs = dataentry["Num_Runs"]
    timesmap = dataentry["times"]
    timeentry = mp.get(timesmap,time)
    if timeentry is None:
        entry = newTimeEntry0(time,register,num_runs)
        lt.addLast(entry["lstregisters"],register)
        mp.put(timesmap,time,entry)
    else:
        entry = me.getValue(timeentry)
        lt.addLast(entry["lstregisters"],register)

    return dataentry

#Requerimiento 4
def addTime(dataentry,register,time):
    lst = dataentry["lstregisters"]
    release_date = dataentry["date"]
    timesmap = dataentry["times"]
    timeentry = mp.get(timesmap,time)
    if timeentry is None:
        entry = newTimeEntry(time,register,release_date)
        lt.addLast(entry["lstregisters"],register)
        mp.put(timesmap,time,entry)
    else:
        entry = me.getValue(timeentry)
        lt.addLast(entry["lstregisters"],register)

    return dataentry

#add Requerimiento 5
def addDate(dataentry,register,record_date):
    lst = dataentry["lstregisters"]
    times = dataentry["times"]
    datesmap = dataentry["dates"]
    dateentry = mp.get(datesmap, record_date)
    if dateentry is None:
        entry = newRecordDateEntry(record_date,register,times)
        lt.addLast(entry["lstregisters"], register)
        mp.put(datesmap,record_date,entry)
    else:
        entry = me.getValue(dateentry)
        lt.addLast(entry["lstregisters"], register)
    
    return dataentry 

def addTimes(dataentry,register,time):
    lst = dataentry["lstregisters"]
    datetimemap = dataentry["times"]
    datetimeentry = om.get(datetimemap,time)
    if datetimeentry is None:
        entry = lt.newList("ARRAY_LIST",cmpfunction=compareIds)
        lt.addLast(entry,register)
        om.put(datetimemap,time,entry)
    else:
        entry = me.getValue(datetimeentry)
        lt.addLast(entry,register)
        om.put(datetimemap,time,entry)

    return datetimeentry


def newPlatformEntry(platform,game):
    platformdt = {"platform":None, "lstgames": None}
    platformdt["platform"] = platform
    platformdt["lstgames"] = lt.newList("SINGLE_LINKED",comparePlatform)
    #lt.addLast(platformdt["lstgames"],game)
    return platformdt

def newPlayerEntry(player,register):
    playerdt = {"players":None,"lstregisters":None}
    playerdt["players"] = player
    playerdt["lstregisters"] = lt.newList("SINGLE_LINKED",comparePlayer)
    return playerdt

#Requerimiento 3
def newTimeEntry0(time,register,num_runs):
    timesdt = {"time":None,"lstregisters":None,"Num_Runs":None}
    timesdt["time"] = time
    timesdt["lstregisters"] = lt.newList("ARRAY_LIST",compareTime)
    timesdt["Num_Runs"] = num_runs
    return timesdt

#Requerimiento 4
def newTimeEntry(time,register,release_date):
    timesdt = {"time":None,"lstregisters":None,"date":None}
    timesdt["time"] = time
    timesdt["lstregisters"] = lt.newList("ARRAY_LIST",compareTime)
    timesdt["date"] = release_date
    return timesdt

#Requerimiento 5
def newRecordDateEntry(record_date, register, time):
    datesdt = {"date": None, "lstregisters": None, "time": None}
    datesdt["date"] = record_date
    datesdt["time"] = time
    datesdt["lstregisters"] = lt.newList("ARRAY_LIST",cmpRecordDate)
    return datesdt


#Requerimiento 1
def gamesinRange(analyzer,date_lo,date_hi,plataforma):# O(N^2)
    maps = om.values(analyzer["release_dates"],date_lo,date_hi) # 1
    
    totalgamesplatform = 0 # 1
    lstgames = lt.newList("ARRAY_LIST",cmpfunction=None) # 1
    for maplatforms in lt.iterator(maps): # N
        
        entry = mp.get(maplatforms["platforms"],plataforma) # 1
        
        if entry is not None: # 1

        
            value = me.getValue(entry) # 1
                
            totalgamesplatform += lt.size(value["lstgames"]) # 1

            for element in lt.iterator(value["lstgames"]): # N
                lt.addLast(lstgames,element) # 1


    ms.sort(lstgames,compareDateAbbreviation) # NlogN
    return totalgamesplatform,lstgames

#Requerimiento 2
def fastestRecordsPlayer(analyzer,player): # O(N^3)
    time_lo = om.minKey(analyzer["times"]) # logN
    time_hi = om.maxKey(analyzer["times"]) # logN
    maps = om.values(analyzer["times"],time_lo,time_hi) # logN
    totalregistersplayer = 0 # 1
    lstregisters = lt.newList("ARRAY_LIST",cmpfunction=None) # 1

    for maplayers in lt.iterator(maps): # N
        keys = mp.keySet(maplayers["players"]) # 1

        for key in lt.iterator(keys): # N
            if player in key: # 1
                value = me.getValue(mp.get(maplayers["players"],key)) # 1
                totalregistersplayer += 1 # 1

                for element in lt.iterator(value["lstregisters"]): # N
                    lt.addLast(lstregisters,element) # 1

    ms.sort(lstregisters,compareTimeRecordDate) # NlogN
    return totalregistersplayer,lstregisters

#Requerimiento 3
def registrosVeloces(analyzer,run_lo,run_hi): # O(NlogN)
    maps = om.values(analyzer["num_runs"],float(run_lo),float(run_hi)) # logN
    
    
    lstregisters = lt.newList("ARRAY_LIST",cmpfunction=None) # 1
    for maptimes in lt.iterator(maps): # N

        minkey = om.minKey(maptimes["times"]) # logN
        minvalue = me.getValue(om.get(maptimes["times"],minkey)) # 1
        
        

        dt = {"Num_Runs":minvalue["Num_Runs"],"Count":lt.size(minvalue["lstregisters"]),"Details":minvalue["lstregisters"]} # 1
 

        lt.addLast(lstregisters,dt) # 1


    return lt.size(lstregisters),lstregisters


#Requerimiento 4
def registrosLentos(analyzer,date_lo,date_hi): # O(NlogN)
    maps = om.values(analyzer["dates"],date_lo,date_hi) # logN
    
     
    lstregisters = lt.newList("ARRAY_LIST",cmpfunction=None) # 1
    for maptimes in lt.iterator(maps): # N
        maxkey = om.maxKey(maptimes["times"]) # logN
        maxvalue = me.getValue(om.get(maptimes["times"],maxkey)) # 1

        dt = {"Record_Date_0":maxvalue["date"],"Count":lt.size(maxvalue["lstregisters"]),"Details":maxvalue["lstregisters"]} # 1

        lt.addLast(lstregisters,dt) # 1


    return lt.size(lstregisters),lstregisters

#Requerimiento 5
def registrosRecientes(analyzer,time_lo,time_hi): # O(NlogN)
    maps = om.values(analyzer["times_0"],float(time_lo),float(time_hi)) # logN

    lstregisters = lt.newList("ARRAY_LIST",cmpfunction=None) # 1
    for mapdates in lt.iterator(maps): # N
        maxkey = om.maxKey(mapdates["dates"]) # logN
        entry = om.get(mapdates["dates"], maxkey) # logN
        maxvalue = me.getValue(entry) # 1
        
        dt = {"Time_0":maxvalue["time"],"Count":lt.size(maxvalue["lstregisters"]),"Details":maxvalue["lstregisters"]} # 1

        lt.addLast(lstregisters,dt) # 1
    


    return lt.size(lstregisters),lstregisters


#Requerimiento 6
def diagramarHistograma(analyzer,anio_lo,anio_hi,segmentos,niveles,op): # O(N^2logN)
    listas = om.values(analyzer["years"],int(anio_lo),int(anio_hi)) # logN
    mapgeneral = om.newMap("RBT",comparefunction=cmpTimes) # logN
    for lista in lt.iterator(listas): # N
        for element in lt.iterator(lista): # N
            if op.lower() == "times": # 1
                key = element["Time_0"] # 1
                entry = om.get(mapgeneral,float(key)) # logN
                if entry is None: # 1
                    lta = lt.newList("ARRAY_LIST",cmpfunction=None) # 1
                    lt.addLast(lta,element) # 1
                    om.put(mapgeneral,float(key),lta) # logN
                else:
                    value = me.getValue(om.get(mapgeneral,float(key))) # 1
                    lt.addLast(value,element) # 1
                    om.put(mapgeneral,float(key),lta) # logN


            elif op.lower() == "time_avg": # 1
                key = element["Time_average"] # 1
                entry = om.get(mapgeneral,float(key))  # logN
                if entry is None: # 1
                    lta = lt.newList("ARRAY_LIST",cmpfunction=None) # 1
                    lt.addLast(lta,element) # 1
                    om.put(mapgeneral,float(key),lta) # logN
                else:
                    value = me.getValue(om.get(mapgeneral,float(key))) # 1
                    lt.addLast(value,element) # 1
                    om.put(mapgeneral,float(key),lta) # logN

            else:
                key = element["Num_Runs"] # 1

                entry = om.get(mapgeneral,float(key)) # logN
                if entry is None: # 1
                    lta = lt.newList("ARRAY_LIST",cmpfunction=None) # 1
                    lt.addLast(lta,element) # 1
                    om.put(mapgeneral,float(key),lta) # logN
                else:
                    value = me.getValue(om.get(mapgeneral,float(key))) # 1
                    lt.addLast(value,element) # 1
                    om.put(mapgeneral,float(key),lta) # logN
        
    
    diff = om.maxKey(mapgeneral) - om.minKey(mapgeneral) # logN

    interval_start = om.minKey(mapgeneral) # logN
    size = diff/int(segmentos) # 1
    interval_size = interval_start+size # 1
    
    dt = {"bin":lt.newList("ARRAY_LIST",cmpfunction=None),"count":lt.newList("ARRAY_LIST",cmpfunction=None),"lvl":lt.newList("ARRAY_LIST",cmpfunction=None),"mark":lt.newList("ARRAY_LIST",cmpfunction=None)} # 1

    for x in range(int(segmentos)): # N
        bin = "(" + str(round(interval_start,2)) + ", " + str(round(interval_size,2)) + "]" # 1
        lt.addLast(dt["bin"],bin) # 1
        count = 0
        for k in lt.iterator(om.keySet(mapgeneral)): # N
            if float(k)>= round(interval_start,2) and float(k)<=round(interval_size,2): # 1
                count +=1 # 1
        lt.addLast(dt["count"],count) # 1
        lvl = round(count/int(niveles)) # 1
        lt.addLast(dt["lvl"],lvl) # 1
        mark = "*"*lvl # 1
        lt.addLast(dt["mark"],mark) # 1
        interval_start = interval_size # 1
        interval_size += size # 1

    
    return om.minKey(mapgeneral),om.maxKey(mapgeneral),om.size(mapgeneral),dt 

#Requerimiento 7
def calcularRentabilidad(analyzer,plataforma,top): # O(N^3)
    entry = om.get(analyzer["platforms"],plataforma) # logN
    dataentry = me.getValue(entry) # 1
    registers = analyzer["registers"] # 1

    for register in lt.iterator(registers): # N
        for game in lt.iterator(dataentry): # N
            if game["Game_Id"] == register["Game_Id"]:
                game["Time_average"] = register["Time_average"] # 1
                game["Time_average1"] = register["Time_average1"] # 1
                game["Time_average1"] = float(register["Time_average1"]) # 1
                if register["Misc"] == "False": # 1
                    register["Misc"] = False # 1
                else:
                    register["Misc"] = True # 1
                if register["Misc"] == False: # 1
                    game["Market_Share"] = marketShare(game,analyzer,plataforma) # N
                    game["Stream_Revenue"] = streamRevenue(game,analyzer,plataforma) # N
                else:
                    game["Market_Share"] = 0 # 1
                    game["Stream_Revenue"] = 0 # 1
        
    ms.sort(dataentry,compareRentabilidad) # NlogN
    return lt.size(dataentry),dataentry


def antiquity(game): # O(1)
    release_year = game["Release_Date"]
    release_year = datetime.strptime(release_year,"%y-%m-%d").date()
    release_year = datetime.strftime(release_year,"%Y")

    if int(release_year) <= 1998:
        antiguedad = 5
    elif int(release_year) > 1998 and int(release_year)<2018:
        antiguedad = (-0.2)*int(release_year) + 404.6
    else:
        antiguedad = int(release_year) -2017
    game["Antiquity"] = antiguedad
    return round(antiguedad,3)

def popularity(game): # O(1)
    popularidad = math.log(float(game["Total_Runs"]))
    game["Popularity"] = popularidad
    return round(popularidad,3)

def revenue(game): # O(1)
    popularidad = popularity(game)
    
    time_avg = round(float(game["Time_average1"])/60,2)
    antiguedad = antiquity(game)
    ingreso = (popularidad*time_avg)/(antiguedad)
    return round(ingreso,3)

def marketShare(game,analyzer,plataforma): # N
    mapa = analyzer["platforms"] # 1
    entry = om.get(mapa,plataforma) # logN
    value = me.getValue(entry) # 1
    pt = om.size(mapa) # logN
    gt = 0


    for juego in lt.iterator(value): # N
        if juego["Game_Id"] == game["Game_Id"]: # 1
            gt+=1



    share = gt/pt # 1
    return round(share,3)

def streamRevenue(game,analyzer,plataforma): # N
    stream = revenue(game)*marketShare(game,analyzer,plataforma)
    return round(stream,2)

#Requerimiento 8
def graficar(analyzer,date,time_lo,time_hi): # O(N^3logN)
    entry = om.get(analyzer["releases"],int(date)) # logN
    valuemap = me.getValue(entry)  # 1
    listatiempos = om.values(valuemap["times"],float(time_lo),float(time_hi))# logN
    countrymap = om.newMap("RBT",cmpCountries) # logN
    for timemap in lt.iterator(listatiempos): # N
        for value in lt.iterator(timemap): # N
            countries = value["Country_0"].split(",") # 1
            for country in countries: # N
                country = country.strip() # 1
                entry = om.get(countrymap,country) # logN

                if entry is None:
                    dataentry = lt.newList("ARRAY_LIST",compareIds) # 1
                    lt.addLast(dataentry,value) # 1
                    om.put(countrymap,country,dataentry) # logN
                else:
                    dataentry = me.getValue(entry) # 1
                    lt.addLast(dataentry,value) # 1
                    om.put(countrymap,country,dataentry) # logN

    unknownkeys = om.keySet(countrymap)
    if lt.isPresent(unknownkeys,"Unknown"):
        countrymap = om.remove(countrymap,"Unknown") # logN
    keys = om.keySet(countrymap) # logN
    lista_registros = om.valueSet(countrymap) # logN
    lista_sizes = lt.newList("ARRAY_LIST",cmpfunction=None) # 1

    for registro in lt.iterator(lista_registros): # N
        tam = lt.size(registro) # 1
        lt.addLast(lista_sizes,tam) # 1

    
    size = lt.size(lista_registros) # 1
    dfk = pandas.DataFrame(lt.iterator(keys)) # 1
    locations = lt.newList("ARRAY_LIST",cmpfunction=None) # 1
    for row in dfk.itertuples(): # N
        c = row[1] # 1
        c = c.replace(".","") # 1
        if c != "Unknown" and c != "": # 1
            location = geolocator.geocode(c) # 1
            dttemp = {"Latitude":float(location.raw['lat']),"Longitude":float(location.raw['lon'])} # 1

            lt.addLast(locations,dttemp) # 1
            

    dfl = pandas.DataFrame(lt.iterator(locations)) # 1
    dfv = pandas.DataFrame(lt.iterator(lista_registros),columns=["elements"]) # 1
    dfs = pandas.DataFrame(lt.iterator(lista_sizes),columns=["elements"]) # 1

    frames = [dfk,dfv,dfs,dfl] # 1
    dffinal = pandas.concat(frames,axis=1,ignore_index=True)# 1
    dffinal.columns = ["Country","Registers","Size","Latitude","Longitude"] # 1

    m = folium.Map() # 1
    markers = MarkerCluster().add_to(m) # 1
    for t in dffinal.itertuples(): # 1
        latitude = t[4] # 1
        longitude = t[5] # 1
        s = t[3] # 1
        text = "Registers:{}".format(t[2]) # 1

        folium.CircleMarker(location=[latitude,longitude],radius=s,popup=text,fill=True,tooltip=t[1]).add_to(markers) # 1
    
    return size,m
    #https://towardsdatascience.com/using-python-to-create-a-world-map-from-a-list-of-country-names-cd7480d03b10


# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(id1,id2):
    if id1 == id2:
        return 0
    elif id1> id2:
        return 1
    else:
        return -1


def comparePlatformMap(plat,entry):
    plat2 = me.getKey(entry)
    if plat == plat2:
        return 0
    elif plat> plat2:
        return 1
    else:
        return -1

def comparePlayersMap(player1,entry):
    player2 = me.getKey(entry)
    if player1 == player2:
        return 0
    elif player1 > player2:
        return 1
    else:
        return -1

def compareTimesMap(time1,entry):
    time2 = me.getKey(entry)
    if time1 == time2:
        return 0
    elif time1>time2:
        return 1
    else:
        return -1


def cmpReleaseDates(date1,date2):
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1

def cmpYears(year1,year2):
    if year1 == year2:
        return 0
    elif year1 > year2:
        return 1
    else:
        return -1

def comparePlatform(plat1,plat2):
    if plat1 == plat2:
        return 0
    elif plat1> plat2:
        return 1
    else:
        return -1

def comparePlayer(play1,play2):
    if play1 == play2:
        return 0
    elif play1 > play2:
        return 1
    else:
        return -1

def compareTime(time1,time2):
    if time1 == time2:
        return 0
    elif time1 > time2:
        return 1
    else:
        return -1

def cmpTimes(time1,time2):
    if time1 == time2:
        return 0
    elif time1 > time2:
        return 1
    else:
        return -1

def cmpRuns(run1,run2):
    if run1 == run2:
        return 0
    elif run1 > run2:
        return 1
    else:
        return -1
def cmpCountries(c1,c2):
    if c1 == c2:
        return 0
    elif c1 > c2:
        return 1
    else:
        return -1
    
def cmpRecordDate(date1,date2):
    if date1 == date2:
        return 0
    elif date1 > date2:
        return 1
    else:
        return -1
    
# Funciones de ordenamiento
def compareDateAbbreviation(el1,el2):
    el1date = datetime.strptime(el1["Release_Date"],"%y-%m-%d")
    el2date = datetime.strptime(el2["Release_Date"],"%y-%m-%d")

    if el1date.date() > el2date.date():
        return True
    elif el1date.date() == el2date.date():
        if el1["Abbreviation"] > el2["Abbreviation"]:
            return True
        else:
            return False
    else:
        return False

def compareTimeRecordDate(reg1,reg2):
    date1 = datetime.strptime(reg1["Record_Date_0"],"%Y-%m-%dT%H:%M:%SZ")
    date2 = datetime.strptime(reg2["Record_Date_0"],"%Y-%m-%dT%H:%M:%SZ")
    if reg1["Time_0"] < reg2["Time_0"]:
        return True
    elif reg1["Time_0"] > reg2["Time_0"]:
        return False
    elif (reg1["Time_0"] == reg2["Time_0"]):
        if date1<date2:
            return True
        elif date1>date2:
            return False
        elif date1 == date2:
            if reg1["Name"] < reg2["Name"]:
                return True
            elif reg1["Name"] > reg2["Name"]:
                return False
            else:
                return False
        else:
            return False     
    else:
        return False

def compareRentabilidad(game1,game2):
    rent1 = game1["Stream_Revenue"]
    rent2 = game2["Stream_Revenue"]

    if rent1 > rent2:
        return True
    else:
        return False

