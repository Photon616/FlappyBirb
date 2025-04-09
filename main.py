import random
import pygame
from pygame.locals import *

pygame.init()

screen_width = 1024
screen_height = 1024

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("test")

clock = pygame.time.Clock()

# image load
kabosu_img = pygame.image.load("kabosu_highres.jpg")
kabosu_img = pygame.transform.scale(kabosu_img, (64, 64))

# variables
player_speed = 5
player_x_offset = 192
player_y_offset = 512.0
player_y_vel = 0.0
terminal_velocity = 100

#classes
class Player:
    def __init__(self, pimg, x, y):
        self.img = pimg
        self.rect = pygame.Rect(x, y, pimg.get_width(), pimg.get_height())
        self.velocity = 0.0

    def update(self):
        self.rect.y += self.velocity
        self.velocity += 0.5
        if self.velocity > terminal_velocity:
            self.velocity = terminal_velocity

    def jump(self):
        self.velocity = -14

    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)

def start_screen():
    running = True
    # to be finished
    in_game()

def in_game():
    pl = Player(kabosu_img, 0, 0)

    running = True
    while running:
        screen.fill(0, 0, 0)

        #blit
        pl.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pl.jump()
            if event.type == pygame.QUIT:
                running = False
                
        pygame.display.update()
        pl.update()

    pygame.quit()
    return

start_screen()

'''
running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)
    
    player_rect = pygame.Rect(player_x_offset, player_y_offset, 64, 64)

    # the gravitational accelaration affects the player. the accelaration stops when the velocity reaches the terminal velocity set previously
    player_y_vel += 0.5

    player_y_offset += player_y_vel

    #BLIT!
    screen.blit(kabosu_img, (player_x_offset, player_y_offset))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_y_vel = -14
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

'''
