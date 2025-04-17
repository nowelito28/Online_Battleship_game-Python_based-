
import socket
import pickle
import sys
from jugador import Jugador
from utils import nombre


if len(sys.argv) == 3:
    ip_servidor, port = sys.argv[1], int(sys.argv[2])
else:
    print("No se ha especificado puerto. Lanzar como python3 01_servidor.py <ip_servidor> <puerto>")
    sys.exit(1)
inactividad = 'Conexión cerrada por inactividad'


class Usuario:
    def __init__(self, nom, enlace):
        self.nombre = nom
        self.socket = enlace
        self.nombre_opon = str


def final(user):
    fin = pickle.loads(user.socket.recv(1024))
    if fin[0] == 'G':
        print('\n*** HAS GANADO LA PARTIDA *** ')
    elif fin[0] == 'P':
        print('\n****', user.nombre_opon, 'HA GANADO LA PARTIDA ****')
    print('Puntos obtenidos en esta partida: ' + fin[1:]+'\n')
    ranking = pickle.loads(user.socket.recv(1024))
    print('\n*** RANKING ***')
    for line in ranking:
        print(line)
    print('\n*** GAME OVER ***')


def inicio(user):
    print('Esperando a entrar en partida...\n')
    ack = user.socket.recv(1024).decode()
    user.socket.sendall(ack.encode())
    if ack:
        bienvenida = pickle.loads(user.socket.recv(1024))
        print(bienvenida[0])
        user.nombre_opon = bienvenida[1]
        print('Enemigo: ', user.nombre_opon, '\n')
        print('Esperando para crear equipo...')

        cara_cruz = pickle.loads(user.socket.recv(1024))
        if cara_cruz:
            j = Jugador()
            user.socket.sendall(pickle.dumps(True))
            return j
    else:
        return


def juego(user, j):
    informe_opon = []
    ganar = False
    while not ganar:
        jugar = user.socket.recv(1024).decode()
        if jugar == 'jugar':
            print('\nTurno tuyo para jugar!')
            print('\n***Informe***')
            if len(informe_opon) == 0:
                print('No hay efecto en tu equipo.')
            else:
                for info in informe_opon:
                    print(info)
                informe_opon = []
            print('\n***Situación de equipo***')
            j.estado_equipo()
            print('\n***Realizar acción***')
            accion = j.realizar_accion()
            user.socket.settimeout(30)
            user.socket.sendall(pickle.dumps(accion))
            results = pickle.loads(user.socket.recv(1024))  # results={'informe':[...],'ganar':True/False,'pers_vivos':n} ó No_response ó No_accion
            if results == 'No_response':
                print(inactividad)
                return
            elif results == 'No_accion':
                ganar = False
            else:
                print('\n***Resultado de la acción***')
                for result in results['informe']:
                    print(result)
                print()
                ganar = results['ganar']
            num_vivos = j.pers_vivos()
            if ganar:
                user.socket.sendall(pickle.dumps(num_vivos))
                break
        elif jugar == 'esperar':
            print('Turno de', user.nombre_opon, '. Espera a tu turno...')
            accion = pickle.loads(user.socket.recv(1024))
            user.socket.settimeout(30)
            if accion == 'No_response':
                print('El jugador'+user.nombre_opon+'no responde.')
                return
            elif accion == 'No_accion':
                user.socket.sendall(pickle.dumps(accion))
                ganar = False
            else:
                results = j.recibir_accion(accion)
                user.socket.sendall(pickle.dumps(results))
                for result in results['informe']:
                    informe_opon.append(result)
                ganar = results['ganar']
        if ganar:
            break
    final(user)


def ver_nom_cogido(nombres, nom):
    for n in nombres:
        if n == nom:
            return True
    return False


def cliente():
    nom = nombre()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip_servidor, port))
    try:
        nombres = pickle.loads(client_socket.recv(1024))
        while ver_nom_cogido(nombres, nom):
            print('¡¡ Nombre ya cogido !!')
            nom = nombre()
        print('Conectado al servidor en el puerto: ', port)
        user = Usuario(nom, client_socket)
        user.socket.sendall(pickle.dumps(user.nombre))
        j = inicio(user)
        juego(user, j)
    except KeyboardInterrupt or TimeoutError or EOFError or OSError or BrokenPipeError:
        client_socket.close()

    print('Cerrando conexión...')
    client_socket.close()


cliente()
