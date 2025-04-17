import random
import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("test")

clock = pygame.time.Clock()
pretendard_black = pygame.font.Font("Assets/Fonts/Pretendard-Black.ttf", 64)

# image load
# kabosu_img = pygame.image.load("Assets/kabosu_highres.jpg")
kabosu_img = pygame.image.load("Assets/Textures/monotoneChecker1k.png")
kabosu_img = pygame.transform.scale(kabosu_img, (48, 48))

checkerboard_img = pygame.image.load("Assets/Textures/uvChecker1k.png")
checkerboard_img = pygame.transform.scale(checkerboard_img, (1024, 1024))
monoCheck_img = pygame.image.load("Assets/Textures/monotoneChecker1k.png")
monoCheck_img = pygame.transform.scale(monoCheck_img, (1024, 1024))

obstacle_checkerboard_img = pygame.image.load("Assets/Textures/uvChecker1k.png")
obstacle_checkerboard_img = pygame.transform.scale(obstacle_checkerboard_img, (64, 512))
obstacle_monoCheck_img = pygame.image.load("Assets/Textures/monotoneChecker1k.png")
obstacle_monoCheck_img = pygame.transform.scale(obstacle_monoCheck_img, (64, 512))

bg_img = pygame.image.load("Assets/Textures/placeholder_800x600.png")

# variables
player_speed = 5
player_x_offset = 200
player_y_offset = 0  
player_y_vel = 0.0
terminal_velocity = 100
gap_range = 160
gap_height = random.randint(200, 400)
score = 0
can_score = True

#classes
class Player:
    def __init__(self, rimg, x, y):
        self.img = rimg
        self.rect = pygame.Rect(x, y, rimg.get_width(), rimg.get_height())
        self.velocity = 0.0

    def update(self):
        self.rect.y += self.velocity
        self.velocity += 0.3
        if self.velocity > terminal_velocity:
            self.velocity = terminal_velocity

    def jump(self):
        self.velocity = -7 - (score // 5)

    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)

class Obstacles:
    def __init__(self, rimg, x, y):
        self.img = rimg
        self.rect = pygame.Rect(x, y, rimg.get_width() * 0.8, rimg.get_height())
        self.velocity = 6

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.x < (-1 * screen_width) + 400:
            self.rect.x = screen_width
            global gap_height 
            global can_score
            gap_height = random.randint(150, 450)
            can_score = True

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x - self.img.get_width() * 0.1, self.rect.y))

    def setHeight(self, height, isAbove):
        if isAbove:
            self.rect.y = (height - self.img.get_height()) - (gap_range / 2)
        else:
            self.rect.y = (height) + (gap_range / 2)
        # self.rect.y = height + ((gap_range / 2) * multiplyer)

def start_screen():
    running = True
    keys = pygame.key.get_pressed()

    while running:
        if True:
            return "game"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # to be finished

def gameOverScreen():
    # to be finished
    return "start"

def in_game():
    global score
    global can_score
    global pretendard_black

    pl = Player(kabosu_img, 192, 0) # the player
    obsBelow = Obstacles(obstacle_checkerboard_img, 1024, 0) # the obstacle coming below
    obsAbove = Obstacles(obstacle_monoCheck_img, 1024, 0) # the obstacle coming above

    score = 0 # reset score
    can_score = True

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
        if pl.rect.y >= screen_height - pl.img.get_height() or pl.rect.y < 0 or pl.rect.colliderect(obsAbove.rect) or pl.rect.colliderect(obsBelow.rect):
            return "gameover"

        # score player
        if pl.rect.x >= obsAbove.rect.x and can_score:
            score += 1
            can_score = False
        
        # show score
        score_text = pretendard_black.render(str(score), True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(400, 300))

        # draw elements
        # background
        screen.blit(bg_img, (0, 0))
        screen.blit(score_text, score_text_rect)

        # other elements
        obsBelow.draw(screen)
        obsAbove.draw(screen)
        pl.draw(screen)

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

def main():
    state = "start"
    while True:
        if state == "start":
            state = start_screen()
        elif state == "game":
            state = in_game()
        elif state == "gameover":
            state = gameOverScreen()
        else:
            break

    pygame.quit()
    return

#initial start
main()

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
