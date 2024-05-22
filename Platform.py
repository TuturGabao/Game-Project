import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1200, 700

STARTING_Y = 449
STARTING_X = 800

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

FPS = 60

background = pygame.image.load("Python/Game/PlatformGame/background.png")
background_width = background.get_width()

tiles = math.ceil(WIDTH / background_width) + 1

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platform Game")

class Enemy:
    def __init__(self, x, y, platforms, bg):
        self.enemy_pos_x = x
        self.enemy_pos_y = y
        self.draw_enemy()
        self.platforms = platforms
        self.falling = False
        self.velocity = 0

        self.Times = 0

        #Direction: Positive = Right ; Negative = Left
        self.direction = ENEMY_SPEED

    def draw_enemy(self):
        self.enemy = pygame.draw.rect(window, (255, 0, 0), (self.enemy_pos_x, self.enemy_pos_y, ENEMY_WIDTH, ENEMY_HEIGHT))

    def gravity(self):
        if self.falling:
            self.fall()

        lowest_platform_y = float('inf')
        for platform in self.platforms:
            if (self.enemy_pos_x + ENEMY_WIDTH > platform.x and self.enemy_pos_x < platform.right) or (self.enemy.x < platform.right and self.enemy.x > platform.x):
                if self.enemy_pos_y < platform.y and platform.y < lowest_platform_y:
                    lowest_platform_y = platform.y

        for platform in self.platforms:
            if self.enemy_pos_y > platform.y + platform.height and self.enemy_pos_y < platform.y + platform.height:
                if self.enemy_pos_x + ENEMY_WIDTH >= platform.x and self.enemy_pos_x <= platform.x + platform.width:
                    self.falling = False
                    self.fall()
            elif self.enemy_pos_y + ENEMY_HEIGHT > platform.y and self.enemy_pos_y < platform.y:
                if self.enemy_pos_x + ENEMY_WIDTH >= platform.x and self.enemy_pos_x <= platform.x + platform.width:
                    self.enemy_pos_y = lowest_platform_y - ENEMY_HEIGHT
                    self.falling = False
                    self.velocity = JUMPING_HEIGHT
                    break

            elif self.enemy_pos_y + ENEMY_HEIGHT < lowest_platform_y:
                if not self.falling:
                    self.fall()

    def fall(self):
        if not self.falling:
            if self.velocity > 0:
                self.velocity = 0
            self.falling = True

        else:
            self.enemy_pos_y -= self.velocity
            self.velocity -= GRAVITY
            if self.velocity < -99999:
                self.falling = False
                self.velocity = JUMPING_HEIGHT
    
    def enemy_movement(self):
        self.gravity()
        self.moving()
    
    def moving(self):
        for platform in self.platforms:
            if self.direction > 0:
                if (self.enemy.y > platform.y and self.enemy.y < platform.bottom) or (self.enemy.bottom < platform.bottom and self.enemy.bottom > platform.y):
                    if self.enemy.right > platform.x - ENEMY_SPEED and self.enemy.right < platform.right - ENEMY_SPEED:
                        self.direction *= -1
            else:
                if (self.enemy.y > platform.y and self.enemy.y < platform.bottom) or (self.enemy.bottom < platform.bottom and self.enemy.bottom > platform.y):
                    if self.enemy.x < platform.right + ENEMY_SPEED and self.enemy.x > platform.x + ENEMY_SPEED:
                        self.direction *= -1

        self.enemy_pos_x += self.direction
        

       

class Player:
    def __init__(self, x, y, platforms, bg):
        self.player_pos_x = x
        self.player_pos_y = y
        self.draw_player()
        self.platforms = platforms
        self.bg = bg
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

        for thing in self.bg:
            thing.x -= PLAYER_SPEED
    
    def left(self):
        for platform in self.platforms:
            if (self.player.y > platform.y and self.player.y < platform.bottom) or (self.player.bottom < platform.bottom and self.player.bottom > platform.y):
                if self.player.x < platform.right + PLAYER_SPEED and self.player.x > platform.x + PLAYER_SPEED:
                    return
                 
        for platform in self.platforms:
            platform.x += PLAYER_SPEED

        for thing in self.bg:
            thing.x += PLAYER_SPEED

    def player_movement(self):
        self.gravity()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.right()
        if keys[pygame.K_q]:
            self.left()
        if keys[pygame.K_SPACE]:
            if not self.jumping and not self.falling:
                self.jump() 

                


class Game:
    def __init__(self):
        self.platforms = []
        self.bg = []
        self.scroll = 0
        self.player = Player(STARTING_X, STARTING_Y, self.platforms, self.bg)
        self.enemy = Enemy(ENEMY_STARTING_X, ENEMY_STARTING_Y, self.platforms, self.bg)
        self.enemy2 = Enemy(ENEMY_STARTING_X, ENEMY_STARTING_Y + 80, self.platforms, self.bg)
        self.enemies = []

        self.enemies.append(self.enemy)
        self.enemies.append(self.enemy2)

    def show_players(self):
        self.player.player_movement()
        self.player.draw_player()

        for enemy in self.enemies:
            enemy.draw_enemy()
            enemy.enemy_movement()

    def check_loss(self):
        for enemy in self.enemies:
            if self.player.player_pos_y + self.player.player.h < enemy.enemy_pos_y:
                continue
            if self.player.player_pos_y > enemy.enemy_pos_y + enemy.enemy.h:
                continue

            if self.player.player_pos_x + self.player.player.w >= enemy.enemy_pos_x and self.player.player_pos_x + self.player.player.w <= enemy.enemy_pos_x + enemy.enemy.w:
                self.lost()
            elif self.player.player_pos_x <= enemy.enemy_pos_x + enemy.enemy.w and self.player.player_pos_x >= enemy.enemy_pos_x:
               self.lost()

    def lost(self):
        print("loose")

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
        self.platforms.append(rightWall)
        self.platforms.append(leftWall)
        return self.platforms

    def draw_bg(self):
        #for i in range(10):
            #self.bg.append(pygame.Rect(WIDTH*i, 0, 5, 600))
        
        for i in range(-1, tiles):
            window.blit(background, (i*background_width + self.scroll, 0))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.right()
        if keys[pygame.K_q]:
            self.left()

        if abs(self.scroll) > background_width:
            self.scroll = 0

        return self.bg

    def right(self):
        for platform in self.platforms:
            if self.player.player.y >= platform.y and self.player.player.y <= platform.y + platform.height:
                if self.player.player.x + self.player.player.width < platform.x or self.player.player.x + self.player.player.width >= platform.x + platform.width:
                    pass
                else:
                    return

        self.scroll -= PLAYER_SPEED

        for enemy in self.enemies:
            enemy.enemy_pos_x -= PLAYER_SPEED
    
    def left(self):
        for platform in self.platforms:
            if self.player.player.y >= platform.y and self.player.player.y <= platform.y + platform.height:
                if self.player.player.x > platform.x + platform.width or self.player.player.x + self.player.player.width <= platform.x:
                    pass
                else:
                    return

        self.scroll += PLAYER_SPEED

        for enemy in self.enemies:
            enemy.enemy_pos_x += PLAYER_SPEED


game = Game()

clock = pygame.time.Clock()

def main():
    run = True
    platforms = game.draw_platform()
    bg = game.draw_bg()
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        window.fill((0, 0, 0))
        game.draw_bg()

        game.show_players()

        game.check_loss()

        for platform in platforms:
            pygame.draw.rect(window, (123, 123, 123), platform)

        for thing in bg:
            pygame.draw.rect(window, (255, 255, 255), thing)

        pygame.display.update()

main()