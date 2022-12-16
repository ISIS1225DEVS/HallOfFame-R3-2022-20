# -*- coding: utf-8 -*-

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

from msilib.schema import tables
from platform import platform
import config as cf
import sys
from time import sleep
import model as md
from DISClib.DataStructures import mapentry as me
import controller as ct
from DISClib.ADT import list as lt
import asyncio as asy
from main_adts import Hash, rbt, Heap
import main_adts as ma
import folium as fo
from controller import timer_y_mem
import webbrowser as web
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
assert cf
from time import sleep, time
from prettytable import PrettyTable, ALL
from tabulate import tabulate

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def imprimir(lista:list, fields_names:list):
        
    tabla=PrettyTable(hrules=ALL, aling="c", max_width=20, min_width=5, field_names=fields_names)
    
    if lista.size() >= 6:
        
        for contenido in lista.first3_last3():
            tabla.add_row([contenido[i] for i in fields_names])
        return tabla
    else:

        for contenido in lista.iterator():
            tabla.add_row([contenido[i] for i in fields_names])
        return tabla
    
def imprimirtop(lista:list, fields_names:list, top, plataforma):
        
    tabla=PrettyTable(hrules=ALL, aling="c", max_width=12, min_width=18, field_names=fields_names)
    unique=0
    contador=0
    anterior=""
    for contenido in lista.iterator():
        if contenido["Platforms"] == plataforma:
            unique+=1  
        if contador < top:
            tabla.add_row([contenido[i] for i in fields_names])
            if contenido["Stream_Revenue"] != anterior:
                contador+=1
            anterior=contenido["Stream_Revenue"]

        
    return tabla, unique

def mini(contenido, names):
    tabla=PrettyTable(hrules=ALL, aling="c", max_width=20, min_width=5, field_names=names)
    for elementos in contenido.iterator():
        tabla.add_row([elementos[i] for i in names])
        año=elementos["date"]
      
    return año, tabla

def imprimir11(lista, names):
    tabla=PrettyTable(hrules=ALL, aling="c", max_width=120, min_width=5, field_names=["Release_Date", "Count", "Details"])
    x=0
    if lista.size()>6:
        for contenido in lista.first3_last3():
            año, mini_tabla=mini(contenido, names)
            tabla.add_row([año, contenido.size(), mini_tabla])
    elif lista.size()<=6:
        for contenido in lista.iterator():
            año, mini_tabla=mini(contenido, names)
            tabla.add_row([año, contenido.size(), mini_tabla])
    
    for contenido in lista.iterator():
        for elementos in contenido.iterator():
            x+=1
    
    return tabla, x
            
            
    
def imprimir5(lista:ma.lista, fields_names:list):
        tabla=PrettyTable(hrules=ALL, aling="c", max_width=12, min_width=5, field_names=fields_names)
        x=1
        
        if lista.size() >= 6:
            
            for contenido in lista.first3_last3():
    
                        tabla.add_row([contenido[i] for i in fields_names])
                        num=contenido["Num_Runs"]
        
            return tabla, num
        else:

            for contenido in lista.iterator():
                tabla.add_row([contenido[i] for i in fields_names])
                num=contenido["Num_Runs"]
            return tabla, num

def imprimir5carol(lista:ma.lista, fields_names:list):
        tabla=PrettyTable(hrules=ALL, aling="c", max_width=12, min_width=5, field_names=fields_names)
        num=0
        centinela=1
        for elementos in lista.iterator():
            for contenido in elementos.iterator():
                if centinela<=5:
                    tabla.add_row([contenido[i] for i in fields_names])
                    centinela+=1
                num+=int(contenido["Num_Runs"])
        return tabla, num
            
        

def imprimir5del4(lista:list, fields_names:list):
        tabla=PrettyTable(hrules=ALL, aling="c", max_width=12, min_width=5, field_names=fields_names)
        x=1
  
        if lista.size() >= 6:
            
            for contenido in lista.first3_last3():
    
                        tabla.add_row([contenido[i] for i in fields_names])
                        num=contenido["Record_Date_0"]
        
            return tabla, num
        else:

            for contenido in lista.iterator():
                tabla.add_row([contenido[i] for i in fields_names])
                num=contenido["Record_Date_0"]
            return tabla, num
def imprimir5del6(lista:list, fields_names:list):
        tabla=PrettyTable(hrules=ALL, aling="c", max_width=12, min_width=5, field_names=fields_names)
        x=1
  
        if lista.size() >= 6:
            
            for contenido in lista.first3_last3():
    
                        tabla.add_row([contenido[i] for i in fields_names])
                        num=contenido["Time_0"]
        
            return tabla, num
        else:

            for contenido in lista.iterator():
                tabla.add_row([contenido[i] for i in fields_names])
                num=contenido["Time_0"]
            return tabla, num

def imprimir5del1(game:dict, fields_names:list):
        tabla=PrettyTable(hrules=ALL, aling="c", max_width=12, min_width=5, field_names=fields_names)
        
        tabla.add_row([game[i] for i in fields_names])
        num=game["date"]
        
        return tabla, num
        

def imprimir_3(lst:list, fields_names:list):
    tabla_principal = PrettyTable(hrules=ALL, aling="c", max_width=1000, min_width=8, field_names=["Num_Runs", "Count", "Details"])
    records=0
    if lst.size()<=6:
        for listas in lst.iterator():
            mini_lista, num=imprimir5(listas, fields_names)
            tabla_principal.add_row([num, listas.size(), mini_lista])
 
    else:
        for listas in lst.first3_last3():
            mini_lista, num=imprimir5(listas, fields_names)
            tabla_principal.add_row([num, listas.size(), mini_lista])
         
    
    for elementos in lst.iterator():
        for elementos2 in elementos.iterator():
            records+=1

    return tabla_principal, records

def imprimir_4(lst:list, fields_names:list):
    tabla_principal = PrettyTable(hrules=ALL, aling="c", max_width=1000, min_width=8, field_names=["Record_Date_0", "Count", "Details"])
    records=0
    if lst.size()<=6:
        for listas in lst.iterator():
            mini_lista, num=imprimir5del4(listas, fields_names)
            tabla_principal.add_row([num, listas.size(), mini_lista])
            records+=listas.size()
    else:
        for listas in lst.first3_last3():
            mini_lista, num=imprimir5del4(listas, fields_names)
            tabla_principal.add_row([num, listas.size(), mini_lista])
            records+=listas.size()

    return tabla_principal, records

def imprimir_6(lst:list, fields_names:list):
    tabla_principal = PrettyTable(hrules=ALL, aling="c", max_width=1000, min_width=8, field_names=["Time_0", "Count", "Details"])
    records=0
    if lst.size()<=6:
        for listas in lst.iterator():
            mini_lista, num=imprimir5del6(listas, fields_names)
            tabla_principal.add_row([num, listas.size(), mini_lista])
            records+=listas.size()
    else:
        for listas in lst.first3_last3():
            mini_lista, num=imprimir5del6(listas, fields_names)
            tabla_principal.add_row([num, listas.size(), mini_lista])
            records+=listas.size()

    return tabla_principal, records

def imprimir1laura(lst:list, fields_names:list):

    tabla_principal = PrettyTable(hrules=ALL, aling="c", max_width=1000, min_width=8, field_names=["date", "Count", "Details"])
    records= 0
    if lst.size() < 6:
        for listas in lst.iterator():
            mini_lista, num=imprimir5del1(listas, fields_names)
            tabla_principal.add_row([num, listas.size() if isinstance(listas, ma.lista) else 1, mini_lista])
            records+=listas.size() if isinstance(listas, ma.lista) else 1
    else:
        for listas in lst.first3_last3():
            mini_lista, num=imprimir5del1(listas, fields_names)
            tabla_principal.add_row([num, listas.size() if isinstance(listas, ma.lista) else 1, mini_lista])
            records+=listas.size() if isinstance(listas, ma.lista) else 1

    return tabla_principal, records


def imprimir1(lista:list, fields_names:list):
        
        tabla=PrettyTable(hrules=ALL, aling="c", max_width=12, min_width=5, field_names=fields_names)
        x=1
        if lista.size() >= 6:
            for contenido in lista.iterator():
                if isinstance(contenido, Heap):
                    contenido.heapsort()
                    for element in contenido.iterator():
                        tabla.add_row([element[i] for i in fields_names])
                        if x>=5:
                            break 
                        x+=1
                if x>=5:
                    break
            return tabla
        else:
            for contenido in lista.iterator():
                if isinstance(contenido, Heap):
                    contenido.heapsort()
                    for element in contenido.iterator():
                        tabla.add_row([element[i] for i in fields_names])
                        if x>5:
                            break 
                        x+=1
                if x>5:
                    break
            return tabla

async def get_location(locator, country):
    return locator.geocode(country)

async def new_map(data):
    mapa=fo.Map((0,0), zoom_start=2.5, control_scale=True)
    geolocator=Nominatim(user_agent="Worldmap")
    for country, heap in data.items():
        cm=MarkerCluster()
        try:
            location= await get_location(geolocator, country)
            for content in heap.iterator():
                if location != None:
                    cm.add_child(fo.Marker((location.latitude, location.longitude), popup="Game_Name:{0}\nRelease_date:{1}\nTime:{2}".format(content["Name"], content["date"], content["Time_0"])))
        except Exception as err:
                print(err)
        mapa.add_child(cm)
        # print("a")
        # sleep(0.005)
    return mapa
    
def tablita(lista, segmentos, niveles):
    inferior = lista.firstElement()["Resultado"]
    superior = lista.lastElement()["Resultado"]
    intervalos = (inferior+superior)/segmentos
    suma = lista.size()
    rango = []
    diccionario = {}

    for elementos in range(1,segmentos+1):
        if elementos == 1:
            rango.append("{0},{1}".format(round(inferior,2),round(intervalos,2)))

        elif elementos == segmentos:
            rango.append("{0},{1}".format(round(intervalos*(segmentos-1),2),round(superior,2)))

        else:
            rango.append("{0},{1}".format(round(intervalos*(elementos-1),2),round(intervalos*(elementos),2)))

    for elementos in rango:
        diccionario["[{0}]".format(elementos)] = 0


    for elementos in rango:
        ranguitos = elementos.split(",")

        for tiempos in lista.iterator():
            aiuda = tiempos["Resultado"]
            if float(ranguitos[0]) <= aiuda <= float(ranguitos[1]):
                if "[{0}]".format(elementos) in diccionario:
                    diccionario["[{0}]".format(elementos)] +=1

    histograma=[]
    for cantidad in diccionario:
        diccionario[cantidad] = [diccionario[cantidad], '*'*round((diccionario[cantidad]//niveles))]
        histograma.append([cantidad, diccionario[cantidad][0], len(diccionario[cantidad][1]), diccionario[cantidad][1]])
 


    resultado = tabulate(histograma, headers=["bin", "count", "lvl", "mark"],tablefmt="grid")
    return resultado, suma, inferior, superior

def printMenu()->None:
    """Imprime el main menu
    ---------------------------------------------------------------------
    Args:
        None
    ---------------------------------------------------------------------
    Return: 
        None"""
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar los videojuegos publicados en un rango de tiempo para una plataforma")
    print("3- Encontrar los 5 registros con menor tiempo para un jugador en específico")
    print("4- Reportar los registros de menor duración dentro de un rango de intentos")
    print("5- Reportar los registros de mayor duración dentro de un rango de fechas")
    print("6- Reportar los registros más recientes en un rango de tiempos récord")
    print("7- Encontrar los 5 videojuegos más rentables para transmitir")
    print("8- Graficar el histograma de tiempos para un año de publicación")
    print("9- Mostrar la distribución de récords por continente")
    print("0- Salir")





def select(selection:str, lista:list)->(str):
    """Se encarga de validar por nombre o número la opción escogida
    ---------------------------------------------------------------------
    Args:
        selection: es la opción ingresada por el usuario
        lista: posibilidades para comparar
    ---------------------------------------------------------------------
    Return: 
        el string con la validación de la opción"""
    if selection.isdigit() and int(selection) >=1 and int(selection)<=len(lista):
        sizes=dict(enumerate(lista))
        return sizes[int(selection)-1]
    elif not selection.isdigit() and selection in lista:
        return selection

def tprint(string:str, letter="=", ljump=False, rjump=True)->None:
    """A través del tamaño de la terminal se encarga de imprimir en el centro
    ---------------------------------------------------------------------
    Args:
        string: str a imprimir
        letter(def='='): es con la que se rellena ambos lados de la terminal
        ljump(def='False'): Bool para salto de línea antes del string
        rjump(def='True'): Bool para salto de línea después del string
    ---------------------------------------------------------------------
    Return: 
        None"""
    columns=cf.ter_size[0]
    left_ter = round((columns-len(string))//2)
    print(("\n" if ljump else "")+letter*(left_ter)+string+letter*(columns-left_ter-len(string))+("\n" if rjump else ""))


def print_sizes()->None:
    """Imprime el los sizes a escoger
    ---------------------------------------------------------------------
    Args:
        None
    ---------------------------------------------------------------------
    Return: 
        None"""
    print("""
Digite uno de los siguientes tamaños:
1)small
2)5pct
3)10pct
4)20pct
5)30pct
6)50pct
7)80pct
8)large
""")

catalog = None

"""
Menu principal
"""
def iniciar_aplicación():
    control=ct.catalog_init()
    data_in=False
    while True: 
        printMenu()
        inputs=input("Selecciona una opción: ").replace(" ", "")
        if inputs.isdigit():
            
            if int(inputs) == 1:
                tprint(" Carga de datos ", letter="-")
                #cargar datos
          
                print_sizes()
                t_archivo=input("Digite el tamaño deseado: ").replace(" ","")
                size=select(t_archivo, ["small", "5pct","10pct","20pct", "30pct","50pct","80pct", "large"])
                if size is None:
                    tprint(" Por favor escoga un tamaño válido ", letter="-")
                    sleep(1)
                    continue
                tprint(" Carga de datos ", letter="-")   
                datos, tiempo= ct.cargar_datos(control, size)
                
                a=datos.get_value("game").get_value("total")
                b=datos.get_value("category").get_value("total")
                
                tprint("", letter="-")
                print("Loaded Speedrunning data properties... ")
                print(f"Total loaded videogames: {a.size()}")
                print(f"Total loaded category records: {b.size()}")
                print("\n")
                tprint("", letter="-")
                print("\n")
                
                print("The first 3 and last 3 videogames loaded in ADTs are...")
                print("Data from games displayed as read from CSV file")
                table=imprimir(a, ["Game_Id", "date", "Name", "Abbreviation", "Platforms", "Total_Runs", "Genres"])
                print(table)
                print("\n")
                tprint("", letter="-")
                print("\n")
                print("The fist 3 and last 3 category records loaded in ADTs are...")
                print("Data from games displayed as read from CSV file")
                table2=imprimir(b, ["Game_Id", "Record_Date_0", "Num_Runs", "Name","Category", "Subcategory", "Country_0",  "Players_0", "Time_0"])
                print(table2)
                if datos is not None: 
                    data_in=True
                else:
                    continue
                tprint(f" {tiempo} ", letter="I")
                
                

            elif int(inputs) == 2 and data_in:
                #Reportar los videojuegos de una plataforma en un rango de tiempo. Se logro uwu

                inferior = input("Ingrese la fecha inferior:")
                superior = input("Ingrese la fecha superior:")
                plataforma = input("Ingrese la plataforma:")

                respuesta, time=ct.req1(datos, inferior, superior, plataforma)
     
                lista, contador=(imprimir11(respuesta, ["Total_Runs",  "Name", "Abbreviation", "Platforms", "Genres"]))
                total= respuesta.size()
                print("\n")
                tprint(f" Req No. 1 Inputs ", letter="=")
                print(f"Games released between {inferior} and {superior}")
                print(f"In plataforma '{plataforma}' ")

                print("\n")
                tprint(f" Req No. 1 Answers ", letter="=")
                y=datos.get_value("game").get_value("plataformas7").get_value(plataforma).size()
                print(f"Avalaible games in'{plataforma}':  {y}")
                
                print(f"Date range between '{inferior}' and '{superior}'")
                print(f"Released games: {contador}")
                print("\n")
                tprint(" Videogames release details ", letter="-")
                if total >=6:
                    
                    print(f"The firs 3 and last 3 in range are:")
                    print(f"There are {total}  elements in range ")

                else:
                    print(f"There are only {total}  elements in range ")
                    
                print(lista)
                tprint(f" {time} ", letter="I")


            elif int(inputs) == 3 and data_in:
                
                jugador= input("ingrese el nombre del jugador: ")
                lst, time=ct.requerimiento2carol(datos, jugador)
                table, num= imprimir5carol(lst, ["Time_0", "Record_Date_0", "Name", "Players_0", "Country_0", "Num_Runs", "Platforms", "Genres", "Category", "Subcategory"])
                tprint(" Req No. 2 Inputs ")
                tprint(f" Speedrun records for player: {jugador} ", letter=" ")
                tprint(" Req No. 2 Answer ")
                tprint(f"Player {jugador} has {num} Speedruns record attemps", letter=" ")
                tprint(f" Player {jugador} details ", letter="-")
                tprint(f"There are only {lst.size()} elements in range", letter=" ")


                print(table)
                tprint(f" {time} ", letter="I")


            elif int(inputs) == 4 and data_in:
                #Reportar los registros más veloces dentro de un rango de intentos
                #Tree by time
                inferior = input("Ingrese el limite inferior del numero de intentos de romper el record:")
                superior = input("Ingrese el limite superior del numero de intentos de romper el record:")
                
                respuesta, time=ct.reqerimiento3(datos, inferior, superior)
                lista, records=(imprimir_3(respuesta, ["Time_0", "Record_Date_0",  "Name", "Players_0", "Country_0", "Platforms", "Genres", "Category", "Subcategory", "Release_Date", "Total_Runs"]))
                total=respuesta.size()
                print("\n")
                tprint(f" Req No. 3 Answer ", letter="=")
                
                print(f"Attempts between {inferior} and {superior}")
                print(f"Total records: {records}")
                print("\n")
                tprint(" Videogames release details ", letter="-")
                
                if total >=6:
                    
                    print(f"There are {total}  elements in range ")
                else:
                    print(f"There are only {total}  elements in range ")
                    
                print(lista)
                tprint(f" {time} ", letter="I")

            elif int(inputs) == 5 and data_in:
                #Reportar los registros más lentos dentro de un rango de fechas. 
                #tree by record date

                inferior = input("Ingrese el limite inferior de la fecha: ")
                hora1 = input("Ingrese la hora: ")
                superior = input("Ingrese el limite superior de la fecha: ")
                hora2 = input("Ingrese la hora: ")

                inferior = inferior+"T"+hora1+"Z"
                superior = superior+"T"+hora2+"Z"
                respuesta, time = ct.requerimiento4(datos, inferior, superior)
                lista, records=(imprimir_4(respuesta, ["Num_Runs", "Time_0",  "Name", "Players_0", "Country_0", "Platforms", "Genres", "Category", "Subcategory", "Release_Date"]))
                total=respuesta.size()
                print("\n")
                tprint(f" Req No. 4 Inputs ", letter="=")
                print(f"Category records between {inferior} and {superior} datetime")
                print("\n")
                tprint(f" Req No. 4 Answers ", letter="=")
                print(f"Attempts between {inferior} and {superior}")
                print(f"Total records: {total}")
                print("\n")
                tprint(" Videogames release details ", letter="-")
                
                if total >=6:
                    
                    print(f"There are {total}  elements in range ")
                    print(f"The firs 3 and last 3 in range are:")
                else:
                    print(f"There are only {total}  elements in range ")
                    
                print(lista)
                tprint(f" {time} ", letter="I")

            elif int(inputs) == 6 and data_in:
                #Reportar los registros más recientes en un rango de tiempos récord.
                #tree by record
                acot_inf=float(input("Ingrese el límite inferior: "))
                acot_sup=float(input("Ingrese el límite superior: "))
                rta, time=ct.requerimiento5(datos, acot_inf, acot_sup)
                lst, total= rta
                tabla=imprimir_6(lst, ["Record_Date_0","Num_Runs" , "Name", "Players_0", "Country_0", "Platforms", "Genres", "Category", "Subcategory", "Release_Date"])
                tprint(" Req No. 5 Inputs ")
                tprint(f" Category records between {acot_inf} and {acot_sup} ", letter=" ")
                tprint(" Req No. 5 Answer ")
                tprint(f"Attemps between {acot_inf} and {acot_sup}", letter=" ")
                tprint(f"Total records {total}", letter=" ")
                tprint(" Videogame release details ", letter="-")
                tprint(f"There are only {lst.size()} elements in range", letter=" ")
                print(f"The firs 3 and last 3 in range are:")

                print(tabla)
                tprint(f" {time} ", letter="I")

            elif int(inputs) == 7 and data_in:
                plataforma=input("Ingrese la plataforma de interés: ")
                top = int(input("Ingrese el top de interes: "))
                y, time=ct.reqeurimiento7(datos, plataforma)
                x, u=y
                table, unique=imprimirtop(x,["Name", "Release_Date", "Platforms", "Genres", "Stream_Revenue", "Market_Share", "Time_Avg", "Total_Runs"], top, plataforma)
                print("\n")
                tprint(f" Req No. 7 Inputs ", letter="=")
                print(f"Find the TOP {top} games for {plataforma} plataform")
                print("\n")
                print("Filtering records by plataform...")
                print("Removing miscelaneous streaming revenue...")
                print("\n")
                tprint(" Req No. 7 Answer ", letter="=")
                y=datos.get_value("game").get_value("plataformas7").get_value(plataforma).size()
                print(f"There are {y} records for {plataforma}...")
                print(f"There are {u} unique records for {plataforma}...")

                print("\n")
                tprint(f"There are only {top} elements in range.")          
                print(table)
                tprint(f" {time} ", letter="I")

            elif int(inputs) == 8 and data_in:

                print("\n")
                print("1- Time_0")
                print("2- Time_1")
                print("3- Time_2")
                print("4- Tiempo promedio registrado")
                print("5- Número de intentos registrados")
                print("\n")
                opcion = int(input("Digite la opción que desea conocer :): "))
                print("\n")
                segmentos = int(input("Digite la cantidad de segmentos: "))
                niveles = int(input("Digite la cantidad de niveles: "))
                anio1 = input("Digite el año inicial: ")
                anio2 = input("Digite el año final: ")
                print("\n")
                inferior = str(anio1)
                superior = str(anio2)
                busca = None
                if opcion == 1:
                    busca = "Time_0"

                if opcion == 2:
                    busca = "Time_1"

                if opcion == 3:
                    busca = "Time_2"

                elif opcion == 4:
                    busca = "Time_Avg"

                elif opcion ==5:
                    busca = "Num_Runs"

                respuesta, time = ct.requerimiento6(datos, inferior, superior, opcion)
                resultado, conteo, primero, segundo = tablita(respuesta, segmentos, niveles)


                tprint(f" Req No. 6 Inputs ", letter="=")
                print(f"Count map (histogram) of the feature: '{busca}'")
                print(f"Data between release years of '{anio1}' of the feature: '{anio2}'")
                print(f"Number of bins: {segmentos}")
                print(f"Registered attemps per scale: {niveles}")
                print("\n")
                tprint(" Req No. 6 Answer ", letter="=")
                print(f"There are '{conteo}'attempts on record.")
                print(f"Lowest value:'{primero}'")
                print(f"Highest value:'{segundo}'")
                print(f"The histogram counts '{conteo}' attempts")
                print("\n")
                tprint(f"'{busca}' Histogram with '{segmentos}' and '{niveles}' attempts per mark lvl")          
                print(resultado)
                print("\n")
                tprint(f" {time} ", letter="I")

   

            elif int(inputs) == 9 and data_in:
                acot_inf=(input("Ingrese el límite inferior: "))
                acot_sup=(input("Ingrese el límite superior: "))
                anio=input("Ingrese el año: ")
                datass, time=ct.requerimiento8(datos, anio, acot_inf, acot_sup)
                mappa= asy.run(new_map(datass))
                mappa.save("world_map.html")
                web.open_new_tab("world_map.html")
                tprint(f" {time} ", letter="I")

            elif int(inputs) == 0:
                #salir xd
                tprint(" Hasta luego ", letter="+")
                sys.exit(0)
            elif not data_in:
                #validar cargar datos
                tprint(" Por favor, primero cargue los datos ", letter="-")
                sleep(1)
            else:
                #Validar rango
                tprint(" Por favor ingrese una opción entre 0-9 ", letter="-")
                sleep(1)
        else:
            #validar opción
            tprint(" Por favor ingrese una opción válida ")
            sleep(1)


if __name__=="__main__":
    iniciar_aplicación()