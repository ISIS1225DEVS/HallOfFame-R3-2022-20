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


from email import header
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from tabulate import tabulate
import sys
import folium
import geopy
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster
import webbrowser
default_limit = 1000
sys.setrecursionlimit(default_limit*10)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada1
"""

speedrunFile= "Speedruns//category_data_urf-8-small.csv"

def newController():
    control = controller.newController()
    return control

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Conocer los videojuegos que se lanzaron en un rango de fechas")
    print("3- Conocer los registros de speedruns para un jugador ")
    print("4- Encontrar los registros más veloces dentro de un rango de intentos")
    print("5- Encontrar los registros más lentos dentro de un rango de fechas.")
    print("6- Encontrar los registros más recientes en un rango de tiempos récord.")
    print("7- Mostrar un histograma con la distribución de la duración de los mejores tiempos ")
    print("8- Encontrar los 5 videojuegos más rentables para retransmitir")
    print('9- Bono sorpresa')

def OpcionMuestra():
    print('------------------------------------------------------------')
    print('Muestras disponibles')
    print('[1] - 5pct')
    print('[2] - 10pct')
    print('[3] - 20pct')
    print('[4] - 30pct')
    print('[5] - 50pct')
    print('[6] - 80pct')
    print('[7] - large')
    print('[8] - small')
    print('------------------------------------------------------------')





def loadData (control): 
    control=controller.loadData(control)
    return control



def printTimeAndMemory(answer):
    """
    Imprime los datos de tiempo y memoria de la carga de datos
    """
    print("Tiempo [ms]: ", f"{answer[0]:.3f}", "||",
            "Memoria [kB]: ", f"{answer[1]:.3f}\n")


def TopAndLast3(catalogo,catalogo2):
    '''
    Esta función premite imprimir todos los primeros y ultimos 3
    programas en una lista
    '''
    print('------------------------------------------------------------')
    print('Loaded Speedrunning data properties...')
    print('Total loaded videogames: {}'.format(lt.size(catalogo)))
    print('Total loaded category records: {}\n'.format(lt.size(catalogo2)))
    print('------------------------------------------------------------\n')
    print('The first 3 and last 3 videogames loaded in ADTs are...\nData from games displayed as read from csv file')
    firstandlast = []
    for informacion in lt.iterator(lt.subList(catalogo, 1, 3)):
        firstandlast.append([informacion['Game_Id'],informacion['Name'],informacion['Genres'],informacion['Platforms'],informacion['Total_Runs'],informacion['Release_Date']])
    for informacion in lt.iterator(lt.subList(catalogo, lt.size(catalogo)-2, 3)):
        firstandlast.append([informacion['Game_Id'],informacion['Name'],informacion['Genres'],informacion['Platforms'],informacion['Total_Runs'],informacion['Release_Date']])
    print(tabulate(firstandlast,headers=['Id','Nombre','Género','Plataformas','Intentos','Fecha de publicación'],tablefmt='grid',maxcolwidths=12))
    print('------------------------------------------------------------\n')
    print('The first 3 and last 3 category records loaded in ADTs are...\nData from games displayed as read from csv file')
    firstandlast = []
    for informacion in lt.iterator(lt.subList(catalogo2, 1, 3)):
        firstandlast.append([informacion['Game_Id'],informacion['Record_Date_0'],informacion['Num_Runs'],informacion['Category'],informacion['Subcategory'],informacion['Country_0'],informacion['Players_0'],informacion['Time_0']])
    for informacion in lt.iterator(lt.subList(catalogo2, lt.size(catalogo)-2, 3)):
        firstandlast.append([informacion['Game_Id'],informacion['Record_Date_0'],informacion['Num_Runs'],informacion['Category'],informacion['Subcategory'],informacion['Country_0'],informacion['Players_0'],informacion['Time_0']])
    print(tabulate(firstandlast,headers=['Id','Record_Date_0','Num_Runs','Category','Subcategory','Country_0','Players_0','Time_0'],tablefmt='grid',maxcolwidths=20))
    print('\n')

def imprimir_resultados(respuesta,conteo,plataforma,limite_inf,limite_max):
    resultado = {}
    cuenta = {}
    resp = []
    print('================== Req No. 1 Answer ==================')
    print(f'Avaliable games in {plataforma}: {conteo}')
    print(f'Date range between {limite_inf} and {limite_max}\n')

    print('----- Videogames release details -----')
    print(f'There are {lt.size(respuesta)} elements in range')
    if lt.size(respuesta)>6:
        print('Las primeras y ultimos 3 programas cargados son:\n')
        for listas in lt.iterator(lt.subList(respuesta,1,3)):
            cuentas = lt.size(listas)
            for elementos in lt.iterator(listas):
                if elementos['Release_Date'] in resultado:
                    resultado[elementos['Release_Date']].append([elementos['Abbreviation'],elementos['Name'],elementos['Platforms'],elementos['Genres'],elementos['Total_Runs']])
                else:
                    resultado[elementos['Release_Date']]=[[elementos['Abbreviation'],elementos['Name'],elementos['Platforms'],elementos['Genres'],elementos['Total_Runs']]]
            cuenta[elementos['Release_Date']] = cuentas
        for listas in lt.iterator(lt.subList(respuesta,lt.size(respuesta)-2,3)):
            cuentas = lt.size(listas)
            for elementos in lt.iterator(listas):
                if elementos['Release_Date'] in resultado:
                    resultado[elementos['Release_Date']].append([elementos['Abbreviation'],elementos['Name'],elementos['Platforms'],elementos['Genres'],elementos['Total_Runs']])
                else:
                    resultado[elementos['Release_Date']]=[[elementos['Abbreviation'],elementos['Name'],elementos['Platforms'],elementos['Genres'],elementos['Total_Runs']]]
            cuenta[elementos['Release_Date']] = cuentas

        for fechas in resultado:
            resp.append([fechas,str(cuenta[fechas]),tabulate(resultado[fechas],headers=['Abbreviation','Name','Plataforms','Genres','Total_Runs'],tablefmt='grid',maxcolwidths=12)])
    elif lt.size(respuesta)<6:
        for listas in lt.iterator(respuesta):
            for elementos in lt.iterator(listas):
                if elementos['Release_Date'] in resultado:
                    resultado[elementos['Release_Date']].append({elementos['Abbreviation'],elementos['Name'],elementos['Platforms'],elementos['Genres'],elementos['Total_Runs']})
                else:
                    resultado[elementos['Release_Date']]=[{elementos['Abbreviation'],elementos['Name'],elementos['Platforms'],elementos['Genres'],elementos['Total_Runs']}]

        for listas in lt.iterator(respuesta):
            cuentas = lt.size(listas)
            for fechas in resultado:
                resp.append([fechas,cuentas,tabulate(resultado[fechas],headers=['Abbreviation','Name','Plataforms','Genres','Total_Runs'],tablefmt='grid',maxcolwidths=12)])
    print(tabulate(reversed(resp),headers=['','Count','Details'],tablefmt='grid'))

def imprimir_re4(respuesta,limite_inf,limite_max):
    resultado = {}
    cuenta = {}
    resp = []
    print('================== Req No. 4 Answer ==================')
    print(f'Attempts between {limite_inf} and {limite_max}\n')

    print('----- Videogames release details -----')
    print(f'There are {lt.size(respuesta)} elements in range')
    if lt.size(respuesta)>6:
        print('Las primeras y ultimos 3 programas cargados son:\n')
        for listas in lt.iterator(lt.subList(respuesta,1,3)):
            cuentas = lt.size(listas)
            for elementos in lt.iterator(listas):
                if elementos['Record_Date_0'] in resultado:
                    resultado[elementos['Record_Date_0']].append([elementos['Num_Runs'],elementos['Time_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']])
                else:
                    resultado[elementos['Record_Date_0']]=[[elementos['Num_Runs'],elementos['Time_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']]]
            cuenta[elementos['Record_Date_0']] = cuentas
        for listas in lt.iterator(lt.subList(respuesta,lt.size(respuesta)-2,3)):
            cuentas = lt.size(listas)
            for elementos in lt.iterator(listas):
                if elementos['Record_Date_0'] in resultado:
                    resultado[elementos['Record_Date_0']].append([elementos['Num_Runs'],elementos['Time_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']])
                else:
                    resultado[elementos['Record_Date_0']]=[[elementos['Num_Runs'],elementos['Time_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']]]
            cuenta[elementos['Record_Date_0']] = cuentas

        for fechas in resultado:
            resp.append([fechas,str(cuenta[fechas]),tabulate(resultado[fechas],headers=['Num_Runs','Time_0','Name','Players_0','Country_0','Category','Subcategory'],tablefmt='grid',maxcolwidths=12)])
    elif lt.size(respuesta)<6:
        for listas in lt.iterator(respuesta):
            for elementos in lt.iterator(listas):
                if elementos['Record_Date_0'] in resultado:
                    resultado[elementos['Record_Date_0']].append([elementos['Num_Runs'],elementos['Time_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']])
                else:
                    resultado[elementos['Record_Date_0']]=[[elementos['Num_Runs'],elementos['Time_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']]]
            cuenta[elementos['Record_Date_0']] = cuentas

        for listas in lt.iterator(respuesta):
            cuentas = lt.size(listas)
            for fechas in resultado:
                resp.append([fechas,cuentas,tabulate(resultado[fechas],headers=['Num_Runs','Time_0','Name','Players_0','Country_0','Category','Subcategory'],tablefmt='grid',maxcolwidths=12)])
    print(tabulate(reversed(resp),headers=['','Count','Details'],tablefmt='grid'))


def imprimir_req3(respuesta,limite_inf,limite_max):
    resultado = {}
    cuenta = {}
    resp = []
    print('================== Req No. 3 Answer ==================')
    print(f'Attempts between {limite_inf} and {limite_max}\n')

    print('----- Videogames release details -----')
    print(f'There are {lt.size(respuesta)} elements in range')
    if lt.size(respuesta)>6:
        print('Las primeras y ultimos 3 programas cargados son:\n')
        for listas in lt.iterator(lt.subList(respuesta,1,3)):
            cuentas = lt.size(listas)
            if lt.size(listas) > 3:
                for elementos in lt.iterator(lt.subList(listas,1,3)):
                    if elementos['Num_Runs'] in resultado:
                        resultado[elementos['Num_Runs']].append([elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']])
                    else:
                        resultado[elementos['Num_Runs']]=[[elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']]]
                cuenta[elementos['Num_Runs']] = cuentas
            else:
                for elementos in lt.iterator(listas):
                    if elementos['Num_Runs'] in resultado:
                        resultado[elementos['Num_Runs']].append([elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']])
                    else:
                        resultado[elementos['Num_Runs']]=[[elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']]]
                cuenta[elementos['Num_Runs']] = cuentas
        for listas in lt.iterator(lt.subList(respuesta,lt.size(respuesta)-2,3)):
            cuentas = lt.size(listas)
            if lt.size(listas) > 3:
                for elementos in lt.iterator(lt.subList(listas,1,3)):
                    if elementos['Num_Runs'] in resultado:
                        resultado[elementos['Num_Runs']].append([elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']])
                    else:
                        resultado[elementos['Num_Runs']]=[[elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']]]
                cuenta[elementos['Num_Runs']] = cuentas
            else:
                for elementos in lt.iterator(listas):
                    if elementos['Num_Runs'] in resultado:
                        resultado[elementos['Num_Runs']].append([elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']])
                    else:
                        resultado[elementos['Num_Runs']]=[[elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']]]
                cuenta[elementos['Num_Runs']] = cuentas

        for fechas in resultado:
            resp.append([fechas,str(cuenta[fechas]),tabulate(resultado[fechas],headers=['Time_0','Record_Date_0','Name','Playes_0','Country_0','Category','Subcategory'],tablefmt='grid',maxcolwidths=12)])
    elif lt.size(respuesta)<6:
        for listas in lt.iterator(respuesta):
            cuentas = lt.size(listas)
            for elementos in lt.iterator(listas):
                if elementos['Num_Runs'] in resultado:
                    resultado[elementos['Num_Runs']].append([elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']])
                else:
                    resultado[elementos['Num_Runs']]=[[elementos['Time_0'],elementos['Record_Date_0'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['Category'],elementos['Subcategory']]]
            cuenta[elementos['Num_Runs']] = cuentas
        for fechas in resultado:
            resp.append([fechas,str(cuenta[fechas]),tabulate(resultado[fechas],headers=['Time_0','Record_Date_0','Name','Playes_0','Country_0','Category','Subcategory'],tablefmt='grid',maxcolwidths=12)])
    print(tabulate(resp,headers=['','Count','Details'],tablefmt='grid'))


def imprimir_req5(respuesta,limite_inf,limite_max):
    resultado = {}
    cuenta = {}
    resp = []
    print('================== Req No. 6 Answer ==================')
    print(f'Attempts between {limite_inf} and {limite_max}\n')
    print(f'Total records: {lt.size(respuesta)}')

    print('----- Videogames release details -----')
    print(f'There are {lt.size(respuesta)} elements in range')
    if lt.size(respuesta)>6:
        print('Las primeras y ultimos 3 programas cargados son:\n')
        for listas in lt.iterator(lt.subList(respuesta,1,3)):
            cuentas = lt.size(listas)
            if lt.size(listas) > 3:
                for elementos in lt.iterator(lt.subList(listas,1,3)):
                    if elementos['Time_0'] in resultado:
                        resultado[elementos['Time_0']].append([elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']])
                    else:
                        resultado[elementos['Time_0']]=[[elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']]]
                cuenta[elementos['Time_0']] = cuentas
            else:
                for elementos in lt.iterator(listas):
                    if elementos['Time_0'] in resultado:
                        resultado[elementos['Time_0']].append([elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']])
                    else:
                        resultado[elementos['Time_0']]=[[elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']]]
                cuenta[elementos['Time_0']] = cuentas
        for listas in lt.iterator(lt.subList(respuesta,lt.size(respuesta)-2,3)):
            cuentas = lt.size(listas)
            if lt.size(listas) > 3:
                for elementos in lt.iterator(lt.subList(listas,1,3)):
                    if elementos['Time_0'] in resultado:
                        resultado[elementos['Time_0']].append([elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']])
                    else:
                        resultado[elementos['Time_0']]=[[elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']]]
                cuenta[elementos['Time_0']] = cuentas
            else:
                for elementos in lt.iterator(listas):
                    if elementos['Time_0'] in resultado:
                        resultado[elementos['Time_0']].append([elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']])
                    else:
                        resultado[elementos['Time_0']]=[[elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']]]
                cuenta[elementos['Time_0']] = cuentas

        for fechas in resultado:
            resp.append([fechas,str(cuenta[fechas]),tabulate(resultado[fechas],headers=['Time_0','Record_Date_0','Name','Playes_0','Country_0','Category','Subcategory'],tablefmt='grid',maxcolwidths=12)])
    elif lt.size(respuesta)<6:
        for listas in lt.iterator(respuesta):
            cuentas = lt.size(listas)
            for elementos in lt.iterator(listas):
                if elementos['Time_0'] in resultado:
                    resultado[elementos['Time_0']].append([elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']])
                else:
                    resultado[elementos['Time_0']]=[[elementos['Record_Date_0'],elementos['Num_Runs'],elementos['Name'],elementos['Players_0'],elementos['Country_0'],elementos['plataforma'],elementos['Category'],elementos['Subcategory']]]
            cuenta[elementos['Time_0']] = cuentas
        for fechas in resultado:
            resp.append([fechas,str(cuenta[fechas]),tabulate(resultado[fechas],headers=['Record_Date_0','Num_Runs','Name','Playes_0','Country_0','plataforma','Category','Subcategory'],tablefmt='grid',maxcolwidths=12)])
    print(tabulate(reversed(resp),headers=['','Count','Details'],tablefmt='grid'))




def Sacar_Rangos(lista,segmentos,niveles):
    print('================== Req No. 6 Answer ==================')
    print(f'There are {lt.size(lista)} attempts on record. ')
    uno = lt.firstElement(lista)['Promedio']
    ultimo = lt.lastElement(lista)['Promedio']
    print(f'Lowest value: {uno}')
    print(f'Highest value: {ultimo}')
    print(f'The histogram count {lt.size(lista)} attempts.')
    print(f'Histogram with {segmentos} bins and {niveles} attempts per mark lvl.')
    valor_de_intervalos = (uno+ultimo)/segmentos
    rangos ={}
    for valores in range(1,segmentos+1):
        if valores == 1:
            rangos['({0},{1}]'.format(uno,round(valor_de_intervalos,2))]=0
        elif valores == segmentos:
            rangos['({0},{1}]'.format(round(valor_de_intervalos*(segmentos-1),2),ultimo)]=0
        else:
            rangos['[{0},{1}]'.format(round(valor_de_intervalos*(valores-1),2),round(valor_de_intervalos*(valores),2))]=0
    for rango in rangos:
        for valores in lt.iterator(lista):
            limites = rango[1:-1].split(',')
            if float(limites[0])<=float(valores['Promedio'])<=float(limites[1]):
                rangos[rango]+=1
    tabulate1 =[]
    for llaves in rangos:
        rangos[llaves] = [rangos[llaves],'+'*(round(rangos[llaves]/niveles))]
        tabulate1.append([llaves,rangos[llaves][0],len(rangos[llaves][1]),rangos[llaves][1]])

    print(tabulate(tabulate1,headers=['bin','count','lvl','mark'],tablefmt='grid',maxcolwidths=50))

def imprimir7(lista,top,plataforma,total):
        '''
    Esta función premite imprimir todos los primeros y ultimos 3
    programas en una lista
    '''
        print('========= Req No. 7 Answer =========')
        print(f'There are {total} records for {plataforma}')
        print(f'There are {lt.size(lista)} unique games for {plataforma}\n')

        firstandlast = []
        for informacion in lt.iterator(lt.subList(lista,1,top)):
            firstandlast.append([informacion['Name'],informacion['Release_Date'],informacion['Stream_Revenue'],informacion['Market_Share'],informacion['Time_Avg'],informacion['Total_Runs']])
        print(tabulate(firstandlast,headers=['Name','Release_Date','Stream_Revenue','Market_Share','Time_Avg','Total_Runs'],tablefmt='grid'))
def PrintReq2(catalogo,name):
    '''
    Esta función premite imprimir todos los primeros y ultimos 3
    programas en una lista
    '''
    print('================== Req No. 2 Answer ==================')
    total = 0
    for informacion in lt.iterator(catalogo):
        total+=int(informacion['Num_Runs'])

    print(f'Player {name} has {total} speedrun record attempets\n')
    print(f'---------- Player {name} details ----------')
    
    firstandlast = []
    if lt.size(catalogo)<=6:
        print(f'There are only {lt.size(catalogo)} elements in range')
        for informacion in lt.iterator(catalogo):
            firstandlast.append([informacion['Time_0'],informacion['Record_Date_0'],informacion['Name'],informacion['Players_0'],informacion['Country_0'],informacion['Num_Runs'],informacion['Category'],informacion['Subcategory']])
        print(tabulate(reversed(firstandlast),headers=['Time_0','Record_Date_0','Name','Players_0','Country_0','Num_Runs','Category','Subcategory'], tablefmt='grid', maxcolwidths=12))
    else:
        print('Las primeras y ultimos 3 programas cargados son:\n')
        for informacion in lt.iterator(lt.subList(catalogo,1,3)):
            firstandlast.append([informacion['Time_0'],informacion['Record_Date_0'],informacion['Name'],informacion['Players_0'],informacion['Country_0'],informacion['Num_Runs'],informacion['Category'],informacion['Subcategory']])
        for informacion in lt.iterator(lt.subList(catalogo,lt.size(catalogo)-2,3)):
            firstandlast.append([informacion['Time_0'],informacion['Record_Date_0'],informacion['Name'],informacion['Players_0'],informacion['Country_0'],informacion['Num_Runs'],informacion['Category'],informacion['Subcategory']])
        print(tabulate(firstandlast,headers=['Time_0','Record_Date_0','Name','Players_0','Country_0','Num_Runs','Category','Subcategory'], tablefmt='grid', maxcolwidths=12))

control=newController()

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        OpcionMuestra()
        muestra = int(input('Escoja la muestra a usar: '))
        datos,tiempo=controller.loadData(control,muestra)
        TopAndLast3(datos['model']["game_data"],datos['model']['category_data'])
        printTimeAndMemory(tiempo)

    elif int(inputs[0]) == 2:
        '''Requerimiento 1: Reportar los videojuegos de una
        plataforma en un rango de tiempo'''

        plataforma = input('Plataforma deseada: ')
        limite_inf = input('Fecha de lanzamiento minima: ')
        limite_max = input('Fecha de lanzamiento maxima: ')
        x,tiempo= controller.GetRangodeFechas(control,plataforma,limite_inf,limite_max)
        print('================== Req No. 1 Inputs ==================')
        print(f'Games relased between {limite_inf} and {limite_max}')
        print(f'In platform: {plataforma}\n')
        res,conteo = x
        imprimir_resultados(res,conteo,plataforma,limite_inf,limite_max)
        printTimeAndMemory(tiempo)
    
    elif int(inputs) == 3:
        name = input('Escriba el nombre del jugador: ')
        resultado,tiempo = controller.getPlayers(control,name)
        print('================== Req No. 2 Inputs ==================')
        print(f'Speedrun records for player: {name}\n')
        PrintReq2(resultado,name)
        printTimeAndMemory(tiempo)

    elif int(inputs[0])== 4:
        ''' Requerimiento 3'''
        intento1=int(input("Intento 1: "))
        intento2=int(input("Intento 2: "))
        resultado,tiempo=controller.getTiemposVeloces(control,intento1, intento2)
        print('================== Req No. 3 Inputs ==================')
        print(f'Category records between {intento1} and {intento2} attempts\n')
        imprimir_req3(resultado,intento1,intento2)
        printTimeAndMemory(tiempo)

    elif int(inputs[0]) == 5:
        '''Requerimiento 4'''
        limite_inf = input('Fecha de lanzamiento minima: ')
        hora_inf = input('Hora: ')
        limite_max = input('Fecha de lanzamiento maxima: ')
        hora_max = input('Hora: ')
        inferior = limite_inf+'T'+hora_inf+'Z'
        maxima = limite_max+'T'+hora_max+'Z'
        resp,tiempo = controller.GetTiemposLentos(control,inferior,maxima)
        print('================== Req No. 4 Inputs ==================')
        print(f'Category records between {inferior} and {maxima} datetime\n')
        imprimir_re4(resp,inferior,maxima)
        printTimeAndMemory(tiempo)

    elif int(inputs) == 6:
        '''Requerimiento 5: Ana Cristina R.'''
        limite_inferior= float(input('Ingresar el tiempo de record mínimo: '))
        limite_superior= float(input('Ingresar el tiempo de record máximo: '))
        resultado,tiempo= controller.GetTiemposRecord(control,limite_inferior, limite_superior)
        print('================== Req No. 5 Inputs ==================')
        print(f'Category records between {limite_inferior} and {limite_superior} runtime')
        imprimir_req5(resultado,limite_inferior,limite_superior)
        printTimeAndMemory(tiempo)

    elif int(inputs) == 7:
        '''Requerimiento 6'''
        opciones = ['El mejor tiempo registrado','El segundo mejor tiempo','El tercer mejor tiempo','Tiempo Promedio Registrado','El número de intentos']
        dateinf = input('Límite inferior del año de lanzamiento: ')
        datesup = input('Límite superior del año de lanzamiento: ')
        segmentos = int(input('Numero de segmentos del Histograma: '))
        niveles = int(input('Niveles de las marcas: '))
        print(tabulate([['Propiedades disponibles'],['1- El mejor tiempo registrado'],['2- El segundo mejor tiempo'],['3- El tercer mejor tiempo'],['4- Tiempo Promedio Registrado'],['5- El número de intentos']]))
        opcion = int(input('Escoja la propiedad que quieras usar: '))
        resultado,tiempo= controller.getHistogram(control,dateinf,datesup,opcion)
        print('\n================== Req No. 6 Inputs ==================')
        print(f'Count map (histogram) of the feature: {opciones[opcion-1]}')
        print(f'Data between release years of {dateinf} and {datesup}')
        print(f'Number of bins: {segmentos}')
        print(f'Registered attempts per scale: {niveles}\n')
        Sacar_Rangos(resultado,segmentos,niveles)
        printTimeAndMemory(tiempo)

    elif int(inputs) == 8:
        plataforma= input('Ingrese la plataforma que desea buscar: ')
        top = int(input('Top a escoger: '))
        resultado,tiempo= controller.getPlataforma(control, plataforma)
        print('\n================== Req No. 7 Inputs ==================')
        print(f'Find the TOP {top} games for {plataforma}.\n')
        print('Filtering records by platform...')
        print('Removing miscelaneous streaming revenue...\n')
        resultado,total = resultado
        imprimir7(resultado,top,plataforma,total) 
        printTimeAndMemory(tiempo)


    elif int(inputs) == 9:
        anio = input('Año de publicación: ')
        inf = input('Límite inferior de la duración del mejor tiempo del récord: ')
        maxi = input('Límite superior de la duración del mejor tiempo del récord: ')
        resultado,tiempo = controller.getMapa(control,anio,inf,maxi)
        printTimeAndMemory(tiempo)
        geolocator = Nominatim(user_agent = 'Getloc')
        def geolocate(country):
            try:
                # Geolocate the center of the country
                loc = geolocator.geocode(country)
                # And return latitude and longitude
                return (loc.latitude, loc.longitude)
            except:
                pass

        #Mapa vacio
        world_map= folium.Map(tiles="cartodbpositron",max_zoom=10)
        marker_cluster = MarkerCluster().add_to(world_map)

        for i in resultado:
            try:
                lat,long = geolocate(i)
                radius=10
                popup_text = """País: {}<br>
                    Número de coincidencias : {}<br>"""
                popup_text = popup_text.format(i,
                                   resultado[i]
                                   )
                folium.CircleMarker(location = [lat, long], radius=radius,popup= popup_text,fill =True).add_to(marker_cluster)
            except:
                pass
        #show the map
        world_map.save('Index.html')
        webbrowser.open('Index.html')
    else:
        sys.exit(0)
sys.exit(0)
