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
from DISClib.ADT import map as mp


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def newAnalyzer():
    analyzer = controller.init()
    return analyzer


def printMenu():
    print("Bienvenido")
    print("1- Inicializar Analizador y Cargar información en el catálogo")
    print("2- Videojuegos publicados en un rango de tiempo")
    print("3- Registros para un jugador")
    print("4- Menor duración en rango de intentos")
    print("5- Mayor Duración en Rango de Fechas")
    print("6- Registros mas recientes en un rango de tiempos")
    print("7- Histograma de propiedades para registro en rango de años")
    print("8- Videojuegos mas rentables")
    print("9- Distribución juegos por continenete")
    print("10- Salir del programa")

def loadData(filename):
    games=controller.loadGame("Speedruns/game_data_utf-8-" + str(filename)+".csv")
    category=controller.loadGame("Speedruns/category_data_utf-8-" + str(filename)+".csv")
    return games, category

#CARGA DE DATOS
def printgames(lista):
    print("                                    ")
    print("---------ARCHIVO JUEGOS---------")
    tamaño = lista['size']
    print("El numero total de juegos es de: " + str(tamaño))
    for i in range(0, 3):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre: "+ str(lista['elements'][i]['Name']))
            print("Id: "+ str(lista['elements'][i]['Game_Id']))
            print("Genero: "+ str(lista['elements'][i]['Genres']))
            print("Plataformas: "+ str(lista['elements'][i]['Platforms']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Total_Runs']))
            print("Fecha de Publicación: "+ str(lista['elements'][i]['Release_Date']))
    k = 0
    for j in range(len(lista['elements'])-3, len(lista["elements"])):
        print("-----Elemento Nº" + str(k+4)+ "-----")
        print("Nombre: "+ str(lista['elements'][j]['Name']))
        print("Id: "+ str(lista['elements'][j]['Game_Id']))
        print("Genero: "+ str(lista['elements'][j]['Genres']))
        print("Plataformas: "+ str(lista['elements'][j]['Platforms']))
        print("Numero Intentos: "+ str(lista['elements'][j]['Total_Runs']))
        print("Fecha de Publicación: "+ str(lista['elements'][j]['Release_Date']))
        k +=1

def printcategory(lista):
    print("                                    ")
    print("---------ARCHIVO CATEGORIAS---------")
    tamaño = lista['size']
    print("El numero total de juegos es de: " + str(tamaño))
    for i in range(0, 3):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Id Juego: "+ str(lista['elements'][i]['Game_Id']))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][i]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][i]['Record_Date_0'][0:10]))

    k = 0
    for j in range(len(lista['elements'])-3, len(lista["elements"])):
            print("-----Elemento Nº" + str(k+4)+ "-----")
            print("Id Juego: "+ str(lista['elements'][j]['Game_Id']))
            print("Categoria: "+ str(lista['elements'][j]['Category']))
            print("Subcategoria: "+ str(lista['elements'][j]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][j]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][j]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][j]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][j]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][j]['Record_Date_0'][0:10]))
            k +=1

#REQUERIMIENTO 2
def printRegistersByTimeandDate(lista):
    tamaño = lista['size']
    print("El numero de registros en el rango de busqueda es de: " + str(tamaño))
    if len(lista['elements']) > 6:
        for i in range(0, 3):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre: "+ str(lista['elements'][i]['Name']))
            print("Id Juego: "+ str(lista['elements'][i]['Game_Id']))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][i]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][i]['Record_Date_0'][0:10]))

        k = 0
        for j in range(len(lista['elements'])-3, len(lista["elements"])):
            print("-----Elemento Nº" + str(k+4)+ "-----")
            print("Nombre: "+ str(lista['elements'][j]['Name']))
            print("Id Juego: "+ str(lista['elements'][j]['Game_Id']))
            print("Categoria: "+ str(lista['elements'][j]['Category']))
            print("Subcategoria: "+ str(lista['elements'][j]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][j]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][j]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][j]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][j]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][j]['Record_Date_0'][0:10]))
            k +=1
    else: 
        for i in range(0, len(lista['elements'])):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre: "+ str(lista['elements'][i]['Name']))
            print("Id Juego: "+ str(lista['elements'][i]['Game_Id']))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][i]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][i]['Record_Date_0'][0:10]))

    
#REQUERIMIENTO 1

def printgamesByPlarformAndDate(lista):
   
    tamaño = lista['size']
    print("El numero de videojuegos en el rango de tiempos es de: " + str(tamaño))
    if len(lista['elements']) > 6:
        for i in range(0, 3):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre: "+ str(lista['elements'][i]['Name']))
            print("Abreviacíon: "+ str(lista['elements'][i]['Abbreviation']))
            print("Plataformas: "+ str(lista['elements'][i]['Platforms']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Total_Runs']))
            print("Fecha de Publicación: "+ str(lista['elements'][i]['Release_Date']))
            
        k = 0
        for j in range(len(lista['elements'])-3, len(lista["elements"])):
            print("-----Elemento Nº" + str(k+4)+ "-----")
            print("Nombre: "+ str(lista['elements'][j]['Name']))
            print("Abreviacíon: "+ str(lista['elements'][j]['Abbreviation']))
            print("Plataformas: "+ str(lista['elements'][j]['Platforms']))
            print("Numero Intentos: "+ str(lista['elements'][j]['Total_Runs']))
            print("Fecha de Publicación: "+ str(lista['elements'][j]['Release_Date']))
            k +=1
    else: 
        for i in range(0, len(lista['elements'])):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre: "+ str(lista['elements'][i]['Name']))
            print("Abreviacíon: "+ str(lista['elements'][i]['Abbreviation']))
            print("Plataformas: "+ str(lista['elements'][i]['Platforms']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Total_Runs']))
            print("Fecha de Publicación: "+ str(lista['elements'][i]['Release_Date']))

#REQUERIMIENTO 7

def printGamesByRentability(lista):
    tamaño = len(lista)
    print('El total de juegos en la plataforma es de: ' + str(tamaño))
    for i in range(0, len(lista['elements'])):
        print("-----Elemento Nº" + str(i+1)+ "-----")
        print("Nombre: "+ str(lista['elements'][i]['Name']))
        print("Abreviacíon: "+ str(lista['elements'][i]['Abbreviation']))
        print("Genero: "+ str(lista['elements'][i]['Genres']))
        print("Numero Intentos: "+ str(lista['elements'][i]['Total_Runs']))
        print("Fecha de Publicación: "+ str(lista['elements'][i]['Release_Date']))
        print("Stream Revenue: "+ str(lista['elements'][i]['StreamRevenue']))

def printRecordsByPlayer(lista):
    tamaño = lista['size']
    print('El total de records del Jugador es de: ' + str(tamaño))
    if len(lista['elements']) > 5:
        for i in range(0, 5):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre: "+ str(lista['elements'][i]['Name']))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][i]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][i]['Record_Date_0'][0:10]))
    else:
        for i in range(0, len(lista['elements'])):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre: "+ str(lista['elements'][i]['Name']))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][i]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][i]['Record_Date_0'][0:10]))

#REQ 3

def printRegistersbyTimeandTrials(lista):
    tamaño = lista['size']
    print("El numero de registros en el rango de busqueda es de: " + str(tamaño))
    if len(lista['elements']) > 6:
        for i in range(0, 3):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre "+ str(lista['elements'][i]['Game_Id']))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][i]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][i]['Record_Date_0'][0:10]))

        k = 0
        for j in range(len(lista['elements'])-3, len(lista["elements"])):
            print("-----Elemento Nº" + str(k+4)+ "-----")
            print("Nombre "+ str(lista['elements'][j]['Game_Id']))
            print("Categoria: "+ str(lista['elements'][j]['Category']))
            print("Subcategoria: "+ str(lista['elements'][j]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][j]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][j]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][j]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][j]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][j]['Record_Date_0'][0:10]))
            k +=1
    else: 
        for i in range(0, len(lista['elements'])):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre "+ str(lista['elements'][i]['Game_Id']))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero Intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Nombre Jugador: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad: "+ str(lista['elements'][i]['Country_0']))
            print("Mejor Tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha Mejor Tiempo: "+ str(lista['elements'][i]['Record_Date_0'][0:10]))

def printMoviesByDate(lista):
    if len(lista['elements']) > 6:
        for i in range(0, 3):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre de videojuego: "+ str(lista['elements'][i]["Name"]))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero de intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Jugadores: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad jugadores: "+ str(lista['elements'][i]['Country_0']))
            print("Plataformas: "+ str(lista["elements"][i]["Platforms"]))
            print("Generos: "+ str(lista["elements"][i]["Genres"]))
            print("Mejor tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha de record: "+ str(lista['elements'][i]['Record_Date_0']))
        
        k = 0
        for j in range(len(lista['elements'])-3, len(lista["elements"])):
            print("-----Elemento Nº" + str(4+k)+ "-----")
            print("Nombre de videojuego: "+ str(lista['elements'][j]["Name"]))
            print("Categoria: "+ str(lista['elements'][j]['Category']))
            print("Subcategoria: "+ str(lista['elements'][j]['Subcategory']))
            print("Numero de intentos: "+ str(lista['elements'][j]['Num_Runs']))
            print("Jugadores: "+ str(lista['elements'][j]['Players_0']))
            print("Nacionalidad jugadores: "+ str(lista['elements'][j]['Country_0']))
            print("Plataformas: "+ str(lista["elements"][j]["Platforms"]))
            print("Generos: "+ str(lista["elements"][j]["Genres"]))
            print("Mejor tiempo: "+ str(lista['elements'][j]['Time_0']))
            print("Fecha de record: "+ str(lista['elements'][j]['Record_Date_0']))
            k +=1
    else: 
        for i in range(0, len(lista['elements'])):
            print("-----Elemento Nº" + str(i+1)+ "-----")
            print("Nombre de videojuego: "+ str(lista['elements'][i]["Name"]))
            print("Categoria: "+ str(lista['elements'][i]['Category']))
            print("Subcategoria: "+ str(lista['elements'][i]['Subcategory']))
            print("Numero de intentos: "+ str(lista['elements'][i]['Num_Runs']))
            print("Jugadores: "+ str(lista['elements'][i]['Players_0']))
            print("Nacionalidad jugadores: "+ str(lista['elements'][i]['Country_0']))
            print("Plataformas: "+ str(lista["elements"][i]["Platforms"]))
            print("Generos: "+ str(lista["elements"][i]["Genres"]))
            print("Mejor tiempo: "+ str(lista['elements'][i]['Time_0']))
            print("Fecha de record: "+ str(lista['elements'][i]['Record_Date_0']))

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        analyzer = newAnalyzer()
        print("Cargando información de los archivos ....")
        filename = "small"
        catalog = loadData(filename)
        gamesfinal = controller.addGamesTotal(catalog)
        categoryfinal = controller.addCatedoryTotal(catalog)  
        printgames(catalog[0]['games'])
        printcategory(catalog[1]['games'])

    elif int(inputs[0]) == 2:
        platform = input("Ingrese la plataforma: ")
        date1 = input("Ingrese la fecha inicial: ")
        date2 = input("Ingrese la fecha final: ")
        resultado = controller.gamesByPlarformAndDate(catalog, platform, date1, date2)
        print("El numero de videojuegos en la plataforma es de: " + str(resultado[1]))
        printgamesByPlarformAndDate(resultado[0])

    elif int(inputs[0]) == 3:
        player = input("Ingrese el jugador: ")
        resultado = controller.gamesbyPlayer(catalog, player)
        printRecordsByPlayer(resultado)

    elif int(inputs[0]) == 4:
        trial_inferior = input("Ingrese el número inferior de intentos: ")
        trial_superior = input("Ingrese el número superior de: ")
        resultado =controller.RegistersbyTimeandTrials(catalog, trial_inferior, trial_superior)
        printRegistersbyTimeandTrials(resultado[0])
        print(resultado[1])

    elif int(inputs[0])==5:
        start=input("Ingrese la fecha de inicio(incluyendo hora): ")
        end=input("Ingrese la fecha de final(incluyendo hora): ")

        lista_final=controller.dateCategory(categoryfinal, start, end)
        
        for i in range(0, len(lista_final[0]["elements"])):
            for j in range(0, len(catalog[0]["games"]["elements"])):
                if(lista_final[0]["elements"][i]["Game_Id"]==catalog[0]["games"]["elements"][j]["Game_Id"]):
                    lista_final[0]["elements"][i]["Name"]=catalog[0]["games"]["elements"][j]["Name"]
                    lista_final[0]["elements"][i]["Platforms"]=catalog[0]["games"]["elements"][j]["Platforms"]
                    lista_final[0]["elements"][i]["Genres"]=catalog[0]["games"]["elements"][j]["Genres"]
        print(lista_final[0]["elements"][i]["Genres"])
        print("El numero de intentos realizados entre "+ str(start)+ " y "+ str(end)+ ":")
        print("Records totales: " + str(len(lista_final[0]["elements"])))
        printMoviesByDate(lista_final[0])
        print("tiempo req 4 "+ str(lista_final[1]))

    elif int(inputs[0]) == 6:
        time1 = input("Ingrese el tiempo inicial: ")
        time2 = input("Ingrese el tiempo final: ")
        resultado =controller.RegistersByTimeandDate(catalog, time1, time2)
        printRegistersByTimeandDate(resultado)

    elif int(inputs[0])==7: 
        year1_input=input("Ingrese el año inicial: ")
        year2_input=input("Ingrese el año final: ")
        year1=year1_input[2:4]
        year2=year2_input[2:4]
        segmentos=input("Ingrese el numero de segmentos: ")
        niveles=input("Ingrese los niveles para la division de las marcaciones: ")
        consulta=input("Ingrese 1, 2 o 3"+ "\n"+ "1.Consulta con todos los tiempos"+ "\n"+ "2.Consulta con tiempos promedios"+ "\n"+ "3.Consulta con el numero de intentos""\n")
        
        if consulta==str(1): 
            print("Contar histograma con todos los tiempos: ")
            print("Datos entre los años de lanzamiento de "+ str(year1_input)+ " y "+str(year2_input))
            print("El numero de segmentos en que se divide el rango del histograma es: "+ str(segmentos))
            print("El numero de niveles en que se dividen las marcas: "+ str(niveles))
        if consulta==str(2): 
            print("Contar histograma con el promedio de los tiempos: ")
            print("Datos entre los años de lanzamiento de "+ str(year1_input)+ " y "+str(year2_input))
            print("El numero de segmentos en que se divide el rango del histograma es: "+ str(segmentos))
            print("El numero de niveles en que se dividen las marcas: "+ str(niveles))
        if consulta==str(3):
            print("Contar histograma con el numero de intentos: ")
            print("Datos entre los años de lanzamiento de "+ str(year1_input)+ " y "+str(year2_input))
            print("El numero de segmentos en que se divide el rango del histograma es: "+ str(segmentos))
            print("El numero de niveles en que se dividen las marcas: "+ str(niveles))

        lista_final=controller.rangeofYears(catalog, year1, year2, segmentos, niveles, consulta)
        print("tiempo req 6 "+ str(lista_final))

    elif int(inputs[0]) == 8:
        platform = input("Ingrese la plataforma: ")
        n = input("Ingrese top N: ")
        resultado = controller.rentability(catalog, platform, n)
        printGamesByRentability(resultado)

    elif int(inputs[0]) == 9:
        year = input("Ingrese el año de publicación sobre el cual quiere obtener el histograma: ")
        time1 = input("Ingrese el tiempo inicial: ")
        time2 = input("Ingrese el tiempo final: ")
        resultado =controller.RegistersByTimeandYear(catalog, year, time1, time2)
        print(resultado)
        
    else:
        sys.exit(0)
sys.exit(0)
