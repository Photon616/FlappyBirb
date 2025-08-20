import pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Player position (for shooting bullets)
player_x, player_y = 400, 500

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 50))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -30  # Moves up

    def update(self):
        self.rect.y += self.speed
        # Remove bullet if it goes off-screen
        if self.rect.bottom < 0:
            self.kill()

# Group to hold all bullets
bullets = pygame.sprite.Group()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Shoot bullet when space is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.add(Bullet(player_x, player_y))

    # Update bullets
    bullets.update()

    # Draw everything
    screen.fill((0, 0, 0))
    bullets.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
