import socket
from _thread import *

from network import Network
import time
network = Network(None)
network.server_start_game()


player_pairs = {}

def threaded_client(cncn, number):
    buffer = ""

    if len(player_pairs) % 2 == 0:
        pair_id = len(player_pairs) // 2 + 1  # Create a new pair
        player_pairs[pair_id] = {number: cncn}  # Store the first player
    else:
        pair_id = (len(player_pairs) // 2) + 1  # Get the last pair
        player_pairs[pair_id][number] = cncn  # Add second player to the pair
        player_pairs[pair_id][number-1].sendall("Timer\n".encode())

    print(player_pairs)
    print(f"{cncn} has connected")
    running = True
    while running:
        try:
            data_received = cncn.recv(2048).decode()
            buffer += data_received
            #print(f"Data received: {data_received}")
            #print(f"Buffer: {buffer}")
            while '\n' in buffer:
                if '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    print(f"Message: {message}")
                    print(f"Remaining buffer: {buffer}")
                    if not message:
                        print("No data")
                        continue

                    command, *data = message.split('|')
                    data = '|'.join(data)
                    print(f"Command: {command}, Data: {data}")
                    if '|' not in data:
                        print("No command")
                        continue

                    if command == "New":
                        print("Processing 'New' command")
                        player, unit_type = data.split('|')
                        opponent_id = [p for p in player_pairs[pair_id] if p != int(player)]
                        if opponent_id:
                            opponent_id = opponent_id[0]
                            if opponent_id in player_pairs[pair_id]:
                                player_pairs[pair_id][opponent_id].sendall(f"New|{player}|{unit_type}\n".encode())
                                time.sleep(0.2)
                                print("Sent 'New' command to opponent")

                    if command == "Move":
                        player, unit_type, index, position = data.split('|')
                        print(f"Player {player} moved {unit_type} {index} to {position}")

                        opponent_id = [p for p in player_pairs[pair_id] if p != int(player)]
                        if opponent_id:
                            opponent_id = opponent_id[0]
                            if opponent_id in player_pairs[pair_id]:
                                player_pairs[pair_id][opponent_id].sendall(
                                    f"Move|{player}|{unit_type}|{index}|{position}\n".encode()
                                )

                                print("Sent 'Move' command to opponent")

        except socket.error as e:
            print(f"Error in connection: {e}")
            running = False

number = 1

while True:
    cncn, addr = network.s_game.accept() #receives the address of the network and connection
    start_new_thread(threaded_client, (cncn, number))
    number += 1
