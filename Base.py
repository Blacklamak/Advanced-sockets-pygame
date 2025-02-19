import pygame


class Base:
    def __init__(self, script, player):
        self.script = script
        self.player = player
        self.base_image = pygame.image.load(f"images/player{self.player}base.png")
        self.base_data ={
            'player1pos': [0, 0],
            'player2pos': [768, 618],
            'player1rect': pygame.Rect(0, 0, self.base_image.get_width(), self.base_image.get_height()),
            'player2rect': pygame.Rect(768, 618, self.base_image.get_width(), self.base_image.get_height()),
            'score1pos': [0, 250],
            'score2pos': [760, 250]


            }
        self.menu = pygame.Surface((300, 300))

        self.status = None #check if it is captured or not
        self.score = 0 #scoring for update
        #self.pos1 = [0, 0]
        #self.pos2 = [768, 618]
        #self.pos = Null# handle pos for the player
        
        """if player == 1:
            self.pos = self.pos1
        elif player == 2:
            self.pos = self."""
        
    def render(self):

        self.script.screen.blit(self.base_image, self.base_data[f'player{self.player}pos'])
        self.script.write(str(self.score), self.base_data[f'score{self.player}pos'])
        self.menufunction()




    def menufunction(self):
        self.mousebutton = pygame.mouse.get_pressed()
        self.mousepos = pygame.mouse.get_pos()

        if self.script.player_number == self.player:
            if self.mousebutton[0] and self.base_data[f'player{self.player}rect'].collidepoint(self.mousepos):
                self.script.opened = True

        if self.script.opened:
            self.menu.fill((255, 255, 255))
            self.Buttons()
            self.script.screen.blit(self.menu, (300, 200))

            

    def Buttons(self):

        close_button_rect = pygame.Rect(268, 0, 32, 32)
        pygame.draw.rect(self.menu, (225, 0, 0), close_button_rect)
        #handle closing window
        mouse_pos_menu = (self.mousepos[0] - 300, self.mousepos[1] -200)
        # Button to buy light soldier
        light_button = pygame.Rect(4, 40, 270, 40)
        pygame.draw.rect(self.menu, (225, 0, 0), light_button)
        self.write("BUY LIGHT UNIT", (4, 50))
        # light button logic

        # Button to handle buying heavy soldier
        heavy_button = pygame.Rect(4, 140, 270, 40)
        pygame.draw.rect(self.menu, (225, 0, 0), heavy_button)
        self.write("BUY HEAVY UNIT", (4, 150))

        # Button to handle tanky soldier
        tank_button = pygame.Rect(4, 240, 270, 40)
        pygame.draw.rect(self.menu, (225, 0, 0), tank_button)
        self.write("BUY TANKY UNIT", (4, 250))
        self.write("x", (268, 0))


        # cost of units
        light_cost = 10
        heavy_cost = 20
        tank_cost = 40

        possible_buy = True
        if self.mousebutton[0] and close_button_rect.collidepoint(mouse_pos_menu):
            self.script.opened = False
        #light

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                if self.script.player_number == self.player:  # Only allow correct player to buy units
                    if light_button.collidepoint(mouse_pos_menu):
                        if self.script.player_number == 1:
                            self.script.Unit1.create('light')
                        elif self.script.player_number == 2:
                            self.script.Unit2.create('light')
                    elif heavy_button.collidepoint(mouse_pos_menu):
                        if self.script.player_number == 1:
                            self.script.Unit1.create('heavy')
                        elif self.script.player_number == 2:
                            self.script.Unit2.create('heavy')
                    elif tank_button.collidepoint(mouse_pos_menu):
                        if self.script.player_number == 1:
                            self.script.Unit1.create('tank')
                        elif self.script.player_number == 2:
                            self.script.Unit2.create('tank')
            """if self.mousebutton[0] and light_button.collidepoint(mouse_pos_menu):
                #print("Light")
                self.script.Unit1.create('light')
                self.script.Unit2.create('light')
                if self.base_data[f'coins{self.player}'] - light_cost <0:
                    possible_buy = False
                else:
                    self.base_data[f'coins{self.player}'] = self.base_data[f'coins{self.player}'] - light_cost
                #print("Light create")
            elif self.mousebutton[0] and heavy_button.collidepoint(mouse_pos_menu):
                #print("Heavy")
                self.script.Unit1.create('heavy')
                self.script.Unit2.create('heavy')
                if self.base_data[f'coins{self.player}'] - heavy_cost <0:
                    possible_buy = False
                else:
                    self.base_data[f'coins{self.player}'] = self.base_data[f'coins{self.player}'] - heavy_cost
                #print("Heavy create")
            elif self.mousebutton[0] and tank_button.collidepoint(mouse_pos_menu):
                #print("Tank")
                self.script.Unit1.create('tank')
                self.script.Unit2.create('tank')
                if self.base_data[f'coins{self.player}'] - tank_cost <0:
                    possible_buy = False
                else:
                    self.base_data[f'coins{self.player}'] = self.base_data[f'coins{self.player}'] - tank_cost
                #print("Tank create")"""
    def write(self, txt, pos):
        font = pygame.font.Font(None, 42)
        font = font.render(txt, 0, (0, 0, 0))
        self.menu.blit(font, pos)


    #def interact_with_unit(self):



        
