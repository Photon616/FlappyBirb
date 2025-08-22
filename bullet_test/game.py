import pygame


pygame.init

#이미지
player_image=pygame.image.load("bullet_test/r.png")
player_rect=player_image.get_rect()
player_rect.topleft=(276,200)

weapon_image=pygame.image.load("bullet_test/i.png")
weapon_rect=player_image.get_rect()
weapon_rect.topleft=(276,200)

weapon_rock=0
weapon_speed=0
weapon_cooldown=0
#화면 설정
screen=pygame.display.set_mode((640,480))
pygame.display.set_caption("game")

#반복
running=True
screen.fill((255,255,255))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #테스트용 조작
    keys=pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y-=0.6
    if keys[pygame.K_s]:    
        player_rect.y+=0.6

    if keys[pygame.K_f] and weapon_rock==0:
        weapon_speed=0.6
        weapon_rect.x=player_rect.x
        weapon_rock=1
        weapon_cooldown=3000
        
    
    if weapon_rock==0:
        weapon_rect.y=player_rect.y+22
    if weapon_rock==1:
        weapon_cooldown-=1
        if  weapon_cooldown<=0:
             weapon_rock = 0 
        

    weapon_rect.x += weapon_speed

    screen.fill((255,255,255))
    screen.blit(weapon_image,weapon_rect)
    screen.blit(player_image,player_rect)
    
    
    pygame.display.update()
pygame.quit()