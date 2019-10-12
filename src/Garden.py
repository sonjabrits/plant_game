from src.Sprites import *
from src.utils.common_utils import *
from src.utils.global_vars import *


class Garden:
    def __init__(self, size=[10, 10]):
        self.grid_size = size
        self.all_group = pygame.sprite.Group()
        self.env_group = pygame.sprite.Group()
        self.background_group = pygame.sprite.Group()
        self.env_grid = self.create_environment(N_ELEMS)

        self.plant_group = pygame.sprite.Group()
        self.plant_grid = [[None for i in range(0, size[1])] for j in range(0, size[0])]
        position = random_position([GARDEN_SIZE[0], GARDEN_SIZE[1]])
        self.temp_sprite = pygame.sprite.Sprite()
        self.temp_sprite.rect = pygame.Rect(int(float(position[0]) * GRID_SIZE), int(float(position[1]) * GRID_SIZE),
                                            GRID_SIZE, GRID_SIZE)

        while len(pygame.sprite.spritecollide(self.temp_sprite, self.env_group, False)) != 0:
            position = random_position([GARDEN_SIZE[0], GARDEN_SIZE[1]])
            self.temp_sprite.rect = pygame.Rect(int(float(position[0]) * GRID_SIZE),
                                                int(float(position[1]) * GRID_SIZE), GRID_SIZE, GRID_SIZE)
        p = Plant(self, position, 0)
        self.plant_elder = p
        self.plant_grid[p.position[0]][p.position[1]] = p
        self.plant_group.add(p)
        self.all_group.add(p)
        self.n_alive = 1
        self.all_plants = 1

        print("Creating new garden")

    def create_environment(self, n_elems):
        environment = [[None for i in range(0, self.grid_size[1])] for j in range(0, self.grid_size[0])]
        for i in range(0, n_elems):
            position = random_position([GARDEN_SIZE[0], GARDEN_SIZE[1]])
            temp_sprite = pygame.sprite.Sprite()
            temp_sprite.rect = pygame.Rect(int(float(position[0]) * GRID_SIZE), int(float(position[1]) * GRID_SIZE),
                                           GRID_SIZE, GRID_SIZE)

            if len(pygame.sprite.spritecollide(temp_sprite, self.env_group, False)) == 0:
                elem_type = randint(0, len(ENV_ELEMS) - 2)
                elem = GardenElem(position, elem_type)
                environment[position[0]][position[1]] = elem
                self.env_group.add(elem)
                self.all_group.add(elem)

        for i in range(0, GARDEN_SIZE[0]):
            for j in range(0, GARDEN_SIZE[1]):
                self.background_group.add(GardenElem([i, j], GRASS))
        return environment

    def tick(self, counter):
        self.env_group.update(counter)
        self.plant_group.update(counter)
        for p in self.plant_group.sprites():
            p.tick()
            if p.ready:
                child = p.spawn()
                if child:
                    self.all_plants += 1
                    self.add_plant(child)

    def add_plant(self, p):
        self.n_alive += 1
        self.plant_group.add(p)
        self.all_group.add(p)

    def is_collision(self, position, group, size=[GRID_SIZE, GRID_SIZE]):
        self.temp_sprite.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        return len(pygame.sprite.spritecollide(self.temp_sprite, group, False)) > 0
