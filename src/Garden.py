from src.Plant import *
from time import time
import numpy as np
from random import randint

ROCK = 0
WATER = 1

ENV_ELEMS = {
    "Rock" : ROCK,
    "Water" : WATER
}

class Garden:
    def __init__(self, size=[10,10], n_elems=10):
        self.grid_size = size
        self.env_elems = []
        self.env_grid = self.create_environment(n_elems)

        self.plants = []
        self.plant_grid = [[None for i in range(0,size[1])] for j in range(0,size[0])]
        position = self.random_position()
        while not self.is_free(self.env_grid, position):
            position = self.random_position()
        p = Plant(self, position, 0)
        self.plant_grid[p.position[0]][p.position[1]] = p
        self.plants.append(p)
        print("Creating new garden")

    def create_environment(self, n_elems):
        environment = [[None for i in range(0, self.grid_size[1])] for j in range(0, self.grid_size[0])]
        for i in range(0, n_elems):
            position = self.random_position()
            if self.is_free(environment, position):
                elem_type = randint(0, len(ENV_ELEMS))
                elem = GardenElem(position, elem_type)
                environment[position[0]][position[1]] = elem
                self.env_elems.append(elem)
        return environment

    def tick(self):
        for p in self.plants:
            p.tick()
            if p.ready:
                child = p.spawn()
                if child:
                    self.add_plant(child)

    def add_plant(self, p):
        self.plants.append(p)
        self.plant_grid[p.position[0]][p.position[1]] = p

        print("Garden currently has " + str(len(self.plants)) + " plants")


    def is_free(self, grid, position):
        if grid[position[0]][position[1]] is not None:
            return False
        return True

    def can_plant(self, position):
        if self.is_free(self.plant_grid, position) and self.is_free(self.env_grid, position):
            return True
        return False

    def random_position(self):
        x = randint(0, self.grid_size[0]-1)
        y = randint(0, self.grid_size[1]-1)
        return [x, y]

class GardenElem:
    def __init__(self, position, elem_type):
        self.elem_type = elem_type
        self.position = position
        self.size = 15



