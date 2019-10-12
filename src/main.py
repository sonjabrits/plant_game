import sys

import pygame

from src.Garden import *
from src.utils.global_vars import *

if __name__ == "__main__":
    pygame.init()

    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    crashed = False
    my_garden = Garden(GARDEN_SIZE)

    characters = pygame.sprite.Group()
    my_char = Character(my_garden, [0, 0])
    characters.add(my_char)

    my_garden.background_group.draw(gameDisplay)

    key_state = [False, False, False, False]  # L, R, U, D

    counter = 0
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()
                main = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    key_state[LEFT] = True
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    key_state[RIGHT] = True
                if event.key == pygame.K_UP or event.key == ord('w'):
                    key_state[UP] = True
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    key_state[DOWN] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    key_state[LEFT] = False
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    key_state[RIGHT] = False
                if event.key == pygame.K_UP or event.key == ord('w'):
                    key_state[UP] = False
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    key_state[DOWN] = False
                if event.key == ord('q'):
                    pygame.quit()
                    sys.exit()
                    main = False

        my_garden.tick(counter)
        my_garden.background_group.draw(gameDisplay)
        my_garden.plant_group.draw(gameDisplay)
        my_garden.env_group.draw(gameDisplay)
        my_char.process_keys(key_state)
        characters.update(counter)
        characters.draw(gameDisplay)

        if my_garden.n_alive < 1:  # len(my_garden.plant_group.sprites()) == 0:
            print("Going to exit, no more living plants")
            crashed = True
        pygame.display.update()
        # pygame.image.save(gameDisplay, "../screenshots/screenshot" + str(counter).zfill(3) + ".jpeg")
        counter += 1
        clock.tick(fps)
