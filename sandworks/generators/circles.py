from numpy import pi
from numpy import array
from numpy.random import random
from numpy.random import randint

from numpy import linspace
from numpy import arange
from numpy import column_stack
from numpy import cos
from numpy import sin

import cairocffi as cairo
from sand import Sand
from ..lib.sand_spline import SandSpline
from ..lib.helpers import hex_to_rgb_decimal, SimpleLinearScale, get_colors


def guide_iterator(x, y):
    while True:
        yield array([[x, y]])


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

    # Output PNG gamma
    gamma = 1.5

    # What frame to write out
    save_frame = args.save_every

    # TODO: Step.  Appears to be jitter multiplier for points along the spline
    # Causes the sand to be more "windswept" towards the later points
    step = 0.0000003 * 0.15

    # The number of points along the spline.  More points means a denser-looking spline.
    point_count = 1000

    # Convert colors to RGB decimal
    sand_color = hex_to_rgb_decimal(args.color)
    bg_color = hex_to_rgb_decimal(args.bg_color)

    # Set alpha
    sand_color.append(0.001)
    bg_color.append(1)

    sand = Sand(width, height)
    sand.set_rgba(sand_color)
    sand.set_bg(bg_color)

    splines = []
    edge = 0.08
    grid = 15
    leap_y = (1.0 - 2 * edge) / (grid - 1) * 0.5 * 0.75
    step = 0.0000001
    inum = 2000
    twopi = pi * 2.0

    splines = []
    for x in linspace(edge, 1.0-edge, grid):
        for y in linspace(edge, 1.0-edge, grid):
            guide = guide_iterator(x, y)
            pnum = randint(10, 150)

            a = random() * twopi + linspace(0, twopi, pnum)
            path = column_stack((cos(a), sin(a))) * leap_y

            scale = arange(pnum).astype('float') * step

            s = SandSpline(guide, path, inum, scale)
        splines.append(s)

    colors = get_colors('p1.png')
    nc = len(colors)

    while True:
        for s in splines:
            print(s)
