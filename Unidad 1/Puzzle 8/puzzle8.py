import tkinter as tk
import random

###########################################################################################################
# Código de la clase Puzzle8 (sin cambios)
class Puzzle8:
    def __init__(self, interface):
        self.interface = interface
        self.interface.title("Puzzle 8 con Tkinter")
        self.numbers = [1,2,0,3,4,5,6,7,8]
        self.obtener_solucionable()
        self.botones = []
        self.crear_interfaz()

    def obtener_solucionable( self ):
        while True:
            random.shuffle( self.numbers )
            if( self.es_solucionable() ): return

    def crear_interfaz(self):
        for i in range(9):
            btn = tk.Button(self.interface, text=str(self.numbers[i]) if self.numbers[i] != 0 else "",
                            font=("Helvetica", 24), width=4, height=2,
                            command=lambda i=i: self.mover(i))
            btn.grid(row=i//3, column=i%3)
            self.botones.append(btn)

    def mover(self, i):
        idx_vacio = self.numbers.index(0)
        if self.es_movimiento_valido(i, idx_vacio):
            self.numbers[idx_vacio], self.numbers[i] = self.numbers[i], self.numbers[idx_vacio]
            self.actualizar_botones()
            if self.numbers == list(range(9)):
                self.mostrar_victoria()

    def es_movimiento_valido(self, i, idx_vacio):
        fila_i, col_i = i // 3, i % 3
        fila_v, col_v = idx_vacio // 3, idx_vacio % 3
        return abs(fila_i - fila_v) + abs(col_i - col_v) == 1

    def actualizar_botones(self):
        for i in range(9):
            texto = str(self.numbers[i]) if self.numbers[i] != 0 else ""
            self.botones[i].config(text=texto)

    def mostrar_victoria(self):
        victoria = tk.Label(self.interface, text="¡Puzzle resuelto!", font=("Helvetica", 18), fg="green")
        victoria.grid(row=3, column=0, columnspan=3)
        
    def es_solucionable(self):
        inversiones = 0
        lista_sin_cero = [n for n in self.numbers if n != 0]
        for i in range(len(lista_sin_cero)):
            for j in range(i + 1, len(lista_sin_cero)):
                if lista_sin_cero[i] > lista_sin_cero[j]:
                    inversiones += 1
        return inversiones % 2 == 0

###########################################################################################################

class NodoPuzzle:
    def __init__(self, estate, latestMove=None, father=None):
        self.estate = tuple(estate) # Convertir a tupla para que sea hashable
        self.latestMove = latestMove 
        self.father = father

###########################################################################################################

class DeepSearch():
    def __init__(self, listOfNumbers):
        self.initial_state = tuple(listOfNumbers)
        self.maxDepth = 100 # Profundidad máxima para la búsqueda
    
    def search(self):

        for depth_limit in range(1, self.maxDepth + 1):
            print(f"Buscando con profundidad {depth_limit}...")
            visited = set()
            solution_node = self.recursive_search(NodoPuzzle(self.initial_state), depth_limit, visited)
            if solution_node:
                return self.reconstruct_path(solution_node)
        return None

    def recursive_search(self, node, depth_limit, visited):
        if node.estate == tuple(range(9)) or node.estate == list([1,2,0,3,4,5,6,7,8]):
            return node
        
        if node.estate in visited or len(visited) > 100000:
            return None
        
        visited.add(node.estate)

        if len(self.reconstruct_path(node)) >= depth_limit:
            return None

        idx_vacio = node.estate.index(0)
        posibles_movimientos = self.obtainPossibleMoves(node.estate, idx_vacio)
        
        for move_value in posibles_movimientos:
            child_state_list = list(node.estate)
            idx_move = child_state_list.index(move_value)
            child_state_list[idx_vacio], child_state_list[idx_move] = child_state_list[idx_move], child_state_list[idx_vacio]
            
            child_node = NodoPuzzle(child_state_list, latestMove=move_value, father=node)
            
            result = self.recursive_search(child_node, depth_limit, visited)
            if result:
                return result
        
        return None

    def obtainPossibleMoves(self, estate, index_vacio):
        result = []
        fila_vacio, col_vacio = index_vacio // 3, index_vacio % 3
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Arriba, Abajo, Izquierda, Derecha

        for df, dc in direcciones:
            nueva_fila, nueva_col = fila_vacio + df, col_vacio + dc
            if 0 <= nueva_fila < 3 and 0 <= nueva_col < 3:
                nuevo_indice = nueva_fila * 3 + nueva_col
                result.append(estate[nuevo_indice])
        return result
        
    def reconstruct_path(self, solution_node):
        path = []
        current_node = solution_node
        while current_node.father is not None:
            path.append(current_node.latestMove)
            current_node = current_node.father
        return path[::-1] # Invertir la lista

if __name__ == "__main__":
    root = tk.Tk()
    juego = Puzzle8(root)
    
    buscador = DeepSearch(juego.numbers)
    juego.solucion = buscador.search()
    
    print("Resultado:", juego.solucion)

    def ejecutar_movimientos():
        # Verificamos si aún hay movimientos pendientes
        if juego.solucion:
            # Saca el valor del primer movimiento de la lista
            siguiente_movimiento_valor = juego.solucion.pop(0)
            
            # Encuentra el índice de la ficha que tiene ese valor
            # Este es el cambio crucial
            siguiente_movimiento_indice = juego.numbers.index(siguiente_movimiento_valor)

            # Realiza el movimiento en la interfaz
            juego.mover(siguiente_movimiento_indice)
            
            # Si aún quedan movimientos, programa el siguiente paso
            if juego.solucion:
                root.after(500, ejecutar_movimientos)
                
    # Llama a la función para empezar la animación después de 1 segundo
    root.after(1000, ejecutar_movimientos)

    root.mainloop()
