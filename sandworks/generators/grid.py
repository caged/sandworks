from numpy import pi
from numpy import array
from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack
from numpy import array
from numpy.random import random
from numpy.random import randint
from time import time
from math import radians

import cairocffi as cairo
from sand import Sand
from ..lib.sand_spline import SandSpline
from ..lib.helpers import hex_to_rgb_decimal, SimpleLinearScale


WIDTH = 900
HEIGHT = 900

cgrid = zeros(WIDTH * HEIGHT)


class Crack:

    def __init__(self, sand):
        self.x = 0  # X position on grid
        self.y = 0  # Y position on grid
        self.t = 0  # Direction of travel
        self.w = WIDTH
        self.h = WIDTH
        self.xs = SimpleLinearScale(domain=array([0, self.w]), range=array([0, 1]))
        self.ys = SimpleLinearScale(domain=array([0, self.h]), range=array([0, 1]))

        self.sand = sand
        self.find_start()

    def find_start(self):
        px = 0
        py = 0
        timeout = 0
        found = False

        while not found or timeout > 1000:
            timeout += 1
            px = randint(self.w)
            py = randint(self.h)

            if(self.grid[py * self.x + px] < 10000):
                found = True

        if found:
            print('FOUND!')


def generate(args):

    width = args.width
    height = args.height

    xscale = SimpleLinearScale(domain=array([0, width]), range=array([0, 1]))
    yscale = SimpleLinearScale(domain=array([0, height]), range=array([0, 1]))

    # Margin as a pixel value of total size.  Convert that margin to a number between 0..1
    # representing the percentage of total pixel size
    margin = args.margin
    margin_x = xscale(margin)
    margin_y = yscale(margin)

    # The current number of cracks
    num = 0
    max_cracks = 200
    cracks = empty(max_cracks, dtype=Crack)

    # Output PNG gamma
    gamma = 1.5

    # What frame to write out
    save_frame = args.save_every

    # The number of points along the spline.  More points means a denser-looking spline.
    stroke_limit = 100

    # Convert colors to RGB decimal
    sand_color = hex_to_rgb_decimal(args.color)
    bg_color = hex_to_rgb_decimal(args.bg_color)

    # Set alpha
    sand_color.append(0.1)
    bg_color.append(1)

    sand = Sand(width, height)
    sand.set_rgba(sand_color)
    sand.set_bg(bg_color)

    splines = []

    # TODO: move to initialization of cgrid
    for y in range(HEIGHT):
        for x in range(WIDTH):
            cgrid[y * WIDTH + x] = 10001

    for k in range(16):
        i = randint(WIDTH * HEIGHT - 1)
        cgrid[i] = randint(360)

    for k in range(3):
        cracks[num] = Crack(sand=sand)
        num += 1

    # c = Crack()
    i = 0
    try:
        while True:
            for n in range(num):
                cracks[n].move()
            # for crack in cracks:
            #     crack.move()
            #
            if i % 100000 == 0:
                sand.write_to_png('tmp/c-{}.png'.format(i))
            i += 1
            # if i % 50000 == 0:
            #     c.sand.write_to_png('tmp/c-{}.png'.format(i))
            # c.move()
            # i += 1
    except KeyboardInterrupt:
        print('Finished!')
