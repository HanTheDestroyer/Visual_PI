import pygame as pg
import numpy as np
import sys
from pi_generator import *
import time


SCREEN_SIZE = [1280, 1280]
RADIUS = 600
ANGLE_INCREMENT = 0.00005
NUMBER_OF_DIGITS = 1000000

COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42)
}


COLORS = list(COLORS.values())


class Simulator:
    def __init__(self, slices):
        pg.init()
        self.clock = pg.time.Clock()
        self.screen = pg.display.set_mode(np.array(SCREEN_SIZE, dtype='int16'))
        self.screen.fill(pg.Color('black'))
        self.center = pg.Rect(540, 540, RADIUS * 2, RADIUS * 2)
        self.center.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[0]/2)
        self.increment = np.pi / 5
        self.screen.fill(pg.Color('black'))
        self.pi = digits_of_pi[0:NUMBER_OF_DIGITS]
        self.slices = slices
        self.pi_image = pg.image.load('pi.png')
        self.pi_rect = self.pi_image.get_rect()
        self.pi_rect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[0]/2)

        # Draw Initial Scene
        pg.draw.circle(self.screen, color=[255, 255, 255],
                       center=[SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2], radius=RADIUS/4, width=5)

        starting_angle = 0

        for i in range(10):
            pg.draw.arc(self.screen, color=COLORS[i], rect=self.center, start_angle=starting_angle,
                        stop_angle=starting_angle + self.increment, width=3)
            starting_angle += self.increment
        time.sleep(5)
        self.draw()



    def draw(self):
        while True:
            for i in np.arange(len(self.pi)-2):
                point1 = self.slices[self.pi[i]].get_point()
                point2 = self.slices[self.pi[i+1]].get_point()
                pg.draw.line(self.screen, color=COLORS[self.pi[i]], start_pos=point1, end_pos=point2, width=1)
                pg.draw.circle(self.screen, color=[0, 0, 0],
                               center=[SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2], radius=RADIUS / 3.8)

                self.screen.blit(self.pi_image, self.pi_rect)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        sys.exit()
                pg.display.update()
                print(i)
                self.clock.tick()
            time.sleep(10)
            break


class Slice:
    def __init__(self, slice_number):
        self.value = slice_number
        self.angles = np.arange(slice_number * np.pi / 5, (slice_number+1) * np.pi / 5, ANGLE_INCREMENT)
        self.points = np.zeros([len(self.angles), 2], dtype=float)
        self.counter = -1
        for i in range(len(self.points)):
            self.points[i][0] = (RADIUS + 5) * np.cos(self.angles[i]) + SCREEN_SIZE[0] / 2
            self.points[i][1] = (RADIUS + 5) * np.sin(self.angles[i]) + SCREEN_SIZE[0] / 2

    def get_point(self):
        self.counter += 1
        if self.counter > (np.pi/5) / ANGLE_INCREMENT:
            self.counter = 0
        return self.points[self.counter]


if __name__ == '__main__':
    pies = []
    for c in range(10):
        pies.append(Slice(c))
    simulator = Simulator(pies)
