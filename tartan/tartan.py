"""
Draw tartans from their thread count definitions
"""
import re
from PIL import Image, ImageDraw


THREAD_DEF_EXPR = r'([A-Z]+)/?(\d+)'
THREAD_COUNT_EXPR = '({0} )*{0}$'.format(THREAD_DEF_EXPR)
COLOURS = {
    "LR": "#EC34C4",
    "R": "#DC0000",
    "DR": "#960000",
    "O": "#EC8048",
    "DO": "#B84C00",
    "LY": "#F9F5C8",
    "Y": "#FFFF00",
    "DY": "#BC8C00",
    "LG": "#86C67C",
    "G": "#008B00",
    "DG": "#004028",
    "LB": "#82CFFD",
    "B": "#0000FF",
    "DB": "#000080",
    "LP": "#C49CD8",
    "P": "#AA00FF",
    "DP": "#440044",
    "W": "#FFFFFF",
    "LN": "#E0E0E0",
    "N": "#C8C8C8",
    "DN": "#5C5C5C",
    "K": "#101010",
    "LT": "#A08858",
    "T": "#98481C",
    "DT": "#4C3428"
}


def parse_threadcount(thread_count):
    """
    Reads a threadcount definition and returns it as a list of thread colours

    A threadcount definition is a space-separated list of strips:
    >>> parse_threadcount('K1 T1')
    ['#101010', '#98481C']

    Each strip consists of a colour code from COLOURS, and a number of threads.
    This function translates that into a list of individual threads of each
    colour.
    >>> parse_threadcount('K2 T3')
    ['#101010', '#101010', '#98481C', '#98481C', '#98481C']
    """
    threads = []
    thread_def_matcher = re.compile(THREAD_DEF_EXPR)

    thread_count = unroll_reflection(thread_count)

    for thread_def in thread_def_matcher.findall(thread_count):
        threads.extend([COLOURS[thread_def[0]]] * int(thread_def[1]))
    return threads


def unroll_reflection(thread_count):
    if '/' in thread_count:
        blocks = thread_count.split(' ')
        return ' '.join(blocks + blocks[-2:0:-1])
    return thread_count


def create_alternating_mask(size):
    """
    Creates a mask to be used in compositing the warp and weft images into
    one woven image.

    The mask returned is a binary mode image of black and white checkerboard,
    with each check being 1 pixel.

    size is a 2-tuple representing width and height (as used in PIL)
    """
    width, height = size
    mask = Image.new('1', size)
    if width % 2:
        # When the width is an odd number, simply alternating between 1 and 0
        # produces an alternating grid - e.g. for 3: 0,1,0  1,0,1
        mask_data = [0, 1] * (width//2) * height
    else:
        # When the width is an even number, the rows direction of the rows must also alternate
        # produces an alternating grid - e.g. for 4: 0,1,0,1  1,0,1,0
        mask_data = ([0, 1] * (width // 2) + [1, 0] * (width // 2)) * (height // 2)
    mask.putdata(mask_data)
    return mask


def draw_weave(threads, size):
    """
    Given a list of thread colours, produce an image representing those threads woven as tartan
    i.e. an even weave with an identical sequence of threads in both warp and weft
    """
    warp, weft, mask = initialise_images(size)
    warp_draw = ImageDraw.Draw(warp)
    weft_draw = ImageDraw.Draw(weft)
    total_threads = len(threads)
    for index in range(size[0]):
        warp_draw.line((index, 0, index, size[1]), fill=threads[index % total_threads])
    for index in range(size[1]):
        weft_draw.line((0, index, size[0], index), fill=threads[index % total_threads])

    warp.paste(weft, mask=mask)
    return warp


def initialise_images(size):
    return Image.new('RGBA', size), Image.new('RGBA', size), create_alternating_mask(size)


def threadcount_to_image(threadcount, size):
    return draw_weave(parse_threadcount(threadcount), size)
