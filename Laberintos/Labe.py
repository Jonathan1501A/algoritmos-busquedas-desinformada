import sys

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class labe():

    def __init__(self, filename):

        # Lee archivo y altura y ancho del laberinto
        with open(filename) as f:
            contents = f.read()

        # Valida el Inicio y el Objetivo
        if contents.count("A") != 1:
            raise Exception("Labe must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Labe must have exactly one goal")

        # Determine alto y ancho del laberitno
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Mantenga un registro de las paredes
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None


    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
    
    # Todas las posibles acciones
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

    # Asegurar que las acciones sean válidas y dentro de los límites del laberinto
        result = []
        for action, (r, c) in candidates:
        # Verifica que esté dentro de los límites del laberinto
            if 0 <= r < self.height and 0 <= c < self.width:
            # Verifica que la posición no sea una pared
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
        return result


    def solve(self):
        """Finds a solution to maze, if one exists."""

        # Mantenga un registro del número de estados explorados
        self.num_explored = 0

        # Inicializar la frontera solo a la posición inicial
        start = Node(state=self.start, parent=None, action=None)
        frontier = QueueFrontier()# linea para pasar de busqueda por expancion(QueueFrontier()) a busqueda profunda (StackFrontier()) 
        frontier.add(start)

        # Inicializar un conjunto explorado vacío
        self.explored = set()

        # Continúe repitiendo hasta encontrar la solución.
        while True:

            # Si no queda nada en la frontera, entonces no hay camino.
            if frontier.empty():
                raise Exception("no solution")

            # Elige un nodo de la frontera
            node = frontier.remove()
            self.num_explored += 1

            # Si el nodo es el objetivo, entonces tenemos una solución.
            if node.state == self.goal:
                actions = []
                cells = []
                
                #Siga los nodos principales para encontrar una solución
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Marcar nodo como explorado
            self.explored.add(node.state)

            # Añadir vecinos a la frontera
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)


    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Crea un Imagen en blanco
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Paredes
                if col:
                    fill = (40, 40, 40)

                # Inicio
                elif (i, j) == self.start:
                    fill = (255, 0, 0)

                # Meta
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)

                # Solucion
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)

                # Explorado
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)

                # Celda Vacia
                else:
                    fill = (237, 240, 252)

                # Dibuje Celda
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python Labe.py Labe.txt")

m = labe(sys.argv[1])
print("Laberinto:")
m.print()
print("Solucionando...")
m.solve()
print("Estados_Explorados:", m.num_explored)
print("Solucion:")
m.print()
m.output_image("Laberinto.png", show_explored=True) #show_explored=True
