
from utils import get_some_position_index, transcribir_data
# lista doble enlazada: 'Ranking' preparada para tratar el fichero de texto 'ranking_extension.txt'


class Nodo:
    def __init__(self, pnt, sig, ant):
        self.dato = pnt  # [nombre(str), puntuación(int), nombre_opon(str), fecha_y_hora]
        self.siguiente = sig
        self.anterior = ant


class Ranking:
    def __init__(self):
        self.top = None
        self.bottom = None
        self.tamanio = 0

    def vacia(self):
        return self.tamanio == 0

    def leer(self, text):
        datos = []
        with open(text, 'r') as f:
            message = f.readlines()
        for line in message:
            for c in line:
                datos.append(c)
            if datos.count('\n') != 0:
                datos.remove('\n')
            positions = get_some_position_index(datos, ':')
            n1, n2, n3 = positions[0], positions[1], positions[2]
            nombre, pnt, nombre_op, fecha = datos[0], datos[n1+1], datos[n2+1], datos[n3+1]
            nombre = transcribir_data(datos[1:n1], nombre)
            pnt = int(transcribir_data(datos[n1 + 2:n2], pnt))
            nombre_op = transcribir_data(datos[n2 + 2:n3], nombre_op)
            fecha = transcribir_data(datos[n3 + 2:], fecha)
            dato = [nombre, pnt, nombre_op, fecha]
            self.insertar(dato)  # Cada dato es [nombre(str), puntuación(int), nombre_opon(str), fecha_y_hora].
            dato, datos = [], []

    def insertar(self, dato):  # Si puntuación coincide con alguna del ranking, la nueva insertada se pone por encima.
        jug = Nodo(dato, None, None)
        if self.vacia():
            self.top = jug
            self.bottom = jug
        elif self.buscar(dato[0]):
            self.modificar(jug)
        elif jug.dato[1] >= self.top.dato[1]:
            jug.siguiente = self.top
            self.top.anterior = jug
            self.top = jug
        elif jug.dato[1] < self.bottom.dato[1]:
            jug.anterior = self.bottom
            self.bottom.siguiente = jug
            self.bottom = jug
        else:  # (jug.dato[1] < self.top.dato[1]) and/or (jug.dato[1] >= self.bottom.dato[1])
            jug_aux = self.top
            while (jug.dato[1] < jug_aux.dato[1]) and jug_aux:
                jug_aux = jug_aux.siguiente
            jug.anterior = jug_aux.anterior
            jug.siguiente = jug_aux
            jug.anterior.siguiente = jug
            jug_aux.anterior = jug
        self.tamanio += 1

    def buscar(self, nombre):
        jug_aux = self.top
        if self.vacia():
            return False
        while (jug_aux.dato[0] != nombre) and jug_aux.siguiente is not None:
            jug_aux = jug_aux.siguiente
        return jug_aux.dato[0] == nombre

    def eliminar(self, jug):
        if jug == self.top:
            self.top = jug.siguiente
            self.top.anterior = None
            jug.siguiente = None
        elif jug == self.bottom:
            self.bottom = jug.anterior
            self.bottom.siguiente = None
            jug.anterior = None
        else:
            jug.anterior.siguiente = jug.siguiente
            jug.siguiente.anterior = jug.anterior
            jug.siguiente = None
            jug.anterior = None
        return jug

    def modificar(self, jug):
        jug_aux = self.top
        while (jug_aux.dato[0] != jug.dato[0]) and jug_aux:
            jug_aux = jug_aux.siguiente
        if jug_aux.dato[0] == jug.dato[0]:
            jug_aux.dato[1] += jug.dato[1]  # se suman la puntuacion nueva a la anterior = total
            jug_aux.dato[3] = jug.dato[3]  # se le cambia la fecha a la más reciente
            jug_ren = self.eliminar(jug_aux)
            self.tamanio -= 1
            self.insertar(jug_ren.dato)
        else:
            print('No está en el ranking')

    def ranking_escrito(self):
        jug_aux = self.top
        rank = []
        while jug_aux:
            frase = jug_aux.dato[0]+':'+str(jug_aux.dato[1])+':'+jug_aux.dato[2]+':'+jug_aux.dato[3]+'\n'
            rank.append(frase)
            jug_aux = jug_aux.siguiente
        return rank

    def mostrar_en_ranking(self, text):
        f = open(text, 'w')
        rank = self.ranking_escrito()
        for frase in rank:
            f.write(frase)
        f.close()
