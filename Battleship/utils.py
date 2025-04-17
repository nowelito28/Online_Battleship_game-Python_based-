
import random
from datetime import datetime, date

# tablero 4x4
col_tablero = 'D'
row_tablero = 4


def limpiar_terminal():
    print(chr(27) + '[2J')


def validar_celda(celda, max_col=col_tablero, max_row=row_tablero):
    min_col = 'A'
    min_row = 1
    try:
        col, row = celda[0].upper(), int(celda[1])
        if len(celda) != 2:
            return False
        elif (col <= max_col) and (row <= max_row) and (col >= min_col) and (row >= min_row):
            return True
        else:
            return False
    except ValueError or TypeError:
        return False


def validar_celda_disponible(celda, equipo):
    for pers in equipo:
        if pers.posicion == celda:
            return False
    return True


def cambiar_col_row(celda):
    c = ord(celda[0]) - ord('A') + 1
    r = int(celda[1])
    return c, r


def validar_celda_contigua(celdap, celdam):
    cp, rp = cambiar_col_row(celdap)
    cm, rm = cambiar_col_row(celdam)
    valido = False
    if celdap == celdam:
        valido = False
    elif (cp == cm) and (abs(rp-rm) == 1):
        valido = True
    elif (rp == rm) and (abs(cp-cm) == 1):
        valido = True
    return valido


def seleccionar_celda():
    coord = str(input('Porfavor, escriba coordenada: '))
    while not validar_celda(coord):
        coord = str(input('Porfavor escriba otra coordenada: '))
    col_mayus = coord[0].upper()
    coord = col_mayus + coord[1]
    return coord


def cel_right(celda):
    colum = celda[0]
    col = chr(int((ord(colum))) + 1)
    return col+celda[1]


def cel_down(celda):
    row = str(int(celda[1]) + 1)
    return celda[0]+row


def cel_down_right(celda):
    col = cel_right(celda)
    row = cel_down(celda)
    return col[0]+row[1]


def seleccionar_area_2x2(celda):
    celda_up_left = celda
    area_2x2 = []
    area_2x2.append(celda_up_left)
    validar = []
    celda_right = cel_right(celda_up_left)
    validar.append(celda_right)
    celda_down = cel_down(celda_up_left)
    validar.append(celda_down)
    celda_down_right = cel_down_right(celda_up_left)
    validar.append(celda_down_right)
    resto = []
    for celda in validar:
        if validar_celda(celda):
            resto.append(celda)
    area_2x2.extend(resto)
    return area_2x2


def par(n):
    if (n % 2) == 0:
        return True
    else:
        return False


def evitar_vida_negativa(n):
    if n < 0:
        return 0
    else:
        return n


def lanzar_moneda():
    m = random.randint(0, 1)
    return m


def nombre():
    nom = str(input('Porfavor, introduzca el nombre del usuario, sin el caracter ":": '))
    name = []
    for n in nom:
        name.append(n)
    if name.count(':') != 0:
        print('Mal escrito.')
        return nombre()
    return nom


def get_some_position_index(lista, char):
    positions = []
    for i in range(len(lista)):
        if lista[i] == char:
            positions.append(i)
    return positions


def fecha():
    actual = str(date.today())+'-'+str(datetime.now().hour)+'-'+str(datetime.now().minute)
    return actual


def transcribir_data(lista, var):
    for char in lista:
        var += char
    return var
