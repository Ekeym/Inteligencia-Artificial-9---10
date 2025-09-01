import tkinter as tkinder
import random

game = 0

board = list( range(9) )
random.shuffle( board )

def printBoard( board ):
    print(f"{board[0:3]}\n{board[3:6]}\n{board[6:9]}")

def move( board, cell ):
    index_0, index_n = board.index(0), board.index(cell)
    if( validMove(index_0, index_n) ) :
        board[index_n], board[index_0] = board[index_0], board[index_n]
        printBoard( board )
        if( validWin( board ) ): endGame()

def validMove( post0, postn ):
    postn_X, postn_Y = postn//3, postn%3
    post0_X, post0_Y = post0//3, post0%3
    return abs( post0_X - postn_X ) + abs( post0_Y - postn_Y ) == 1
    
def validWin( board ):
    copyBoard = list.copy(board).sort()
    return copyBoard == board

def endGame( game ):
    game = 1
    print('has ganado, wiii...\n\n\nsalte lo que sigue no esta programado')


# Comenzar juego
printBoard( board )

while( game == 0 ):
    ficha = input('Por favor, mueve una ficha: ')
    ficha = int(ficha)
    move( board, ficha )