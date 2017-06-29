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


class Generator:
    def __init__(self, args):
        count = 10000
        sand = Sand(args.size)
        sand.set_bg([1, 1, 1, 1])
        sand.set_rgba([
            189 / 255,
            67 / 255,
            67 / 255,
            0.2
        ])

        aa = random((count, 2))
        bb = random((count, 2))
        cc = randint(0, 200, size=count)
        sand.paint_strokes(aa, bb, cc)
        sand.write_to_png('./strokes-random.png')

        aa = standard_exponential((count, 2))
        bb = standard_exponential((count, 2))
        cc = randint(0, 200, size=count)
        sand.paint_strokes(aa, bb, cc)
        sand.write_to_png('./strokes-exponential.png')

        aa = standard_cauchy((count, 2))
        bb = standard_cauchy((count, 2))
        cc = randint(0, 200, size=count)
        sand.paint_strokes(aa, bb, cc)
        sand.write_to_png('./strokes-cauchy.png')

        aa = standard_normal((count, 2))
        bb = standard_normal((count, 2))
        cc = randint(0, 200, size=count)
        sand.paint_strokes(aa, bb, cc)
        sand.write_to_png('./strokes-normal.png')
