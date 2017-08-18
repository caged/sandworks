from numpy import pi
from numpy import array
from numpy import arange
from numpy import zeros
from numpy import empty
from numpy import array
from numpy.random import randint
from numpy.random import uniform
from numpy.random import shuffle
from numpy.random import choice
from numpy import cos
from numpy import sin
from functools import lru_cache
import os

from sand import Sand
from ..lib.helpers import hex_to_rgb_decimal, SimpleLinearScale, get_colors


DPI = 300
WIDTH = int(os.environ.get('WIDTH', 5)) * DPI
HEIGHT = int(os.environ.get('HEIGHT', 5)) * DPI


@lru_cache(maxsize=1)
def image_colors(img):
    return get_colors(img)


class SandPainter:
    def __init__(self, sand, xs, ys, colors):
        self.sand = sand
        self.xs = xs
        self.ys = ys
        self.g = uniform(0.01, 0.1)
        self.grains = 75
        self.colors = colors
        self.color = colors[choice(len(colors))]

    def render(self, x, y, ox, oy):
        max_g = 1.0
        self.g += uniform(-0.050, 0.050)
        self.g = 0 if self.g < 0 else self.g
        self.y = max_g if self.g > max_g else self.g

        w = self.g / (self.grains - 1)
        for i in range(self.grains):
            a = 0.1 - i / (self.grains * 10.0)
            self.sand.set_rgba(self.color + [a])
            dots = array([[
                self.xs(ox + (x - ox) * sin(sin(i * w))),
                self.ys(oy + (y - oy) * sin(sin(i * w)))
            ]])
            self.sand.paint_dots(dots)


class Crack:

    def __init__(self, sand, colors):
        self.x = 0  # X position on grid
        self.y = 0  # Y position on grid
        self.t = 0  # Direction of travel
        self.w = WIDTH
        self.h = HEIGHT
        self.g = uniform(0.01, 0.1)
        self.grains = 64

        self.xs = SimpleLinearScale(domain=array([0, self.w]), range=array([0, 1]))
        self.ys = SimpleLinearScale(domain=array([0, self.h]), range=array([0, 1]))

        self.painter = SandPainter(
            sand=sand,
            xs=self.xs,
            ys=self.ys,
            colors=colors)

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

        self.region_color()

        dots = array([[
            self.xs(self.x + uniform(-z, z)),
            self.ys(self.y + uniform(-z, z))
        ]])

        self.painter.sand.set_rgba([50 / 255, 50 / 255, 50 / 255, 0.3])
        self.painter.sand.paint_dots(dots)

        if cx >= 0 and cx < self.w and cy >= 0 and cy < self.h:
            if cgrid[cy * self.w + cx] > 10000 or abs(cgrid[cy * self.w + cx] - self.t) < 5:
                cgrid[cy * self.w + cx] = int(self.t)
            elif abs(cgrid[cy * self.w + cx] - self.t) > 2:
                self.find_start()
                make_crack(sand=self.painter.sand, colors=self.painter.colors)
        else:
            self.find_start()
            make_crack(sand=self.painter.sand, colors=self.painter.colors)

    def region_color(self):
        global cgrid
        rx = self.x
        ry = self.y
        openspace = True

        while openspace:
            rx += 0.81 * sin(self.t * pi / 180)
            ry -= 0.81 * cos(self.t * pi / 180)
            cx = int(rx)
            cy = int(ry)

            if cx >= 0 and cx < self.w and cy >= 0 and cy < self.h:
                if not cgrid[cy * self.w + cx] > 10000:
                    openspace = False
            else:
                openspace = False

        self.painter.render(rx, ry, self.x, self.y)


num = 0
maxnum = 200
cracks = empty(maxnum, dtype=Crack)
cgrid = zeros(WIDTH * HEIGHT)


def make_crack(sand, colors):
    global num
    global maxnum
    global cracks

    if num < maxnum:
        cracks[num] = Crack(sand=sand, colors=colors)
        num += 1


def generate(args):
    global cgrid

    width = WIDTH
    height = HEIGHT

    # What frame to write out
    save_frame = args.save_every
    frame_prefix = args.frame_prefix
    exit_frame = args.exit_frame

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

    if args.color_from_image:
        colors = get_colors(args.color_from_image)
    else:
        colors = [hex_to_rgb_decimal(args.color)]

    # TODO: move to initialization of cgrid
    for y in range(HEIGHT):
        for x in range(WIDTH):
            cgrid[y * WIDTH + x] = 10001

    for k in range(16):
        i = randint(WIDTH * HEIGHT - 1)
        cgrid[i] = randint(360)

    for k in range(3):
        make_crack(sand, colors=colors)

    i = 0
    try:
        while True:
            for n in range(num):
                cracks[n].move()

            if i % save_frame == 0 and i is not 0:
                sand.write_to_png('{}/{}-{}.png'.format(
                    args.out_dir,
                    frame_prefix,
                    int(i / save_frame)))
            i += 1

            if exit_frame and (i / save_frame) > exit_frame:
                sand.write_to_png('{}/{}-0.png'.format(
                    args.out_dir,
                    frame_prefix))

                return False

    except KeyboardInterrupt:
        print('Finished!')
        sand.write_to_png('tmp/{}-0.png'.format(frame_prefix))
