import socket
import threading
import pickle

# Define a class to represent the game scene
class scene:
    def __init__(self, matrix, over, counter):
        self.matrix = matrix
        self.over = over
        self.winner = 0
        self.counter = counter

# Function to check if a player has won
def check_if_won(game):
    for row in range(3):
        if game[row][0] == game[row][1] == game[row][2] != " ":
            return True
    for col in range(3):
        if game[0][col] == game[1][col] == game[2][col] != " ":
            return True
    if game[0][0] == game[1][1] == game[2][2] != " ":
        return True
    if game[0][2] == game[1][1] == game[2][0] != " ":
        return True
    return False

# Function to handle the game logic for a single client
def handle_connection(client, player):
    while True:
        # Receive data from the client and update the game scene
        data = pickle.loads(client.recv(1024))
        data.counter += 1
        matrix = data.matrix

        # Check if the game is over
        data.over = check_if_won(matrix)
        if data.over:
            print(f'Player {player} won')
            data.winner = player
            # Send the updated game state to all clients
            for client in clients:
                client.send(pickle.dumps(data))
            break
        elif data.winner == 0 and data.counter == 9:
            print("It's a Tie")
            # Send the updated game state to all clients
            for client in clients:
                client.send(pickle.dumps(data))
            break
        else:
            # Send the updated game state to the other player
            if player == 'X':
                client2.send(pickle.dumps(data))
            elif player == 'O':
                client1.send(pickle.dumps(data))

# Create a socket for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 8888))
server.listen(2)

print("Waiting for players...")

# Accept two clients
client1, addr1 = server.accept()
client1.send("X".encode())
print(f"Player 1 connected: {addr1}")
client2, addr2 = server.accept()
client2.send("O".encode())
print(f"Player 2 connected: {addr2}")

clients = [client1, client2]

# Create threads to handle each client
thread1 = threading.Thread(target=handle_connection, args=(client1, "X"))
thread2 = threading.Thread(target=handle_connection, args=(client2, "O"))

# Start the game
thread1.start()
thread2.start()