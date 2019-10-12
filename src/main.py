import sys

from src.Garden import Garden
from src.Sprites import Plant, GardenElem, Character
from src.utils.global_vars import *
from src.utils.common_utils import *
from src.utils.game_screen import GameHandler

if __name__ == "__main__":
    pygame.init()

    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    my_game_handler = GameHandler(gameDisplay)
    clock = pygame.time.Clock()
    crashed = False
    key_state = [False, False, False, False]  # L, R, U, D
    counter = 0

    my_garden = Garden(GARDEN_SIZE)
    my_garden.background_group.draw(gameDisplay)

    characters = pygame.sprite.Group()
    my_char = Character(my_garden)
    characters.add(my_char)

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
        my_game_handler.message_display("Flowers: " + str(my_char.inventory["flowers"]))

        if my_garden.n_alive < 1:
            print("Going to exit, no more living plants")
            print("Congratz, you collected " + str(my_char.inventory["flowers"]) + " flowers")
            crashed = True
        pygame.display.update()
        counter += 1
        clock.tick(fps)

    my_garden.background_group.draw(gameDisplay)
    my_game_handler.message_display("Congratulations! You got " + str(my_char.inventory["flowers"]) + " FLOWERS",
                                    [int(SCREEN_SIZE[0] / 2), int(SCREEN_SIZE[1] / 2)])

    pygame.display.update()
    pygame.time.wait(2000)
