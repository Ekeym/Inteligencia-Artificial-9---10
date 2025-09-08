import tkinter as tkinder
import random

class Puzzle8:
    def __init__(self, interface):
        self.interface = interface
        self.interface.title("Puzzle 8 con Tkinter")
        self.numbers = list(range(9))
        random.shuffle(self.numbers)
        self.botones = []
        self.crear_interfaz()

    def crear_interfaz(self):
        for i in range(9):
            btn = tkinder.Button(self.interface, text=str(self.numbers[i]) if self.numbers[i] != 0 else "",
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
        victoria = tkinder.Label(self.interface, text="¡Puzzle resuelto!", font=("Helvetica", 18), fg="green")
        victoria.grid(row=3, column=0, columnspan=3)

class NodoPuzzle:
    def __init__(self, key, value):
        self.key = key
        self.value = value          # Lista de 9 números
        self.chilren = []               # Lista de chilren (máximo 4)

    def new(self, child):
        if len(self.chilren) < 4:
            self.chilren.append(child)

class ArbolPuzzle:
    def __init__(self, root):
        self.root = NodoPuzzle(0, root)

    def searchKey(self, key, nodo=self.root):
        

    def esta_vacio(self):
        return self.root is None

class DeepSearch():
    lastestMove = 0
    deepness = 0
    possiblesMoves = []

    def __init__(self, listOfNumbers):
        self.listOfNumers = listOfNumbers
        doSearch()


    def obtainPossibleMoves( self ):
        pass

    def

    def doSearch( self ):
        self.possiblesMoves = self.obtainPossibleMoves(  )





        self.
        self.doSearch()





























# Ejecutar la aplicación
# if __name__ == "__main__":
#     root = tkinder.Tk()
#     app = Puzzle8(root)
#     print(app.numbers)

#     root.mainloop()


























































# game = 0

# board = list( range(9) )
# random.shuffle( board )

# def printBoard( board ):
#     print(f"{board[0:3]}\n{board[3:6]}\n{board[6:9]}")

# def move( board, cell ):
#     index_0, index_n = board.index(0), board.index(cell)
#     if( validMove(index_0, index_n) ) :
#         board[index_n], board[index_0] = board[index_0], board[index_n]
#         printBoard( board )
#         if( validWin( board ) ): endGame()

# def validMove( post0, postn ):
#     postn_X, postn_Y = postn//3, postn%3
#     post0_X, post0_Y = post0//3, post0%3
#     return abs( post0_X - postn_X ) + abs( post0_Y - postn_Y ) == 1
    
# def validWin( board ):
#     copyBoard = list.copy(board).sort()
#     return copyBoard == board

# def endGame( game ):
#     game = 1
#     print('has ganado, wiii...\n\n\nsalte lo que sigue no esta programado')


# # Comenzar juego
# printBoard( board )

# while( game == 0 ):
#     ficha = input('Por favor, mueve una ficha: ')
#     ficha = int(ficha)
#     move( board, ficha )
