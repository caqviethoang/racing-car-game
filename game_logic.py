import random
import pygame
from pathlib import Path

class GameLogic:
    def __init__(self, display_width, display_height, root_path):
        self.display_width = display_width
        self.display_height = display_height
        self.root_path = root_path
        self.initialize_game_state()
    
    def initialize_game_state(self):
        self.crashed = False
        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 40

        # Player cars
        self.player_cars = [
            pygame.image.load(self.root_path + "/img/car_1.png"),
            pygame.image.load(self.root_path + "/img/car_2.png"),
            pygame.image.load(self.root_path + "/img/car_3.png")
        ]
        self.selected_car_index = 0
        self.carImg = self.player_cars[self.selected_car_index]

        # Enemy cars
        self.enemy_cars = [
            pygame.image.load(self.root_path + "/img/enemy_car_1.png"),
            pygame.image.load(self.root_path + "/img/enemy_car_2.png")
        ]
        self.current_enemy_car = random.choice(self.enemy_cars)
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -700
        self.enemy_car_speed = 5
        self.enemy_car_width = 40
        self.enemy_car_height = 50

        # Background images
        self.bg_images = [
            pygame.image.load(self.root_path + "/img/back_ground.jpg"),
            pygame.image.load(self.root_path + "/img/back_ground_1.jpg"),
            pygame.image.load(self.root_path + "/img/back_ground_2.jpg")
        ]
        for i in range(len(self.bg_images)):
            self.bg_images[i] = pygame.transform.scale(self.bg_images[i], (360, 600))
        
        self.current_bg_img_index = 0
        self.bgImg = self.bg_images[self.current_bg_img_index]
        
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0
        
        self.left_pressed = False
        self.right_pressed = False
    
    def select_car(self, car_index):
        if 0 <= car_index < len(self.player_cars):
            self.selected_car_index = car_index
            self.carImg = self.player_cars[car_index]
            return True
        return False
    
    def update_background(self):
        # Change background image every 1000 points
        if self.count > 0 and self.count % 1000 == 0:
            self.current_bg_img_index = (self.current_bg_img_index + 1) % len(self.bg_images)
            self.bgImg = self.bg_images[self.current_bg_img_index]
    
    def update_enemy_car(self):
        self.enemy_car_starty += self.enemy_car_speed

        if self.enemy_car_starty > self.display_height:
            self.enemy_car_starty = -100 - self.enemy_car_height
            self.enemy_car_startx = random.randrange(310, 450)
            self.current_enemy_car = random.choice(self.enemy_cars)
    
    def check_collision(self, car_x, car_y, car_width):
        if car_y < self.enemy_car_starty + self.enemy_car_height:
            if (car_x > self.enemy_car_startx and car_x < self.enemy_car_startx + self.enemy_car_width or 
                car_x + car_width > self.enemy_car_startx and car_x + car_width < self.enemy_car_startx + self.enemy_car_width):
                return True
        
        if car_x < 280 or car_x > 470:
            return True
        
        return False
    
    def increase_difficulty(self):
        if self.count % 100 == 0:
            self.enemy_car_speed += 0.5
            self.bg_speed += 0.5
    
    def update_background_position(self):
        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600