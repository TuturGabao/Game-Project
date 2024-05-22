import pygame
WIDTH, HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 10, 20
FPS = 60
VELOCITY = 1
GRAVITY = 1
PLAYER_SPEED = 5
ENEMY_SPEED = 1
JUMPING_HEIGHT = 15
window = pygame.display.set_mode((WIDTH, HEIGHT))
class Player:
    def __init__(self, platforms, enemy):
        self.player_pos_x = 200
        self.player_pos_y = 350
        self.draw_player()
        self.platforms = platforms
        self.jumping = False
        self.velocity = 0
        self.falling = False
        self.enemy = enemy
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
            
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.velocity = JUMPING_HEIGHT

        else:
            self.player_pos_y -= self.velocity
            self.velocity -= GRAVITY
            if self.velocity < -JUMPING_HEIGHT:
                self.jumping = False
            
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

    def draw_player(self):
        self.player = pygame.draw.rect(window, (0, 0, 255), (self.player_pos_x, self.player_pos_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    def right(self):
        for platform in self.platforms:
            if (self.player.y > platform.y and self.player.y < platform.bottom) or (self.player.bottom < platform.bottom and self.player.bottom > platform.y):
                if self.player.right > platform.x - PLAYER_SPEED and self.player.right < platform.right - PLAYER_SPEED:
                    return
        
        self.enemy.enemy_pos_x -= PLAYER_SPEED
        for platform in self.platforms:
            platform.x -= PLAYER_SPEED
    
    def left(self):
        for platform in self.platforms:
            if (self.player.y > platform.y and self.player.y < platform.bottom) or (self.player.bottom < platform.bottom and self.player.bottom > platform.y):
                if self.player.x < platform.right + PLAYER_SPEED and self.player.x > platform.x + PLAYER_SPEED:
                    return
        
        self.enemy.enemy_pos_x += PLAYER_SPEED
        for platform in self.platforms:
            platform.x += PLAYER_SPEED

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

class Enemy:
    def __init__(self, x, y, platforms):
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
        self.enemy = pygame.draw.rect(window, (255, 0, 0), (self.enemy_pos_x, self.enemy_pos_y, PLAYER_WIDTH, PLAYER_HEIGHT))
        if self.enemy_pos_x <= 0:
            return
        if self.enemy.h == 0:
            self.enemy.h = 25
            self.enemy.y = 100

    def gravity(self):
        if self.falling:
            self.fall()
        platform_y = 9999

        for platform in self.platforms:
            if (self.enemy.right > platform.x and self.enemy.x < platform.right):
                if self.enemy.y < platform.y and platform.y < platform_y:
                    platform_y = platform.y

        for platform in self.platforms:
            if self.enemy.y > platform.y + platform.height and self.enemy.y < platform.y + platform.height + 20:
                if self.enemy_pos_x + self.enemy.width >= platform.x and self.enemy_pos_x <= platform.x + platform.width:
                    self.falling = False
                    self.fall()
            elif self.enemy_pos_y + PLAYER_HEIGHT > platform.y and self.enemy_pos_y < platform.y:
                if self.enemy_pos_x + PLAYER_WIDTH >= platform.x and self.enemy_pos_x <= platform.x + platform.width:
                    self.enemy_pos_y = platform_y - PLAYER_HEIGHT
                    self.falling = False
                    self.velocity = JUMPING_HEIGHT
                    break

            elif self.enemy.bottom < platform_y - 1:
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

clock = pygame.time.Clock()
platforms = []
platforms.append(pygame.Rect(0, 400, 10000, 200))
platforms.append(pygame.Rect(100, 320, 100, 20))
platforms.append(pygame.Rect(100, 290, 10, 30))
platforms.append(pygame.Rect(190, 290, 10, 30))
def main():
    run = True
    enemy = Enemy(150, 300, platforms)
    player = Player(platforms, enemy)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
        window.fill((20, 150, 200))
        player.draw_player()
        enemy.draw_enemy()
        player.player_movement()
        enemy.enemy_movement()
        for platform in platforms:
            pygame.draw.rect(window, (123, 123, 123), platform)
        pygame.display.update()
main()