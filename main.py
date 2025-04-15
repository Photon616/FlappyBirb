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
kabosu_img = pygame.image.load("Assets/kabosu_highres.jpg")
# kabosu_img = pygame.image.load("Assets/monotoneChecker1k.png")
kabosu_img = pygame.transform.scale(kabosu_img, (64, 64))
checkerboard_img = pygame.image.load("Assets/uvChecker1k.png")
checkerboard_img = pygame.transform.scale(checkerboard_img, (128, 1024))
monoCheck_img = pygame.image.load("Assets/monotoneChecker1k.png")
monoCheck_img = pygame.transform.scale(monoCheck_img, (128, 1024))

# variables
player_speed = 5
player_x_offset = 192
player_y_offset = 256  
player_y_vel = 0.0
terminal_velocity = 100
gap_range = 256
gap_height = random.randint(256, 1024 - 256)
score = 0

#classes
class Player:
    def __init__(self, rimg, x, y):
        self.img = rimg
        self.rect = pygame.Rect(x, y, rimg.get_width(), rimg.get_height())
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

class Obstacles:
    def __init__(self, rimg, x, y):
        self.img = rimg
        self.rect = pygame.Rect(x, y, rimg.get_width() * 0.5, rimg.get_height())
        self.velocity = 8

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.x < (-1 * screen_width) + 512:
            self.rect.x = screen_width
            global gap_height 
            gap_height = random.randint(256, 1024 - 256)

    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)

    def setHeight(self, height, isAbove):
        if isAbove:
            self.rect.y = (height - self.img.get_height()) - (gap_range / 2)
        else:
            self.rect.y = (height) + (gap_range / 2)
        # self.rect.y = height + ((gap_range / 2) * multiplyer)


def start_screen():
    running = True
    # to be finished
    '''
    player_speed = 5
    player_x_offset = 192
    player_y_offset = 256  
    player_y_vel = 0.0
    terminal_velocity = 100
    gap_range = 256
    gap_height = random.randint(256, 1024 - 256)
    '''
    in_game()

def in_game():
    global score

    pl = Player(kabosu_img, 192, 0) # the player
    obsBelow = Obstacles(checkerboard_img, 1024, 0) # the obstacle coming below
    obsAbove = Obstacles(monoCheck_img, 1024, 0) # the obstacle coming above
    score = 0 # reset score

    running = True
    while running:
        # initiallize the screen
        screen.fill((0, 0, 0))
        clock.tick(60)

        # initiallize the variables

        # tell the obstacles height of the gap
        obsAbove.setHeight(gap_height, True)
        obsBelow.setHeight(gap_height, False)

        # check if player is dead
        if pl.rect.y >= screen_height - pl.img.get_height() or pl.rect.y < 0:
            gameOverScreen()

        # print(pl.rect.y)

        #draw elements
        pl.draw(screen)
        obsBelow.draw(screen)
        obsAbove.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pl.jump()
            if event.type == pygame.QUIT:
                running = False
        
        # update sprites' position and the screen itself
        pl.update()
        obsBelow.update()
        obsAbove.update()
        pygame.display.update()

    pygame.quit()
    return

def gameOverScreen():
    running = True
    # to be finished
    start_screen()

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
