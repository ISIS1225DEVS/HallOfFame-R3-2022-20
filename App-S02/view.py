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
from prettytable import PrettyTable
import pandas as pd
import folium 
import time
import tracemalloc
import numpy as np
import matplotlib.pyplot as plt 

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido")
    print("*- Inicializar Programa")
    print("0- Cargar información en el catálogo")
    print("1- Reporte de videojuegos de una plataforma en un rango de tiempo")
    print("2- Reporte de record de los mejores tiempos de un jugador")
    print("3- Reporte de registros más veloces en un rango de intentos")
    print("4- Reporte de los registros más lentos dentro de un rango de fechas")
    print("5- Reporte de los registros más recientes en un rango de tiempos record")
    print("6- Histograma de tiempos para un año de publicación")
    print("7- Top 5 de videojuegso más rentables para retransmitir")
    print("8- Distribución de records por país en un año de publicación y en un rango de tiempo")
    print("\nPor favor elija una opción")


def printEleccionArchivo1():
    '''O(1)'''
    print("\nElija el tamaño de archivo que desea cargar")
    print("1- small")
    print("2- 05pct")
    print("3- 10pct")
    print("4- 20pct")
    print("5- 30pct")
    print("6- 50pct")
    print("7- 80pct")
    print("8- large")


catalog = None

#Funciones para imprimir datos
def printRegGameData(load):
    x = PrettyTable()
    x.field_names = ["Nombre", "Género", "Plataforma", "Total Runs", "Fecha de publicación"]
    x.max_width=20
    x.hrules = True
    x.align="l"

    w = PrettyTable()
    w.field_names = ["Videojuego","Game_Id", "Categoría", "Subcategoría", "Jugadores"]
    w.max_width=20
    w.hrules = True
    w.align="l"

    register = load['register']
    game = load['games']
    i = 1
    j = 1
    print("\nEstos son los primeros y últimos 3 videojuegos cargados: ")
    for g in lt.iterator(game): 
        if i <= 3 or i > lt.size(game) - 3:
            x.add_row([g["Name"], g["Genres"], g["Platforms"], g["Total_Runs"], g["Release_Date"]])
        i += 1
    print(x)
    print("\nEstos son los primeros y últimos 3 registros cargados: ")
    for reg in lt.iterator(register):
        name = controller.getRegName(load, reg) 
        if j <= 3 or j > lt.size(register) - 3:
            jugador = "Jugador: " + str(reg['Players_0']) + "\nPaís: " + str(reg['Country_0']) + "\nFecha: " + str(reg['Record_Date_0']) + "\nTiempo: " + str(reg['Time_0'])
            w.add_row([name, reg["Game_Id"], reg["Category"], reg["Subcategory"], jugador])
        j += 1
    print(w)

def printReq1(total):
    x = PrettyTable()
    x.field_names = ["Nombre", "Abrevación", "Género", "Plataforma", "Total Runs", "Fecha de publicación"]
    x.max_width=20
    x.hrules = True
    x.align="l"
    i = 1
    print("\nTotal de videojuegos en el rango de fechas: ", str(lt.size(total)))
    #print(total)
    for g in lt.iterator(total):
        gg= g['first']['info']
        #print(gg)
        if i <= 3 or i > lt.size(total) - 3:
            x.add_row([gg["Name"], gg['Abbreviation'], gg["Genres"], gg["Platforms"], gg["Total_Runs"], gg["Release_Date"]])
        i += 1
    
    print(x)

def getTime():
    '''O(1)'''
    return float(time.perf_counter()*1000)

def deltaTime(start, end):
    '''O(1)'''
    elapsed = float(end - start)
    return elapsed

def getMemory():
    return tracemalloc.take_snapshot()

def deltaMemory(stop_memory,start_memory):
    memory_diff = stop_memory.compare_to(start_memory,"filename")
    delta_memory = 0.0
    for stat in memory_diff:
        delta_memory += stat.size_diff
    delta_memory/=1024
    return delta_memory
    
def printReq4(regs, load):
    w = PrettyTable()
    w.field_names = ["Videojuego", "Game_Id", "Categoría","Subcategoría", "Num_Runs", "Jugador","Nacionalidad", "Tiempo 0", "Fecha"]
    w.max_width=20
    w.hrules = True
    w.align="l"
    i = 0
    for reg in lt.iterator(regs):
        name = controller.getRegName(load, reg) 
        if i <= 3 or i > lt.size(regs) - 3:
            w.add_row([name, reg["Game_Id"], reg["Category"],reg['Subcategory'], reg['Num_Runs'], reg['Players_0'], reg['Country_0'], reg['Time_0'], reg["Record_Date_0"]])
        i += 1
    print(w)
def printReq7(lstgames, top):
    w = PrettyTable()
    w.field_names = ["Videojuego", "Release_Date", "Platforms","Genres", "Stream_revenue", "Market_Share","Time_Avg", "Total_Runs"]
    w.max_width=20
    w.hrules = True
    w.align="l"
    i = 0
    for g in lt.iterator(lstgames): 
        if i < int(top):
            w.add_row([g["Name"], g['Release_Date'], g['Platforms'], g['Genres'], g['streamrevenue'], g['marketshare'], g['time_average'], g['Total_Runs']])
        i += 1
    print(w)
def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('True', 'true', 'TRUE', 'T', 't', '1', 1, True):
        return True
    else:
        return False

def printReg3(total):
     x = PrettyTable()
     x.field_names = ["Num_Runs", "Count", "Details"]
     x.max_width=20
     x.hrules = True
     x.align="l"
     i = 1

     w = PrettyTable()
     w.field_names = ["Time_0","Record_date_0","Name","Players_0","Country","Plataforms","Genres","Category","Subcategory","Release_date"] 
     w.max_width=20
     w.hrules = True
     w.align="l"
     i = 0
     
    
     for g in lt.iterator(total):
        if i <= 6:
             x.add_row([g["Num_Runs"], g["name"],g["Time_0"]])
        i += 1
     print(x)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if str(inputs[0]) == '*':
        print("Inicializando ....")
        catalog = controller.init()

    elif int(inputs[0]) == 0:
        printEleccionArchivo1()
        input_archivo = input('Seleccione una opción para continuar\n')
        if input_archivo == "1":
            id = "small"
        elif input_archivo == "2":
            id = "5pct"
        elif input_archivo == "3":
            id = "10pct"
        elif input_archivo == "4":
            id = "20pct"
        elif input_archivo == "5":
            id = "30pct"
        elif input_archivo == "6":
            id = "50pct"
        elif input_archivo == "7":
            id = "80pct"
        elif input_archivo == "8":
            id = "large,"
        else:
            print("\nDebe elegir una opción válida\n")
            break

        #start_time = getTime()

        

        print("\nSe ha realizado la elección de archivo a cargar.\n")
        print("Cargando información de los archivos ....")
        load = controller.loadData(catalog, id)
        tamReg = controller.cons_catalog_findSize(catalog,"register")
        tamGame = controller.cons_catalog_findSize(catalog,"games")
        print("Registros cargados: ", tamReg)
        print("Videojuegos cargados: ", tamGame)
        printRegGameData(load)

        #end_time = getTime()
        #delta_time = deltaTime(start_time, end_time
        #print("Delta tiempo requerimiento: {}".format(delta_time))

    
        #end_time = getTime()
        #delta_time = deltaTime(start_time, end_time)
        #print("Delta tiempo requerimiento: {}".format(delta_time))

        
    
    elif int(inputs[0]) == 1:
        #Espacio para poner req1
        start_time = getTime()
        print("\nBuscando videojuegos en un rango de fechas: ")
        initialDate = input("Fecha Inicial (DD/MM/YYYY): ")
        finalDate = input("Fecha Final (DD/MM/YYYY): ")
        platform = input("Plataforma: ")
        print("Desea observar el uso de memoria? (True/False)")
        mem = input("Respuesta: ")
        mem = castBoolean(mem)
        total = controller.getGamesByRange(catalog, initialDate, finalDate, platform, mem)
        #print(total)
        printReq1(total[0])
        print("Altura del arbol: " + str(controller.indexHeight(catalog)))
        print("Elementos en el arbol: " + str(controller.indexSize(catalog)))
        print("Menor Llave: " + str(controller.minKey(catalog)))
        print("Mayor Llave: " + str(controller.maxKey(catalog)))
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))

    elif int(inputs[0]) == 2:
        #Espacio para poner req2
        start_time = getTime()
        player = input('Introduzca el nombre del jugador a buscar: ')
        
        #start_time = getTime()
        tracemalloc.start()
        start_memory = getMemory()

        data_player = controller.req2(catalog,player)

        #print(data_player)
        print('\n'+'-'*30)
        print('\nEl número de registros del jugador {} en donde obtuvo el mejor tiempo es: {}'.format(player,len(data_player)))
        headers = ['Time_0','Record_Date_0','Name','Players_0','Country_0','Num_Runs','Category','Subcategory']
        x = PrettyTable()
        x.field_names = headers
        longitud = len(data_player)
        if longitud<=5:
            for row in data_player:
                x.add_row([row[i] for i in headers])
        else:
            for row in (data_player[0:5]):
                x.add_row([row[i] for i in headers])
        print('\n'+'-'*30+'\n')
        print(x)
        print('\n'+'-'*30+'\n')

        #end_time = getTime()
        #delta_time = deltaTime(start_time, end_time)
        #print("Delta tiempo requerimiento: {}".format(delta_time))

        end_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(end_memory,start_memory)
        print("Delta memoria requerimiento: {}".format(delta_memory))
        
    elif int(inputs[0]) == 3:
        start_time = getTime()
        #Espacio para poner req3
        print("\nBuscando los registros con menor duracion entre: ")
        iRuns = input("Limite de intentos inferior: ")
        fRuns = input("Limite de intentos superior: ")
        total = controller.ordernarReg3(catalog,iRuns,fRuns)
        printReg3(total) 
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))
    elif int(inputs[0]) == 4:
        start_time = getTime()
        #Espacio para poner req4
        iDate = input("Fecha inicial (%Y-%m-%dT%H:%M:%S%z): ")
        fDate = input("Fecha final (%Y-%m-%dT%H:%M:%S%z): ")
        regs = controller.ordenarReq4(catalog, iDate, fDate)
        printReq4(regs, load)
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))

    elif int(inputs[0]) == 5:
        #Espacio para poner req5
        start_time = getTime()
        print('Introduzca los límites de tiempo: ')
        l_inf = float(input('Límite Inferior: '))
        l_sup = float(input('Límite Superior: '))

        #start_time = getTime()
        tracemalloc.start()
        start_memory = getMemory()

        data_interval = controller.req5(catalog,l_inf,l_sup)

        #print(data_interval)
        longitud = len(data_interval)
        headers = ['Time_0','Record_Date_0','Num_Runs','Name','Players_0','Country_0','Category','Subcategory']
        x = PrettyTable()
        x.field_names = headers
        if longitud<=6:
            for row in data_interval:
                x.add_row([row[i] for i in headers])
        else:
            for row in (data_interval[0:3]+data_interval[longitud-3:longitud]):
                x.add_row([row[i] for i in headers])
        print('\n'+'-'*30)
        print('\nEl número de registros dentro del intervalo son: {}'.format(len(data_interval)))
        print('\n'+'-'*30+'\n')
        print(x)

        #end_time = getTime()
        #delta_time = deltaTime(start_time, end_time)
        #print("Delta tiempo requerimiento: {}".format(delta_time))

        end_memory = getMemory()
        tracemalloc.stop()
        delta_memory = deltaMemory(end_memory,start_memory)
        print("Delta memoria requerimiento: {}".format(delta_memory))

    elif int(inputs[0]) == 6:
        #Espacio para poner req6
        start_time = getTime()
        iDate = input("Limite inferior del año de lanzamiento: ")
        fDate = input("Limite superior del año de lanzamiento: ")
        segmentos = float(input("Número de segmentos: "))
        niveles = float(input("Número de niveles: "))
        print("Seleccione el tipo de consulta que desea realizar: ")
        print("1. El mejor tiempo registrado (Time_0), el segundo mejor tiempo (Time_1), el tercer mejor tiempo (Time_2).")
        print("2. El tiempo promedio registrado")
        print("3. El número de intentos registrados")
        seleccion = input("\n Elija una opción valida: ")
        datos = controller.getReq6(catalog, iDate, fDate)
        if int(seleccion) == 1:
            lst = controller.ordenarReq6Time_0(datos)
            primero = round(float(lt.getElement(lst, 1)['Time_0']),2)
            ultimo = round(float(lt.getElement(lst, lt.size(lst))['Time_0']),2)
            tamrang = round(((primero + ultimo)/segmentos),2)
            i = 0
            bins = lt.newList()
            while i < segmentos:
                count = 0
                lim = primero + tamrang
                
                for reg in lt.iterator(lst):
                    if float(reg['Time_0']) > primero and float(reg['Time_0']) < lim:
                        count += 1
                mark = int(count//niveles)
                bin = [primero, lim, count, mark]
                lt.addLast(bins, bin)        
                primero = lim        
                i += 1
        elif int(seleccion) == 2:
            lst = controller.ordenarReq6Prom(datos)
            primero = round(lt.getElement(lst, 1)['Promedio'],2)
            ultimo = round(lt.getElement(lst, lt.size(lst))['Promedio'],2)
            tamrang = round(((primero + ultimo)/segmentos),2)
            i = 0
            bins = lt.newList()
            while i < segmentos:
                count = 0
                lim = primero + tamrang
                
                for reg in lt.iterator(lst):
                    if float(reg['Promedio']) > primero and float(reg['Promedio']) < lim:
                        count += 1
                mark = int(count//niveles)
                bin = [primero, lim, count, mark]
                lt.addLast(bins, bin)        
                primero = lim        
                i += 1
        elif int(seleccion) == 3:
            lst = controller.ordenarReq6Num(datos)
            primero = round(lt.getElement(lst, 1)['Num_Runs'],2)
            ultimo = round(lt.getElement(lst, lt.size(lst))['Num_Runs'],2)
            tamrang = round(((primero + ultimo)/segmentos),2)
            i = 0
            bins = lt.newList()
            while i < segmentos:
                count = 0
                lim = primero + tamrang
                
                for reg in lt.iterator(lst):
                    if float(reg['Num_Runs']) > primero and float(reg['Num_Runs']) < lim:
                        count += 1
                mark = int(count//niveles)
                bin = [primero, lim, count, mark]
                lt.addLast(bins, bin)        
                primero = lim        
                i += 1
        else:
            print("Seleccione una opción valida")
            sys.exit(0)

        x = PrettyTable()
        x.field_names = ["bin", "Count", "lvl", "mark"]
        x.max_width=30
        x.hrules = True
        x.align="l"
        canequita =[]
        limites =[]
        for bin in lt.iterator(bins):
             mark = "* "*bin[3]
             x.add_row([(bin[0], bin[1]), bin[2], bin[3], mark])
             caneca = ['('+ str(bin[0]) + str(bin[1]) +')', bin[2]]
             limites += bin[0:2]
             canequita.append(caneca)
        print(x)
        histo =pd.DataFrame(canequita)
        histo.columns = ['limites', 'count']
        plt.figure()
        histo.hist()
        plt.savefig('hist')
        #print(histo)

        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))


    elif int(inputs[0]) == 7:
        #Espacio para poner req7
        start_time = getTime()
        platform = input("Plataforma: ")
        top = input("Ingrese el número de Top N: ")
        lstgames = controller.getIdByPlatform(catalog, platform)
        regs = controller.getRegsByPlatform(catalog, lstgames)
        mapareg = regs[0]
        regtotal = regs[1]
        controller.calculosreq7(lstgames, catalog, regs, platform)
        lst = controller.ordenarReq7(lstgames)
        printReq7(lst, top)
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))

    elif int(inputs[0]) == 8:
        #Espacio para poner req8 (BONO)
        start_time = getTime()
        anio = input('Introduzca el año de publicación: ')
        print('\nIntroduzca los límites de tiempo: ')
        l_inf = float(input('Límite Inferior: '))
        l_sup = float(input('Límite Superior: '))
        interactive_graph = controller.req8(catalog,anio,l_inf,l_sup)
        print('\n'+'-'*30)
        print('\nEl número de registros dentro del intervalo y año señalados son: {}'.format(len(interactive_graph)))
        print('\n'+'-'*30+'\n')
        m = folium.Map(location=[0,0])
        end_time = getTime()
        delta_time = deltaTime(start_time, end_time)
        print("Delta tiempo requerimiento: {}".format(delta_time))
    else:
        sys.exit(0)
sys.exit(0)