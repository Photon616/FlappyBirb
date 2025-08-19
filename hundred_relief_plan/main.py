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
player_img = pygame.transform.scale(player_img, (64, 64))

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
    
    def jump(self, jump_speed):
        self.y_vel = -jump_speed
    
    def draw(self):
        screen.blit(self.rimg, (self.x, self.y))
    
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
    pl = Player(player_img, 128, 0, 50, 128, 0, 64, 64)
    fall_speed = 0.3
    jump_speed = 8.0

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0)) # draw background

        pl.update(fall_speed) # update the position of the player
        pl.draw() # blit rimg on the screen

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
'''
