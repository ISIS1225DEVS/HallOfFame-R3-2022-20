# -*- coding: utf-8 -*-

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
from itertools import chain
from types import FunctionType
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import heap as he
from DISClib.DataStructures import rbt as rb
from DISClib.Algorithms.Sorting import heapsort as heaps
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import orderedmap as om
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.Algorithms.Sorting import selectionsort as selection
assert cf

#objectos para el manejo de datos

#Class for adt list
class lista:
    """Creación de ADT lista
    ---------------------------------------------------------------------"""
    __slots__=["lista"]
    def __init__(self:object, dataestructure="SINGLE_LINKED", adt=None) -> None:
        """Contructor para crear una lista vacía
        ---------------------------------------------------------------------
        Args:
            self: Instancia
            dataestructure: Tipo de estructura de datos a utilizar para implementar
            la lista. Los tipos posibles pueden ser: ARRAY_LIST,
            SINGLE_LINKED y DOUBLE_LINKED.
            adt:En caso de que adt no sea None, se crea la clase y la lista por
            parametro se introduce como atributo
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        if adt is not None:
            self.lista=adt
        else:
            self.lista=lt.newList(datastructure=dataestructure)    
    def __str__(self) -> str:
        return str(self.lista)
    def __add__(self, other) -> chain:
        listt=self.lista
        pass
    def __call__(self) -> ...:
        return self.lista
    def __type__(self) -> str:
        return "rbt"
    def __iadd__(self) -> chain:
        pass
    def add_last(self:object, element:...) -> None:
        """Añade un elemento a la última posición de la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
            elemento: Elemento a añadir al inicio
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.addLast(self.lista, element)        
    def iterator(self:object) -> iter:
        """Retorna un iterador para la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            Iterador
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.iterator(self.lista)
    def present(self:object, element:...)->bool:
        """Informa si el elemento element esta presente en la lista.

        Informa si un elemento está en la lista.
        Si esta presente, retorna la posición en la que se encuentra
        o cero (0) si no esta presente. Se utiliza la función de comparación
        utilizada durante la creación de la lista para comparar los elementos.
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
            elemento: Elemento a buscar
        ---------------------------------------------------------------------
        Return: 
            Bool de si el elemento está presente
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.isPresent(self, element)
    def firstElement(self:object) -> ...:
        """Retorna el primer elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            Primer elemento
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.firstElement(self.lista)
    def lastElement(self:object) -> ...:
        """Retorna el último elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            Último elemento
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.lastElement(self.lista)
    def deleteElement(self:object, pos) -> None:
        """elimina el elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
            pos: Posición del elemento a eliminar
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.deleteElement(self.lista, pos)
    def removeFirst(self:object) -> None:
        """elimina el primer elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.removeFirst(self.lista)
    def removeLast(self:object) -> None:
        """elimina el último elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.removeLast(self.lista)
    def insertElement(self:object, elem, pos)->None:
        """inserta el elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
            pos: Posición del elemento a insertar
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.insertElement(self.lista, elem, pos)
    def size(self:object) -> int:
        """Retorna el número de elementos de la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            Tamaño de la lista
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.size(self.lista)
    def add_first(self:object, element:...) -> None:
        """_summary_

        Args:
            self (object): _description_
            element (_type_): _description_
        """
        lt.addFirst(self.lista, element)     
    def sublist(self:object, pos:int, numelem:int)->list:
        return lista(adt=lt.subList(self.lista, pos, numelem))
    def merge_sort(self:object, cmp:FunctionType)->object:
        self.lista=merge.sort(self.lista, cmp)
        return self      
    def selecion_sort(self:object, cmp:FunctionType)->object:
        self.lista=selection.sort(self.lista, cmp)
        return self
    def get(self:object, pos)->...:
        return lt.getElement(self.lista, pos)
    def first3_last3(self:object) -> chain:
        if self.size()>=6:
            return chain(self.sublist(1, 3).iterator(),self.sublist(self.size()-2, 3).iterator()) 
    def __iter__(self):
        return lt.iterator(self())


#class hash
class Hash:
    """Creación de Hash map
    ---------------------------------------------------------------------"""
    __slots__=["mapa"]
    def __init__(self, capacidad, tipo, factor, cmpf) -> None:
        """Contructor para crear el ADT hash map
        ---------------------------------------------------------------------
        Args:
            self: Instancia
            capacidad: Tamaño inicial de la tabla
            tipo: separate chaining ('CHAINING' ) o linear probing('PROBING')
            factor: Factor de carga inicial de la tabla
            cmpf: Funcion de comparación entre llaves
        ---------------------------------------------------------------------
        Return: 
            DISC.ADT: Hash map para almacenar la información
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        self.mapa=mp.newMap(capacidad,
                    maptype=tipo,
                    loadfactor=factor, 
                    comparefunction=cmpf)
    #Basic functions
    def __str__(self) -> str:
        return str(self.mapa)
    def __type__(self) -> str:
        return "rbt"
    def keys(self) -> list:
        """Retorna una class lista con todas las llaves de la tabla de hash
        ---------------------------------------------------------------------
        Args:
            self: Instancia(mapa)
        ---------------------------------------------------------------------
        Return: 
            DISC.ADT: lista de valores
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lista(adt=mp.keySet(self.mapa))
    def values(self) -> list:
        """Retorna una class lista con todas los valores de la tabla de hash
        ---------------------------------------------------------------------
        Args:
            self: Instancia(mapa)
        ---------------------------------------------------------------------
        Return: 
            DISC.ADT: lista de valores
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lista(adt=mp.valueSet(self.mapa))
    def items(self) -> zip:
        """Retorna una class zip con todas las llaves y valores de la tabla de hash
        ---------------------------------------------------------------------
        Args:
            self: Instancia(mapa)
        ---------------------------------------------------------------------
        Return: 
            DISC.ADT: zip de llaves y valores
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return zip(self.keys().iterator(),  self.values().iterator())
    def size(self) -> int:
        """Retorna el tamaño del hash map
        ---------------------------------------------------------------------
        Args:
            self: Instancia(mapa)
        ---------------------------------------------------------------------
        Return: 
            DISC.ADT: tamaño de la lista
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return mp.size(self.mapa) 
    def __get(self, key) -> ...:
        """Obetiene una pareja llave-valor
        ---------------------------------------------------------------------
        Args:
            self: Instancia(mapa)
            key: La llave asociada a la pareja
        ---------------------------------------------------------------------
        Return: 
            DISC.ADT: Pareja llave-valor
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return mp.get(self.mapa, key)
    def set_value(self:object, key:...,value:...):
        me.setValue(self.__get(key), value)
    def set_key(self:object, key:...,new_key:...):
        me.setKey(self.__get(key), new_key)
    def get_value(self, key) -> ...:
        return me.getValue(self.__get(key)) 
    def get_key(self, key) -> ...:
        return me.getKey(self.__get(key))
    def size_keys(self):
        return lt.size(self.keys())
    def put(self, key, value)  -> None:
        mp.put(self.mapa, key, value)
    def contains(self, key) -> bool:
        return mp.contains(self.mapa, key)






#class rbt

class rbt:
    __slots__=["tree"]
    def __init__(self, cmpf,ttype="RBT") -> None:
        self.tree=rb.newMap(cmpfunction=cmpf, omaptype=ttype, datastructure="CHAINING" )
    def __str__(self) -> str:
        return str(self.tree)
    def __type__(self) -> str:
        return "rbt"
    def get(self, key):
        return rb.get(self.tree, key)
    def put(self, key, value):
        rb.put(self.tree, key, value)
    def remove(self, key):
        rb.remove(self.tree, key)
    def contains(self, key):
        return rb.contains(self.tree, key)
    def size(self):
        return rb.size(self.tree)
    def isEmpty(self):
        return rb.isEmpty(self.tree)
    def keys(self):
        return lista(adt=rb.keySet(self.tree))
    def values(self):
        return lista(adt=rb.valueSet(self.tree))
    def items(self)->zip:
        return zip(self.keys.iterator(), self.values.iterator())
    def minKey(self):
        return rb.minKey(self.tree)
    def maxKey(self):
        return rb.maxKey(self.tree)
    def delMin(self):
        rb.deleteMin(self.tree)
    def delMax(self):
        rb.maxKey(self.tree)
    def floor(self, key):
        return rb.floor(self.tree, key)
    def ceiling(self, key):
        return rb.ceiling(self.tree, key)
    def select(self):
        return rb.select()
    def rank(self, key): 
        rb.rank(self.tree, key)
    def keys_range(self, keylo, keyhi):
        return lista(adt=rb.keys(self.tree, keylo, keyhi))
    def values_range(self, valuelo, valuehi):
        return lista(adt=rb.values(self.tree, valuelo, valuehi))
    def items_range(self, keylo, keyhi, valuelo, valuehi, cmpf):
        return zip(self.keys_range(keylo,keyhi, cmpf), valuelo, valuehi, cmpf)
    def get_value(self, key):
        value=self.get(key)
        return me.getValue(value) if value is not None else None
    def height(self)->int:
        return rb.height(self.tree)


class Heap:  
    def __init__(self, cmpf) -> None:
        self.mapa=he.newHeap(cmpf)
    def __type__(self) -> str:
        return "heap"
    def __add__(self, other) -> chain: 
        size1=self.mapa["size"]
        size2=other.mapa["size"]
        sizef=int(size1) + int(size2)
        lista1=self.mapa["elements"]["elements"]
        lista2=other.mapa["elements"]["elements"]
        listaf=lista1+lista2
        self.mapa["size"]=sizef
        self.mapa["elements"]["size"]=sizef
        self.mapa["elements"]["elements"]=listaf
        return self
    def __iadd__(self, other) -> chain:
        return self + other
    def size(self):
        return he.size(self.mapa)
    def  __str__(self) -> str:
        return str(self.mapa)
    def __call__(self) -> list:
        return self.mapa
    def isEmpty(self):
        return he.isEmpty(self.mapa)
    def min(self):
        return he.min(self.heap)
    def insert(self, elem):
        he.insert(self.mapa, elem)
    def heapsort(self):
        heaps.heapSort(self.mapa)
    def delMin(self):
        he.delMin(self.mapa)
    def iterator(self:object) -> iter:
        """Retorna un iterador para la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            Iterador
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.iterator(self.mapa["elements"])
    def present(self:object, element:...)->bool:
        """Informa si el elemento element esta presente en la lista.

        Informa si un elemento está en la lista.
        Si esta presente, retorna la posición en la que se encuentra
        o cero (0) si no esta presente. Se utiliza la función de comparación
        utilizada durante la creación de la lista para comparar los elementos.
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
            elemento: Elemento a buscar
        ---------------------------------------------------------------------
        Return: 
            Bool de si el elemento está presente
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.isPresent(self.mapa["elements"], element)
    def firstElement(self:object) -> ...:
        """Retorna el primer elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            Primer elemento
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.firstElement(self.mapa["elements"])
    def lastElement(self:object) -> ...:
        """Retorna el último elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            Último elemento
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        return lt.lastElement(self.mapa["elements"])
    def deleteElement(self:object, pos) -> None:
        """elimina el elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
            pos: Posición del elemento a eliminar
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.deleteElement(self.mapa["elements"], pos)
    def removeFirst(self:object) -> None:
        """elimina el primer elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.removeFirst(self.mapa["elements"])
    def removeLast(self:object) -> None:
        """elimina el último elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.removeLast(self.mapa["elements"])
    def insertElement(self:object, elem, pos)->None:
        """inserta el elemento en la lista
        ---------------------------------------------------------------------
        Args:
            self: Instancia(lista)
            pos: Posición del elemento a insertar
        ---------------------------------------------------------------------
        Return: 
            None
        ---------------------------------------------------------------------
        Raises:
            Exception"""
        lt.insertElement(self.mapa["elements"], elem, pos)
    def add_first(self:object, element:...) -> None:
        """_summary_

        Args:
            self (object): _description_
            element (_type_): _description_
        """
        lt.addFirst(self.mapa["elements"], element)     
    def sublist(self:object, pos:int, numelem:int)->list:
        return lista(adt=lt.subList(self.mapa["elements"], pos, numelem))
    def merge_sort(self:object, cmp:FunctionType)->object:
        self.mapa["elements"]=merge.sort(self.mapa["elements"], cmp)
        return self
    # def sort(self:object)->object:
    #     self.mapa=heaps.heapSort(self.mapa)   
    def get(self:object, pos)->...:
        return lt.getElement(self.mapa["elements"], pos)
    def first3_last3(self:object) -> chain:
        if self.size()>=6:
            return chain(self.sublist(1, 3).iterator(),self.sublist(self.size()-2, 3).iterator()) 



