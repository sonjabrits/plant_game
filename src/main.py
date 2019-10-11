from src.utils.GraphDrawer import *
import pygame

from src.Garden import ROCK

fps = 0.5
WIDTH = 800
LENGTH = 800
GREEN = (  0, 255,   0)

GARDEN_SIZE = [10, 10]
N_ELEMS = 20

if __name__ == "__main__":
    pygame.init()

    gameDisplay = pygame.display.set_mode((WIDTH, LENGTH))
    clock = pygame.time.Clock()

    crashed = False
    my_garden = Garden(GARDEN_SIZE, N_ELEMS)

    dirty_recs = []

    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        my_garden.tick()
        for p in my_garden.plants:
            x = int(float(p.position[0])/GARDEN_SIZE[0]*WIDTH)
            y = int(float(p.position[1])/GARDEN_SIZE[1]*LENGTH)
            size = 3 + p.age
            if p.alive:
                pygame.draw.rect(gameDisplay, GREEN, [x, y, size, size])
            else:
                color = pygame.Color('orange')
                pygame.draw.rect(gameDisplay, color, [x, y, size, size])


        for elem in my_garden.env_elems:
            x = int(float(elem.position[0])/GARDEN_SIZE[0]*WIDTH)
            y = int(float(elem.position[1])/GARDEN_SIZE[1]*LENGTH)
            size = elem.size
            if elem.elem_type == ROCK:
                color = pygame.Color('lightgray')
                pygame.draw.circle(gameDisplay, color, [x, y], size)
            if elem.elem_type == WATER:
                color = pygame.Color('blue')
                pygame.draw.circle(gameDisplay, color, [x, y], size)
        my_graphdrawer = GraphDrawer()
        my_graphdrawer.draw_family_graph(my_garden)

        if my_garden.n_alive == 0:
            crashed = True
        print(pygame.time.get_ticks()/1000)
        pygame.display.update()
        clock.tick(fps) #


