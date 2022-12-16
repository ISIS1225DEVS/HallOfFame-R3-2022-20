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
from App import controller
from DISClib.ADT import list as lt
from datetime import datetime
from tabulate import tabulate
from textwrap import wrap
assert cf

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


cont = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("//"+"-" *50 +"//")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información")
    print("3- Encontrar los videojuegos publicados en un rango de tiempo para una plataforma")
    print("4- Reportar los récords más veloces de los mejores tiempos de un jugador en específico")
    print("5- Reportar los registros más veloces dentro de un rango de intentos")
    print("6- Reportar los registros más lentos dentro de un rango de fechas")
    print("7- Reportar los registros más recientes en un rango de tiempos récord")
    print("8- Graficar el histograma de tiempos para un año de publicación")
    print("9- Encontrar el top N DE videojuegos más rentables para retransmitir")
    print("10 - Mostrar la distribución de récords por país en un año de publicación en un rango de tiempos")
    print("//"+"-" *50 + "//")
    print("0- Salir")

def imprimirTitulos(titulos):

    titulos_print = []
    for titulo in lt.iterator(titulos):
        titulo_print = titulo.copy()
        for key in titulo_print.keys():
            if type(titulo_print[key]) == list:
                titulo_print[key] = '\n'.join(titulo_print[key])
        titulos_print.append(titulo_print)
    return tabulate(titulos_print, headers='keys', tablefmt='grid', stralign='left', numalign='left')


def printLoadData(cont):
    games = cont['games']
    categories = cont['categories']

    print('\n')
    print('-'*50)
    print('Se cargaron ' + str(lt.size(games)) + ' videojuegos en total.')
    print('-'*50)
    print('Los 3 primeros y los 3 ultimos videojuegos cargadas fueron:')
    print('-'*50)
    games_six = controller.getSix(games)
    print(imprimirTitulos(games_six))
    print('\n')
    print('-'*50)
    print('Se cargaron ' + str(lt.size(categories)) + ' registros en total.')
    print('-'*50)
    print('Los 3 primeros y los 3 ultimos registros cargadas fueron:')
    print('-'*50)
    cate_six = controller.getSix(categories)
    print(imprimirTitulos(cate_six))

#=====================================
#Requerimiento 1
#=====================================

def printGameInRange(total, lst, totalgames, platform):
    print('-'*70)
    print('El número total de videojuegos disponibles en ' + platform + ' es de ' + str(total))
    print('-'*70)
    print('El número total de videojuegos disponibles en el rango es de ' + str(totalgames))
    print('-'*70)
    lst_six= controller.getSix(lst)
    sublist = lt.newList()
    print('-'*70)
    print('Imprimiendo las primeras 3 y las ultimas 3 Release_Date cargadas de ' + str(lt.size(lst)))
    for release in lt.iterator(lst_six):
        for i in lt.iterator(release['games']):
            l = {'Total_Runs': str(i['Total_Runs']),
                'Name':i['Name'], 
                'Abbreviation': i['Abbreviation'], 
                'Platforms':i['Platforms'], 
                'Genres':i['Genres']}
            exist = False
            position = 1
            for b in lt.iterator(sublist):
                if b['Release_Date'] == i['Release_Date']:
                    exist = True
                    position_t = position
                position += 1 
            if exist == True:
                x = lt.getElement(sublist,position_t)
                x['Count'] += 1
                lt.addLast(x['Details'], l)
            else:
                dicct = {'Release_Date': i['Release_Date'],
                        'Count' : 1,
                        'Details': lt.newList()}
                lt.addLast(dicct['Details'],l)
                lt.addLast(sublist, dicct)
    for b in lt.iterator(sublist):
        b['Details']=[imprimirTitulos(b['Details'])]
    sublist = controller.sortByReleaseDate(sublist)
    print(imprimirTitulos(sublist))

#=====================================
#Requerimiento 2
#=====================================
def printJugador(lst, jugador):
    lst_res = lt.newList()
    num_runs = 0
    if lt.size(lst) > 5:
        lst_5 = lt.subList(lst,1,5)
    else:
        lst_5 = lst
    for registro in lt.iterator(lst_5):
        dicct = {'Time_0': registro['registro']['Time_0'],
                'Record_Date_0': registro['registro']['Record_Date_0'],
                'Name': registro['game']['info']['Name'],
                'Players_0': registro['registro']['Players_0'],
                'Country_0': registro['registro']['Country_0'],
                'Num_Runs': registro['registro']['Num_Runs'],
                'Platforms': registro['game']['info']['Platforms'],
                'Genres': registro['game']['info']['Genres'],
                'Category': registro['registro']['Category'],
                'Subcategory': registro['registro']['Subcategory']}
        num_runs += dicct['Num_Runs']
        lt.addLast(lst_res, dicct)
        lst_res = controller.sortByTime(lst_res)
    print('-'*70)
    print('Imprimiendo información del jugador ' + jugador)
    print('-'*70)
    print('El jugador tiene ' + str(lt.size(lst)) + ' registros con el mejor tiempo')
    print('-'*70)
    print('El jugador ha realizado  ' + str(num_runs) + ' intentos para obtener el mejor tiempo')
    print('-'*70)
    print('Imprimiedo los mejores 5 registros')
    print('-'*70)
    print(imprimirTitulos(lst_res))

#=====================================
#Requerimiento 3
#=====================================

def printnum(lst):
    lst_six = controller.getSix(lst)
    total = 0
    for y in lt.iterator(lst):
        total += y['Count']
    for x in lt.iterator(lst_six):
        tabulate_registros = lt.newList()
        for registro in lt.iterator(x['Details']):
            dicct = {'Time_0': registro['registro']['Time_0'],
                    'Record_Date_0': registro['registro']['Record_Date_0'],
                    'Name': registro['game']['info']['Name'],
                    'Players_0': registro['registro']['Players_0'],
                    'Country_0': registro['registro']['Country_0'],
                    'Platforms': registro['game']['info']['Platforms'],
                    'Genres': registro['game']['info']['Genres'],
                    'Category': registro['registro']['Category'],
                    'Subcategory': registro['registro']['Subcategory'],
                    'Release_Date': registro['game']['info']['Release_Date']}
            lt.addLast(tabulate_registros, dicct)
        tabulate_registros = controller.sortByTime(tabulate_registros)
        x['Details'] = imprimirTitulos(tabulate_registros)
    print('-'*70)
    print('Se encontraron ' + str(total) + ' registros en el rango ingresado')
    print('-'*70)
    print('Imprimiento los primeros 3 registros y los ultimos 3 registros . . . ')
    print('-'*70)
    print(imprimirTitulos(lst_six))

#=====================================
#Requerimiento 4
#=====================================

def printRecords(record_list):

    print_date_records = []

    for fecha_registro in lt.iterator(record_list):
        print_records = []

        for registro in lt.iterator(fecha_registro):
            record = {"Num_Runs": registro["Num_Runs"],
            "Time_0": registro["Time_0"],
            "Name": '\n'.join(wrap(registro["Name"], 16)),
            "Players_0": '\n'.join(wrap(', '.join(registro["Players_0"]), 16)),
            "Country_0": '\n'.join(wrap(', '.join(registro["Country_0"]), 16)),
            "Platforms": '\n'.join(wrap(', '.join(registro["Platforms"]), 16)),
            "Genres": '\n'.join(wrap(registro["Genres"], 16)),
            "Category": '\n'.join(wrap(registro["Category"], 16)),
            "Subcategory": '\n'.join(wrap(', '.join(registro["Subcategory"]), 16)),
            "Release_Date": registro["Release_Date"]}

            print_records.append(record)

        details = tabulate(print_records, headers='keys', tablefmt='fancy_grid')
        fecha = {"Record_Date_0": lt.getElement(fecha_registro, 1)["Record_Date_0"], 
        "count": lt.size(fecha_registro),
        "details": details}
        print_date_records.append(fecha)

    print(tabulate(print_date_records, headers='keys', tablefmt='fancy_grid'))

#=====================================
#Requerimiento 5
#=====================================

def printrangeTime(lst):
    lst_six = controller.getSix(lst)
    total = 0
    for y in lt.iterator(lst):
        total += y['Count']
    for x in lt.iterator(lst_six):
        tabulate_registros = lt.newList()
        for registro in lt.iterator(x['Details']):
            dicct = {'Record_Date_0': registro['registro']['Record_Date_0'],
                    'Num_Runs': registro['registro']['Num_Runs'],
                    'Name': registro['game']['info']['Name'],
                    'Players_0': registro['registro']['Players_0'],
                    'Country_0': registro['registro']['Country_0'],
                    'Platforms': registro['game']['info']['Platforms'],
                    'Genres': registro['game']['info']['Genres'],
                    'Category': registro['registro']['Category'],
                    'Subcategory': registro['registro']['Subcategory'],
                    'Release_Date': registro['game']['info']['Release_Date']}
            lt.addLast(tabulate_registros, dicct)
        tabulate_registros = controller.sortByReleaseDate(tabulate_registros)
        x['Details'] = imprimirTitulos(tabulate_registros)
    print('-'*70)
    print('Se encontraron ' + str(total) + ' registros en el rango ingresado')
    print('-'*70)
    print('Imprimiento los primeros 3 registros y los ultimos 3 registros . . . ')
    print('-'*70)
    print(imprimirTitulos(lst_six))
    #print(imprimirTitulos(lst))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input("Seleccione una opción para continuar\n>")

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        pct= int(input("Ingrese el tamaño de los datos que desea cargar: "))
        if pct == 100:
            pct = 'large'
        elif pct == 0:
            pct = 'small'
        else:
            pct = str(pct) + "pct"
        print("\nCargando información ....")
        cont = controller.loadData(cont, pct)
        printLoadData(cont)

    elif int(inputs[0]) == 3:
        platform = input('Ingrese la plataforma que desea buscar: ')
        rangeinf = input('Ingrese el limite inferior de fechas que desea buscar: ')
        rangesup = input('Ingrese el limite superior de fechas que desea buscar: ')
        rangeinf = datetime.strptime(rangeinf, "%y-%m-%d")
        rangesup = datetime.strptime(rangesup, "%y-%m-%d")
        total, lst, totalgames = controller.gamesInRange(cont, platform, rangesup, rangeinf)
        printGameInRange(total, lst, totalgames, platform)
    elif int(inputs[0]) == 4:
        jugador = input('Ingrese el nombre del jugador que desea consultar: ')
        lst = controller.registroJugador(cont,jugador)
        printJugador(lst,jugador)
    elif int(inputs[0]) == 5:
        limiteinf= input("ingrese el límite inferior del número de intentos para romper el récord: ")
        limitesup= input("ingrese el límite superior del número de intentos para romper el récord: ")
        lst,time = controller.numInRangemap(cont, limiteinf, limitesup)
        printnum(lst)
        print(time)


    elif int(inputs[0]) == 6:
        rangeinf = input('Ingrese el limite inferior de fecha y hora que desea buscar (ej. 2019-03-06T04:03:53Z): ')
        rangesup = input('Ingrese el limite superior de fecha y hora que desea buscar (ej. 2021-10-17T15:48:00Z): ')
        rangeinf = datetime.fromisoformat(rangeinf.replace("Z",""))
        rangesup = datetime.fromisoformat(rangesup.replace("Z",""))

        total = controller.slowInRange(cont, rangesup, rangeinf)
        print("-"*50)
        print("Total records: " + str(total[1]))
        printRecords(total[0])
    elif int(inputs[0]) == 7:
        rangeinf = float(input('Ingrese el limite inferior de tiempo que desea buscar: '))
        rangesup = float(input('Ingrese el limite superior de tiempo que desea buscar: '))
        lst = controller.rangeTime(cont, rangesup, rangeinf)
        printrangeTime(lst)

    
    elif int(inputs[0]) == 8:

        rangeinf = input('Ingrese el año inferior que desea buscar: ')
        rangesup = input('Ingrese el año superior que desea buscar: ')
        num_segmentos = int(input("Ingrese el número de segmentos en que se divide el rango de propiedad en el histograma: "))
        num_niveles = int(input("Ingrese el número de niveles en que se dividen las marcas de jugadores en el histograma: "))
        propiedad = input("Consultar una de las propiedades (Time_0, Time_1, Time_2, Time_Avg, Num_Runs): ")

        total = controller.propertyHistogram(cont, rangeinf, rangesup, num_segmentos, num_niveles, propiedad)

        print("Se encontraron " + str(total[1]) + " registros en el rango de fechas.")
        print("El valor mínimo: " + str(round(total[3],2)))
        print("El valor máximo: " + str(round(total[4],2)))
        print("Se usaron " + str(total[2]) + " elementos para crear el histograma.")
        
        for segmento in total[0]:
            segmento["mark"] = '\n'.join(wrap(segmento["mark"], 16))

        print(tabulate(total[0], headers='keys', tablefmt='fancy_grid'))

    elif int(inputs[0]) == 9:
        platform = input('Ingrese la plataforma que desea buscar: ')
        top = int(input('Ingrese el número de videojuegos que desea buscar: '))
        lst = controller.topNmasrentables(cont, platform, top)
        print(imprimirTitulos(lst))
    else:
        sys.exit(0)




