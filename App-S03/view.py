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
assert cf
import datetime as dt
from tabulate import tabulate
from time import time
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# Límite de recursión incrementado

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

def printMenu():
    print("Bienvenido\n")
    print("0 - Cargar información de juegos y categorías ")
    print("1 - Encontrar los videojuegos en un rango de tiempo para una plataforma ")
    print("2 - Encontrar los 5 mejores tiempos para un jugador ")
    print("3 - Mejores tiempos récord en un rango de intentos ")
    print("4 - Peores tiempos récord en un rango de fechas ")
    print("5 - Tiempos récord más recientes en un rango de tiempos ")
    print("6 - Histograma de propiedades para los tiempos en un rango de años ")
    print("7 - Top N videojuegos más rentables ")
    print("8 - Gráfica de distribución de intentos por país en un rango de años de publicación ")
    print("9- EXIT")

"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    
    if int(inputs[0]) == 0:
        control=controller.init()
        size = input("Indique el tamaño de los archivos que desea cargar (small,5pct,10pct,20pct,30pct,50pct,80pct,large):")
        print("Cargando información de los archivos ... \n")
        controller.loaddata(control,size)

        games = control["Games"]["elements"]
        categories = control["Categories"]["elements"]
        print("\nLA CARGA DE DATOS HA FINALIZADO:\n")
        print("total games: ",control["Games"]["size"])
        print("total categories: ",control["Categories"]["size"],"\n")

        table_headers = ['Game_Id','Release Date','Name','Abbreviation','Platforms','Total_Runs','Genres']
        table = []

        for i in range(3):
            game = []
            game.append(games[i]['Game_Id'])
            game.append(games[i]['Release_Date'])
            game.append(games[i]["Name"])
            game.append(games[i]['Abbreviation'])
            platformstr = ''
            platforms = games[i]['Platforms'].split(",")
            for i in range(len(platforms)):
                    if len(platformstr) == 0:
                        platformstr += "" + str(platforms[i])
                    else:
                        platformstr += "\n" + str(platforms[i])
            game.append(platformstr)
            game.append(games[i]['Total_Runs'])
            game.append(games[i]['Genres'])
            table.append(game)

        for i in range(3):
            b_game = []
            b_game.append(games[-i-1]['Game_Id'])
            b_game.append(games[-i-1]['Release_Date'])
            b_game.append(games[-i-1]["Name"])
            b_game.append(games[-i-1]['Abbreviation'])
            platformstr = ''
            platforms = games[-i-1]['Platforms'].split(",")
            for i in range(len(platforms)):
                    if len(platformstr) == 0:
                        platformstr += "" + str(platforms[i])
                    else:
                        platformstr += "\n" + str(platforms[i])
            b_game.append(platformstr)
            b_game.append(games[-i-1]['Total_Runs'])
            b_game.append(games[-i-1]['Genres'])
            table.append(b_game)

        table = tabulate(table,headers = table_headers, tablefmt = "fancy_grid")
        print(table)
        print("Dato extra de prueba:")
        print(games[0])
        print("\n")

        c_table_headers = ['Game_Id','Record_Date_0','Num_Runs','Category','Subcategory','Country_0','Players_0','Time_0']
        c_table = []

        for i in range(3):
            category = []
            category.append(categories[i]['Game_Id'])
            category.append(categories[i]['Record_Date_0'])
            category.append(categories[i]['Num_Runs'])
            category.append(categories[i]['Category'])
            category.append(categories[i]['Subcategory'])
            category.append(categories[i]['Country_0'])
            category.append(categories[i]['Players_0'])
            category.append(categories[i]['Time_0'])
            c_table.append(category)
        for i in range(3):
            bcategory = []
            bcategory.append(categories[-i-1]['Game_Id'])
            bcategory.append(categories[-i-1]['Record_Date_0'])
            bcategory.append(categories[-i-1]['Num_Runs'])
            bcategory.append(categories[-i-1]['Category'])
            bcategory.append(categories[-i-1]['Subcategory'])
            bcategory.append(categories[-i-1]['Country_0'])
            bcategory.append(categories[-i-1]['Players_0'])
            bcategory.append(categories[-i-1]['Time_0'])
            c_table.append(bcategory)
            

        ctable = tabulate(c_table,headers = c_table_headers, tablefmt = "fancy_grid")
        print(ctable)
        print("Dato extra de prueba:")
        print(categories[0])
        print("\n")
        # print(control["Platforms"])
        Platforms = control["Platforms"]

    elif int(inputs[0]) == 1:
        date_sup = dt.datetime.strptime(input("Ingrese la fecha superior para el rango: (%Y-%m-%d)"),"%Y-%m-%d")
        date_inf = dt.datetime.strptime(input("Ingrese la fecha inferior para el rango: (%Y-%m-%d)"),"%Y-%m-%d")
        platform = input("Ingrese la plataforma que desea indagar: ")
        
        start = time()

        games,ammount = controller.findbplt(date_sup,date_inf,control,platform)
        print(f"\nJuegos disponibles en en {platform}: {ammount}")
        print(f"Juegos lanzados entre {date_inf} y {date_sup} para {platform}:",games["size"]) 
        # print(games)
        
        big_table = []
        b_table_h = ["Release_Date","Details"]
        
        records = games["elements"]

        for i in range(3):
            record = []
            record.append(records[i]['Release_Date'])
            details = ""
            details += "Total runs: " + str(records[i]['Total_Runs'])
            details += "\nName: " + str(records[i]['Name'])
            details += "\nAbbreviation: " + str(records[i]['Abbreviation'])
            details += "\nPlatforms: " + str(records[i]['Platforms'])
            details += "\nGenres: " + str(records[i]['Genres'])
            record.append(details)
            big_table.append(record)
        for i in range(3):
            record = []
            record.append(records[-i-1]['Release_Date'])
            details = ""
            details += "Total runs: " + str(records[-i-1]['Total_Runs'])
            details += "\nName: " + str(records[-i-1]['Name'])
            details += "\nAbbreviation: " + str(records[-i-1]['Abbreviation'])
            details += "\nPlatforms: " + str(records[-i-1]['Platforms'])
            details += "\nGenres: " + str(records[-i-1]['Genres'])
            record.append(details)
            big_table.append(record)

        table = tabulate(big_table,headers = b_table_h, tablefmt = "fancy_grid")
        print(table)

        stop = time()
        print(f"Elapsed time: {stop - start}")
        
    elif int(inputs[0]) == 2:
        player = input("Indique el jugador que quiere buscar: ")

        start = time()

        list = controller.findply(player,control)
        if list["size"]<=5:
            for i in range(list["size"]):
                print(list["elements"][i])
                print("\n")
        else:
            for i in range(5):
                print(list["elements"][i])
                print("\n")

        stop = time()
        print(f"Elapsed time: {stop - start}")


    elif int(inputs[0]) == 3:
        sup = int(input("Ingrese la cantidad superior de intentos: "))
        inf = int(input("Ingrese la cantidad inferior de intentos: "))

        start = time()

        list = controller.findbnr(sup,inf,control)
        if list["size"]<6:
            for i in range(list["size"]):
                print(list["elements"][i])
                print("\n")
        else:
            for i in range(3):
                print(list["elements"][i])
                print("\n")
            print(list["elements"][-1])
            print("\n")
            print(list["elements"][-2])
            print("\n")
            print(list["elements"][-3])

        stop = time()
        print(f"Elapsed time: {stop - start}")

    elif int(inputs[0]) == 4:
        date_sup = dt.datetime.strptime(input("Ingrese la fecha superior para el rango: (%Y-%m-%d %H:%M:%S) "),"%Y-%m-%d %H:%M:%S")
        date_inf = dt.datetime.strptime(input("Ingrese la fecha inferior para el rango: (%Y-%m-%d %H:%M:%S) "),"%Y-%m-%d %H:%M:%S")

        start = time()

        lst=controller.findbd0(date_sup,date_inf,control)
        if lst["size"]<=6:
            for i in range(lst["size"]):
                print(lst["elements"][i])
                print("\n")
        else:
            for i in range(3):
                print(lst["elements"][i])
                print("\n")
            print(lst["elements"][-1])
            print("\n")
            print(lst["elements"][-2])
            print("\n")
            print(lst["elements"][-3])

        stop = time()
        print(f"Elapsed time: {stop - start}")

    elif int(inputs[0]) == 5:
        sup = float(input("Ingrese el tiempo superior para el rango: "))
        inf = float(input("Ingrese el tiempo inferior para el rango: "))

        start = time()

        lst = controller.firbt0(sup,inf,control)
        if lst["size"]<=6:
            for i in range(lst["size"]):
                print(lst["elements"][i])
                print("\n")
        else:
            for i in range(3):
                print(lst["elements"][i])
                print("\n")
            print(lst["elements"][-1])
            print("\n")
            print(lst["elements"][-2])
            print("\n")
            print(lst["elements"][-3])

        stop = time()
        print(f"Elapsed time: {stop - start}")

    elif int(inputs[0]) == 6:

        sup_year = input("Ingrese el año superior para el cual desea el histograma: ")
        sup = dt.datetime.strptime(sup_year+"-01-01", "%Y-%m-%d")
        inf_year = input("Ingrese el año inferior para el cual desea el histograma: ")
        inf = dt.datetime.strptime(inf_year+"-01-01", "%Y-%m-%d")
        n = int(input("Ingrese el número de casillas en el que desea dividir la información: "))
        x = int(input("Ingrese la cantidad de elementos que desea agrupar por marcador: "))
        prop = int(input("Tomando en cuenta las siguientes propiedades: \n 1) Gráfica Time_0 \n 2) Gráfica Time_1 \n 3) Gráfica Time_2 \n 4) Gráfica del promedio de los tiempos \n 5) Gráfica Num_Runs \n  Elija una opción:  "))
        
        start = time()
        
        mind,maxd,cat,counter,lvl = controller.hist(sup,inf,n,x,prop,control)
        print("\nMin value: ",mind,"\n")
        print("Max value: ",max,"\n")
        print("Bin, Count, lvl, Mark\n")
        for i in range(n):
            print(cat["elements"][i]," ",counter["elements"][i]," ",lvl["elements"][i]*"*","\n")

        stop = time()
        print(f"Elapsed time: {stop - start}")

    elif int(inputs[0]) == 7:
        plat = input("Ingrese el nombre de la plataforma: ")
        N = int(input("Ingrese el top a consultar: "))

        start = time()

        lst = controller.findtop(plat,N,control)
        for i in range(N):
            entry = mp.get(control["Games mp"],lst["elements"][i]["Game_Id"])
            print("\n",me.getValue(entry))

        stop = time()
        print(f"Elapsed time: {stop - start}")

    elif int(inputs[0]) == 8:
        pass


    else:
        sys.exit(0)
sys.exit(0)
