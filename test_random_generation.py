import pygame
from scipy import interpolate
from scipy.spatial import distance
import numpy as np
import time
from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm
import settings

INTERPOLATION_POINTS = 500
MIN_DISTANCE = 30

def get_angle(u, v):
    return dot(u, v) / norm(u) / norm(v)

class PathMaker:
    def generate_random_point(self):
        x_min, y_min, x_max, y_max = self.rect
        x = np.random.randint(x_min, x_max)
        y = np.random.randint(y_min, y_max)
        return x, y

    def start_array(self):
        return [self.generate_random_point() for _ in range(20)]


    def update_array(self):
        self.ControlPoints.pop(0)
        np = self.generate_random_point()
        last_v = (self.ControlPoints[-1][0] - self.ControlPoints[-2][0],
                  self.ControlPoints[-1][1] - self.ControlPoints[-2][1])
        angle = get_angle((np[0] - self.ControlPoints[-1][0], np[1] - self.ControlPoints[-1][1]), last_v)
        while distance.euclidean(self.ControlPoints[-1], np) < MIN_DISTANCE and 0.1 < angle and angle < 1:
            np = self.generate_random_point()
            angle = get_angle((np[0] - self.ControlPoints[-1][0], np[1] - self.ControlPoints[-1][1]), last_v)
        self.ControlPoints.append(np)

    def B_spline(self, waypoints):
        x = []
        y = []
        for point in waypoints:
            x.append(point[0])
            y.append(point[1])
        tck, u, *rest = interpolate.splprep([x, y])
        point_cnt = int((u[len(u) // 2 - 1] - u[len(u) // 2 - 2]) * settings.INTERPOLATION_POINTS)
        u = np.linspace(u[len(u) // 2 - 2], u[len(u) // 2 - 1], num=point_cnt)
        smooth = interpolate.splev(u, tck)
        return smooth

    def __init__(self, rect):
        self.rect = rect
        self.ControlPoints = self.start_array()

    def get_path(self):
        smooth = self.B_spline(self.ControlPoints)
        self.update_array()
        return smooth


def generate_random_point(rect):
    x_min, y_min, x_max, y_max = rect
    x = np.random.randint(x_min, x_max)
    y = np.random.randint(y_min, y_max)
    return x, y


def start_array(rect):
    return [generate_random_point(rect) for _ in range(20)]


def update_array(arr, rect):
    arr.pop(0)
    np = generate_random_point(rect)
    last_v = (arr[-1][0]-arr[-2][0], arr[-1][1]-arr[-2][1])
    angle = get_angle((np[0]-arr[-1][0], np[1]-arr[-1][1]), last_v)
    while distance.euclidean(arr[-1], np) < MIN_DISTANCE and 0.1 < angle and angle < 1:
        np = generate_random_point(rect)
        angle = get_angle((np[0] - arr[-1][0], np[1] - arr[-1][1]), last_v)
    arr.append(np)


X_history = []
Y_history = []
T_history = []
pygame.init()
pygame.display.set_caption("RRT path planning")
map = pygame.display.set_mode((800,800))
map.fill((255, 255, 255))
running = True
rect = (100, 300, 700, 500)
#ControlPoints = start_array(rect)
pathmaker = PathMaker((100,100, 600, 600))

while(running):
    #smooth = B_spline(ControlPoints)
    X_smooth, Y_smooth = path = pathmaker.get_path()
    #"""
    X_history += X_smooth.tolist()
    Y_history += Y_smooth.tolist()
    #T_history.append(ControlPoints[len(ControlPoints)//2-1])
    #update_array(ControlPoints, rect)
    map.fill((255, 255, 255))
    for x, y in zip(X_history, Y_history):
        pygame.draw.circle(map, (255, 0, 0), (x, y), 2, 0)
    #for point in T_history:
    #    pygame.draw.circle(map, (0, 0, 0), point, 7, 0)
    pygame.display.update()
    time.sleep(0.1)
    #"""

