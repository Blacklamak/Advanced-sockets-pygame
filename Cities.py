import pygame
class City:
    def __init__(self, script):
        self.script = script
        #2 dimensional array of cities [][]
        self.cities = [[pygame.image.load('images/city1.png'), 1],
                       [pygame.image.load('images/city2.png'), 2],
                       [pygame.image.load('images/city3.png'), 3]]
        self.cities_data = {
            'city1': pygame.Rect(self.script.screen.get_width()-32, 0, 32, 32),
            'city2': pygame.Rect(0 ,self.script.screen.get_height() - 32 ,32, 32),
            'city3': pygame.Rect(self.script.screen.get_width()/2, self.script.screen.get_height()/2, 32, 32),
        }
        self.cities_stats = {
            'city1': "idle",
            'city2': "idle",
            'city3': "idle"
        }   

    def render(self):
        for city_name, rect in self.cities_data.items():
            if self.cities_stats[city_name].startswith("captured_"):
                player = self.cities_stats[city_name].split("_")[1]
                color = (255, 0, 0) if player == "1" else (0, 0, 255)
                pygame.draw.rect(self.script.screen, color, (rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4),
                                 3)
        for images in self.cities:
            self.script.screen.blit(images[0], (self.cities_data[f'city{images[1]}'].x,self.cities_data[f'city{images[1]}'].y))
        for city, stats in self.cities_stats.items():
            if stats.startswith("captured"):
                print(city + " Captured")

    def check_income(self):
        self.current_time = pygame.time.get_ticks()
        self.script.main_timer = self.current_time - self.script.shared_timer

        if (self.current_time - self.script.shared_timer) >= 30000:
            print("5 seconds passed - Checking city income...")
            self.script.waves += 1
            for city_name, capture_status in self.cities_stats.items():
                if capture_status.startswith("captured"):
                    player = int(capture_status.split("_")[1])  # Extract player number
                    if player == 1:
                        self.script.Unit1.money += 50
                    else:
                        self.script.Unit2.money += 50

                    print(f"💰 {city_name} added 10 coins to Player {player}")

            self.script.shared_timer = self.current_time

