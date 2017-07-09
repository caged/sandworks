import numpy.random
from numpy import pi
from numpy import array
from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack
from numpy.random import random
from numpy.random import standard_exponential, standard_cauchy, standard_normal
from numpy.random import randint

from sand import Sand
from ..lib.helpers import hex_to_rgb_decimal


def generate(args):
    count = args.count

    # Convert colors to RGB decimal
    sand_color = hex_to_rgb_decimal(args.color)
    bg_color = hex_to_rgb_decimal(args.bg_color)

    # Set alpha
    sand_color.append(0.1)
    bg_color.append(1)

    distributions = [
        'random',
        'standard_exponential',
        'standard_cauchy',
        'standard_normal'
    ]

    group_a = [
        'paint_strokes'
    ]

    group_b = [
        'paint_filled_circles',
        'paint_circles'
    ]

    group_c = [
        'paint_dots'
    ]

    group_d = [
        'paint_triangles'
    ]

    for group in group_a:
        for distribution in distributions:
            print('Generating {} with {} distribution'.format(group, distribution))

            sand = Sand(args.width, args.height)
            sand.set_bg(bg_color)
            sand.set_rgba(sand_color)

            method = getattr(numpy.random, distribution)
            aa = method((count, 2))
            bb = method((count, 2))
            cc = randint(0, 500, size=count)
            getattr(sand, group)(aa, bb, cc)
            sand.write_to_png('tmp/{}-{}.png'.format(group, distribution))

    for group in group_b:
        for distribution in distributions:
            print('Generating {} with {} distribution'.format(group, distribution))

            sand = Sand(args.width, args.height)
            sand.set_bg(bg_color)
            sand.set_rgba(sand_color)

            method = getattr(numpy.random, distribution)
            aa = method((count, 2))
            bb = method(count)
            cc = randint(0, 250, size=count)
            getattr(sand, group)(aa, bb, cc)
            sand.write_to_png('tmp/{}-{}.png'.format(group, distribution))

    for group in group_c:
        for distribution in distributions:
            print('Generating {} with {} distribution'.format(group, distribution))

            sand = Sand(args.width, args.height)
            sand.set_bg(bg_color)
            sand.set_rgba(sand_color)

            method = getattr(numpy.random, distribution)
            aa = method((count * 100, 2))
            getattr(sand, group)(aa)
            sand.write_to_png('tmp/{}-{}.png'.format(group, distribution))

    for group in group_d:
        for distribution in distributions:
            print('Generating {} with {} distribution'.format(group, distribution))

            sand = Sand(args.width, args.height)
            sand.set_bg(bg_color)
            sand.set_rgba(sand_color)

            method = getattr(numpy.random, distribution)
            aa = method((count, 2))
            bb = method((count, 2))
            cc = method((count, 2))
            dd = randint(0, 500, size=count)
            getattr(sand, group)(aa, bb, cc, dd)
            sand.write_to_png('tmp/{}-{}.png'.format(group, distribution))
