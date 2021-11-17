import pygame
from classes import all_objects, DefaultTank, DefaultWall
from random import randint, choice


FPS = 60


pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Tanks Offline")
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()


p1 = DefaultTank(100, 100, (1, 0), (0, 255, 0))
p1.set_controls(pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a, pygame.K_SPACE)
p2 = DefaultTank(900, 900, (-1, 0), (255, 0, 255))
p2.set_controls(pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_KP0)


for _ in range(5):
    DefaultWall(randint(50, 950), randint(50, 700), 20, randint(200, 600), (0, 150, 0))
    DefaultWall(randint(50, 700), randint(50, 950), randint(200, 600), 20, (0, 150, 0))


while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
    keys = pygame.key.get_pressed()

    for object in all_objects:
        object.update(keys)
    screen.fill((255, 255, 255))
    for object in all_objects:
        object.draw(screen)

    pygame.display.update()
