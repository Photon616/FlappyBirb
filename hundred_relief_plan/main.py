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
pretendard_black = pygame.font.Font("hundred_relief_plan/Assets/Fonts/Pretendard-Black.ttf", 64)
pretendard = pygame.font.Font("hundred_relief_plan/Assets/Fonts/Pretendard-Regular.ttf", 32)

score = 0

# load images here
# if errors are occuring, try removing hundred_relief_plan from the directory.
enemy_img = pygame.image.load("hundred_relief_plan/Assets/Textures/monotoneChecker1k.png") 
enemy_img = pygame.transform.scale(enemy_img, (64, 48))
bullet_img = pygame.image.load("hundred_relief_plan/Assets/Textures/missile.png") 
bullet_img = pygame.transform.scale(bullet_img, (50, 10))
cue_img = pygame.image.load("hundred_relief_plan/Assets/Textures/player_box.png") 
cue_img = pygame.transform.scale(cue_img, (32, scrnH))
# effects
explosion_img = pygame.image.load("hundred_relief_plan/Assets/Textures/uvChecker1k.png") 
explosion_img = pygame.transform.scale(explosion_img, (128, 128))
package_img = pygame.image.load("hundred_relief_plan/Assets/Textures/uvChecker1k.png") 
package_img = pygame.transform.scale(package_img, (48, 48))
slcr_effect_img = pygame.image.load("hundred_relief_plan/Assets/Textures/hollow_white_circle.png") 
slcr_effect_img = pygame.transform.scale(slcr_effect_img, (96, 96))
# items
silencer_img = pygame.image.load("hundred_relief_plan/Assets/Textures/monotoneChecker1k.png") 
silencer_img = pygame.transform.scale(silencer_img, (64, 64))
# bg
start_screen_background = pygame.image.load("hundred_relief_plan/Assets/Textures/placeholder_640x480.png")
gameover_screen_background = pygame.image.load("hundred_relief_plan/Assets/Textures/placeholder_800x600.png")

# load player images
player_sprites = []
player_sprites.append(pygame.image.load("hundred_relief_plan/Assets/Textures/player_drone_sheets_2/0.png"))
player_sprites.append(pygame.image.load("hundred_relief_plan/Assets/Textures/player_drone_sheets_2/1.png"))
player_sprites.append(pygame.image.load("hundred_relief_plan/Assets/Textures/player_drone_sheets_2/2.png"))
player_sprites.append(pygame.image.load("hundred_relief_plan/Assets/Textures/player_drone_sheets_2/3.png"))

# load explosion sprites
explosion_sprites = []

# classes
class Player:
    def __init__(self, sprites, x, y, y_spd_limit, rect_x, rect_y, rect_size_x, rect_size_y):
        self.sprites = sprites
        self.x = x
        self.y = y
        self.y_spd = 0
        self.y_spd_limit = y_spd_limit
        self.rect = pygame.Rect(rect_x, rect_y, rect_size_x, rect_size_y)
    
    def update(self, fall_speed):
        self.y_spd += fall_speed 

        if self.y_spd > self.y_spd_limit:
            self.y_spd = self.y_spd_limit

        self.y += self.y_spd # adds on y coordinate to go down

        # checks if the player is colliding with the top and bottom of the screen
        if (self.y + self.rect.height) > scrnH:
            self.y = scrnH - self.rect.height
            self.y_spd = 0
        elif self.y < 0:
            self.y = 0
            self.y_spd = 0

        self.rect.y = self.y
    
    def jump(self, jump_speed):
        self.y_spd = -jump_speed
    
    def draw(self, frame):
        screen.blit(self.sprites[frame], (self.x, self.y))
    
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
    def __init__(self, image, pos, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.timer = 15  # frames until disappears

    def update(self):
        self.timer -= 1
        self.rect.x -= self.speed
        if self.timer <= 0:
            self.kill()

class Relief_Package(pygame.sprite.Sprite):
    def __init__(self, image, x, y, y_spd, x_spd_limit):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))
        self.x = x
        self.y = y
        self.x_spd = 0
        self.y_spd = y_spd
        self.x_spd_limit = x_spd_limit
    
    def update(self, fall_speed):
        self.x_spd += fall_speed 

        if self.x_spd > self.x_spd_limit:
            self.x_spd = self.x_spd_limit

        self.y += self.y_spd # adds on y coordinate to go down
        self.x -= self.x_spd

        self.rect.x = self.x
        self.rect.y = self.y

        if self.rect.top >= scrnH or self.rect.right <= 0:
            self.kill()

class Silencer_Item(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed, kill_coord):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))
        self.x = x
        self.y = y
        self.speed = speed
        self.kill_coord = kill_coord
    
    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < self.kill_coord:
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
    global pretendard
    global pretendard_black

    # universal
    running = True
    pl = Player(player_sprites, 128, 0, 50, 128, 0, 64, 48)
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    effects = pygame.sprite.Group()
    relief_packages = pygame.sprite.Group()
    silencers = pygame.sprite.Group()
    fall_speed = 0.3
    jump_speed = 8.0 

    #player
    pl_frame = 0
    pl_frame_time = 0
    pl_frame_duration = .1
 
    # attention
    attention = 0

    # enemy
    enemy_duration = 4 # in sec. division will be done after
    enemy_time = (enemy_duration - 1) * 60
    enemy_speed = 4

    # weapon
    weapon_duration = .5 # in sec
    weapon_time = weapon_duration * 60
    bullet_speed = 10

    # supply package
    supply_duration = 2 # in sec
    supply_time = 0

    # silencer item
    slcr_duration = 7
    slcr_time = 0
    silenced = False

    global score
    score = 0

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0)) # draw background

        # spawning enemies
        if enemy_time / 60 >= enemy_duration - (attention / 100): # adds when time matches with duration.
            # print("enemy added")
            enemies.add(Obstacle(enemy_img, 680, enemy_speed + random.randrange(-1, 1), 110, 340, pl.rect.right, cue_img))
            # print("really added")
            enemy_time = 0 # initialize time to prevent overflow/save memory

        # spawining silencer items
        if slcr_time / 60 >= slcr_duration: # similar to enemies
            silencers.add(Silencer_Item(silencer_img, 680, random.randrange(110, 340), enemy_speed, -10))
            slcr_time = 0

        # supply and scoring
        if supply_time / 60 >= supply_duration:
            if pl.y_spd < 0:
                package_speed = -1
            else:
                package_speed = pl.y_spd * .5
            relief_packages.add(Relief_Package(package_img, pl.rect.centerx - 24, pl.rect.centery - 24, package_speed + 2, 50))
            score += 10  # add score
            supply_time = 0
        
        # updating player sprite's frame
        if pl_frame_time / 60 >= pl_frame_duration:
            pl_frame += 1
            if pl_frame >= 4:
                pl_frame = 0
            pl_frame_time = 0

        # handling collisions between items and player
        slcr_col = pygame.sprite.spritecollide(pl, silencers, dokill = False)
        for col_obj in slcr_col:
            silenced = True
            col_obj.kill()
        
        score_text = pretendard_black.render(str(int(score)), True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(scrnW / 2, scrnH / 2))

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_f] and weapon_time / 60 >= weapon_time:
        #     print("pew-")
        #     bullets.add(Bullet(bullet_img, pl.x, pl.y, bullet_speed, scrnW))
        #     weapon_time = 0

        pl.update(fall_speed) # update the position of the player
        bullets.update()
        effects.update()
        enemies.update()
        relief_packages.update(0.2)
        silencers.update()
        for target_enemy in enemies:
            if target_enemy.is_over:
                return "gameover"

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)

        for bullet, hit_list in hits.items():
            for hit_enemy in hit_list:
                effects.add(Explosion(explosion_img, hit_enemy.rect.center, enemy_speed))

        screen.blit(score_text, score_text_rect)

        bullets.draw(screen)
        enemies.draw(screen) 
        relief_packages.draw(screen)
        pl.draw(pl_frame) # blit rimg on the screen
        effects.draw(screen)
        silencers.draw(screen)

        # draw silenced effect
        if silenced:
            screen.blit(slcr_effect_img, (pl.rect.centerx - 48, pl.rect.centery - 48))

        # attention bar
        # bar_bg = pygame.Surface((scrnW, 16))
        # bar_bg.fill((0, 255, 0))
        # bar_bg.blit(screen, (120, 0))
        pygame.draw.rect(screen, (255, 255, 255), ((0 - scrnW) + (attention * (scrnW / 300)), 0, scrnW, 32))  
        if weapon_time >= weapon_duration * 60:
            weapon_bar_x = weapon_duration * 60
        else:
            weapon_bar_x = weapon_time
        pygame.draw.rect(screen, (0, 255, 0), ((0 - scrnW) + (weapon_bar_x * (scrnW / (weapon_duration * 60))), scrnH - 16, scrnW, 16))  
        #print(weapon_bar_x * ((scrnW / weapon_duration) * 60))

        pygame.display.update() # update the screen
        
        # raise one on every time variables
        enemy_time += 1
        weapon_time += 1
        supply_time += 1
        pl_frame_time += 1
        slcr_time += 1

        if attention > 0:
            attention -= 0.2

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pl.jump(jump_speed)
                if event.key == pygame.K_f and weapon_time / 60 >= weapon_duration:
                    # print("bullet shot")
                    bullets.add(Bullet(bullet_img, pl.x, pl.rect.center[1] - 5, bullet_speed, scrnW))
                    if not silenced:
                        if enemy_duration - ((attention + 40) / 100) < 1:
                            attention = 300
                        else:
                            attention += 50 # adds 0.2 to attention, speeding up enemy spawns
                    else:
                        silenced = False 
                    weapon_time = 0
                if event.key == pygame.K_ESCAPE:
                    return "start"
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
    
    #return "start"

def game_over_screen():
    global pretendard
    global pretendard_black
    global score

    running = True
    #print("test")

    # for continue timer
    cntn_time = 0
    cntn_duration = 1

    while running:
        clock.tick(60)
        screen.fill((0, 0, 0)) # draw background
        # screen.blit(gameover_screen_background, (0, 0))
        
        score_text = pretendard_black.render(f"{str(int(score))}", True, (255, 255, 255))
        score_text_rect = score_text.get_rect(center=(scrnW / 2, scrnH / 2 - 100))
        screen.blit(score_text, score_text_rect)
        
        cntn_text = pretendard_black.render(f"SPACE로 복귀", True, (255, 255, 255))
        cntn_text_rect = cntn_text.get_rect(center=(scrnW / 2, scrnH / 2 + 100))

        if cntn_time >= cntn_duration * 60:
            screen.blit(cntn_text, cntn_text_rect)

        pygame.display.update() # update the screen

        cntn_time += 1

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and cntn_time >= cntn_duration * 60:
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
░██       ░██ ░██     ░██ ░██████████ ░███    ░██ ░██████████░██████░██████████ ░██         ░███████   
░██       ░██ ░██     ░██ ░██         ░████   ░██ ░██          ░██  ░██         ░██         ░██   ░██  
░██  ░██  ░██ ░██     ░██ ░██         ░██░██  ░██ ░██          ░██  ░██         ░██         ░██    ░██ 
░██ ░████ ░██ ░██████████ ░█████████  ░██ ░██ ░██ ░█████████   ░██  ░█████████  ░██         ░██    ░██ 
░██░██ ░██░██ ░██     ░██ ░██         ░██  ░██░██ ░██          ░██  ░██         ░██         ░██    ░██ 
░████   ░████ ░██     ░██ ░██         ░██   ░████ ░██          ░██  ░██         ░██         ░██   ░██  
░███     ░███ ░██     ░██ ░██████████ ░██    ░███ ░██        ░██████░██████████ ░██████████ ░███████                                                              
'''
