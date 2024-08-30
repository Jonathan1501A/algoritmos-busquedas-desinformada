from collections import deque

class Estado:
    def __init__(self, misioneros, canibales, bote, camino=None):
        self.misioneros = misioneros
        self.canibales = canibales
        self.bote = bote  # 'izquierda' o 'derecha'
        self.camino = camino if camino is not None else []

    def es_valido(self):
        # Verificar si el estado es válido
        # La condición revisa tanto la orilla izquierda como la derecha.
        if self.misioneros < 0 or self.canibales < 0 or self.misioneros > 3 or self.canibales > 3:
            return False
        if (self.misioneros > 0 and self.misioneros < self.canibales) or (3 - self.misioneros > 0 and 3 - self.misioneros < 3 - self.canibales):
            return False
        return True

    def es_meta(self):
        # Verificar si hemos alcanzado el estado meta (todos los misioneros y caníbales están en la derecha)
        return self.misioneros == 0 and self.canibales == 0 and self.bote == 'derecha'

    def proximos_estados(self):
        # Generar todos los posibles próximos estados desde el estado actual
        movimientos = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]  # posibles movimientos
        proximos = []
        for m, c in movimientos:
            if self.bote == 'izquierda':
                nuevo_estado = Estado(self.misioneros - m, self.canibales - c, 'derecha', self.camino + [(m, c, 'derecha')])
            else:
                nuevo_estado = Estado(self.misioneros + m, self.canibales + c, 'izquierda', self.camino + [(m, c, 'izquierda')])
            if nuevo_estado.es_valido():
                proximos.append(nuevo_estado)
        return proximos

    def __repr__(self):
        return f"({self.misioneros}, {self.canibales}, {self.bote})"

def bfs():
    estado_inicial = Estado(3, 3, 'izquierda')
    cola = deque([estado_inicial])
    visitados = set()

    while cola:
        estado_actual = cola.popleft()

        if estado_actual.es_meta():
            return estado_actual.camino

        visitados.add((estado_actual.misioneros, estado_actual.canibales, estado_actual.bote))

        for estado in estado_actual.proximos_estados():
            if (estado.misioneros, estado.canibales, estado.bote) not in visitados:
                cola.append(estado)

    return None

# Ejecutar BFS para encontrar la solución
solucion = bfs()

if solucion:
    print("Solución encontrada:")
    for paso in solucion:
        print(f"Mover {paso[0]} misionero(s) y {paso[1]} caníbal(es) a la orilla {paso[2]}.")
else:
    print("No se encontró solución.")
