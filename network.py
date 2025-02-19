import socket
import threading
import time

import pygame.time


class Network:
    def __init__(self, script):
        self.IP = "192.168.1.139"#socket.gethostbyname(socket.gethostname())
        self.port = 4444
        self.addr = (self.IP, self.port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port_game = 8888
        self.addr_game = (self.IP, self.port_game)
        self.s_game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()
        self.script = script

    #function to initiate client side of the network
    def client_start(self):
        try:
            self.s.connect(self.addr)
            self.s.send(str("Hi I connected").encode())
        except socket.error:
            print(socket.error)

    #function to initiate server side of the network
    def server_start(self):
        try:
            self.s.bind(self.addr)
            self.s.listen(20)
            print("Successfully connected to assigned IP")
        except socket.error as e:
            print(f"Failed to connect to assigned IP: {e}")
            print("Failed to connect to assigned IP")

    def send(self, data):
        try:
            self.s.sendall(str(data).encode())
        except socket.error:
            print("Failed to send data")

    def receive(self):
        try:
            return self.s.recv(2048).decode()
        except socket.error:
            print("Socket reception error")

    def server_start_game(self):
        try:
            self.s_game.bind(self.addr_game)
            self.s_game.listen(20)

            print("Successfully connected to assigned IP")
        except socket.error:
            print("Failed to connect to assigned IP")

    def client_start_game(self, player_number):
        try:
            self.s_game.connect(self.addr_game)
            player_number_update = f"player_number|{player_number}"
            self.send_game(player_number_update)
            #self.s_game.send(str("Hi I connected").encode())
        except socket.error:
            print(socket.error)

    def send_game(self, data):
        try:
            self.s_game.sendall((str(data)+'\n').encode())
        except socket.error:
            print("Failed to send data")

    def receive_game(self):
        buffer = ""
        while True:
            try:
                with self.lock:
                    print("Waiting to receive data")
                    data = self.s_game.recv(2048).decode()
                    buffer += data

                    while '\n' in buffer:
                        message, buffer = buffer.split('\n', 1)
                        print(f"Reception: {message}")
                        if message.startswith("Timer"):
                            print("Trying to sync timer.....👌")
                            self.script.cities.current_time = pygame.time.get_ticks()
                            self.script.shared_timer = pygame.time.get_ticks()
                            self.script.main_timer = pygame.time.get_ticks()
                            self.script.waves = 0
                        if message.startswith("New|"):
                            _, player, unit_type = message.split('|')
                            print(f"🎯 Processing 'New' command for {unit_type} (Player {player})")

                            # ✅ Ensure that only the opponent creates the unit
                            if int(player) == self.script.player_number:
                                print("⚠️ Ignoring 'New' command - This player already created the unit.")
                            else:
                                if int(player) == 1:
                                    self.script.Unit1.create(unit_type)
                                else:
                                    self.script.Unit2.create(unit_type)

                                print(f"✅ Created {unit_type} for Player {player} on opponent's screen.")


                        elif message.startswith("Move|"):
                            _, player, unit_type, index, position = message.split('|')
                            x, y = map(int, position.split(','))
                            index = int(index)
                            key = f'player_{player}_units_{unit_type}'
                            unit_list = self.script.Unit1.unit_data if int(player) == 1 else self.script.Unit2.unit_data

                            # Ensure the unit list exists
                            if key not in unit_list:
                                print(f" Error: {key} not found in unit_list")
                                continue

                            #  Ensure the index is within range
                            index = int(index)
                            if index >= len(unit_list[key]):
                                print(f" Error: Tried to move {unit_type} {index}, but only {len(unit_list[key])} exist.")
                                continue

                            # Now we safely update the position
                            #unit_list[key][index].x = x
                            #unit_list[key][index].y = y
                            if int(player) == 1:
                                self.script.Unit1.unit_data[key][index].x = x
                                self.script.Unit1.unit_data[key][index].y = y
                                print("processing movement")
                            else:
                                self.script.Unit2.unit_data[key][index].x = x
                                self.script.Unit2.unit_data[key][index].y = y
                            print(f"Updated Player {player}'s {unit_type} {index} to position ({x}, {y})")


            except socket.error:
                print("Socket reception error")

    def start_receive_thread(self):
        print("Starting receive thread...")
        receive_thread = threading.Thread(target=self.receive_game, daemon=True)
        receive_thread.start()

