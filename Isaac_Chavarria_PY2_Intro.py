# ✦✦✦✦✦✦✦✦✦  P R O Y E C T O #2  ✦✦✦✦✦✦✦✦✦


# ✦✦✦✦✦✦✦✦✦  T E R R E N O S  ✦✦✦✦✦✦✦✦✦

class Casilla:
    def __init__(self, tipo):
        self.tipo = tipo

    def puede_pasar_jugador(self):
        return False

    def puede_pasar_enemigo(self):
        return False


class Camino(Casilla):
    def __init__(self):
        super().__init__("camino")

    def puede_pasar_jugador(self):
        return True

    def puede_pasar_enemigo(self):
        return True


class Muro(Casilla):
    def __init__(self):
        super().__init__("muro")


class Tunel(Casilla):
    def __init__(self):
        super().__init__("tunel")

    def puede_pasar_jugador(self):
        return True


class Liana(Casilla):
    def __init__(self):
        super().__init__("liana")

    def puede_pasar_enemigo(self):
        return True



# ✦✦✦✦✦✦✦✦✦  M A P A   Y   G E N E R A C I Ó N  ✦✦✦✦✦✦✦✦✦

import random

def crear_matriz_vacia(cantidad_filas, cantidad_columnas):
    return [[None for _ in range(cantidad_columnas)] for _ in range(cantidad_filas)]


def generar_mapa(cantidad_filas=15, cantidad_columnas=20):
    opciones_casilla = [Camino, Muro, Tunel, Liana]

    mapa = [
        [random.choice(opciones_casilla)() for _ in range(cantidad_columnas)]
        for _ in range(cantidad_filas)
    ]

    crear_camino_principal(mapa, cantidad_filas, cantidad_columnas)
    return mapa


def crear_camino_principal(mapa, cantidad_filas, cantidad_columnas):
    # Ruta garantizada hacia la salida
    fila_actual, columna_actual = 0, 0
    mapa[fila_actual][columna_actual] = Camino()

    for columna in range(1, cantidad_columnas):
        mapa[fila_actual][columna] = Camino()

    for fila in range(1, cantidad_filas):
        mapa[fila][cantidad_columnas - 1] = Camino()

    mapa[cantidad_filas - 1][cantidad_columnas - 1] = Camino()



# ✦✦✦✦✦✦✦✦✦  M O VI M I E N T O S   J U G A D O R  ✦✦✦✦✦✦✦✦✦

class Jugador:
    def __init__(self, fila_inicial, columna_inicial):
        self.fila = fila_inicial
        self.columna = columna_inicial
        self.energia = 100
        self.energia_maxima = 100

    def mover(self, direccion, mapa, correr=False):
        costo = 2 if correr else 1
        if self.energia < costo:
            return

        nueva_fila = self.fila
        nueva_columna = self.columna

        if direccion == "arriba":
            nueva_fila -= 1
        elif direccion == "abajo":
            nueva_fila += 1
        elif direccion == "izquierda":
            nueva_columna -= 1
        elif direccion == "derecha":
            nueva_columna += 1

        if nueva_fila < 0 or nueva_fila >= len(mapa):
            return
        if nueva_columna < 0 or nueva_columna >= len(mapa[0]):
            return

        casilla_destino = mapa[nueva_fila][nueva_columna]

        if not casilla_destino.puede_pasar_jugador():
            return

        self.fila = nueva_fila
        self.columna = nueva_columna
        self.energia -= costo

    def recuperar_energia(self):
        if self.energia < self.energia_maxima:
            self.energia += 1



# ✦✦✦✦✦✦✦✦✦  M O V I M I E N T O S   E N E M I G O  ✦✦✦✦✦✦✦✦✦

class Enemigo:
    def __init__(self, fila_inicial, columna_inicial):
        self.fila = fila_inicial
        self.columna = columna_inicial

    def mover(self, direccion, mapa):
        nueva_fila = self.fila
        nueva_columna = self.columna

        if direccion == "arriba":
            nueva_fila -= 1
        elif direccion == "abajo":
            nueva_fila += 1
        elif direccion == "izquierda":
            nueva_columna -= 1
        elif direccion == "derecha":
            nueva_columna += 1

        if nueva_fila < 0 or nueva_fila >= len(mapa):
            return
        if nueva_columna < 0 or nueva_columna >= len(mapa[0]):
            return

        casilla_destino = mapa[nueva_fila][nueva_columna]

        if not casilla_destino.puede_pasar_enemigo():
            return

        self.fila = nueva_fila
        self.columna = nueva_columna


# ✦✦✦✦✦✦✦✦✦  M O D O   E S C A P A  ✦✦✦✦✦✦✦✦✦

def modo_escapa():
    mapa = generar_mapa()
    jugador = Jugador(0, 0)

    enemigos = [
        Enemigo(5, 5),
        Enemigo(10, 3),
        Enemigo(7, 12)
    ]

    juego_activo = True

    while juego_activo:
        comando = input("Mover (w/a/s/d): ")

        if comando == "w":
            jugador.mover("arriba", mapa)
        elif comando == "s":
            jugador.mover("abajo", mapa)
        elif comando == "a":
            jugador.mover("izquierda", mapa)
        elif comando == "d":
            jugador.mover("derecha", mapa")

        # movimiento simple de enemigos para que no genere problemas
        # Cambiarlo despues por el completo
        for enemigo in enemigos:
            enemigo.mover(random.choice(["arriba","abajo","izquierda","derecha"]), mapa)

        # colisión
        for enemigo in enemigos:
            if enemigo.fila == jugador.fila and enemigo.columna == jugador.columna:
                print("Fuiste atrapado.")
                juego_activo = False

        # salida
        if (jugador.fila, jugador.columna) == (len(mapa)-1, len(mapa[0])-1):
            print("¡Escapaste!")
            juego_activo = False
