from numpy import pi
from numpy import array
from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import empty
from numpy import column_stack
from numpy import array
from numpy.random import random
from numpy.random import randint
from numpy.random import uniform
from numpy import cos
from numpy import sin
from time import time
from math import radians

import cairocffi as cairo
from sand import Sand
from ..lib.sand_spline import SandSpline
from ..lib.helpers import hex_to_rgb_decimal, SimpleLinearScale


WIDTH = 1000
HEIGHT = 1000


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
        global cgrid
        px = 0
        py = 0
        timeout = 0
        found = False

        while not found:
            px = randint(self.w)
            py = randint(self.h)
            # print(cgrid[py * self.w + px], cgrid[py * self.w + px] < 10000, timeout)
            if(cgrid[py * self.w + px] < 10000):
                found = True

        if found:
            a = cgrid[py * self.w + px]
            if randint(100) < 50:
                a -= 90 + int(uniform(-2, 2.1))
            else:
                a += 90 + int(uniform(-2, 2.1))
            self.start_crack(px, py, a)

    def start_crack(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        self.x += 0.61 * cos(t * pi / 180)
        self.y += 0.61 * sin(t * pi / 180)

    def move(self):
        global cgrid

        px = self.x
        py = self.y
        self.x += 0.42 * cos(self.t * pi / 180)
        self.y += 0.42 * sin(self.t * pi / 180)

        z = 0.33
        cx = int(self.x + uniform(-z, z))
        cy = int(self.y + uniform(-z, z))

        # dots = random((1, 2))
        dots = array([[
            self.xs(self.x),
            self.ys(self.y)
        ]])
        self.sand.paint_dots(dots)

        if cx >= 0 and cx < self.w and cy >= 0 and cy < self.h:
            if cgrid[cy * self.w + cx] > 10000 or abs(cgrid[cy * self.w + cx] - self.t) < 5:
                cgrid[cy * self.w + cx] = int(self.t)
            elif abs(cgrid[cy * self.w + cx] - self.t) > 2:
                self.find_start()
                make_crack(sand=self.sand)
        else:
            self.find_start()
            make_crack(sand=self.sand)


num = 0
maxnum = 200
cracks = empty(maxnum, dtype=Crack)
cgrid = zeros(WIDTH * HEIGHT)


def make_crack(sand):
    global num
    global maxnum
    global cracks

    if num < maxnum:
        cracks[num] = Crack(sand=sand)
        num += 1


def generate(args):
    global cgrid
    width = WIDTH
    height = HEIGHT

    xscale = SimpleLinearScale(domain=array([0, width]), range=array([0, 1]))
    yscale = SimpleLinearScale(domain=array([0, height]), range=array([0, 1]))

    # Margin as a pixel value of total size.  Convert that margin to a number between 0..1
    # representing the percentage of total pixel size
    margin = args.margin
    margin_x = xscale(margin)
    margin_y = yscale(margin)

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
        make_crack(sand)

    i = 0
    try:
        while True:
            for n in range(num):
                cracks[n].move()

            if i % 1000 == 0:
                sand.write_to_png('tmp/c-{}.png'.format(i))
            i += 1

    except KeyboardInterrupt:
        print('Finished!')
        sand.write_to_png('tmp/c-{}.png'.format(i))
