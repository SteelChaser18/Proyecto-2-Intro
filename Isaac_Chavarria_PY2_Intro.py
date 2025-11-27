# ✦✦✦✦✦✦✦✦✦  P R O Y E C T O #2  ✦✦✦✦✦✦✦✦✦

# ✦✦✦✦✦✦✦✦✦  M E N Ú   P R I N C I P A L  ✦✦✦✦✦✦✦✦✦

def menu_principal():
    print("✦✦✦✦✦✦✦✦✦  B I E N V E N I D O  ✦✦✦✦✦✦✦✦✦")
    print("Registro de jugador\n")

    nombre_jugador = registrar_jugador()
    print(f"\nBienvenido, {nombre_jugador}.\n")

    while True:
        print("✦✦✦✦✦✦✦✦✦  M E N Ú   P R I N C I P A L  ✦✦✦✦✦✦✦✦✦")
        print("1. Modo Escapa")
        print("2. Modo Cazador")
        print("3. Ver Puntajes")
        print("4. Salir\n")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\nIniciando Modo Escapa...\n")
            modo_escapa(nombre_jugador)

        elif opcion == "2":
            print("\nIniciando Modo Cazador...\n")
            modo_cazador(nombre_jugador)

        elif opcion == "3":
            print("\nMostrando puntajes...\n")
            mostrar_puntajes()

        elif opcion == "4":
            print("Saliendo del juego...")
            break

        else:
            print("Opción inválida. Intente de nuevo.\n")

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
    mapa = []

    for _ in range(cantidad_filas):
        fila = []
        for _ in range(cantidad_columnas):
            numero = random.random()

            if numero < 0.70:
                fila.append(Camino())
            elif numero < 0.80:
                fila.append(Muro())
            elif numero < 0.90:
                fila.append(Tunel())
            else:
                fila.append(Liana())

        mapa.append(fila)

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


# ✦✦✦✦✦✦✦✦✦  P E R S E C U C I Ó N   D E   E N E M I G O S  ✦✦✦✦✦✦✦✦✦

def obtener_direccion_hacia(jugador, enemigo, mapa):
    diferencia_fila = jugador.fila - enemigo.fila
    diferencia_columna = jugador.columna - enemigo.columna

    opciones = []

    if abs(diferencia_fila) > abs(diferencia_columna):
        if diferencia_fila < 0:
            opciones.append("arriba")
        elif diferencia_fila > 0:
            opciones.append("abajo")

        if diferencia_columna < 0:
            opciones.append("despacho_izquierda")
        elif diferencia_columna > 0:
            opciones.append("derecha")
    else:
        if diferencia_columna < 0:
            opciones.append("izquierda")
        elif diferencia_columna > 0:
            opciones.append("derecha")

        if diferencia_fila < 0:
            opciones.append("arriba")
        elif diferencia_fila > 0:
            opciones.append("abajo")

    direcciones_validas = []
    for direccion in opciones:
        nueva_fila = enemigo.fila
        nueva_columna = enemigo.columna

        if direccion == "arriba":
            nueva_fila -= 1
        elif direccion == "abajo":
            nueva_fila += 1
        elif direccion == "izquierda":
            nueva_columna -= 1
        elif direccion == "derecha":
            nueva_columna += 1

        if not (0 <= nueva_fila < len(mapa)) or not (0 <= nueva_columna < len(mapa[0])):
            continue

        casilla_destino = mapa[nueva_fila][nueva_columna]

        if casilla_destino.puede_pasar_enemigo():
            direcciones_validas.append(direccion)

    if not direcciones_validas:
        return None

    return direcciones_validas[0]


# ✦✦✦✦✦✦✦✦✦  H U I D A   D E   E N E M I G O S  ✦✦✦✦✦✦✦✦✦

def obtener_direccion_huir(jugador, enemigo, mapa):
    diferencia_fila = jugador.fila - enemigo.fila
    diferencia_columna = jugador.columna - enemigo.columna

    opciones = []

    # invertir la lógica: alejarse del jugador
    if abs(diferencia_fila) > abs(diferencia_columna):
        if diferencia_fila < 0:
            opciones.append("abajo")
        elif diferencia_fila > 0:
            opciones.append("arriba")

        if diferencia_columna < 0:
            opciones.append("derecha")
        elif diferencia_columna > 0:
            opciones.append("izquierda")
    else:
        if diferencia_columna < 0:
            opciones.append("derecha")
        elif diferencia_columna > 0:
            opciones.append("izquierda")

        if diferencia_fila < 0:
            opciones.append("abajo")
        elif diferencia_fila > 0:
            opciones.append("arriba")

    # validar direcciones
    direcciones_validas = []
    for direccion in opciones:
        nueva_fila = enemigo.fila
        nueva_columna = enemigo.columna

        if direccion == "arriba":
            nueva_fila -= 1
        elif direccion == "abajo":
            nueva_fila += 1
        elif direccion == "izquierda":
            nueva_columna -= 1
        elif direccion == "derecha":
            nueva_columna += 1

        if not (0 <= nueva_fila < len(mapa)) or not (0 <= nueva_columna < len(mapa[0])):
            continue

        casilla_destino = mapa[nueva_fila][nueva_columna]

        if casilla_destino.puede_pasar_enemigo():
            direcciones_validas.append(direccion)

    if not direcciones_validas:
        return None

    return direcciones_validas[0]

# ✦✦✦✦✦✦✦✦✦  T R A M P A S  ✦✦✦✦✦✦✦✦✦

import time

class SistemaTrampas:
    def __init__(self):
        self.trampas = []
        self.tiempo_ultima_colocacion = 0
        self.cooldown = 5
        self.max_trampas = 3

    def colocar_trampa(self, fila, columna):
        instante_actual = time.time()

        # cooldown
        if instante_actual - self.tiempo_ultima_colocacion < self.cooldown:
            return

        # límite de trampas activas
        if len(self.trampas) >= self.max_trampas:
            return

        self.trampas.append({
            "fila": fila,
            "columna": columna,
            "tiempo_colocada": instante_actual
        })

        self.tiempo_ultima_colocacion = instante_actual

    def verificar_enemigos(self, enemigos):
        enemigos_eliminados = []

        for trampa in self.trampas:
            for enemigo in enemigos:
                if enemigo.fila == trampa["fila"] and enemigo.columna == trampa["columna"]:
                    enemigos_eliminados.append(enemigo)
                    self.trampas.remove(trampa)
                    break

        return enemigos_eliminados

# ✦✦✦✦✦✦✦✦✦  M O D O   E S C A P A  ✦✦✦✦✦✦✦✦✦

def modo_escapa(nombre_jugador):
    mapa = generar_mapa()
    jugador = Jugador(0, 0)

    enemigos = [
        Enemigo(6, 7),
        Enemigo(3, 12),
        Enemigo(10, 2)
    ]

    sistema_trampas = SistemaTrampas()
    cooldown_trampa = 0

    while True:

        mostrar_mapa(mapa, jugador, enemigos)

        print("Movimiento (w/a/s/d) | trampa (t) | salir (q)")
        comando = input("› ").lower()

        if comando == "q":
            print("Juego cancelado.")
            break

        # movimiento
        if comando == "w":
            jugador.mover("arriba", mapa)
        elif comando == "s":
            jugador.mover("abajo", mapa)
        elif comando == "a":
            jugador.mover("izquierda", mapa)
        elif comando == "d":
            jugador.mover("derecha", mapa)

        # colocar trampa
        if comando == "t":
            if cooldown_trampa == 0 and len(sistema_trampas.trampas) < sistema_trampas.max_trampas:
                sistema_trampas.colocar_trampa(jugador.fila, jugador.columna)
                cooldown_trampa = 3
            else:
                print("No puedes colocar trampa aún.")

        if cooldown_trampa > 0:
            cooldown_trampa -= 1

        # enemigos persiguen
        for enemigo in enemigos:
            direccion = obtener_direccion_hacia(jugador, enemigo, mapa)
            if direccion:
                enemigo.mover(direccion, mapa)

        # contacto → derrota
        for enemigo in enemigos:
            if enemigo.fila == jugador.fila and enemigo.columna == jugador.columna:
                print("Un enemigo te atrapó. ¡DERROTA!")
                return

        # trampas activas
        enemigos_eliminados = sistema_trampas.verificar_enemigos(enemigos)
        for enemigo in enemigos_eliminados:
            enemigos.remove(enemigo)
            enemigos.append(
                Enemigo(
                    random.randint(0, len(mapa)-1),
                    random.randint(0, len(mapa[0])-1)
                )
            )

        # victoria → salida
        if (jugador.fila, jugador.columna) == (len(mapa)-1, len(mapa[0])-1):
            print("\n¡HAS ESCAPADO!")
            print(f"Energía restante: {jugador.energia} pts")
            guardar_puntaje(nombre_jugador, jugador.energia, "escapa")
            break


# ✦✦✦✦✦✦✦✦✦  M O D O   C A Z A D O R  ✦✦✦✦✦✦✦✦✦

def modo_cazador(nombre_jugador):
    mapa = generar_mapa()
    jugador = Jugador(0, 0)

    enemigos = [
        Enemigo(6, 7),
        Enemigo(3, 12),
        Enemigo(10, 2)
    ]

    puntos = 0
    sistema_trampas = SistemaTrampas()  # solo para mostrar mapa, no se usan trampas

    while True:

        mostrar_mapa(mapa, jugador, enemigos)

        print("Mover (w/a/s/d) | salir (q)")
        comando = input("› ").lower()

        if comando == "q":
            print("Juego cancelado.")
            break

        # movimiento del jugador
        if comando == "w":
            jugador.mover("arriba", mapa)
        elif comando == "s":
            jugador.mover("abajo", mapa)
        elif comando == "a":
            jugador.mover("izquierda", mapa)
        elif comando == "d":
            jugador.mover("derecha", mapa)

        # enemigos huyen
        for enemigo in enemigos:
            direccion = obtener_direccion_huir(jugador, enemigo, mapa)
            if direccion:
                enemigo.mover(direccion, mapa)

        # atrapados → +10 pts
        capturados = []
        for enemigo in enemigos:
            if enemigo.fila == jugador.fila and enemigo.columna == jugador.columna:
                print("Enemigo atrapado (+10 pts)")
                puntos += 10
                capturados.append(enemigo)

        for enemigo in capturados:
            enemigos.remove(enemigo)
            enemigos.append(
                Enemigo(
                    random.randint(0, len(mapa)-1),
                    random.randint(0, len(mapa[0])-1)
                )
            )

        # enemigo llega a salida → -5 pts
        for enemigo in enemigos:
            if (enemigo.fila, enemigo.columna) == (len(mapa)-1, len(mapa[0])-1):
                print("Un enemigo escapó (-5 pts)")
                puntos -= 5

    # fin
    print(f"\nPuntaje final: {puntos}")
    guardar_puntaje(nombre_jugador, puntos, "cazador")


# ✦✦✦✦✦✦✦✦✦  R E G I S T R O   D E   J U G A D O R  ✦✦✦✦✦✦✦✦✦

import json
import os

def registrar_jugador():
    nombre = input("Ingrese su nombre: ").strip()

    if not nombre:
        print("Nombre inválido.")
        return registrar_jugador()

    datos = {"nombre": nombre}

    # crea archivo si no existe
    if not os.path.exists("jugadores.json"):
        with open("jugadores.json", "w") as archivo:
            json.dump([], archivo)

    # carga lista actual
    with open("jugadores.json", "r") as archivo:
        jugadores = json.load(archivo)

    # agrega nuevo jugador si no existe
    if nombre not in jugadores:
        jugadores.append(nombre)

    with open("jugadores.json", "w") as archivo:
        json.dump(jugadores, archivo, indent=4)

    return nombre

# ✦✦✦✦✦✦✦✦✦  P U N T A J E S :   G U A R D A R   ✦✦✦✦✦✦✦✦✦

def guardar_puntaje(nombre_jugador, puntos, modo):
    datos = cargar_puntajes()

    # agrega puntaje
    datos[modo].append({
        "jugador": nombre_jugador,
        "puntos": puntos
    })

    # ordenar y limitar a top 5
    datos[modo] = sorted(datos[modo], key=lambda x: x["puntos"], reverse=True)[:5]

    with open("puntajes.json", "w") as archivo:
        json.dump(datos, archivo, indent=4)

# ✦✦✦✦✦✦✦✦✦  P U N T A J E S :   C A R G A R   ✦✦✦✦✦✦✦✦✦

def cargar_puntajes():
    if not os.path.exists("puntajes.json"):
        with open("puntajes.json", "w") as archivo:
            json.dump({"escapa": [], "cazador": []}, archivo)

    with open("puntajes.json", "r") as archivo:
        return json.load(archivo)


# ✦✦✦✦✦✦✦✦✦  M O S T R A R   P U N T A J E S  ✦✦✦✦✦✦✦✦✦

def mostrar_puntajes():
    datos = cargar_puntajes()

    print("\n✦✦✦✦✦  TOP 5 - MODO ESCAPA  ✦✦✦✦✦")
    for item in datos["escapa"]:
        print(f"{item['jugador']} - {item['puntos']} pts")

    print("\n✦✦✦✦✦  TOP 5 - MODO CAZADOR  ✦✦✦✦✦")
    for item in datos["cazador"]:
        print(f"{item['jugador']} - {item['puntos']} pts")

    print()


# ✦✦✦✦✦✦✦✦✦  V I S U A L I Z A R   M A P A  ✦✦✦✦✦✦✦✦✦

def mostrar_mapa(mapa, jugador, enemigos):
    salida_fila = len(mapa) - 1
    salida_col = len(mapa[0]) - 1

    for fila in range(len(mapa)):
        linea = ""
        for columna in range(len(mapa[0])):

            # Prioridad: jugador > enemigo > salida > terreno
            if jugador.fila == fila and jugador.columna == columna:
                linea += " P "
                continue

            if any(e.fila == fila and e.columna == columna for e in enemigos):
                linea += " E "
                continue

            if fila == salida_fila and columna == salida_col:
                linea += " S "
                continue

            casilla = mapa[fila][columna]

            if isinstance(casilla, Camino):
                linea += " . "
            elif isinstance(casilla, Muro):
                linea += " * "
            elif isinstance(casilla, Tunel):
                linea += " U "
            elif isinstance(casilla, Liana):
                linea += " L "
            else:
                linea += " ? "
        print(linea)
    print()


# ✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦✦    

if __name__ == "__main__":
    menu_principal()
