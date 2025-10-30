import pygame
from pathlib import Path
from user_manager import UserManager
from game_logic import GameLogic
from game_ui import GameUI
from time import sleep

class CarRacing:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.display_width = 800
        self.display_height = 600
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.root_path = str(Path(__file__).parent)
        
        self.user_manager = UserManager()
        self.game_logic = GameLogic(self.display_width, self.display_height, self.root_path)
        self.game_ui = GameUI(self.display_width, self.display_height, self.root_path)
        
        self.current_user = None
        self.current_score = 0
        self.game_paused = False
        
        # Khởi tạo âm nhạc
        self.initialize_music()

    def initialize_music(self):
        """Khởi tạo và load nhạc nền"""
        try:
            # Load nhạc nền menu
            self.menu_music = self.root_path + "/audio/menu_music.mp3"
            # Load nhạc nền game
            self.game_music = self.root_path + "/audio/game_music.mp3"
            
            # Thiết lập volume mặc định
            pygame.mixer.music.set_volume(0.5)
        except:
            print("Không thể load file nhạc")

    def play_menu_music(self):
        """Phát nhạc nền menu"""
        try:
            pygame.mixer.music.load(self.menu_music)
            pygame.mixer.music.play(-1)
        except:
            print("Không thể phát nhạc menu")

    def play_game_music(self):
        """Phát nhạc nền game"""
        try:
            pygame.mixer.music.load(self.game_music)
            pygame.mixer.music.play(-1)
        except:
            print("Không thể phát nhạc game")

    def stop_music(self):
        """Dừng nhạc"""
        pygame.mixer.music.stop()

    def toggle_music(self):
        """Tắt/bật nhạc"""
        if pygame.mixer.music.get_volume() > 0:
            pygame.mixer.music.set_volume(0.0)
        else:
            pygame.mixer.music.set_volume(0.5)

    def set_music_volume(self, volume):
        """Điều chỉnh volume (0.0 đến 1.0)"""
        pygame.mixer.music.set_volume(volume)

    def volume_settings_screen(self):
        """Màn hình cài đặt âm lượng"""
        current_volume = pygame.mixer.music.get_volume()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Xử lý click trên thanh volume
                    volume_bar_rect = pygame.Rect(250, 250, 300, 30)
                    if volume_bar_rect.collidepoint(event.pos):
                        # Tính volume dựa trên vị trí click
                        rel_x = event.pos[0] - volume_bar_rect.x
                        new_volume = max(0.0, min(1.0, rel_x / volume_bar_rect.width))
                        pygame.mixer.music.set_volume(new_volume)
                        current_volume = new_volume
                    
                    # Nút back
                    if pygame.Rect(300, 350, 200, 50).collidepoint(event.pos):
                        return
                    
                    # Nút tắt/bật nhạc
                    if pygame.Rect(300, 420, 200, 50).collidepoint(event.pos):
                        self.toggle_music()
                        current_volume = pygame.mixer.music.get_volume()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            self.gameDisplay.blit(self.game_ui.menu_bg, (0, 0))
            overlay = pygame.Surface((self.display_width, self.display_height))
            overlay.set_alpha(180)
            overlay.fill(self.game_ui.black)
            self.gameDisplay.blit(overlay, (0, 0))
            
            title = self.game_ui.title_font.render("MUSIC", True, self.game_ui.gold)
            self.gameDisplay.blit(title, (self.display_width/2 - title.get_width()/2, 80))
            
            # Vẽ thanh volume
            volume_rect = self.game_ui.draw_volume_bar(self.gameDisplay, 250, 250, 300, 30, current_volume)
            
            # Hiển thị volume hiện tại
            volume_text = self.game_ui.button_font.render(f"Volume: {int(current_volume * 100)}%", True, self.game_ui.white)
            self.gameDisplay.blit(volume_text, (self.display_width/2 - volume_text.get_width()/2, 300))
            
            mouse_pos = pygame.mouse.get_pos()
            
            # Nút tắt/bật nhạc
            back_rect = self.game_ui.draw_button(self.gameDisplay, 300, 350, 200, 50, "BACK",
                           pygame.Rect(300, 350, 200, 50).collidepoint(mouse_pos))
            
            # Nút back
            music_text = "MUTE MUSIC" if current_volume > 0 else "UNMUTE MUSIC"
            mute_rect = self.game_ui.draw_button(self.gameDisplay, 300, 420, 200, 50, music_text,
                           pygame.Rect(300, 420, 200, 50).collidepoint(mouse_pos))
            
            pygame.display.update()
            self.clock.tick(60)

    def pause_menu(self):
        """Menu pause trong game"""
        self.game_paused = True
        
        while self.game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        self.game_paused = False
                        return True
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Nút resume
                    if pygame.Rect(300, 250, 200, 50).collidepoint(event.pos):
                        self.game_paused = False
                        return True
                    
                    # Nút volume settings
                    if pygame.Rect(300, 320, 200, 50).collidepoint(event.pos):
                        self.volume_settings_screen()
                    
                    # Nút main menu
                    if pygame.Rect(300, 390, 200, 50).collidepoint(event.pos):
                        self.game_paused = False
                        self.current_user = None
                        self.game_logic.initialize_game_state()
                        self.play_menu_music()
                        return False

            # Vẽ overlay pause
            overlay = pygame.Surface((self.display_width, self.display_height))
            overlay.set_alpha(128)
            overlay.fill(self.game_ui.black)
            self.gameDisplay.blit(overlay, (0, 0))
            
            # Tiêu đề pause
            title = self.game_ui.title_font.render("GAME PAUSED", True, self.game_ui.gold)
            self.gameDisplay.blit(title, (self.display_width/2 - title.get_width()/2, 150))
            
            mouse_pos = pygame.mouse.get_pos()
            
            # Các nút trong menu pause
            resume_rect = self.game_ui.draw_button(self.gameDisplay, 300, 250, 200, 50, "RESUME",
                                         pygame.Rect(300, 250, 200, 50).collidepoint(mouse_pos))
            
            volume_rect = self.game_ui.draw_button(self.gameDisplay, 300, 320, 200, 50, "MUSIC",
                                         pygame.Rect(300, 320, 200, 50).collidepoint(mouse_pos))
            
            menu_rect = self.game_ui.draw_button(self.gameDisplay, 300, 390, 200, 50, "MAIN MENU",
                                       pygame.Rect(300, 390, 200, 50).collidepoint(mouse_pos))
            
            # Hướng dẫn
            hint_text = self.game_ui.score_font.render("Press ESC or P to resume", True, self.game_ui.white)
            self.gameDisplay.blit(hint_text, (self.display_width/2 - hint_text.get_width()/2, 470))
            
            pygame.display.update()
            self.clock.tick(60)
        
        return True

    def main_menu(self):
        self.play_menu_music()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    login_rect = pygame.Rect(300, 200, 200, 50)
                    register_rect = pygame.Rect(300, 270, 200, 50)
                    high_score_rect = pygame.Rect(300, 340, 200, 50)
                    volume_rect = pygame.Rect(300, 410, 200, 50)
                    quit_rect = pygame.Rect(300, 480, 200, 50)
                    
                    if login_rect.collidepoint(event.pos):
                        if self.login_screen():
                            return True
                    elif register_rect.collidepoint(event.pos):
                        self.register_screen()
                    elif high_score_rect.collidepoint(event.pos):
                        self.high_score_screen()
                    elif volume_rect.collidepoint(event.pos):
                        self.volume_settings_screen()
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        return False
            
            self.gameDisplay.blit(self.game_ui.menu_bg, (0, 0))
            overlay = pygame.Surface((self.display_width, self.display_height))
            overlay.set_alpha(128)
            overlay.fill(self.game_ui.black)
            self.gameDisplay.blit(overlay, (0, 0))
            
            # Draw title with shadow effect
            title = self.game_ui.title_font.render("CAR RACING GAME", True, self.game_ui.gold)
            title_shadow = self.game_ui.title_font.render("CAR RACING GAME", True, self.game_ui.light_blue)
            self.gameDisplay.blit(title_shadow, (self.display_width/2 - title.get_width()/2 + 3, 83))
            self.gameDisplay.blit(title, (self.display_width/2 - title.get_width()/2, 80))
            
            # Draw buttons with hover effect
            mouse_pos = pygame.mouse.get_pos()
            login_rect = self.game_ui.draw_button(self.gameDisplay, 300, 200, 200, 50, "LOGIN", 
                                         pygame.Rect(300, 200, 200, 50).collidepoint(mouse_pos))
            register_rect = self.game_ui.draw_button(self.gameDisplay, 300, 270, 200, 50, "REGISTER", 
                                           pygame.Rect(300, 270, 200, 50).collidepoint(mouse_pos))
            high_score_rect = self.game_ui.draw_button(self.gameDisplay, 300, 340, 200, 50, "HIGH SCORES", 
                                             pygame.Rect(300, 340, 200, 50).collidepoint(mouse_pos))
            volume_rect = self.game_ui.draw_button(self.gameDisplay, 300, 410, 200, 50, "MUSIC", 
                                         pygame.Rect(300, 410, 200, 50).collidepoint(mouse_pos))
            quit_rect = self.game_ui.draw_button(self.gameDisplay, 300, 480, 200, 50, "QUIT", 
                                       pygame.Rect(300, 480, 200, 50).collidepoint(mouse_pos))

            # Hiển thị volume hiện tại
            volume_percent = int(pygame.mixer.music.get_volume() * 100)
            volume_display = self.game_ui.score_font.render(f"Current Volume: {volume_percent}%", True, self.game_ui.white)
            self.gameDisplay.blit(volume_display, (10, self.display_height - 30))

            if self.current_user:
                user_bg = pygame.Rect(5, 5, 250, 35)
                pygame.draw.rect(self.gameDisplay, self.game_ui.dark_blue, user_bg)
                pygame.draw.rect(self.gameDisplay, self.game_ui.light_blue, user_bg, 2)
                user_text = self.game_ui.score_font.render(f"Player: {self.current_user}", True, self.game_ui.gold)
                self.gameDisplay.blit(user_text, (15, 12))
            
            pygame.display.update()
            self.clock.tick(60)

    def login_screen(self):
        # ... (giữ nguyên code login_screen từ trước)
        username = ""
        password = ""
        username_active = False
        password_active = False
        message = ""
        message_color = (255, 100, 100)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    username_rect = pygame.Rect(250, 200, 300, 40)
                    password_rect = pygame.Rect(250, 280, 300, 40)
                    
                    if username_rect.collidepoint(event.pos):
                        username_active = True
                        password_active = False
                    elif password_rect.collidepoint(event.pos):
                        username_active = False
                        password_active = True
                    elif pygame.Rect(250, 350, 300, 50).collidepoint(event.pos):
                        success, msg, high_score = self.user_manager.login(username, password)
                        if success:
                            self.current_user = username
                            self.current_score = 0
                            message = f"Welcome back, {username}! High score: {high_score}"
                            message_color = (100, 255, 100)
                            pygame.display.update()
                            sleep(1)
                            return True
                        else:
                            message = msg
                            message_color = (255, 100, 100)
                    elif pygame.Rect(250, 420, 300, 50).collidepoint(event.pos):
                        return False
                    else:
                        username_active = False
                        password_active = False
                
                if event.type == pygame.KEYDOWN:
                    if username_active:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += event.unicode
                    elif password_active:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        else:
                            password += event.unicode
            
            self.gameDisplay.blit(self.game_ui.menu_bg, (0, 0))
            overlay = pygame.Surface((self.display_width, self.display_height))
            overlay.set_alpha(180)
            overlay.fill(self.game_ui.black)
            self.gameDisplay.blit(overlay, (0, 0))
            
            title = self.game_ui.title_font.render("LOGIN", True, self.game_ui.gold)
            self.gameDisplay.blit(title, (self.display_width/2 - title.get_width()/2, 80))
            
            username_rect = self.game_ui.draw_input_box(self.gameDisplay, 250, 200, 300, 40, username, username_active)
            password_rect = self.game_ui.draw_input_box(self.gameDisplay, 250, 280, 300, 40, "*" * len(password), password_active)
            
            username_label = self.game_ui.input_font.render("Username:", True, self.game_ui.white)
            password_label = self.game_ui.input_font.render("Password:", True, self.game_ui.white)
            self.gameDisplay.blit(username_label, (250, 175))
            self.gameDisplay.blit(password_label, (250, 255))
            
            mouse_pos = pygame.mouse.get_pos()
            login_rect = self.game_ui.draw_button(self.gameDisplay, 250, 350, 300, 50, "LOGIN", 
                                         pygame.Rect(250, 350, 300, 50).collidepoint(mouse_pos))
            back_rect = self.game_ui.draw_button(self.gameDisplay, 250, 420, 300, 50, "BACK TO MENU", 
                                       pygame.Rect(250, 420, 300, 50).collidepoint(mouse_pos))
            
            if message:
                msg_surf = self.game_ui.input_font.render(message, True, message_color)
                self.gameDisplay.blit(msg_surf, (self.display_width/2 - msg_surf.get_width()/2, 490))
            
            pygame.display.update()
            self.clock.tick(60)

    def register_screen(self):
        # ... (giữ nguyên code register_screen từ trước)
        username = ""
        password = ""
        username_active = False
        password_active = False
        message = ""
        message_color = (255, 100, 100)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    username_rect = pygame.Rect(250, 200, 300, 40)
                    password_rect = pygame.Rect(250, 280, 300, 40)
                    
                    if username_rect.collidepoint(event.pos):
                        username_active = True
                        password_active = False
                    elif password_rect.collidepoint(event.pos):
                        username_active = False
                        password_active = True
                    elif pygame.Rect(250, 350, 300, 50).collidepoint(event.pos):
                        success, msg = self.user_manager.register(username, password)
                        if success:
                            message = msg
                            message_color = (100, 255, 100)
                            pygame.display.update()
                            sleep(1)
                            return
                        else:
                            message = msg
                            message_color = (255, 100, 100)
                    elif pygame.Rect(250, 420, 300, 50).collidepoint(event.pos):
                        return
                    else:
                        username_active = False
                        password_active = False
                
                if event.type == pygame.KEYDOWN:
                    if username_active:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        else:
                            username += event.unicode
                    elif password_active:
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        else:
                            password += event.unicode
            
            self.gameDisplay.blit(self.game_ui.menu_bg, (0, 0))
            overlay = pygame.Surface((self.display_width, self.display_height))
            overlay.set_alpha(180)
            overlay.fill(self.game_ui.black)
            self.gameDisplay.blit(overlay, (0, 0))
            
            title = self.game_ui.title_font.render("REGISTER", True, self.game_ui.gold)
            self.gameDisplay.blit(title, (self.display_width/2 - title.get_width()/2, 80))
            
            username_rect = self.game_ui.draw_input_box(self.gameDisplay, 250, 200, 300, 40, username, username_active)
            password_rect = self.game_ui.draw_input_box(self.gameDisplay, 250, 280, 300, 40, "*" * len(password), password_active)
            
            username_label = self.game_ui.input_font.render("Username:", True, self.game_ui.white)
            password_label = self.game_ui.input_font.render("Password:", True, self.game_ui.white)
            self.gameDisplay.blit(username_label, (250, 175))
            self.gameDisplay.blit(password_label, (250, 255))
            
            mouse_pos = pygame.mouse.get_pos()
            register_rect = self.game_ui.draw_button(self.gameDisplay, 250, 350, 300, 50, "REGISTER", 
                                           pygame.Rect(250, 350, 300, 50).collidepoint(mouse_pos))
            back_rect = self.game_ui.draw_button(self.gameDisplay, 250, 420, 300, 50, "BACK TO MENU", 
                                       pygame.Rect(250, 420, 300, 50).collidepoint(mouse_pos))
            
            if message:
                msg_surf = self.game_ui.input_font.render(message, True, message_color)
                self.gameDisplay.blit(msg_surf, (self.display_width/2 - msg_surf.get_width()/2, 490))
            
            pygame.display.update()
            self.clock.tick(60)

    def high_score_screen(self):
        # ... (giữ nguyên code high_score_screen từ trước)
        high_scores = self.user_manager.get_high_scores()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(300, 500, 200, 50).collidepoint(event.pos):
                        return
            
            self.gameDisplay.blit(self.game_ui.menu_bg, (0, 0))
            overlay = pygame.Surface((self.display_width, self.display_height))
            overlay.set_alpha(180)
            overlay.fill(self.game_ui.black)
            self.gameDisplay.blit(overlay, (0, 0))
            
            title = self.game_ui.title_font.render("HIGH SCORES", True, self.game_ui.gold)
            self.gameDisplay.blit(title, (self.display_width/2 - title.get_width()/2, 50))
            
            # Display high scores
            y_offset = 150
            for i, (username, score) in enumerate(high_scores[:10]):
                score_text = self.game_ui.button_font.render(f"{i+1}. {username}: {score}", True, self.game_ui.white)
                self.gameDisplay.blit(score_text, (self.display_width/2 - score_text.get_width()/2, y_offset))
                y_offset += 40
            
            mouse_pos = pygame.mouse.get_pos()
            back_rect = self.game_ui.draw_button(self.gameDisplay, 300, 500, 200, 50, "BACK", 
                                       pygame.Rect(300, 500, 200, 50).collidepoint(mouse_pos))
            
            pygame.display.update()
            self.clock.tick(60)

    def car_selection_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    car_rects = self.game_ui.draw_car_selection(self.gameDisplay, self.game_logic.player_cars, self.game_logic.selected_car_index)
                    
                    for i, rect in enumerate(car_rects):
                        if rect.collidepoint(event.pos):
                            self.game_logic.select_car(i)
                    
                    if pygame.Rect(300, 450, 200, 50).collidepoint(event.pos):
                        return True
            
            self.gameDisplay.blit(self.game_ui.menu_bg, (0, 0))
            car_rects = self.game_ui.draw_car_selection(self.gameDisplay, self.game_logic.player_cars, self.game_logic.selected_car_index)
            
            mouse_pos = pygame.mouse.get_pos()
            start_rect = self.game_ui.draw_button(self.gameDisplay, 300, 450, 200, 50, "START GAME", 
                                         pygame.Rect(300, 450, 200, 50).collidepoint(mouse_pos))
            
            pygame.display.update()
            self.clock.tick(60)

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.game_logic.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Race')
        
        if not self.main_menu():
            return
        
        if not self.car_selection_screen():
            return
            
        self.run_car()

    def run_car(self):
        self.play_game_music()
        car_speed = 5

        while not self.game_logic.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_logic.crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.game_logic.left_pressed = True
                    if event.key == pygame.K_RIGHT:
                        self.game_logic.right_pressed = True
                    # Phím P hoặc ESC để pause
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        if not self.pause_menu():
                            return  # Quay về menu chính
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.game_logic.left_pressed = False
                    if event.key == pygame.K_RIGHT:
                        self.game_logic.right_pressed = False

            if self.game_logic.left_pressed:
                self.game_logic.car_x_coordinate -= car_speed
            if self.game_logic.right_pressed:
                self.game_logic.car_x_coordinate += car_speed

            self.game_logic.update_background()
            
            self.gameDisplay.fill(self.game_ui.black)
            self.back_ground_road()

            self.run_enemy_car(self.game_logic.enemy_car_startx, self.game_logic.enemy_car_starty)
            self.game_logic.update_enemy_car()

            self.car(self.game_logic.car_x_coordinate, self.game_logic.car_y_coordinate)
            self.game_ui.draw_score(self.gameDisplay, self.game_logic.count, self.current_user)
            
            # Hiển thị hướng dẫn pause
            pause_text = self.game_ui.score_font.render("Press P or ESC to pause", True, self.game_ui.white)
            self.gameDisplay.blit(pause_text, (self.display_width - pause_text.get_width() - 10, 10))
            
            # Hiển thị volume hiện tại
            volume_text = self.game_ui.score_font.render(f"Volume: {int(pygame.mixer.music.get_volume() * 100)}%", True, self.game_ui.white)
            self.gameDisplay.blit(volume_text, (self.display_width - volume_text.get_width() - 10, 35))
            
            self.game_logic.count += 1
            self.game_logic.increase_difficulty()

            if self.game_logic.check_collision(self.game_logic.car_x_coordinate, self.game_logic.car_y_coordinate, self.game_logic.car_width):
                self.game_logic.crashed = True
                self.current_score = self.game_logic.count
                if self.current_user:
                    self.user_manager.update_high_score(self.current_user, self.current_score)
                self.display_message("GAME OVER !!!")

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        self.stop_music()
        self.game_ui.draw_game_over(self.gameDisplay, self.current_score, self.current_user, self.user_manager)
        
        mouse_pos = pygame.mouse.get_pos()
        replay_rect = self.game_ui.draw_button(self.gameDisplay, 250, 350, 140, 50, "PLAY AGAIN", 
                                      pygame.Rect(250, 350, 140, 50).collidepoint(mouse_pos))
        menu_rect = self.game_ui.draw_button(self.gameDisplay, 410, 350, 140, 50, "MAIN MENU", 
                                    pygame.Rect(410, 350, 140, 50).collidepoint(mouse_pos))
        
        self.game_ui.draw_credit(self.gameDisplay)
        pygame.display.update()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_rect.collidepoint(event.pos):
                        waiting = False
                        self.current_score = 0
                        self.game_logic.initialize_game_state()
                        self.run_car()
                        return
                    elif menu_rect.collidepoint(event.pos):
                        waiting = False
                        self.current_user = None
                        self.game_logic.initialize_game_state()
                        self.play_menu_music()
                        self.racing_window()
                        return
            
            mouse_pos = pygame.mouse.get_pos()
            replay_rect = self.game_ui.draw_button(self.gameDisplay, 250, 350, 140, 50, "PLAY AGAIN", 
                                          pygame.Rect(250, 350, 140, 50).collidepoint(mouse_pos))
            menu_rect = self.game_ui.draw_button(self.gameDisplay, 410, 350, 140, 50, "MAIN MENU", 
                                        pygame.Rect(410, 350, 140, 50).collidepoint(mouse_pos))
            
            pygame.display.update()
            self.clock.tick(60)

    def back_ground_road(self):
        self.gameDisplay.blit(self.game_logic.bgImg, (self.game_logic.bg_x1, self.game_logic.bg_y1))
        self.gameDisplay.blit(self.game_logic.bgImg, (self.game_logic.bg_x2, self.game_logic.bg_y2))
        self.game_logic.update_background_position()

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.game_logic.current_enemy_car, (thingx, thingy))

if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()