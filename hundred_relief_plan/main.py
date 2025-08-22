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
# if not loading, try removing hundred_relief_plan in the directory.
player_img = pygame.image.load("hundred_relief_plan/Assets/Textures/uvChecker1k.png") 
player_img = pygame.transform.scale(player_img, (64, 48))

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
    
class Obstacle:
    def __init__(self, rimg, x, y, speed, y_range_min, y_range_max, kill_coord):
        self.rimg = rimg
        self.x = x
        self.y = y
        self.init_x = x
        self.speed = speed
        self.y_range_min = y_range_min
        self.y_range_max = y_range_max
        self.kill_coord = kill_coord

    def update(self):
        self.x -= self.speed
        # if self.x <= self.kill_coord:
        #     self.kill()

def start_screen():
    running = True
    in_game()
    while running:
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
    fall_speed = 0.3
    jump_speed = 8.0

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0)) # draw background

        enemies.add(Obstacle(pl.x, pl.y))

        pl.update(fall_speed) # update the position of the 
        enemies.update()

        pl.draw() # blit rimg on the screen
        enemies.draw() 

        pygame.display.update() # update the screen

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pl.jump(jump_speed)
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

def game_over_screen():
    running = True

    while running:
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
there's a starman waiting in the sky
he'd like to come and see us but he thinks he'd blow our minds
there's a starman waiting in the sky
he told us not to blow it 'cause he knows it's all worthwhile
he told me
let the children lose it
let the children use it
let all the children boogie

 _______ .__   __.  _______   _______  __   _______  __       _______     ____    __    ____  __    __   _______ .__   __. 
|   ____||  \ |  | |       \ |   ____||  | |   ____||  |     |       \    \   \  /  \  /   / |  |  |  | |   ____||  \ |  | 
|  |__   |   \|  | |  .--.  ||  |__   |  | |  |__   |  |     |  .--.  |    \   \/    \/   /  |  |__|  | |  |__   |   \|  | 
|   __|  |  . `  | |  |  |  ||   __|  |  | |   __|  |  |     |  |  |  |     \            /   |   __   | |   __|  |  . `  | 
|  |____ |  |\   | |  '--'  ||  |     |  | |  |____ |  `----.|  '--'  |      \    /\    /    |  |  |  | |  |____ |  |\   | 
|_______||__| \__| |_______/ |__|     |__| |_______||_______||_______/        \__/  \__/     |__|  |__| |_______||__| \__| 
'''
