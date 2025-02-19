import threading

import pygame
import sys
from network import Network
from Base import Base
from Units import *
from Cities import City
from _thread import *
import time

pygame.init()

class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 650), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.network = Network(self)
        self.username = ""
        self.state = "LoginScreen"
        self.data = ""
        self.online_players = []
        self.invitee = ""
        self.opponent = ""
        self.lock = threading.Lock()
        self.player_number = 1
        self.winner = ""


    #functions to display on screen
    def write(self, txt, pos):
        font = pygame.font.Font(None, 32)
        font = font.render(txt, 0, (0, 0, 0))
        self.screen.blit(font, pos)

    def receive(self):

        while True:
            data = self.network.receive()
            pygame.display.flip()
            with self.lock:
                print(str(data))
                if data == "WaitingRoom":
                    self.state = "WaitingRoom"

                elif data.startswith("Players:"):
                    data = data[8:]
                    self.online_players = data.split(",")
                    #print("online players", str(self.online_players))

                elif data.startswith("Invitation:"):
                    data = data[11:]
                    self.data = data
                    self.invitee = self.data.split()
                    self.invitee = self.invitee[-1]

                    #adding time to control invitation
                elif data.startswith("Accepted:"):
                    print("Accepted")
                    data = data[9:]
                    print(f"{data}")
                    self.opponent = data
                    self.player_number = 1

                    self.state = "Game"


                #else:
                   # self.data = data
                    #time.sleep(4)
                    #print(self.data)

    def display_buttons(self, users, clicked):
        """ The script you see below is to display the available
    users a button to display as a screen"""
        button_rect = []
        button_y = 1
        mouse_pos = pygame.mouse.get_pos()
        for user in users:
            if user != "":
                button_rect.append(pygame.Rect(20, button_y * 40, 300, 35))
                pygame.draw.rect(self.screen, (225, 0, 225), button_rect[button_y - 1])
                self.write(user, (20, button_y * 40))
                button_y += 1

        index = 1
        for button in button_rect:
            if button.collidepoint(mouse_pos):
                if clicked:
                    self.write(f" Clicking {self.online_players[index]}", (300, 500))
                    self.network.send(f"Inviting|{self.online_players[index]}")
                    print("Sending invite")
                else:
                    self.write(f" Hovering over {self.online_players[index]}", (300, 500))
            index += 1

            #function for the actual login screen

    def accept_button(self, state):
        color = (225, 0, 0) if state else (0, 0, 225)
        button_rect = pygame.Rect(700, 600, 100, 35)
        pygame.draw.rect(self.screen, color, button_rect)
        self.write("Accept", (705, 600))
        return button_rect

    def login_screen(self):

        #colour
        blue = (0, 0, 220)
        red = (220, 0, 0)

        #input box details
        name_box_rect = pygame.Rect(140, 250, 300, 35)
        password_box_rect = pygame.Rect(140, 330, 300, 35)

        #button details
        login_button_rect = pygame.Rect(320, 370, 120, 40)
        register_button_rect = pygame.Rect(140, 370, 120, 40)

        #Input details
        username_txt = ""
        password_txt = ""
        selected_box = 0
        start_new_thread(self.receive, ())

        while self.state != "WaitingRoom" and self.state == "LoginScreen" and self.state != "Game":

            selected_button = ""
            self.screen.fill((120, 120, 120))

            #display input box
            self.write("Username:", (140, 220))
            pygame.draw.rect(self.screen, blue, name_box_rect, 2)
            self.write("Password:", (140, 300))
            pygame.draw.rect(self.screen, blue, password_box_rect, 2)

            #display buttons
            pygame.draw.rect(self.screen, red, login_button_rect)
            pygame.draw.rect(self.screen, red, register_button_rect)
            self.write("Register", (140, 375))
            self.write("Log in", (320, 375))

            #display written text
            self.write(username_txt, (name_box_rect.x +5 , name_box_rect.y +5))
            self.write("*" * len(password_txt), (password_box_rect.x+ 5, password_box_rect.y +5))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if name_box_rect.collidepoint(event.pos):
                        selected_box = 0
                    elif password_box_rect.collidepoint(event.pos):
                        selected_box = 1
                    elif register_button_rect.collidepoint(event.pos):
                        selected_button = "register"
                    elif login_button_rect.collidepoint(event.pos):
                        selected_button = "login"
                        self.username = username_txt

                elif event.type == pygame.KEYDOWN:
                    if selected_box == 0:
                        if event.key == pygame.K_BACKSPACE:
                            username_txt = username_txt[:-1]
                        else:
                            username_txt += event.unicode
                    elif selected_box == 1:
                        if event.key == pygame.K_BACKSPACE:
                            password_txt = password_txt[:-1]
                        else:
                            password_txt += event.unicode

            #script to execute the buttons
            if selected_button == "register":
                self.network.s.send(str(f"Register|{username_txt}@{password_txt}").encode())
            if selected_button == "login":
                self.network.s.send(str(f"Login|{username_txt}@{password_txt}").encode())

            #print("Still in login screen")
            self.clock.tick(60)
            pygame.display.update()

    #function for the waiting room
    def waiting_room(self):
        pygame.display.set_caption("WaitingRoom")
        start_new_thread(self.receive, ())
        invited = False
        start_time = None

        while self.state != "Game" or self.state != "LoginScreen" and self.state != "Game":
            if self.state == "Game":
                print("Game")
            #print("You are in waiting room")
            clicked = False
            if self.data != "":
                if start_time is None:
                    start_time = time.time()
                invited = True
            else:
                invited = False
                start_time = None
            if start_time is not None:
                spent_time = time.time() - start_time
            else:
                spent_time = 0
            if spent_time >= 7:
                self.data = ""
                start_time = None
                invited = False

            #print(f"Time spent: {spent_time: .2f}")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        clicked = True


            #print(self.online_players)
            self.screen.fill((255, 255, 255))

            self.write(self.data, (50, 500))
            self.display_buttons(self.online_players, clicked)

            accept_button = self.accept_button(invited)
            #for debugging invitee
            self.write(self.invitee, (600, 30))

            #handling command to accept request
            mx, my = pygame.mouse.get_pos()
            if clicked and  accept_button.collidepoint(mx, my) and invited:
                self.network.send(f"Accepted|{self.invitee}")
                self.opponent = self.invitee
                #player number
                self.player_number = 2
                self.state = "Game"

                break
            self.clock.tick(60)
            pygame.display.update()

    def easy_send(self):
        pass

    def main_game(self):
        #early network stuff
        self.network.s.close()
        print(self.player_number)
        #send this if you are player
        self.shared_timer = pygame.time.get_ticks()
        self.main_timer = 0

        pygame.display.set_caption("King of Kings")
        #start_new_thread(self.network.receive_game(), ())
        #mousepos = pygame.mouse.get_pos()
        self.opened = False

        self.base1 = Base(self, 1)
        self.base2 = Base(self, 2)

        self.Unit1 = Units(self, 1)
        self.Unit2 = Units(self, 2)

        self.cities = City(self)
        self.coins = None
        self.waves = 0

        self.network.start_receive_thread()
        while  self.state == "Game":
            self.network.s.close()
            self.clock.tick(60)
            self.mouse_pos = pygame.mouse.get_pos()
            self.screen.fill((120, 120, 120))
            # render the base on the screen
            self.write(self.coins, (300, 5))

            self.write(self.username, (100, 100))
            self.write(str(self.Unit1.money), (300, 100))
            self.write(str(self.Unit2.money), (400, 100))
            self.write("TIMER" +str(int(self.main_timer/1000)), (300, 20))
            self.write("Waves"+ str(self.waves), (300, 55))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            #self.write("Main Game", (30, 30))
            #self.write(f"You vs {self.opponent}", (100, 100))

            self.Unit1.render()
            self.Unit2.render()

            #render city
            self.cities.render()

            self.base1.render()
            self.base2.render()
            self.cities.check_income()
            mini_map = self.screen.copy()
            mini_map = pygame.transform.scale(mini_map, (200, 150))
            self.screen.blit(mini_map ,(1, 500))
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 498, 202, 152), 2)

            #ending game
            if self.waves == 7:
                self.state = "EndGame"
            if self.base1.score > self.base2.score and self.waves >= 7:
                self.winner = str(1)
                self.state = "EndGame"

            elif self.base1.score < self.base2.score and self.waves >= 7:
                self.winner = str(2)
                self.state = "EndGame"
            elif self.base1.score == self.base2.score and self.waves >= 7:
                self.winner = "Tie"
                self.state = "EndGame"

            #print(self.clock.get_fps())
            #self.write(str(self.clock.get_fps()), (100, 100))
            pygame.display.flip()

    def end_game(self):
        pygame.display.set_caption("EndGame")
        while self.state == "EndGame":
            self.screen.fill((225, 225, 225))
            self.write(f"Player {self.winner} wins", (300, 300))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(60)
            pygame.display.flip()
            print("End")
            print(self.winner)

game = Game()
game.network.client_start()
game.network.client_start_game(game.player_number)
while True:

    #game.main_game()
    if game.state == "WaitingRoom":
        game.waiting_room()
    elif game.state == "Game" :
        game.main_game()
    elif game.state == "LoginScreen":
        game.login_screen()
    elif game.state == "EndGame":
        game.end_game()
