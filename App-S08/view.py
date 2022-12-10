"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from tabulate import tabulate
import pandas
import folium
import webbrowser
assert cf
default_limit = 3000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""



def printMenu():
    print("Bienvenido")
    print("c- Cargar información en el catálogo")
    print("a- Cargar analyzer")
    print("1- Reportar los videojuegos de una plataforma en un rango de tiempo.")
    print("2- Reportar los récords más veloces de los mejores tiempos de un jugador en específico. ")
    print("3- Conocer los registros más veloces en un rango de intentos.")
    print("4- Conocer los registros más lentos dentro de un rango de fechas.")
    print("5- Conocer los registros más recientes para un rango de tiempos record.")
    print("6- Diagramar un histograma de propiedades para los registros en un rango de años.")
    print("7- Encontrar el Top N de los videojuegos más rentables para retransmitir.")
    print("8- Graficar la distribución de intentos por país en un rango de años de publicación.")


gamesfile = "Speedruns/game_data_utf-8-large.csv"
categoryfile = "Speedruns/category_data_utf-8-large.csv"




def tabulateGeneral(lista,cols,width):
    df = pandas.DataFrame(lt.iterator(lista),columns=cols)
    frames = [df.head(3),df.tail(3)]
    dffinal = pandas.concat(frames)
    tabulador = tabulate(dffinal,maxcolwidths=width,tablefmt="grid",headers=cols,showindex=False)
    return tabulador

def tabulateReq1(lista,cols,width):
    df = pandas.DataFrame(lt.iterator(lista),columns=cols)
    tabulador = tabulate(df.head(5),maxcolwidths=width,tablefmt="grid",headers=cols,showindex=False)
    return tabulador

def subTabulateReq(lista_dt,subcols,subwidth):
    df = pandas.DataFrame(lt.iterator(lista_dt),columns=subcols)
    
    tabulador = tabulate(df,headers=subcols,maxcolwidths=subwidth,tablefmt="grid",showindex=False)
    return tabulador


def tabulateReq3(lista,subcols,subwidth):
    tablas = lt.newList("ARRAY_LIST",cmpfunction=None)
    for item in lt.iterator(lista):
        itemcopy = {"Num_Runs":None,"Count":None,"Details":None}
        itemcopy["Num_Runs"] = item["Num_Runs"]
        itemcopy["Count"] = item["Count"]

        subvalor = item["Details"]
       
        
        newitem = subTabulateReq(subvalor,subcols,subwidth)

        itemcopy["Details"] = newitem
        lt.addLast(tablas,itemcopy)


    df = pandas.DataFrame(lt.iterator(tablas))
    frames = [df.head(3),df.tail(3)]
    dffinal = pandas.concat(frames)
    #dffinal = dffinal[::-1]
    tabulador = tabulate(dffinal,tablefmt="grid",headers="keys",showindex=False)
    return tabulador

def tabulateReq4(lista,subcols,subwidth):
    tablas = lt.newList("ARRAY_LIST",cmpfunction=None)
    for item in lt.iterator(lista):
        itemcopy = {"Record_Date_0":None,"Count":None,"Details":None}
        itemcopy["Record_Date_0"] = item["Record_Date_0"]
        itemcopy["Count"] = item["Count"]

        subvalor = item["Details"]
        newitem = subTabulateReq(subvalor,subcols,subwidth)

        itemcopy["Details"] = newitem
        lt.addLast(tablas,itemcopy)


    df = pandas.DataFrame(lt.iterator(tablas))
    frames = [df.head(3),df.tail(3)]
    dffinal = pandas.concat(frames)
    dffinal = dffinal[::-1]
    tabulador = tabulate(dffinal,tablefmt="grid",headers="keys",showindex=False)
    return tabulador

def tabulateReq5(lista,subcols,subwidth):
    tablas = lt.newList("ARRAY_LIST",cmpfunction=None)
    for item in lt.iterator(lista):
        itemcopy = {"Time_0":None,"Count":None,"Details":None}
        itemcopy["Time_0"] = item["Time_0"]
        itemcopy["Count"] = item["Count"]

        subvalor = item["Details"]
        newitem = subTabulateReq(subvalor,subcols,subwidth)

        itemcopy["Details"] = newitem
        lt.addLast(tablas,itemcopy)


    df = pandas.DataFrame(lt.iterator(tablas))
    frames = [df.head(3),df.tail(3)]
    dffinal = pandas.concat(frames)
    tabulador = tabulate(dffinal,tablefmt="grid",headers="keys",showindex=False)
    return tabulador


def tabulateReq6(intervalos,width):
    dt = {}
    for key,val in intervalos.items():
        dt[key] = lt.iterator(val)
    tabulador = tabulate(dt,tablefmt="grid",headers="keys",maxcolwidths=width)
    return tabulador

def tabulateReq7(lista,cols,width,top):
    df = pandas.DataFrame(lt.iterator(lista),columns=cols)
    tabulador = tabulate(df.head(int(top)),maxcolwidths=width,tablefmt="grid",headers=cols,showindex=False)
    return tabulador
catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if inputs[0] == "c":
        print("Cargando información de los archivos ....")
        cont = controller.init()

    elif inputs[0] == "a":
        print("\nCargando información de juegos y registros ....")
        controller.loadData(cont,gamesfile,categoryfile)
        print("Total de registros cargados: ",lt.size(cont["registers"]))
        print("Total de videojuegos cargados: ",lt.size(cont["games"]))

        print("The first 3 and last 3 games in content range are...:")
        print(tabulateGeneral(cont["games"],["Name","Genres","Platforms","Total_Runs","Release_Date"],[None,10,15,None,None]))
        
        print("The first 3 and last 3 speedruns in content range are...:")
        print(tabulateGeneral(cont["registers"],["Name","Category","Subcategory","Players_0","Country_0","Time_0","Record_Date_0"],[None,None,None,10,10,None,None]))

    elif int(inputs[0]) == 1:
        plataforma = input("Ingrese la plataforma: ")
        date_lo = input("Ingrese el límite inferior de fecha de lanzamiento: ")
        date_hi = input("Ingrese el límite superior de fecha de lanzamiento: ")
        print("{} Req No. 1 Inputs {}".format("="*15,"="*15))
        print("Games released between '{}' and '{}'\nIn platform: '{}'\n".format(date_lo,date_hi,plataforma))

        time1,tamaniolista,lista_juegos = controller.gamesinRange(cont,date_lo,date_hi,plataforma)
        print("Available games in '{}': {}".format(plataforma,tamaniolista))
        print("Date range between '{}' and '{}'".format(date_lo,date_hi))
        print("Released games: {}".format(tamaniolista))
        print(tabulateReq1(lista_juegos,["Name","Abbreviation","Genres","Platforms","Total_Runs","Release_Date"],[None,None,10,10,None,None]))
        print("Time: ",time1)
    
    elif int(inputs[0]) == 2:
        jugador = input("Ingrese el nombre del jugador: ")
        time2,tamaniolista,lista_registros = controller.fastestRecordsPlayer(cont,jugador)

        print("El número total de registros donde el mejor tiempo lo tenga " + jugador +":",tamaniolista)
        print("The first 5 registers in content range are...:")
        print(tabulateReq1(lista_registros,["Time_0","Record_Date_0","Name","Players_0","Country_0","Num_Runs","Platforms","Genres","Category","Subcategory"],[None,10,10,10,10,None,10,10,5,None]))
        print("Time: ", time2)

    elif int(inputs[0]) == 3:
        run_lo = input("Ingrese el límite inferior de intentos: ")
        run_hi = input("Ingrese el límite superior de intentos: ")
        print("{} Req No. 3 Inputs {}".format("="*15,"="*15))
        print("Category records between '{}' and '{}' attempts.\n".format(run_lo,run_hi))

        time3,tamanio,lista_tiempos = controller.registrosVeloces(cont,run_lo,run_hi)
        print("{} Req No. 3 Answer {}".format("="*15,"="*15))
        print("Attempts between '{}' and '{}'".format(run_lo,run_hi))
        print("Total records: \n",tamanio)
        print("{} Videogames release details {}".format("-"*6,"-"*6))
        print("There are '{}' elements in range.".format(tamanio))
        print("The first 3 and last 3 in range are:")

        print(tabulateReq3(lista_tiempos,["Time_0","Record_Date_0","Name","Players_0","Country_0","Platforms","Genres","Category","Subcategory","Release_Date"]\
            ,[None,None,None,10,None,10,10,None,10,None]))
        
        print("Time: ",time3)
        
    elif int(inputs[0]) == 4:
        date_lo = input("Ingrese el límite inferior de fecha de lanzamiento: ")
        date_hi = input("Ingrese el límite superior de fecha de lanzamiento: ")
        print("{} Req No. 4 Inputs {}".format("="*15,"="*15))
        print("Category records between '{}' and '{}' datetime.\n".format(date_lo,date_hi))

        time4,tamanio,lista_tiempos = controller.registrosLentos(cont,date_lo,date_hi)
        print("{} Req No. 4 Answer {}".format("="*15,"="*15))
        print("Attempts between '{}' and '{}'".format(date_lo,date_hi))
        print("Total records: \n",tamanio)
        print("{} Videogames release details {}".format("-"*6,"-"*6))
        print("There are '{}' elements in range.".format(tamanio))
        print("The first 3 and last 3 in range are:")

        print(tabulateReq4(lista_tiempos,["Num_Runs","Time_0","Name","Players_0","Country_0","Platforms","Genres","Category","Subcategory","Release_Date"]\
            ,[None,None,None,10,None,10,10,None,10,None]))
        
        print("Time: ",time4)

    elif int(inputs[0]) == 5:
        time_lo = input("Ingrese el límite inferior de los tiempos: ")
        time_hi = input("Ingrese el límite superior de los tiempos: ")

        print("{} Req No. 5 Inputs {}".format("="*15,"="*15))
        print("Category records between '{}' and '{}' runtime.\n".format(time_lo,time_hi))

        time5,tamanio,lista_dates = controller.registrosRecientes(cont,time_lo,time_hi)
        print("{} Req No. 5 Answer {}".format("="*15,"="*15))
        print("Attempts between '{}' and '{}'".format(time_lo,time_hi))
        print("Total records: \n",tamanio)
        print("{} Videogames release details {}".format("-"*6,"-"*6))
        print("There are '{}' elements in range.".format(tamanio))
        print("The first 3 and last 3 in range are:")

        print(tabulateReq5(lista_dates,["Record_Date_0","Num_Runs","Name","Players_0","Country_0","Platforms","Genres","Category","Subcategory","Release_Date"]\
            ,[None,None,None,10,None,10,10,None,10,None]))

        print("Time: ",time5)

    elif int(inputs[0]) == 6:
        anio_lo = input("Ingrese el límite inferior del año de lanzamiento: ")
        anio_hi = input("Ingrese el límite superior del año de lanzamiento: ")
        segmentos = input("Ingrese el número de segmentos en que se divide el rango de propiedad en el histograma: ")
        niveles = input("Ingrese el número de niveles en que se dividen las marcas de jugadores en el histograma: ")
        op = input("Seleccione lo que desea consultar (Times,Time_Avg,Num_runs): ")
        time6, lowest_value, max_value, tamanio, dt_intervalos = controller.diagramarHistograma(cont,anio_lo,anio_hi,segmentos,niveles,op)

        print("{} Req No. 6 Inputs {}".format("="*15,"="*15))
        print("Count map (histograma) of the feature: '{}'\nData between release years of '{}' and '{}'".format(op,anio_lo,anio_hi))
        print("Number of bins: ",segmentos)
        print("Registered attempts per scale: ",niveles)

        print("{} Req No. 6 Answer {}".format("="*15,"="*15))
        print("There are '{}' attempts on record.".format(tamanio))
        print("Lowest value: '{}'".format(round(lowest_value,2)))
        print("Highest value: '{}'".format(max_value))
        print("The histogram counts '{}' attempts.".format(tamanio))
        print("'{}' Histogram with '{}' bins and '{}' attempts per mark lvl.".format(op,segmentos,niveles))

        print(tabulateReq6(dt_intervalos,[None,None,None,15]))
        print("NOTE: Each '*' represents 7 attempts.")

        print("Time: ",time6)
    
    elif int(inputs[0]) == 7:
        plataforma = input("Ingrese la plataforma de interés: ")
        top = input("Ingrese el top de los videojuegos para retransmitir: ")


        time7,tamanio,lista_rentabilidad = controller.calcularRentabilidad(cont,plataforma,top)
        print("tamaño",tamanio)
        print("Top ",top)
        print(tabulateReq7(lista_rentabilidad,["Game_Id","Name","Release_Date","Platforms","Genres","Stream_Revenue","Market_Share","Time_average","Total_Runs","Popularity","Antiquity"],[None,10,None,10,10,None,None,None,None,None,None],top))

        print("Time: ",time7)
    
    elif int(inputs[0]) == 8:
        release = input("Ingrese el año de publicación sobre el cual se quiere obtener los histogramas: ")
        time_min = input("Ingrese el límite inferior de la duración del mejor tiempo del récord: ")
        time_hi = input("Ingrese el límite superior de la duración del mejor tiempo del récord: ")
        time8,size,mapa= controller.graficar(cont,release,time_min,time_hi)
        print("Número total de registros de speedrun en '{}' en el rango de tiempos desde '{}' hasta '{}': {}".format(release,time_min,time_hi,size))
        mapa.save("m.html")
        webbrowser.open("m.html")

        print("Time: ",time8)
    
    else:
        sys.exit(0)
sys.exit(0)
