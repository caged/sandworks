from time import time

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
from ..lib.helpers import hex_to_rgb_decimal, SimpleLinearScale, get_colors, _rnd_interpolate


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
    sand_color.append(0.1)
    bg_color.append(1)

    sand = Sand(width, height)
    sand.set_rgba(sand_color)
    sand.set_bg(bg_color)

    for i in range(0, 100):
        num_points = 1500
        angle = random() * (pi * 2) + linspace(0, (pi * 2), num_points)
        points = column_stack((cos(angle), sin(angle))) * (1.0 * random() * 0.4)
        path = array([[0.5, 0.5]]) + _rnd_interpolate(points, 1000, ordered=True)

        sand.paint_dots(path)

    file_name = '{}/{}.png'.format(
        args.out_dir,
        int(time()))

    sand.write_to_png(file_name)
