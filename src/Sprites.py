import os

import names
import pygame

from src.Garden import *
from src.utils.common_utils import *
from src.utils.global_vars import *

ENV_ELEMS = ["rock", "water", "grass"]
ROCK = 0
WATER = 1
GRASS = 2

CHAR_MODES = ["left", "right", "up", "down", "stand"]
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
STAND = 4

FLOWER_STATES = ["growing", "mature", "wilting", "dying", "dead"]
GROWING = 0
MATURE = 1
WILTING = 2
DYING = 3
DEAD = 4


class Plant(pygame.sprite.Sprite):
    def __init__(self, garden, position, id, parent=None):
        pygame.sprite.Sprite.__init__(self)
        self.garden = garden
        self.id = id
        self.name = names.get_first_name()
        if parent:
            self.parent = parent
        else:
            self.parent = None
        self.position = position
        self.children = pygame.sprite.Group()
        self.ready = False
        self.age = 0.0
        self.alive = True
        self.age_rate = 1
        self.ages = [0, 105, 400, 600, 700, 750]
        self.spawn_r = 3
        self.spawn_chance = 0.8

        self.rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        self.state = GROWING
        self.all_images = {}
        for mode in FLOWER_STATES:
            for name in os.listdir("../sprites/flower/" + mode + "/"):
                if name.endswith(".png"):
                    if mode not in self.all_images.keys():
                        self.all_images[mode] = []
                    self.all_images[mode].append(
                        pygame.transform.scale(
                            pygame.image.load("../sprites/flower/" + mode + "/" + name).convert_alpha(),
                            (GRID_SIZE, GRID_SIZE)))
        self.img_idx = 0
        self.image = self.all_images[FLOWER_STATES[self.state]][self.img_idx]

    def age_plant(self):
        if self.alive:
            self.age += self.age_rate
            if self.age > self.ages[self.state + 1]:
                self.state += 1
                self.img_idx = 0
                self.ready = True
            if self.age > self.ages[DEAD]:
                self.state = DEAD
                self.kill_flower()
                return True
        return False

    def kill_flower(self):
        self.garden.n_alive -= 1
        self.alive = False
        self.kill()

    def tick(self):
        return self.age_plant()

    def spawn(self):
        self.ready = False
        if self.spawn_chance > random():  # Make it less likely to actually spawn a child plant
            [x, y] = random_position([GARDEN_SIZE[0], GARDEN_SIZE[1]], self.position, [self.spawn_r, self.spawn_r])
            temp_sprite = pygame.sprite.Sprite()
            temp_sprite.rect = pygame.Rect(int(float(x) * GRID_SIZE), int(float(y) * GRID_SIZE), GRID_SIZE, GRID_SIZE)

            if len(pygame.sprite.spritecollide(temp_sprite, self.garden.all_group, False)) == 0:
                child = Plant(self.garden, [x, y], self.garden.all_plants, self)
                self.children.add(child)
                return child
        return None

    def update(self, counter):
        age_gap = self.ages[self.state + 1] - self.ages[self.state] if self.state < len(FLOWER_STATES) - 1 else 0
        age_base = self.ages[self.state]
        age_interval = self.age - age_base
        self.img_idx = min(round(age_interval / age_gap * len(self.all_images[FLOWER_STATES[self.state]])),
                           len(self.all_images[FLOWER_STATES[self.state]]) - 1)
        self.image = self.all_images[FLOWER_STATES[self.state]][self.img_idx]


class GardenElem(pygame.sprite.Sprite):
    def __init__(self, position, elem_type):
        pygame.sprite.Sprite.__init__(self)
        self.elem_type = elem_type
        self.position = position
        self.size = 15
        self.rect = pygame.Rect(int(float(position[0]) * GRID_SIZE), int(float(position[1]) * GRID_SIZE), GRID_SIZE,
                                GRID_SIZE)
        string_t = ENV_ELEMS[self.elem_type]
        self.images = []
        for name in os.listdir("../sprites/" + string_t + "/"):
            if name.endswith(".png"):
                self.images.append(
                    pygame.transform.scale(pygame.image.load("../sprites/" + string_t + "/" + name).convert_alpha(),
                                           (GRID_SIZE, GRID_SIZE)))
        self.img_idx = randint(0, len(self.images) - 1)
        self.image = self.images[self.img_idx]

    def update(self, counter):
        if ((counter % fps) + 1) % int(math.ceil(fps / ANIMATION_SPEED)) == 0:
            if self.img_idx < len(self.images) - 1:
                self.img_idx += 1
            else:
                self.img_idx = 0
            self.image = self.images[self.img_idx]


class Character(pygame.sprite.Sprite):
    def __init__(self, garden, position=None):
        pygame.sprite.Sprite.__init__(self)
        self.garden = garden
        if position is not None:
            self.position = position
        else:
            position = random_position([GRID_SIZE * (GARDEN_SIZE[0] - 1), GRID_SIZE * (GARDEN_SIZE[1] - 1)])
            print(self.garden.is_collision(position, self.garden.env_group))
            while self.garden.is_collision(position, self.garden.env_group):
                print(position)
                position = random_position([GARDEN_SIZE[0], GARDEN_SIZE[1]])
            self.position = position
        self.rect = pygame.Rect(int(float(position[0]) * GRID_SIZE), int(float(position[1]) * GRID_SIZE),
                                GRID_SIZE,
                                GRID_SIZE)
        self.inventory = {"flowers": 0}
        self.mode = STAND
        self.all_images = {}
        for name in os.listdir("../sprites/character/" + "/"):
            if name.endswith(".png"):
                for mode in CHAR_MODES:
                    if mode in name:
                        if mode not in self.all_images.keys():
                            self.all_images[mode] = []
                        self.all_images[mode].append(
                            pygame.transform.scale(
                                pygame.image.load("../sprites/character/" + name).convert_alpha(),
                                (GRID_SIZE, GRID_SIZE)))
        self.img_idx = 0
        self.image = self.all_images[CHAR_MODES[self.mode]][self.img_idx]

    def update(self, counter):
        if ((counter % fps) + 1) % int(math.ceil(float(fps) / float(ANIMATION_SPEED))) == 0:
            if self.img_idx < len(self.all_images[CHAR_MODES[self.mode]]) - 1:
                self.img_idx += 1
            else:
                self.img_idx = 0
            self.image = self.all_images[CHAR_MODES[self.mode]][self.img_idx]

        plant_collide = pygame.sprite.spritecollide(self, self.garden.plant_group, False)
        for plant in plant_collide:
            if plant.state == MATURE:
                plant.kill_flower()
                self.inventory["flowers"] += 1

    def process_keys(self, key_state):
        self.garden.temp_sprite = pygame.sprite.Sprite()
        x = self.position[0]
        y = self.position[1]

        if True not in key_state:
            if self.mode != STAND:
                self.change_mode(STAND)
        if key_state[DOWN] or key_state[UP]:
            if key_state[DOWN]:
                if self.mode != DOWN:
                    self.change_mode(DOWN)
                if key_state[LEFT] or key_state[RIGHT]:
                    temp = max(0, min(self.position[1] + MOVE_SIZE / 2, GRID_SIZE * (GARDEN_SIZE[1] - 1)))
                    if not self.garden.is_collision([x, temp], self.garden.env_group):
                        y = temp
                else:
                    temp = max(0, min(self.position[1] + MOVE_SIZE, GRID_SIZE * (GARDEN_SIZE[1] - 1)))
                    if not self.garden.is_collision([x, temp], self.garden.env_group):
                        y = temp

            if key_state[UP]:
                if self.mode != UP:
                    self.change_mode(UP)
                if key_state[LEFT] or key_state[RIGHT]:
                    temp = max(0, min(self.position[1] - MOVE_SIZE / 2, GRID_SIZE * (GARDEN_SIZE[1] - 1)))
                    if not self.garden.is_collision([x, temp], self.garden.env_group):
                        y = temp
                else:
                    temp = max(0, min(self.position[1] - MOVE_SIZE, GRID_SIZE * (GARDEN_SIZE[1] - 1)))
                    if not self.garden.is_collision([x, temp], self.garden.env_group):
                        y = temp

            if not (key_state[LEFT] and key_state[RIGHT]):
                if key_state[LEFT]:
                    temp = max(0, min(self.position[0] - MOVE_SIZE / 2, GRID_SIZE * (GARDEN_SIZE[0] - 1)))
                    if not self.garden.is_collision([temp, y], self.garden.env_group):
                        x = temp

                if key_state[RIGHT]:
                    temp = max(0, min(self.position[0] + MOVE_SIZE / 2, GRID_SIZE * (GARDEN_SIZE[0] - 1)))
                    if not self.garden.is_collision([temp, y], self.garden.env_group):
                        x = temp
        else:
            if key_state[LEFT] and key_state[RIGHT]:
                if self.mode != STAND:
                    self.change_mode(STAND)
            else:
                if key_state[LEFT]:
                    if self.mode != LEFT:
                        self.change_mode(LEFT)
                    temp = max(0, min(self.position[0] - MOVE_SIZE, GRID_SIZE * (GARDEN_SIZE[0] - 1)))
                    if not self.garden.is_collision([temp, y], self.garden.env_group):
                        x = temp
                if key_state[RIGHT]:
                    if self.mode != RIGHT:
                        self.change_mode(RIGHT)
                    temp = max(0, min(self.position[0] + MOVE_SIZE, GRID_SIZE * (GARDEN_SIZE[0] - 1)))
                    if not self.garden.is_collision([temp, y], self.garden.env_group):
                        x = temp

        self.position = [x, y]
        self.rect = pygame.Rect(int(x), int(y),
                                GRID_SIZE,
                                GRID_SIZE)

    def change_mode(self, mode):
        self.mode = mode
        self.image = self.all_images[CHAR_MODES[self.mode]][self.img_idx]
