from numpy import pi
from numpy import array
from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack

from sand import Sand


class Generator:
    def __init__(self, args):
        count = args.count
        sand = Sand(SIZE)
        sand.set_bg(BG)
        sand.set_rgba(FRONT)
