from numpy import pi
from numpy import array
from numpy import linspace
from numpy import arange
from numpy import zeros
from numpy import column_stack
from numpy import array
from time import time

from sand import Sand
from ..lib.sand_spline import SandSpline
from ..lib.helpers import hex_to_rgb_decimal, SimpleLinearScale


def guide_iterator(x, y):
    while True:
        yield array([[x, y]])


def generate(args):
    # Number of lines
    line_count = args.lines

    xscale = SimpleLinearScale(domain=array([0, args.width]), range=array([0, 1]))
    yscale = SimpleLinearScale(domain=array([0, args.height]), range=array([0, 1]))

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

    sand = Sand(args.width, args.height)
    sand.set_rgba(sand_color)
    sand.set_bg(bg_color)

    splines = []

    # For each y column
    for index, ypos in enumerate(linspace(margin_y, 1.0 - margin_y, line_count)):
        # TODO: 4?  Not sure what purpose this number serves.
        pnum = 4 + index
        guide = guide_iterator(0.5, ypos)

        x = linspace(-1, 1.0, pnum) * (1.0 - 2 * margin_x) * 0.5
        y = zeros(pnum, 'float')
        path = column_stack([x, y])
        scale = arange(pnum).astype('float') * step

        spline = SandSpline(guide, path, point_count, scale)
        splines.append(spline)

    j = 0
    while True:
        for s in splines:
            xy = next(s)
            sand.paint_dots(xy)
            if not j % (save_frame * line_count):
                frame_number = int(j / save_frame)
                print('Saving frame {}'.format(frame_number))
                sand.write_to_png('{}/{}-{}.png'.format(
                    args.out_dir,
                    int(time()),
                    frame_number),
                    gamma)
            j += 1
