

class Nodo:
    def __init__(self, jug, sig):
        self.jugador = jug  # jug = tupla (socket del usuario, nombre del usuario)
        self.siguiente = sig


class Lobby:
    def __init__(self):
        self.frente = None
        self.final = None
        self.tamanio = 0

    def vacia(self):
        return self.tamanio == 0

    def encolar(self, jug):
        new_jug = Nodo(jug, None)

        if self.vacia():
            self.frente = new_jug
            self.final = new_jug
        else:
            self.final.siguiente = new_jug
            self.final = new_jug
        self.tamanio += 1

    def desencolar(self):
        if not self.vacia():
            self.tamanio -= 1
            if self.frente == self.final:
                jug = self.frente.jugador
                self.frente = None
                self.final = None
            else:
                jug = self.frente.jugador
                self.frente = self.frente.siguiente
            return jug

    def mostrar_frente(self):
        if not self.vacia():
            return self.frente.jugador

    def buscar(self, jug):
        if self.vacia():
            return None
        else:
            jug_prim = self.frente
            while jug_prim and (jug_prim.jugador != jug) and (jug_prim.siguiente is not None):
                jug_prim = jug_prim.siguiente
            if jug_prim.jugador == jug:
                return True
            else:
                return False

    def mostrar_lobby(self):
        jug_prim = self.frente
        if not jug_prim:
            print('La cola se encuantra vacía.\n')
        else:
            while jug_prim:
                print(jug_prim.jugador, end=' => ')
                jug_prim = jug_prim.siguiente
            print("\n")

    def eliminar(self, jug):
        if jug == self.frente:
            self.frente = jug.siguiente
            jug.siguiente = None
        elif jug == self.final:
            jug_aux = self.frente
            while jug_aux.siguiente != self.final:
                jug_aux = jug_aux.siguiente
            jug_aux.siguiente = None
            self.final = jug_aux
        else:
            jug_aux = self.frente
            while jug_aux.siguiente != jug:
                jug_aux = jug_aux.siguiente
            jug_aux.siguiente = jug.siguiente
            jug.siguiente = None
        self.tamanio -= 1
