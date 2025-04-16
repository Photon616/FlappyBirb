import random
import pygame
from pygame.locals import *

pygame.init()

screen_width = 1024
screen_height = 1024

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("test")

clock = pygame.time.Clock()
pretendard_black = pygame.font.Font("Assets/Fonts/Pretendard-Black.ttf", 128)

# image load
# kabosu_img = pygame.image.load("Assets/kabosu_highres.jpg")
kabosu_img = pygame.image.load("Assets/Textures/monotoneChecker1k.png")
kabosu_img = pygame.transform.scale(kabosu_img, (64, 64))

checkerboard_img = pygame.image.load("Assets/Textures/uvChecker1k.png")
checkerboard_img = pygame.transform.scale(checkerboard_img, (1024, 1024))
monoCheck_img = pygame.image.load("Assets/Textures/monotoneChecker1k.png")
monoCheck_img = pygame.transform.scale(monoCheck_img, (1024, 1024))

obstacle_checkerboard_img = pygame.image.load("Assets/Textures/uvChecker1k.png")
obstacle_checkerboard_img = pygame.transform.scale(obstacle_checkerboard_img, (128, 1024))
obstacle_monoCheck_img = pygame.image.load("Assets/Textures/monotoneChecker1k.png")
obstacle_monoCheck_img = pygame.transform.scale(obstacle_monoCheck_img, (128, 1024))

# variables
player_speed = 5
player_x_offset = 192
player_y_offset = 256  
player_y_vel = 11.0
terminal_velocity = 100
gap_range = 256
gap_height = random.randint(374, 1024 - 374)
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
        self.velocity = -11 - (score // 5)

    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)

class Obstacles:
    def __init__(self, rimg, x, y):
        self.img = rimg
        self.rect = pygame.Rect(x, y, rimg.get_width() * 0.8, rimg.get_height())
        self.velocity = 8

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.x < (-1 * screen_width) + 512:
            self.rect.x = screen_width
            global gap_height 
            gap_height = random.randint(374, 1024 - 374)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x - self.img.get_width() * 0.1, self.rect.y))

    def setHeight(self, height, isAbove):
        if isAbove:
            self.rect.y = (height - self.img.get_height()) - (gap_range / 2)
        else:
            self.rect.y = (height) + (gap_range / 2)
        # self.rect.y = height + ((gap_range / 2) * multiplyer)

class parallax_bg:
    def __init__(self, rimg, x, y, velFac):
        self.img = rimg
        self.rect = pygame.Rect(x, y, rimg.get_width(), rimg.get_height())
        self.velocity = 8
        self.factor = velFac

    def update(self):
        self.rect.x -= self.velocity * self.factor
        if self.rect.x < -1024:
            self.rect.x = screen_width

    def draw(self, surface):
        surface.blit(self.img, self.rect.topleft)

def start_screen():
    running = True

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
    global pretendard_black

    pl = Player(kabosu_img, 192, 0) # the player
    obsBelow = Obstacles(obstacle_checkerboard_img, 1024, 0) # the obstacle coming below
    obsAbove = Obstacles(obstacle_monoCheck_img, 1024, 0) # the obstacle coming above

    bg1_left = parallax_bg(checkerboard_img, 0, 850, 2) # the first layer of parallax background(left)
    bg1_right = parallax_bg(checkerboard_img, 1024, 850, 2) # the first layer of parallax background(right)

    bg2_left = parallax_bg(checkerboard_img, 0, 700, 1) # the second layer of parallax background(left)
    bg2_right = parallax_bg(checkerboard_img, 1024, 700, 1) # the second layer of parallax background(right)

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
        if pl.rect.y >= screen_height - pl.img.get_height() or pl.rect.y < 0 or pl.rect.colliderect(obsAbove.rect) or pl.rect.colliderect(obsBelow.rect):
            return "gameover"

        # score player
        if pl.rect.x == obsAbove.rect.x:
            score += 1
        
        # show score
        score_text = pretendard_black.render(str(score), True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(512, 512))

        # draw elements
        # background
        screen.blit(score_text, score_text_rect)
        
        bg2_left.draw(screen)
        bg2_right.draw(screen)

        bg1_left.draw(screen)
        bg1_right.draw(screen)

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

        bg1_left.update()
        bg1_right.update()

        bg2_left.update()
        bg2_right.update()

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
