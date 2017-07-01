from numpy import pi
from numpy import array
from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack

from sand import Sand
from ..lib.color import hex_to_rgb_decimal


def generate(args):
    # Number of lines
    line_count = args.lines

    # Margin as a percent of total canvas size
    margin = 0.05

    # Convert colors to RGB decimal
    sand_color = hex_to_rgb_decimal(args.color)
    bg_color = hex_to_rgb_decimal(args.bg_color)

    # Set alpha
    sand_color.append(0.1)
    bg_color.append(1)

    sand = Sand(args.size)
    sand.set_rgba(sand_color)
    sand.set_bg(bg_color)

    for index, ypos in enumerate(linspace(margin, 1.0 - margin, line_count)):
        print(index, ypos)
