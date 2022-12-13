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


from turtle import title
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Trees import traversal as it
from datetime import datetime
import datetime as datetime
import math 
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
def NewCatalog():

    catalog={"category_data":None,
                "game_data":None,
                'platforms':None,
                'recordsEntreFechas': None,
                "registros_rango_intentos":None,
                'name_players':None,
                'years':None,
                'Ids':None,
                'RecordEntreTiempos':None,
                'top': None
                }
    catalog["category_data"]=lt.newList('ARRAY_LIST')
    catalog["game_data"]=lt.newList('ARRAY_LIST')
    catalog['platforms']=mp.newMap(numelements=200,
                                    maptype='PROBING',
                                    loadfactor=0.5)
    catalog['recordsEntreFechas']=om.newMap(omaptype='RBT',
                                    comparefunction=cmpDates)

    catalog["registros_rango_intentos"]=om.newMap(omaptype="RBT",
                                         comparefunction=cmpintentos)
    catalog['name_players']=om.newMap(omaptype='RBT',
                                    comparefunction=cmpplayers2)
    catalog['years']= om.newMap(omaptype='RBT',
                                    comparefunction=cmpplayers2)
    catalog['Ids'] = mp.newMap(numelements=200,
                                    maptype='PROBING',
                                    loadfactor=0.5)
    catalog['RecordEntreTiempos']=om.newMap(omaptype="RBT",
                                         comparefunction=cmpTiempos)
    catalog['top']= mp.newMap(numelements=200,
                                    maptype='PROBING',
                                    loadfactor=0.5)
    return catalog



def AddGameData(catalog,videogames):
    lt.addLast(catalog['game_data'],videogames)
    for plataformas in videogames['Platforms'].split(','):
        addReleaseDate(catalog,plataformas.strip(),videogames)
    AddIds(catalog,videogames)
def AddCategorys(catalog,videogames):
    lt.addLast(catalog['category_data'],videogames)
    addRecordDate(catalog,videogames)
    addRegistroIntentos(catalog,videogames)
    AddInPlayers(catalog,videogames)
    addRecordYears(catalog,videogames)
    addRecordTiempos(catalog, videogames)
    for plataformas in videogames['plataforma'].split(','):
        addTop(catalog, videogames, plataformas.strip())

# Construccion de modelos

# Funciones para agregar informacion al catalogo

def addReleaseDate(catalog,plataforma,games):
    map = catalog['platforms']
    existordermap = mp.contains(map, plataforma)
    if existordermap:
        entry = mp.get(map, plataforma)
        list_In = me.getValue(entry)
    else:
        list_In = om.newMap(omaptype='RBT',
                            comparefunction=cmpDates)
        mp.put(map, plataforma, list_In)
    AddInTrees(list_In, games)

def AddInTrees(arbol,game):
    existordermap = om.contains(arbol, game['Release_Date'] )
    if existordermap:
        entry = om.get(arbol, game['Release_Date'])
        list_In = me.getValue(entry)
    else:
        list_In =lt.newList('ARRAY_LIST')
        om.put(arbol, game['Release_Date'], list_In)
    lt.addLast(list_In, game)

def AddTreeTop (arbol, game):
    existordermap = om.contains(arbol, game['Name'] )
    if existordermap:
        entry = om.get(arbol, game['Name'])
        list_In = me.getValue(entry)
    else:
        list_In =lt.newList('ARRAY_LIST')
        om.put(arbol, game['Name'], list_In)
    lt.addLast(list_In, game)

def AddInPlayers(catalog,games):
    map = catalog['name_players']
    existordermap = om.contains(map, games['Players_0'] )
    if existordermap:
        entry = om.get(map, games['Players_0'])
        list_In = me.getValue(entry)
    else:
        list_In =lt.newList('ARRAY_LIST')
        om.put(map,games['Players_0'], list_In)
    lt.addLast(list_In, games)

def addRecordDate(catalog,games):
    map = catalog['recordsEntreFechas']
    existordermap = om.contains(map, games['Record_Date_0'])
    if existordermap:
        entry = om.get(map, games['Record_Date_0'])
        valor = me.getValue(entry)
    else:
        valor = lt.newList('ARRAY_LIST')
        om.put(map, games['Record_Date_0'], valor)
    lt.addLast(valor,games)

def addRecordTiempos(catalog,games):
    map = catalog['RecordEntreTiempos']
    existordermap = om.contains(map, float(games['Time_0']))
    if existordermap:
        entry = om.get(map, float(games['Time_0']))
        valor = me.getValue(entry)
    else:
        valor = lt.newList('ARRAY_LIST')
        om.put(map, float(games['Time_0']), valor)
    lt.addLast(valor,games)

def addRegistroIntentos(catalog, games):

    map=catalog["registros_rango_intentos"]
    existordermap=om.contains(map,int(games["Num_Runs"]))
    if existordermap:
        entry=om.get(map,int(games["Num_Runs"]))
        valor=me.getValue(entry)
    else:
        valor=lt.newList("ARRAY_LIST")
        om.put(map,int(games["Num_Runs"]),valor)
        
    lt.addLast(valor,games)

def addRecordYears(catalog,games):
    map = catalog['years']
    existordermap = om.contains(map, games['Lanzamiento'])
    if existordermap:
        entry = om.get(map, games['Lanzamiento'])
        valor = me.getValue(entry)
    else:
        valor = lt.newList('ARRAY_LIST')
        om.put(map, games['Lanzamiento'], valor)
    lt.addLast(valor,games)

def AddIds(catalog,games):
    map = catalog['Ids']
    existordermap = mp.contains(map, games['Game_Id'])
    if existordermap:
        pass
    else:
        mp.put(map, games['Game_Id'], {'Name':games['Name'],'AnioLanzamiento':games['Release_Date'][:4],'plataforma':games['Platforms']})

def addTop (catalog, games, plataformas): 
    map = catalog['top']
    existordermap = mp.contains(map, plataformas)
    if existordermap:
        entry = mp.get(map, plataformas)
        list_In = me.getValue(entry)
    else:
        list_In = om.newMap(omaptype='RBT',
                            comparefunction=cmpDates)
        mp.put(map, plataformas, list_In)
    AddTreeTop(list_In, games)
# Funciones para creacion de datos
# Funciones de consulta

def GetRangodeFechas(catalogo,plataforma,limite_inf,limite_max):
    resp = None
    title = mp.get(catalogo['platforms'], plataforma)
    if title:
        arbol = me.getValue(title)
        resp = om.values(arbol,limite_inf,limite_max)
        for listas in lt.iterator(resp):
            listas = merge.sort(listas,cmpReleaseDate)
    return resp,lt.size(om.valueSet(arbol))

def GetTiemposPequeños(catalogo,limite_inf,limite_max):
    resp = om.values(catalogo['recordsEntreFechas'],limite_inf,limite_max)
    for listas in lt.iterator(resp):
        listas = merge.sort(listas,cmpTimeNum)
    return resp

def getRegistrosRecientes(catalogo, limite_inferior, limite_superior):
    resultado= om.values(catalogo['RecordEntreTiempos'], limite_inferior, limite_superior)
    for listas in lt.iterator(resultado):
        listas = merge.sort(listas,cmpRecordDate)
    return resultado

def getRangodeIntentos(catalog,plataforma,intento1, intento2):
    resultado=None
    pareja=mp.get(catalog["platforms"], plataforma)
    if pareja:
        resultado=me.getValue(pareja)
        resultado=om.values(resultado,intento1,intento2)
        for listas in lt.iterator(resultado):
            if lt.size(listas)>1:
                listas=merge.sort(resultado,cmpintentos)
    return resultado

def getTiemposVeloces(catalog,intento1,intento2):
    resultado=om.values(catalog["registros_rango_intentos"],intento1,intento2)
    for listas in lt.iterator(resultado):
        listas = merge.sort(listas,cmpTime)
    return resultado

def getPlayersTimes(catalog,nombre):
    res = om.get(catalog['name_players'],nombre)
    res = me.getValue(res)
    res = merge.sort(res,cmpTime)
    return res

def getId(catalog,ids):
    res = mp.get(catalog['Ids'],ids)['value']
    return res

def getAverageYears(catalog,inferior,mayor,opcion):
    resp = om.values(catalog['years'],inferior,mayor)
    promedios = lt.newList('ARRAY_LIST')
    times=['Time_0','Time_1','Time_2']
    for listas in lt.iterator(resp):
        for juegos in lt.iterator(listas):
            valores =[]
            if 1<= opcion <= 3:
                if juegos[times[opcion-1]] != "":
                    lt.addLast(promedios,{'Promedio':round(float(juegos[times[opcion-1]]),2)})
            elif opcion ==4:
                if juegos['Time_0'] != "":
                    valores.append(float(juegos['Time_0']))
                if juegos['Time_1'] != "":
                    valores.append(float(juegos['Time_1']))
                if juegos['Time_2'] != "":
                    valores.append(float(juegos['Time_2']))
                lt.addLast(promedios,{'Promedio':round(sum(valores)/len(valores),2)})
            elif opcion == 5:
                if juegos['Num_Runs'] != "":
                    lt.addLast(promedios,{'Promedio':int(juegos['Num_Runs'])})
    return merge.sort(promedios,cmpPromedios)

def Factor_de_antiguedad(release_date):
    resultado = 0
    if int(release_date)>=2018:
        resultado = int(release_date)-2017
    elif 1998<int(release_date)<2018:
        resultado = (-1/5)*int(release_date)+ 404.6
    else: 
        resultado = 5
    return resultado

def getPlataforma(catalogo, plataforma): 
    resultado= mp.get(catalogo['top'], plataforma)
    valor= om.valueSet(me.getValue(resultado))
    total=0
    resultado = lt.newList('ARRAY_LIST')
    for listas in lt.iterator(valor):
        total+=lt.size(listas)

    for listas in lt.iterator(valor):
        TotalRuns = 0 
        cantidadjuegos=0
        name = ''
        anio = ''
        Time_Avg=0
        divisor = 0
        revenue = 0
        marketshare = 0
        cantidadjuegos=lt.size(listas)
        for registros in lt.iterator(listas):
            if registros['Misc'] == True:
                None
            else:
                TotalRuns+=int(registros['Num_Runs'])
            tiempos = 0
            dividendo = 0
            if registros['Time_0'] != "":
                tiempos+=float(registros['Time_0'])
                dividendo+=1
            if registros['Time_1'] != "":
                tiempos+=float(registros['Time_1'])
                dividendo+=1
            if registros['Time_2'] != "":
                tiempos+=float(registros['Time_2'])
                dividendo+=1
            Time_Avg+=tiempos
            divisor+=1
        name = registros['Name']
        anio= registros['Lanzamiento']
        Time_Avg1=Time_Avg/divisor
        marketshare = cantidadjuegos/total
        revenue = (math.log(TotalRuns)*Time_Avg1)/Factor_de_antiguedad(anio)
        lt.addLast(resultado,{'Name':name,'Release_Date':anio,'Stream_Revenue':round(revenue*marketshare,2),'Market_Share':round(marketshare,3),'Time_Avg':Time_Avg1,'Total_Runs':TotalRuns})
    organizado = merge.sort(resultado,cmpStream)
    return organizado,total


def MapaInteractivoInformacion(catalogo,lanzamiento,limite_inf,limite_max):
    resp = None
    resp = om.get(catalogo['years'],lanzamiento)
    resp = me.getValue(resp)
    diccionario ={}
    for valores in lt.iterator(resp):
        if float(limite_inf)<=float(valores['Time_0'])<=float(limite_max):
            paises = valores['Country_0'].split(',')
            for pais in paises:
                if pais == 'Unknown':
                    None
                else:
                    if pais in diccionario:
                        diccionario[pais]+=1
                    else:
                        diccionario[pais]=1
    return diccionario



# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def cmpDates(date1,date2):
    resultado = 0
    if date1> date2:
        resultado = 1
    elif date1<date2:
        resultado = -1
    return resultado

def cmpplayers2(date1,date2):
    resultado = 0
    if date1> date2:
        resultado = 1
    elif date1<date2:
        resultado = -1
    return resultado


def cmpintentos(intento1,intento2):
    resultado=0
    if int(intento1>intento2):
        resultado=1
    elif int(intento1<intento2):
        resultado=-1
    return resultado

def cmpTiempos(tiempo1,tiempo2):
    resp = 0
    if float(tiempo1>tiempo2):
        resp=-1
    elif float(tiempo1<tiempo2):
        resp=1
    return resp 

def cmpReleaseDate(game1,game2):
    try:
        resultado = False
        if game1['Release_Date']<game2['Release_Date']:
            resultado = True
        elif game1['Release_Date']==game2['Release_Date']:
            if game1['Abbrreviation']<game2['Abbrreviation']:
                resultado = True
            elif game1['Name']<game2['Name']:
                resultado = True
        return resultado
    except:
        pass

def cmpTime(game1,game2):
    try:
        resultado = False
        if float(game1['Time_0']>game2['Time_0']):
            resultado = True
        elif float(game1['Time_0']==game2['Time_0']):
            if game1['Record_Date_0']<game2['Record_Date_0']:
                resultado = True
            elif game1['Name']<game2['Name']:
                resultado = True
        return resultado
    except:
        pass

def cmpTimeNum(game1,game2):
    try:
        resultado = False
        if float(game1['Time_0']>game2['Time_0']):
            resultado = True
        elif float(game1['Time_0']==game2['Time_0']):
            if game1['Num_Runs']<game2['Num_Runs']:
                resultado = True
            elif game1['Name']<game2['Name']:
                resultado = True
        return resultado
    except:
        pass

def cmpRecordDate(game1,game2):
    try:
        resultado = False
        if float(game1['Record_Date_0']>game2['Record_Date_0']):
            resultado = True
        elif float(game1['Record_Date_0']==game2['Record_Date_0']):
            if game1['Num_Runs']<game2['Num_Runs']:
                resultado = True
            elif game1['Name']<game2['Name']:
                resultado = True
        return resultado
    except:
        pass

def cmpPromedios(intento1,intento2):
    resultado=False
    if float(intento1['Promedio']<intento2['Promedio']):
        resultado=True
    return resultado
    
def cmpStream(intento1,intento2):
    resultado=False
    if float(intento1['Stream_Revenue']>intento2['Stream_Revenue']):
        resultado=True
    return resultado