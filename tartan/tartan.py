"""
Draw tartans from their thread count definitions
"""
import itertools
import re
from PIL import Image, ImageDraw


THREAD_DEF_EXPR = r'([A-Z]+)/?(\d+)'
THREAD_COUNT_EXPR = '({0} )*{0}$'.format(THREAD_DEF_EXPR)
COLOURS = {
    "LR": ["#EC34C4", "Light red"],
    "R": ["#DC0000", "Red"],
    "DR": ["#960000", "Dark red"],
    "O": ["#EC8048", "Orange"],
    "DO": ["#B84C00", "Dark orange"],
    "LY": ["#F9F5C8", "Light yellow"],
    "Y": ["#FFFF00", "Yellow"],
    "DY": ["#BC8C00", "Dark yellow"],
    "LG": ["#86C67C", "Light green"],
    "G": ["#008B00", "Green"],
    "DG": ["#004028", "Dark green"],
    "LB": ["#82CFFD", "Light blue"],
    "B": ["#0000FF", "Blue"],
    "DB": ["#000080", "Dark blue"],
    "LP": ["#C49CD8", "Light purple"],
    "P": ["#AA00FF", "Purple"],
    "DP": ["#440044", "Deep Purple"],
    "W": ["#FFFFFF", "White"],
    "LN": ["#E0E0E0", "Light grey"],
    "N": ["#C8C8C8", "Grey"],
    "DN": ["#5C5C5C", "Dark grey"],
    "K": ["#101010", "Black"],
    "LT": ["#A08858", "Light brown"],
    "T": ["#98481C", "Brown"],
    "DT": ["#4C3428", "Dark brown"]
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
    stripe_def_matcher = re.compile(THREAD_DEF_EXPR)

    thread_count = unroll_reflection(thread_count)
    return list(itertools.chain.from_iterable(
        stripe_def_to_list(stripe_def[0], stripe_def[1]) for stripe_def in stripe_def_matcher.findall(thread_count)
    ))


def stripe_def_to_list(colour_code, threads):
    """
    Turns a stripe definition into a list of threads.

    The list consists of n strings of the requested colour.
    >>> stripe_def_to_list('DR', '5')
    ['#960000', '#960000', '#960000', '#960000', '#960000']
    """
    return [COLOURS[colour_code][0]] * int(threads)

def unroll_reflection(thread_count):
    """
    If a threadcount is a symmetrical, as signified by the /, "unroll" it by reversing the
    non-terminal stripes:

    >>> unroll_reflection('B/1 LB1 Y/1')
    'B/1 LB1 Y/1 LB1'

    NOOP if not symmetrical
    >>> unroll_reflection('B1 LB1 Y1')
    'B1 LB1 Y1'
    """
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
    warp, weft, mask = _initialise_images(size)
    warp_draw = ImageDraw.Draw(warp)
    weft_draw = ImageDraw.Draw(weft)
    total_threads = len(threads)
    for index in range(size[0]):
        warp_draw.line((index, 0, index, size[1]), fill=threads[index % total_threads])
    for index in range(size[1]):
        weft_draw.line((0, index, size[0], index), fill=threads[index % total_threads])

    warp.paste(weft, mask=mask)
    return warp


def _initialise_images(size):
    """
    It takes three same-sized images to make a tartan.
    1. The warp stripes
    2. The weft stripes
    3. The mask that makes the weft appear to go "behind" the warp
    """
    return Image.new('RGBA', size), Image.new('RGBA', size), create_alternating_mask(size)


def threadcount_to_image(threadcount, size):
    """
    Turns a threadcount definition into a PIL Image of the given size.
    """
    return draw_weave(parse_threadcount(threadcount), size)
