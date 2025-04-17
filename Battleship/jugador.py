
from personaje import Medico, Inteligencia, Artillero, Francotirador
from utils import validar_celda, validar_celda_disponible, seleccionar_area_2x2, evitar_vida_negativa


class Jugador:
    def __init__(self):
        self.equipo = []
        self.crear_equipo()
        self.posicionar_equipo()
        self.informe = []

    def crear_equipo(self):
        print('Equipo: Médico, Inteligencia, Artillero, Francotirador')
        m = Medico()
        i = Inteligencia()
        a = Artillero()
        f = Francotirador()
        equipo = [m, i, a, f]
        for pers in equipo:
            pers.get_equipo_total(equipo)
            pers.vida_actual = pers.vida_maxima
        self.equipo = equipo

    def posicionar_equipo(self):
        print('Vamos a posicionar a nuestros personajes en el tablero!')
        for pers in self.equipo:
            print('(', pers.nom, ')')
            pos = input('Introduzaca una coordenada; columna: letras; fila: numeros: ')
            while not validar_celda(pos.upper()) or None or not validar_celda_disponible(pos.upper(), self.equipo):
                if not validar_celda(pos.upper()) or None:
                    print('Ups, no sirve esa coordenada')
                    pos = str(input('Introduzaca una coordenada; columna: letras ; fila: numeros: '))
                elif not validar_celda_disponible(pos.upper(), self.equipo):
                    print('Celda, ocupada.')
                    pos = str(input('Introduzaca una coordenada; columna: letras ; fila: numeros: '))
            pers.posicion = pos.upper()
        print('Posicionamiento completado.\n')

    def equipo_curado(self, equipo):
        for pers in equipo:
            if pers.vida_actual < pers.vida_maxima:
                return False
        return True

    def seleccion_accion(self, x):
        n = 0
        for pers in self.equipo:
            n = n+1
            if x == n:
                return pers.mover(self.equipo)
            if pers.enfriamiento_restante == 0:
                if (type(pers) is Medico) and not self.equipo_curado(self.equipo):
                    n = n + 1
                    if x == n:
                        return pers.habilidad()
                if type(pers) is Inteligencia:
                    n = n + 1
                    if x == n:
                        return pers.habilidad()
                if type(pers) is Artillero:
                    n = n + 1
                    if x == n:
                        return pers.habilidad()
                if type(pers) is Francotirador:
                    n = n + 1
                    if x == n:
                        return pers.habilidad()

    def realizar_accion(self):
        n = 0
        for pers in self.equipo:
            n += 1
            print('{}. Mover ({})'.format(n, pers.nom))
            if pers.enfriamiento_restante == 0:
                if (type(pers) is Medico) and not self.equipo_curado(self.equipo):
                    n += 1
                    print('{}. Curar a un compañero. ({})'.format(n, pers.nom))
                if type(pers) is Inteligencia:
                    n += 1
                    print('{}. Revelar a enemigos en un área 2x2. Daño {}. ({})'.format(n, pers.danyo_causa, pers.nom))
                if type(pers) is Artillero:
                    n += 1
                    print('{}. Disparar area (2x2). Daño {}. ({})'.format(n, pers.danyo_causa, pers.nom))
                if type(pers) is Francotirador:
                    n += 1
                    print('{}. Disparar a una celda. Daño {}. ({})'.format(n, pers.danyo_causa, pers.nom))
        s_a = int(input('Seleccione acción de este turno: '))
        while type(s_a) is not int or (s_a < 1) or (s_a > n):
            s_a = int(input('Porfavor, escriba el numero correspondiente con la acción seleccionada: '))
        return self.seleccion_accion(s_a)

    def quitar_muertos(self):
        for per in self.equipo:
            if per.vida_actual <= 0:
                self.equipo.remove(per)
        return self.equipo

    def como_afecta_a_enemigos(self, ataque):
        area_2x2 = seleccionar_area_2x2(ataque[1:])
        alcanzados = []
        for per in self.equipo:
            for celda in area_2x2:
                if per.posicion == celda:
                    if ataque[0] == 'A':
                        per.vida_actual -= 1
                    else:
                        per.vida_actual = per.vida_actual
                    alcanzados.append(per)
        return alcanzados

    def como_afecta_a_enemigo(self, celda):
        alcanzado = []
        for per in self.equipo:
            if per.posicion == celda:
                per.vida_actual -= 3
                alcanzado.append(per)
                return alcanzado

    def ganar(self):
        for per in self.equipo:
            if per.militar is True:
                return False
        return True

    def pers_vivos(self):
        n = 0
        for per in self.equipo:
            n += 1
        return n

    def recibir_accion(self, ataque):
        if ataque[0] == 'F':
            resultado = self.como_afecta_a_enemigo(ataque[1:])
        else:
            resultado = self.como_afecta_a_enemigos(ataque)
        resultados_accion = {}
        info_total = []
        self.quitar_muertos()
        info = str
        if not resultado:
            if ataque[0] == 'F':
                info = 'Francotirador no ha herido a nadie en la posición: '+ataque[1:]
            elif ataque[0] == 'I':
                info = 'Inteligencia no ha visto a nadie en el área dada por la celda: '+ataque[1:]
            elif ataque[0] == 'A':
                info = 'Artillero no ha herido a nadie en el área dada por la celda: '+ataque[1:]
            info_total.append(info)
        else:
            for per in resultado:
                if ataque[0] == 'I':
                    info = '{} ha sido visto en {}. [Vidas restantes: {}]'.format(per.nom, per.posicion, evitar_vida_negativa(per.vida_actual))
                elif (ataque[0] == 'A') or (ataque[0] == 'F'):
                    info = '{} ha sido herido en {}. [Vidas restantes: {}]'.format(per.nom, per.posicion, evitar_vida_negativa(per.vida_actual))
                info_total.append(info)
        resultados_accion['informe'] = info_total
        if self.ganar():
            resultados_accion['ganar'] = True
        else:
            resultados_accion['ganar'] = False
        num_pers_vivos = self.pers_vivos()
        resultados_accion['pers_vivos'] = num_pers_vivos
        return resultados_accion

    def estado_equipo(self):
        for pers in self.equipo:
            print('{} está en {} [Vida {}/{}]'.format(pers.nom, pers.posicion, evitar_vida_negativa(pers.vida_actual), pers.vida_maxima))
