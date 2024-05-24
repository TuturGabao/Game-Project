import pygame
import math
import pygame_gui
import check_box 

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1200, 700

STARTING_Y = 449
STARTING_X = 150

PLAYER_HEIGHT = 25
PLAYER_WIDTH = 15

ENEMY_HEIGHT = 25
ENEMY_WIDTH = 15

ENEMY_STARTING_X = 400
ENEMY_STARTING_Y = 300

VELOCITY = 1
GRAVITY = 1

PLAYER_SPEED = 5
ENEMY_SPEED = 3

JUMPING_HEIGHT = 15

fps = 60
FPS_UI = 1000

BUTTON_HEIGHT, BUTTON_WIDTH = 40, 140

settings = False

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

play_button_rect = pygame.Rect(WIDTH/2-BUTTON_WIDTH/2, 150, BUTTON_WIDTH, BUTTON_HEIGHT)
play_button = pygame_gui.elements.UIButton(
    play_button_rect,
    "Play",
    manager
)
settings_button_rect = pygame.Rect(WIDTH/2-BUTTON_WIDTH/2, 200, BUTTON_WIDTH, BUTTON_HEIGHT)
settings_button = pygame_gui.elements.UIButton(
    settings_button_rect,
    "Settings",
    manager
)
leave_button_rect = pygame.Rect(WIDTH/2-BUTTON_WIDTH/2, 250, BUTTON_WIDTH, BUTTON_HEIGHT)
leave_button = pygame_gui.elements.UIButton(
    leave_button_rect,
    "Leave",
    manager
)

menu_button_rect = pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT)
menu_button = pygame_gui.elements.UIButton(
    menu_button_rect,
    "Menu",
    manager
)

FPS_slider_rect = pygame.Rect(WIDTH/2-(BUTTON_WIDTH+30)/2, 100, BUTTON_WIDTH+30, BUTTON_HEIGHT)
FPS_slider = pygame_gui.elements.UIHorizontalSlider(
    FPS_slider_rect,
    60,
    (30, 120),
    manager
)
FPS_label_menu_rect = pygame.Rect(FPS_slider.get_relative_rect().x, FPS_slider.get_relative_rect().y + 35, BUTTON_WIDTH+30, BUTTON_HEIGHT)
FPS_label_menu = pygame_gui.elements.UILabel(
    FPS_label_menu_rect,
    "FPS: 60",
    manager
)

menu_buttons = [
    play_button,
    settings_button,
    leave_button
]
playing_buttons = [
    menu_button
]
settings_buttons = [
    FPS_slider,
    FPS_label_menu
]

background = pygame.image.load("Python/Game/PlatformGame/background.png")
background_width = background.get_width()

tiles = math.ceil(WIDTH / background_width) + 1

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Game")

CheckBox = check_box.Checkbox(window, WIDTH/2-(BUTTON_WIDTH+30)/2, 200, 0, (123, 123, 123), "Show FPS", (255, 255, 255), (255, 0, 0), 22, (255, 255, 255))

font = pygame.font.SysFont("Calibri", 18)
FPS_game = font.render("FPS: 60.0", True, (255, 255, 255))

class Enemy:
    def __init__(self, x, y, platforms):
        self.enemy_pos_x = x
        self.enemy_pos_y = y
        self.platforms = platforms
        self.falling = True
        self.velocity = 0
        self.direction = ENEMY_SPEED

    def draw_enemy(self):
        self.enemy = pygame.draw.rect(window, (255, 0, 0), (self.enemy_pos_x, self.enemy_pos_y, ENEMY_WIDTH, ENEMY_HEIGHT))

    def gravity(self):
        if self.falling:
            self.enemy_pos_y += self.velocity
            self.velocity += GRAVITY
            self.check_platform_collision()
            self.check_platform_under_enemy()
      
    def get_nearest_platform(self):
        lowest_platform = self.platforms[0]
        for platform in self.platforms:
            if (self.enemy_pos_x + PLAYER_WIDTH > platform.x and self.enemy_pos_x < platform.right):
                if self.enemy_pos_y < platform.y and platform.y < lowest_platform.y:
                    lowest_platform = platform

        return lowest_platform

    def check_platform_under_enemy(self):
        lowest_platform = self.get_nearest_platform()

        if self.enemy_pos_x + ENEMY_WIDTH > lowest_platform.x and self.enemy_pos_x < lowest_platform.right:
            if self.enemy_pos_y + ENEMY_HEIGHT >= lowest_platform.y:
                self.falling = True

    def check_platform_collision(self):
        self.falling = True
        for platform in self.platforms:
            if self.enemy_pos_x + ENEMY_WIDTH > platform.x and self.enemy_pos_x < platform.x + platform.width:
                if self.enemy_pos_y + ENEMY_HEIGHT >= platform.y and self.enemy_pos_y + ENEMY_HEIGHT <= platform.y + self.velocity:
                    self.enemy_pos_y = platform.y - ENEMY_HEIGHT
                    self.falling = False
                    self.velocity = 0
                    break

    def enemy_movement(self):
        self.gravity()
        self.moving()

    def moving(self):
        edge_detected = False
        for platform in self.platforms:
            if self.direction > 0:  # Moving right
                if self.enemy_pos_x + ENEMY_WIDTH >= platform.x and self.enemy_pos_x + ENEMY_WIDTH <= platform.x + ENEMY_SPEED:
                    if self.enemy_pos_y + ENEMY_HEIGHT > platform.y and self.enemy_pos_y < platform.y + platform.height:
                        edge_detected = True
                        break
            else:  # Moving left
                if self.enemy_pos_x <= platform.x + platform.width and self.enemy_pos_x >= platform.x + platform.width - ENEMY_SPEED:
                    if self.enemy_pos_y + ENEMY_HEIGHT > platform.y and self.enemy_pos_y < platform.y + platform.height:
                        edge_detected = True
                        break

        if not edge_detected:
            self.enemy_pos_x += self.direction
        else:
            self.direction *= -1
            self.enemy_pos_x += self.direction
        

       

class Player:
    def __init__(self, x, y, platforms):
        self.player_pos_x = x
        self.player_pos_y = y
        self.draw_player()
        self.platforms = platforms
        self.jumping = False
        self.velocity = 0
        self.falling = False

    def draw_player(self):
        self.player = pygame.draw.rect(window, (0, 0, 255), (self.player_pos_x, self.player_pos_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    def gravity(self):
        if self.jumping:
            self.jump() 
        
        if self.falling:
            self.fall()

        for platform in self.platforms:
            if self.player.y > platform.y + platform.height and self.player.y < platform.y + platform.height + 20:
                if self.player_pos_x + self.player.width >= platform.x and self.player_pos_x <= platform.x + platform.width:
                    self.jumping = False
                    self.falling = False
                    self.fall()
            elif self.player_pos_y + self.player.height > platform.y and self.player_pos_y < platform.y:
                if self.player_pos_x + self.player.width >= platform.x and self.player_pos_x <= platform.x + platform.width:
                    self.player_pos_y = platform.y - self.player.height
                    self.jumping = False
                    self.falling = False
                    self.velocity = JUMPING_HEIGHT
                    break

            elif self.player.bottom <= platform.y - 1:
                if not self.jumping and not self.falling:
                    self.fall()
            
    def fall(self):
        if not self.falling:
            if self.velocity > 0:
                self.velocity = 0
            self.falling = True

        else:
            self.player_pos_y -= self.velocity
            self.velocity -= GRAVITY
            if self.velocity < -99999:
                self.falling = False
                self.velocity = JUMPING_HEIGHT

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.velocity = JUMPING_HEIGHT

        else:
            self.player_pos_y -= self.velocity
            self.velocity -= GRAVITY
            if self.velocity < -JUMPING_HEIGHT:
                self.jumping = False

    def right(self):
        for platform in self.platforms:
            if (self.player.y > platform.y and self.player.y < platform.bottom) or (self.player.bottom < platform.bottom and self.player.bottom > platform.y):
                if self.player.right > platform.x - PLAYER_SPEED and self.player.right < platform.right - PLAYER_SPEED:
                    return
        
        for platform in self.platforms:
            platform.x -= PLAYER_SPEED
    
    def left(self):
        for platform in self.platforms:
            if (self.player.y > platform.y and self.player.y < platform.bottom) or (self.player.bottom < platform.bottom and self.player.bottom > platform.y):
                if self.player.x < platform.right + PLAYER_SPEED and self.player.x > platform.x + PLAYER_SPEED:
                    return
                 
        for platform in self.platforms:
            platform.x += PLAYER_SPEED

    def player_movement(self):
        self.gravity()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and keys[pygame.K_q]:
            pass
        elif keys[pygame.K_d]:
            self.right()
        elif keys[pygame.K_q]:
            self.left()
        if keys[pygame.K_SPACE]:
            if not self.jumping and not self.falling:
                self.jump() 

                


class Game:
    def __init__(self):
        self.platforms = [] 
        self.platforms = self.draw_platform()

        #Everything[0] -> Platforms, Everything[1] -> Enemies, Everything[2] -> Other
        self.everything = []
        self.scroll = 0
        self.just_lost = False
        self.creating_player_enemies()

    #Used to reset all the elements of the screen (if lost)
    def creating_player_enemies(self):
        self.player = Player(STARTING_X, STARTING_Y, self.platforms)
        self.enemy = Enemy(ENEMY_STARTING_X, ENEMY_STARTING_Y, self.platforms)
        self.enemy2 = Enemy(ENEMY_STARTING_X, ENEMY_STARTING_Y + 80, self.platforms)
        self.enemy3 = Enemy(ENEMY_STARTING_X - 280, ENEMY_STARTING_Y - 50, self.platforms)
        self.enemies = []

        self.enemies.append(self.enemy)
        #self.enemies.append(self.enemy2)
        #self.enemies.append(self.enemy3)

    def reseting_everything(self):
        self.player = None
        self.enemies = []
        self.platforms = []


    def show_players(self):
        self.player.player_movement()                                                                                                                                           #type: ignore
        self.player.draw_player()                                                                                                                                               #type: ignore

        for enemy in self.enemies:
            enemy.draw_enemy()
            enemy.enemy_movement()

    def check_loss(self):
        for enemy in self.enemies:
            if self.player.player_pos_y + self.player.player.h < enemy.enemy_pos_y:                                                                                             #type: ignore
                continue
            if self.player.player_pos_y > enemy.enemy_pos_y + enemy.enemy.h:                                                                                                    #type: ignore
                continue

            if self.player.player_pos_x + self.player.player.w >= enemy.enemy_pos_x and self.player.player_pos_x + self.player.player.w <= enemy.enemy_pos_x + enemy.enemy.w:   #type: ignore
                self.lost()
            elif self.player.player_pos_x <= enemy.enemy_pos_x + enemy.enemy.w and self.player.player_pos_x >= enemy.enemy_pos_x:                                               #type: ignore
               self.lost()

    def lost(self):
        self.reseting_everything()
        self.creating_player_enemies()
        self.scroll = 0

        self.just_lost = True

    def draw_platform(self):
        base = pygame.Rect(0, 450, 10000, HEIGHT-450)

        centerRectLeft = pygame.Rect(470, 370, 20, 15)
        centerRect = pygame.Rect(330, 380, 160, 15)
        centerRectRight = pygame.Rect(330, 370, 20, 15)

        leftRect = pygame.Rect(80, 300, 140, 15)
        rightRect = pygame.Rect(580, 300, 140, 15)
        centerRect2 = pygame.Rect(330, 220, 160, 15)
        rightWall = pygame.Rect(750, 0, 10, 600)
        leftWall = pygame.Rect(40, 0, 10, 600)

        self.platforms.append(base)

        self.platforms.append(centerRectLeft)
        self.platforms.append(centerRect)
        self.platforms.append(centerRectRight)

        self.platforms.append(leftRect)
        #self.platforms.append(rightRect)
        self.platforms.append(centerRect2)
        #self.platforms.append(rightWall)
        self.platforms.append(leftWall)
        return self.platforms

    def draw_bg(self):  
        for i in range(-1, tiles):
            window.blit(background, (i*background_width + self.scroll, 0))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and keys[pygame.K_q]:
            pass
        elif keys[pygame.K_d]:
            self.right()
        elif keys[pygame.K_q]:
            self.left()

        if abs(self.scroll) > background_width:
            self.scroll = 0

    def right(self):
        for platform in self.platforms:
            if self.player.player.y >= platform.y and self.player.player.y <= platform.y + platform.height:                                                              #type: ignore
                if self.player.player.x + self.player.player.width < platform.x or self.player.player.x + self.player.player.width >= platform.x + platform.width:       #type: ignore
                    pass
                else:
                    return

        self.scroll -= PLAYER_SPEED

        for enemy in self.enemies:
            enemy.enemy_pos_x -= PLAYER_SPEED
    
    def left(self):
        for platform in self.platforms:
            if self.player.player.y >= platform.y and self.player.player.y <= platform.y + platform.height:                                                              #type: ignore
                if self.player.player.x > platform.x + platform.width or self.player.player.x + self.player.player.width <= platform.x:                                  #type: ignore
                    pass
                else:
                    return

        self.scroll += PLAYER_SPEED

        for enemy in self.enemies:
            enemy.enemy_pos_x += PLAYER_SPEED

    def handle_labels(self):
        global fps
        global playing
        if playing:
            color = (0, 0, 0)
        else:
            color = (255, 255, 255)
        FPS_game = font.render("FPS: " + float.__str__(actual_fps/2), True, color)
        if CheckBox.checked:
            window.blit(FPS_game, (WIDTH - BUTTON_WIDTH + 15, 20, BUTTON_WIDTH, BUTTON_HEIGHT))
        fps = round(FPS_slider.get_current_value())
        FPS_label_menu.set_text("FPS: " + int.__str__(fps))

    def handle_buttons(self, event, playing):
        global settings
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == play_button:
            for button in menu_buttons:
                button.hide()
            for button in playing_buttons:
                button.show()
            playing = True

        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == settings_button:
            for button in menu_buttons:
                button.hide()
            for button in settings_buttons:
                button.show()
            menu_button.show()
            settings = True

        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == leave_button:
            quit()

        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == menu_button:
            self.lost()
            for button in menu_buttons:
                button.show()
            for button in playing_buttons:
                button.hide()
            for button in settings_buttons:
                button.hide()
            playing = False
            settings = False

        return playing

game = Game()

clock = pygame.time.Clock()

def main():
    global settings
    global actual_fps
    global fps
    global playing
    run = True
    playing = False
    platforms = game.draw_platform()
    actual_fps = 60.0

    for button in settings_buttons:
        button.hide()
    for button in playing_buttons:
        button.hide()

    while run:
        clock.tick(fps)
        actual_fps = round(clock.get_fps(), 1)
        manager.update(clock.tick(FPS_UI) / 1000.0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if settings:
                CheckBox.update_checkbox(event)

            manager.process_events(event)

            playing = game.handle_buttons(event, playing)

            if game.just_lost == True:
                game.just_lost = False
                platforms = game.draw_platform()
            
        window.fill((0, 0, 0))

        if settings:
            CheckBox.render_checkbox()

        if playing:
            game.draw_bg()

            game.show_players()

            game.check_loss()

            if game.just_lost == True:
                game.just_lost = False
                platforms = game.draw_platform()

            for platform in platforms:
                pygame.draw.rect(window, (123, 123, 123), platform)

        print(fps)
        game.handle_labels()
        manager.draw_ui(window)
        pygame.display.update()

main()
