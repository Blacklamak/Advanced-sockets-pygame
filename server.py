import socket

from _thread import *
from network import Network

network = Network(None)

network.server_start()


def check_username_and_password(username, password):
    file = open("logindetails.txt", "r")
    for line in file:
        line = line.strip()
        name, code = line.split("@")
        #print(line)
        #print(f"{name},{code}")
        """if name == username:
            print("correct username")
        if code == password:
            print("correct password")"""
        if name == username and code == password:
            return True
    return False

#functions to handle data stored on the screen
def register( username, password):
    file = open("logindetails.txt", "a")
    file.write(f"{username}@{password}\n")

players = {}

#actual server code to handle received messages
def threaded_client(cncn, number):
    global players
    print(f"{cncn} has connected with id{number}")
    state = "LoginScreen"
    me = ""
    while state == "LoginScreen":
        try:
            data = cncn.recv(2048).decode()
            print(data)
            command, data = data.split('|')
            username, password = data.split('@')
            if command == "Register":
                register(username, password)
            elif command == "Login":
                if check_username_and_password(username, password):
                    #print("Correct details, Login successful")
                    players.update({username: cncn})
                    me = username
                    cncn.send(str("WaitingRoom").encode())
                    #print(players)
                    state="WaitingRoom"
                else:
                    print(f"Try again")
        except:
            print("Password and username not sent")
    while state =="WaitingRoom":
        try:
            online_players = ""
            for keys in players:
                online_players += f",{keys}"
            for connections in players.values():
                connections.send(f"Players:{online_players}".encode())
            data = cncn.recv(2048).decode()
            command, data = data.split('|')
            if command == "Inviting":
                for key in players:
                    if key == data:
                        players[key].send(f"Invitation: You got an invite from {me}".encode())
                        print(key)
            elif command == "Accepted":
                for key in players:
                    if key == data:
                        players[key].send(f"Accepted:{me}".encode())
                        print(key)
        except Exception as e:
            print("Error in waitingroom is: ",e)
            break
number = 1
while True:
    cncn, addr = network.s.accept() #receives the address of the network and connection
    start_new_thread(threaded_client, (cncn, number))
    number += 1
