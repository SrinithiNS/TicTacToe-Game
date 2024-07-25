import socket
import threading
import pickle

# Class to represent the game scene
class scene:
    def __init__(self, matrix, over, counter):
        self.matrix = matrix
        self.over = over 
        self.winner = 0
        self.counter = counter

# Class to manage the Tic-Tac-Toe game
class TicTacToe:
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.you = " "
        self.opponent = " "
        self.winner = None
        self.game_over = False
        self.counter = 0

    # Function to initialize a game with a server
    def self_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.you = client.recv(1024).decode()
        if self.you == "O":
            self.opponent = "X"
        elif self.you == "X":
            self.opponent = "O"
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    # Function to handle the game logic for a single client
    def handle_connection(self, client):
        if self.you == 'X':
            move = input("Enter a move (row,column): ")
            if self.check_valid_move(move.split(',')):
                self.apply_move(move.split(','), self.you)
                self.print_board()
                data = scene(self.board, self.game_over, self.counter)
                client.send(pickle.dumps(data))
                self.board = data.matrix
            else:
                print("Invalid move!")

        while True:
            data = pickle.loads(client.recv(1024))
            self.counter = data.counter
            self.board = data.matrix
            self.print_board()
            if data.winner != 0:
                if self.you == data.winner:
                    print("You Won!")
                    break
                else:
                    print("You Lost!")
                    break
            if data.winner == 0 and data.counter == 9:
                print("It's a tie!")
                break
            check = True
            while check:
                move = input("Enter a move (row,column): ")
                if self.check_valid_move(move.split(',')):
                    check = False
                else:
                    print('Invalid move')
                
            self.apply_move(move.split(','), self.you)
            self.print_board()
            data = scene(self.board, self.game_over, self.counter)
            client.send(pickle.dumps(data))
            if data.over:
                break
            self.board = data.matrix
        
        client.close()

    # Function to apply a player's move to the board
    def apply_move(self, move, player):
        if self.game_over:
            return
        self.board[int(move[0])][int(move[1])] = player

    # Function to check if a move is valid
    def check_valid_move(self, move):
        if(int(move[0]) <= 2 and int(move[0]) >= 0 and int(move[1]) <= 2 and int(move[1]) >= 0):
            return self.board[int(move[0])][int(move[1])] == " "
        else:
            return False

    # Function to print the current game board
    def print_board(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("----------------")

# Create a TicTacToe game instance
game = TicTacToe()

# Connect to the TicTacToe server
game.self_game("localhost", 8888)
