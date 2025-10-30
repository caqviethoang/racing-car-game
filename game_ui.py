import pygame
from time import sleep

class GameUI:
    def __init__(self, display_width, display_height, root_path):
        self.display_width = display_width
        self.display_height = display_height
        self.root_path = root_path
        
        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.gold = (255, 215, 0)
        self.light_blue = (100, 149, 237)
        self.dark_blue = (25, 25, 112)
        self.green = (100, 255, 100)
        self.red = (255, 100, 100)
        
        # Fonts
        self.title_font = pygame.font.SysFont("arial", 60, True)
        self.button_font = pygame.font.SysFont("arial", 28, True)
        self.input_font = pygame.font.SysFont("arial", 22)
        self.score_font = pygame.font.SysFont("arial", 20)
        
        # Load images
        self.menu_bg = pygame.image.load(self.root_path + "/img/menu_bg.jpg")
        self.menu_bg = pygame.transform.scale(self.menu_bg, (self.display_width, self.display_height))
        self.carImg = pygame.image.load(self.root_path + "/img/car_1.png")

    def draw_button(self, surface, x, y, width, height, text, active=False):
        button_rect = pygame.Rect(x, y, width, height)
        
        if active:
            pygame.draw.rect(surface, self.light_blue, button_rect)
            pygame.draw.rect(surface, self.gold, button_rect, 3)
        else:
            pygame.draw.rect(surface, self.dark_blue, button_rect)
            pygame.draw.rect(surface, self.light_blue, button_rect, 2)
        
        text_surf = self.button_font.render(text, True, self.white)
        text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
        surface.blit(text_surf, text_rect)
        
        return button_rect

    def draw_input_box(self, surface, x, y, width, height, text, active=False):
        if active:
            pygame.draw.rect(surface, (240, 240, 240), (x, y, width, height))
            pygame.draw.rect(surface, self.gold, (x, y, width, height), 3)
        else:
            pygame.draw.rect(surface, (220, 220, 220), (x, y, width, height))
            pygame.draw.rect(surface, self.light_blue, (x, y, width, height), 2)
        
        text_surf = self.input_font.render(text, True, self.black)
        surface.blit(text_surf, (x + 10, y + 8))
        
        return pygame.Rect(x, y, width, height)

    def draw_score(self, surface, count, current_user=None):
        score_bg = pygame.Rect(0, 0, 200, 50)
        pygame.draw.rect(surface, (0, 0, 0, 128), score_bg)
        
        font = pygame.font.SysFont("arial", 20, True)
        text = font.render("SCORE: " + str(count), True, self.gold)
        surface.blit(text, (10, 10))

        if current_user:
            user_text = font.render(f"PLAYER: {current_user}", True, self.light_blue)
            surface.blit(user_text, (10, 35))

    def draw_game_over(self, surface, current_score, current_user, user_manager):
        overlay = pygame.Surface((self.display_width, self.display_height))
        overlay.set_alpha(180)
        overlay.fill(self.black)
        surface.blit(overlay, (0, 0))
        
        # Game over message
        font = pygame.font.SysFont("arial", 72, True)
        text = font.render("GAME OVER !!!", True, self.gold)
        text_shadow = font.render("GAME OVER !!!", True, (255, 100, 100))
        surface.blit(text_shadow, (402 - text.get_width() // 2, 192 - text.get_height() // 2))
        surface.blit(text, (400 - text.get_width() // 2, 190 - text.get_height() // 2))
        
        # Score display
        score_font = pygame.font.SysFont("arial", 28)
        score_text = score_font.render(f"Score: {current_score}", True, self.white)
        surface.blit(score_text, (400 - score_text.get_width() // 2, 270))
        
        # High score display
        if current_user:
            high_score = user_manager.users[current_user].get('high_score', 0)
            high_score_text = score_font.render(f"High Score: {high_score}", True, self.white)
            surface.blit(high_score_text, (400 - high_score_text.get_width() // 2, 310))

    def draw_credit(self, surface):
        font = pygame.font.SysFont("arial", 14)
        credit_text = font.render("Car Racing Game - Developed with PyGame", True, self.white)
        surface.blit(credit_text, (self.display_width - credit_text.get_width() - 10, 
                                 self.display_height - 20))

    def draw_car_selection(self, surface, car_images, selected_index):
        overlay = pygame.Surface((self.display_width, self.display_height))
        overlay.set_alpha(180)
        overlay.fill(self.black)
        surface.blit(overlay, (0, 0))
        
        # Title
        title = self.title_font.render("SELECT YOUR CAR", True, self.gold)
        surface.blit(title, (self.display_width/2 - title.get_width()/2, 50))
        
        # Draw cars
        car_width, car_height = 80, 160
        spacing = 20
        total_width = len(car_images) * car_width + (len(car_images) - 1) * spacing
        start_x = (self.display_width - total_width) // 2
        
        car_rects = []
        for i, car_img in enumerate(car_images):
            x = start_x + i * (car_width + spacing)
            y = 200
            
            # Draw selection border
            if i == selected_index:
                pygame.draw.rect(surface, self.gold, (x-10, y-10, car_width+20, car_height+20), 4)
                pygame.draw.rect(surface, self.green, (x-8, y-8, car_width+16, car_height+16), 2)
            
            # Scale and draw car image
            scaled_car = pygame.transform.scale(car_img, (car_width, car_height))
            surface.blit(scaled_car, (x, y))
            
            car_rects.append(pygame.Rect(x, y, car_width, car_height))
            
            # Car number
            car_text = self.button_font.render(f"Car {i+1}", True, self.white)
            surface.blit(car_text, (x + car_width//2 - car_text.get_width()//2, y + car_height + 10))
        
        return car_rects

    def draw_volume_bar(self, surface, x, y, width, height, volume):
        """Vẽ thanh điều chỉnh volume có thể click"""
        # Background
        pygame.draw.rect(surface, self.dark_blue, (x, y, width, height))
        # Volume level
        volume_width = int(width * volume)
        pygame.draw.rect(surface, self.green, (x, y, volume_width, height))
        # Border
        pygame.draw.rect(surface, self.light_blue, (x, y, width, height), 2)
        
        # Volume indicator
        indicator_x = x + volume_width
        pygame.draw.line(surface, self.gold, (indicator_x, y-5), (indicator_x, y+height+5), 3)
        
        return pygame.Rect(x, y, width, height)