import math
from random import randint


def random_position(limits, center=None, radius=None):
    if center is None:
        center = [round(limits[0] / 2), round(limits[1] / 2)]
        radius = [math.floor(limits[0] / 2), math.floor(limits[1] / 2)]
    x = max(0, min(center[0] + randint(-radius[0], radius[0]), limits[0] - 1))
    y = max(0, min(center[1] + randint(-radius[1], radius[1]), limits[1] - 1))
    return [x, y]
