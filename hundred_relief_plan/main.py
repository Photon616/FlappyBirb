import random
import time
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

scrnW = 640 # the width of the game window(pixels)
scrnH = 480 # the height of the game window(pixels)

screen = pygame.display.set_mode((scrnW, scrnW))
pygame.display.set_caption("operation")

clock = pygame.time.Clock()

# load images here

# classes
class Player:
    def __init__(self, rimg, x, y, y_vel_limit, rect_x, rect_y):
        self.rimg = rimg
        self.x = x
        self.y = y
        self.y_vel = 0
        self.y_vel_limit = y_vel_limit
        self.rect = pygame.Rect(x, y, rect_x, rect_y)
    
    def update(self, fall_speed):
        self.y_vel += fall_speed # adds on y coordinate to go down

        if self.y_vel > self.y_vel_limit:
            self.y_vel = self.y_vel_limit

        self.y += self.y_vel
    

def start_screen():
    running = True

    while running:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "game"
                if event.type == pygame.QUIT:
                    running = False

def in_game():
    running = True

    while running:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # return "game"
                        ''
                if event.type == pygame.QUIT:
                    running = False

def game_over_screen():
    running = True

    while running:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "start"
                if event.type == pygame.QUIT:
                    running = False

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
