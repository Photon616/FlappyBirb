import random
import time
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

scrnW = 640 # the width of the game window(pixels)
scrnH = 480 # the height of the game window(pixels)

screen = pygame.display.set_mode((scrnW, scrnH))
pygame.display.set_caption("operation")

clock = pygame.time.Clock()

# load images here
# if errors are occuring, try removing hundred_relief_plan from the directory.
player_img = pygame.image.load("hundred_relief_plan/Assets/Textures/uvChecker1k.png") 
player_img = pygame.transform.scale(player_img, (64, 48))
enemy_img = pygame.image.load("hundred_relief_plan/Assets/Textures/monotoneChecker1k.png") 
enemy_img = pygame.transform.scale(enemy_img, (64, 48))
bullet_img = pygame.image.load("hundred_relief_plan/Assets/Textures/kabosu_highres.jpg") 
bullet_img = pygame.transform.scale(bullet_img, (50, 10))
cue_img = pygame.image.load("hundred_relief_plan/Assets/Textures/player_box.png") 
cue_img = pygame.transform.scale(cue_img, (32, scrnH))
explosion_img = pygame.image.load("hundred_relief_plan/Assets/Textures/uvChecker1k.png") 
explosion_img = pygame.transform.scale(explosion_img, (96, 96))

start_screen_background = pygame.image.load("hundred_relief_plan/Assets/Textures/placeholder_640x480.png")
gameover_screen_background = pygame.image.load("hundred_relief_plan/Assets/Textures/placeholder_800x600.png")

# classes
class Player:
    def __init__(self, rimg, x, y, y_vel_limit, rect_x, rect_y, rect_size_x, rect_size_y):
        self.rimg = rimg
        self.x = x
        self.y = y
        self.y_vel = 0
        self.y_vel_limit = y_vel_limit
        self.rect = pygame.Rect(rect_x, rect_y, rect_size_x, rect_size_y)
    
    def update(self, fall_speed):
        self.y_vel += fall_speed 

        if self.y_vel > self.y_vel_limit:
            self.y_vel = self.y_vel_limit

        self.y += self.y_vel # adds on y coordinate to go down

        # checks if the player is colliding with the top and bottom of the screen
        if (self.y + self.rect.height) > scrnH:
            self.y = scrnH - self.rect.height
            self.y_vel = 0
        elif self.y < 0:
            self.y = 0
            self.y_vel = 0

        self.rect.y = self.y
    
    def jump(self, jump_speed):
        self.y_vel = -jump_speed
    
    def draw(self):
        screen.blit(self.rimg, (self.x, self.y))
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image, x, speed, y_range_min, y_range_max, kill_coord, cue_img):
        super().__init__()
        self.image = image
        self.y = random.randrange(y_range_min, y_range_max, 1)
        self.rect = self.image.get_rect(topleft=(x, self.y))
        self.init_x = x
        self.speed = speed
        self.y_range_min = y_range_min
        self.y_range_max = y_range_max
        self.kill_coord = kill_coord
        self.cue_img = cue_img
        self.is_over = False

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < self.kill_coord:
            self.is_over = True
            #self.kill()

        screen.blit(self.cue_img, (self.rect.right - 32, 0))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, kill_coord):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.speed = speed
        self.kill_coord = kill_coord
    
    def update(self):
        self.rect.x += self.speed
        # print("updated")
        if self.rect.left < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = pos)
        self.timer = 15  # frames until disappears
    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

def start_screen():
    running = True
    
    while running:
        clock.tick(60)
        #screen.fill((0, 0, 0)) # draw background
        screen.blit(start_screen_background, (0, 0))
        
        pygame.display.update() # update the screen

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "game"
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

def in_game():
    running = True
    pl = Player(player_img, 128, 0, 50, 128, 0, 64, 48)
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    effects = pygame.sprite.Group()
    fall_speed = 0.3
    jump_speed = 8.0 
    enemy_duration = 4 # in sec. division will be done after
    enemy_time = (enemy_duration - 1) * 60
    enemy_speed = 4
    weapon_duration = .5 # in sec
    weapon_time = weapon_duration * 60
    bullet_speed = 10

    score = 0

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0)) # draw background

        if enemy_time / 60 >= enemy_duration: # adds when time matches with duration.
            # print("enemy added")
            enemies.add(Obstacle(enemy_img, 680, enemy_speed, 110, 340, pl.rect.right, cue_img))
            # print("really added")
            enemy_time = 0 # initialize time to prevent overflow/save memory

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_f] and weapon_time / 60 >= weapon_time:
        #     print("pew-")
        #     bullets.add(Bullet(bullet_img, pl.x, pl.y, bullet_speed, scrnW))
        #     weapon_time = 0

        pl.update(fall_speed) # update the position of the player
        bullets.update()
        effects.update()
        enemies.update()
        for target_enemy in enemies:
            if target_enemy.is_over:
                return "gameover"

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)

        for bullet, hit_list in hits.items():
            for hit_enemy in hit_list:
                score += 10  # add score
                effects.add(Explosion(explosion_img, hit_enemy.rect.center))

        bullets.draw(screen)
        enemies.draw(screen) 
        pl.draw() # blit rimg on the screen
        effects.draw(screen)

        pygame.display.update() # update the screen
        enemy_time += 1
        weapon_time += 1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pl.jump(jump_speed)
                if event.key == pygame.K_f and weapon_time / 60 >= weapon_duration:
                    # print("bullet shot")
                    bullets.add(Bullet(bullet_img, pl.x, pl.y, bullet_speed, scrnW))
                    weapon_time = 0
                if event.key == pygame.K_ESCAPE:
                    return "start"
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
    
    #return "start"


def game_over_screen():
    running = True
    #print("test")

    while running:
        clock.tick(60)
        #screen.fill((0, 0, 0)) # draw background
        screen.blit(gameover_screen_background, (0, 0))
        
        pygame.display.update() # update the screen

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "start"
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

def main():
    state = "start"
    while True:
        if state == "start":
            state = start_screen()
        elif state == "game":
            state = in_game()
        elif state == "gameover":
            state = game_over_screen()
        else:
            break

    pygame.quit()
    return

main()

'''
 _______ .__   __.  _______   _______  __   _______  __       _______     ____    __    ____  __    __   _______ .__   __. 
|   ____||  \ |  | |       \ |   ____||  | |   ____||  |     |       \    \   \  /  \  /   / |  |  |  | |   ____||  \ |  | 
|  |__   |   \|  | |  .--.  ||  |__   |  | |  |__   |  |     |  .--.  |    \   \/    \/   /  |  |__|  | |  |__   |   \|  | 
|   __|  |  . `  | |  |  |  ||   __|  |  | |   __|  |  |     |  |  |  |     \            /   |   __   | |   __|  |  . `  | 
|  |____ |  |\   | |  '--'  ||  |     |  | |  |____ |  `----.|  '--'  |      \    /\    /    |  |  |  | |  |____ |  |\   | 
|_______||__| \__| |_______/ |__|     |__| |_______||_______||_______/        \__/  \__/     |__|  |__| |_______||__| \__| 
'''
