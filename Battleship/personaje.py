
from utils import validar_celda, validar_celda_disponible, validar_celda_contigua, seleccionar_celda


class Personaje:
    def __init__(self):
        self.posicion = str
        self.vida_actual = int
        self.enfriamiento_restante = 0  # 0(puede utilizar habilidad); 1(no puede utilizar habilidad)
        self.equipo_total = []

    def habilidad(self):
        raise NotImplementedError

    def get_equipo_total(self, equipo):
        self.equipo_total = equipo

    def get_cull_down_pasive(self):
        for pers in self.equipo_total:
            pers.enfriamiento_restante = 0

    def get_cull_down(self):
        for pers in self.equipo_total:
            pers.enfriamiento_restante = 0
        self.enfriamiento_restante = 1

    def condiciones(self, pos, equipo):
        pos = pos.upper()
        ok1 = validar_celda(pos)
        ok2 = validar_celda_disponible(pos, equipo)
        ok3 = validar_celda_contigua(self.posicion, pos)
        return pos, ok1, ok2, ok3

    def mover(self, equipo):
        pos = input('A donde desea moverlo: ')
        pos, ok1, ok2, ok3 = self.condiciones(pos, equipo)
        while (not ok1) or (not ok2) or (not ok3):
            pos = input('Porfavor, escoja otra posicion: ')
            pos, ok1, ok2, ok3 = self.condiciones(pos, equipo)
        self.posicion = pos
        print('El personaje se ha movido a: ', self.posicion, '\n')
        self.get_cull_down_pasive()
        return 'No_accion'


class Medico(Personaje):
    def __init__(self):
        super().__init__()
        self.nom = 'Medico'
        self.vida_maxima = 1
        self.militar = False
        self.danyo_causa = 0

    def life(self, pers):
        pers.vida_actual = pers.vida_maxima
        print('Ha curado a {} [Vidas: {}/{}]\n'.format(pers.nom, pers.vida_actual, pers.vida_maxima))
        return 'No_accion'

    def curar(self, i):
        x = int(input('Elija compañero al que curar (1 vida): '))
        while type(x) is not int or (x < 1) or (x > i):
            x = int(input('Porfavor, escriba el numero correspondiente al compañero que quiere curar: '))
        n = 0
        for pers in self.equipo_total:
            if self.herido(pers):
                n = n + 1
                if x == n:
                    return self.life(pers)

    def herido(self, pers):
        if pers.vida_actual < pers.vida_maxima:
            return True
        else:
            return False

    def habilidad(self):
        self.get_cull_down()
        n = 0
        for pers in self.equipo_total:
            if self.herido(pers):
                n = n + 1
                print('{}. {} [Vidas: {}/{}]'.format(n, pers.nom, pers.vida_actual, pers.vida_maxima))
        return self.curar(n)


class Inteligencia(Personaje):
    def __init__(self):
        super().__init__()
        self.nom = 'Inteligencia'
        self.vida_maxima = 2
        self.militar = False
        self.danyo_causa = 0

    def habilidad(self):
        self.get_cull_down()
        print('Indica las coordenadas de la esquina superior izquierda de la zona de observación (área 2x2):')
        celda_up_left = seleccionar_celda()
        return 'I' + celda_up_left


class Artillero(Personaje):
    def __init__(self):
        super().__init__()
        self.nom = 'Artillero'
        self.vida_maxima = 2
        self.militar = True
        self.danyo_causa = 1

    def habilidad(self):
        self.get_cull_down()
        print('Indica las coordenadas de la esquina superior izquierda en la que disparar (área 2x2):')
        celda_up_left = seleccionar_celda()
        return 'A' + celda_up_left


class Francotirador(Personaje):
    def __init__(self):
        super().__init__()
        self.nom = 'Francotirador'
        self.vida_maxima = 3
        self.militar = True
        self.danyo_causa = 3

    def habilidad(self):
        self.get_cull_down()
        print('Indica las coordenadas de la celda a la que disparar:')
        coord = seleccionar_celda()
        return 'F' + coord
