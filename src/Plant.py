from random import randint
from src.Garden import *
import names

class Plant:
    def __init__(self, garden, position, id, parent=None):
        self.garden = garden
        self.id = id
        self.name = names.get_first_name()
        if parent:
            self.parent = parent
        else:
            self.parent = None
        self.position = position
        self.children = []
        self.ready = False
        self.age = 0.0
        self.age_max = 40
        self.age_rate = 2
        self.spawn_ages = [10, 16, 20]
        self.spawn_r = 3
        self.alive = True

    def age_plant(self):
        if self.age != self.age_max:
            self.age += self.age_rate
        else:
            self.alive = False

    def tick(self):
        self.age_plant()
        if self.age in self.spawn_ages:
            self.ready = True

    def spawn(self):
        if self.ready:
            self.ready = False
            x = max(0, min(self.position[0]+randint(-self.spawn_r, self.spawn_r), self.garden.grid_size[0]-1))
            y = max(0, min(self.position[1]+randint(-self.spawn_r, self.spawn_r), self.garden.grid_size[1]-1))

            if self.garden.can_plant([x, y]):
                child = Plant(self.garden, [x, y], len(self.garden.plants), self)
                self.children.append(child)
                print("New child plant spawned! Number of children:" + str(len(self.children)))
                return child
        return None




