
import socket
import sys
import pickle
import threading
from lobby import Lobby
from ranking import Ranking
from utils import lanzar_moneda, fecha

if len(sys.argv) == 4:
    port, num_max_partidas, fichero_ranking = int(sys.argv[1]), int(sys.argv[2]), str(sys.argv[3])
else:
    print("Porfavor, lanzar como python3 servidor.py <puerto> <numero_partidas_simultáneas> <fichero_ranking>")
    sys.exit(1)
ip_host = socket.gethostname()
lock_lobby = threading.Lock()
lock_partidas = threading.Lock()
lock_nombres = threading.Lock()
lock_ranking = threading.Lock()
num_partidas = 0
nombres = []
lobby = Lobby()
ranking = Ranking()
ranking.leer(fichero_ranking)
ranking.mostrar_en_ranking(fichero_ranking)


def meter_en_ranking(j1, pnt_1, j2, pnt_2, time_win):
    global ranking
    ranking_actual = []
    lock_ranking.acquire()
    try:
        ranking.insertar([j1[1], pnt_1, j2[1], time_win])
        ranking.insertar([j2[1], pnt_2, j1[1], time_win])
        ranking.mostrar_en_ranking(fichero_ranking)  # sobreescribe el nuevo ranking en el fichero de texto
        ranking_actual = ranking.ranking_escrito()
    finally:
        lock_ranking.release()
        return ranking_actual


def mensaje_ganador(jug, pnt, ganador, ranking_actual):
    if jug == ganador:
        jug[0].sendall(pickle.dumps('G'+str(pnt)))
    else:
        jug[0].sendall(pickle.dumps('P'+str(pnt)))
    jug[0].sendall(pickle.dumps(ranking_actual))  # servidor envia a cada jugador el ranking en una lista


def informar_ganador(j1, j2, ganador, pnt_1, pnt_2, time_win):
    global ranking
    ranking_actual = meter_en_ranking(j1, pnt_1, j2, pnt_2, time_win)
    mensaje_ganador(j1, pnt_1, ganador, ranking_actual)
    mensaje_ganador(j2, pnt_2, ganador, ranking_actual)
    print(j1[1]+' y '+j2[1]+' abandonan el servidor.\n')
    j1[0].close()
    j2[0].close()


def comparar_puntos(j1, j2, pnt_1, pnt_2, ganador):
    if (j1 == ganador) and (pnt_2 > pnt_1):
        pnt_1, pnt_2 = 1000, 900
        return pnt_1, pnt_2
    elif (j2 == ganador) and (pnt_1 > pnt_2):
        pnt_2, pnt_1 = 1000, 900
        return pnt_1, pnt_2
    else:
        return pnt_1, pnt_2


def puntuacion(j, ganador, turnos, num_vivos, num_vivos_op):
    puntos = 0
    if j == ganador:
        puntos += (max(0, (20-turnos))*20)+1000
    else:
        if turnos > 10:
            puntos += (turnos-10)*20
    puntos += num_vivos*100
    num_eliminados = 4-num_vivos_op
    puntos += num_eliminados*100
    return puntos


def crear_puntuaciones(j1, j2, ganador, n_pers_vivos_1, results, turno_1, turno_2):
    num_vivos_2, num_vivos_1 = results['pers_vivos'], n_pers_vivos_1
    pnt_1 = puntuacion(j1, ganador, turno_1, num_vivos_1, num_vivos_2)
    pnt_2 = puntuacion(j2, ganador, turno_2, num_vivos_2, num_vivos_1)
    pnt_1, pnt_2 = comparar_puntos(j1, j2, pnt_1, pnt_2, ganador)
    time_win = fecha()
    return pnt_1, pnt_2, time_win


def ver_resultados(resultados, j1, j2, turno_1, turno_2):
    if resultados == 'No_accion':
        perdido = False
    else:
        perdido = resultados['ganar']
        if resultados['ganar']:
            n_pers_vivos_1 = pickle.loads(j1[0].recv(1024))
            ganador = j1
            pnt_1, pnt_2, time_win = crear_puntuaciones(j1, j2, ganador, n_pers_vivos_1, resultados, turno_1, turno_2)
            informar_ganador(j1, j2, ganador, pnt_1, pnt_2, time_win)
    return perdido


def turno(j1, j2, turno_1, turno_2):
    j1[0].sendall('jugar'.encode())
    j2[0].sendall('esperar'.encode())

    accion = pickle.loads(j1[0].recv(1024))
    j1[0].settimeout(30)
    j2[0].sendall(pickle.dumps(accion))

    results = pickle.loads(j2[0].recv(1024))
    j1[0].sendall(pickle.dumps(results))

    return ver_resultados(results, j1, j2, turno_1, turno_2)


def jugar(j1, j2):
    global num_partidas, nombres
    ganar = False
    turno_1, turno_2 = 0, 0
    while not ganar:
        turno_1 += 1
        ganar = turno(j1, j2, turno_1, turno_2)
        if ganar:
            break
        elif not ganar:
            turno_2 += 1
            ganar = turno(j2, j1, turno_2, turno_1)
            if ganar:
                break
    lock_partidas.acquire()  # si se sale del bucle, es que uno de los jugadores ha gando y se termina la partida
    try:
        num_partidas -= 1
    finally:
        lock_partidas.release()
    lock_nombres.acquire()
    try:
        nombres.remove(j1[1])
        nombres.remove(j2[1])
    finally:
        lock_nombres.release()


def hacer_equipos(j1, j2):
    j1[0].sendall(pickle.dumps(True))
    finish1 = pickle.loads(j1[0].recv(1024))
    j1[0].settimeout(30)
    if finish1:
        j2[0].sendall(pickle.dumps(True))
        finish2 = pickle.loads(j2[0].recv(1024))
        j2[0].settimeout(30)
        return finish2


def turno_equipos(j1, j2, m, j1_cc, j2_cc):
    finish2 = bool
    if m == j1_cc:
        hacer_equipos(j1, j2)
    elif m == j2_cc:
        hacer_equipos(j2, j1)
    return finish2


def hacer_turnos(j1, j2):
    global num_partidas
    try:
        j1_cara_cruz, j2_cara_cruz = 1, 0
        m = lanzar_moneda()
        finish = turno_equipos(j1, j2, m, j1_cara_cruz, j2_cara_cruz)
        if finish:
            if m == j1_cara_cruz:
                jugar(j1, j2)
            elif m == j2_cara_cruz:
                jugar(j2, j1)
    except TimeoutError:
        j1[0].sendall(pickle.dumps('No_response'))
        j2[0].sendall(pickle.dumps('No_response'))
        print(j1[1] + ' y ' + j2[1] + ' abandonan el servidor, por inactividad.')
        j1[0].close()
        j2[0].close()
        lock_lobby.acquire()
        try:
            num_partidas -= 1
        finally:
            lock_lobby.release()


def empezar(j1, j2):
    try:
        bienvenida = 'Bienvenido a Tacttical Battle! A jugar!\n'
        j1[0].sendall(pickle.dumps((bienvenida, j2[1])))
        j2[0].sendall(pickle.dumps((bienvenida, j1[1])))
        hacer_turnos(j1, j2)
    except KeyboardInterrupt or EOFError:  # para cerrar hilo
        j1[0].close()
        j2[0].close()
        return


def actividad_ind(jug):
    global lobby, nombres
    ack = '.'
    try:
        jug[0].sendall(ack.encode())
        response = jug[0].recv(1024).decode()
        if response:
            return jug
    except BrokenPipeError:
        lock_nombres.acquire()
        try:
            nombres.remove(jug[1])
        finally:
            lock_nombres.release()
        return None


def lanzar_partida():
    global num_partidas, lobby
    jugs = []
    try:
        print('HAY MESAS LIBRES!!!\n')
        while True:
            if (lobby.tamanio > 0) and (num_partidas < num_max_partidas) and (len(jugs) < 2):
                lock_lobby.acquire()
                jug = lobby.desencolar()
                lock_lobby.release()
                jug_act = actividad_ind(jug)
                if jug_act:
                    jugs.append(jug)
                else:
                    print(jug[1] + ' se ha desconectado.\n')
                if len(jugs) < 2:
                    continue
                elif jugs[0][0] and jugs[1][0]:
                    threading.Thread(target=empezar, args=(jugs[0], jugs[1])).start()
                    lock_partidas.acquire()
                    num_partidas += 1
                    lock_partidas.release()
                    print('{} y {} están jugando.\n'.format(jugs[0][1], jugs[1][1]))
                    jugs = []
                    continue
            elif num_partidas >= num_max_partidas:
                break
        print('Esperando a que se liberen mesas...\n')
        while True:
            if num_partidas < num_max_partidas:
                lanzar_partida()  # recursividad
                return
    except KeyboardInterrupt:  # para cerrar hilo
        if jugs:
            for jug in jugs:
                jug[0].close()
        lock_lobby.acquire()
        while lobby.tamanio > 0:
            jug = lobby.desencolar()
            jug[0].close()
        lock_lobby.release()
        return


def servidor():
    global lobby, nombres
    print('Arrancando servidor...')
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip_host, port))
    print('Servidor en dirección IP: {}; en el puerto: {}'.format(ip_host, port))
    server_socket.listen()
    server_socket.settimeout(1000)
    print('Esperando jugadores y comenzar la primera partida...\n')
    threading.Thread(target=lanzar_partida).start()
    while True:
        try:
            client_socket = server_socket.accept()
            client_socket[0].sendall(pickle.dumps(nombres))  # Evitar que dos jugadores juegen con el mismo nombre
            user_nom = pickle.loads(client_socket[0].recv(1024))
            lock_nombres.acquire()
            nombres.append(user_nom)
            lock_nombres.release()
            print(user_nom, 'se ha conectado al servidor.\n')
            s_n = (client_socket[0], user_nom)
            lock_lobby.acquire()
            lobby.encolar(s_n)  # tupla (socket del usuario, nombre del usuario)
            lock_lobby.release()
        except KeyboardInterrupt or TimeoutError or EOFError:
            break

    print('Cerrando servidor...')
    server_socket.close()


servidor()
