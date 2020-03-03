"""
Twitter bot for random Tartan
"""
from io import BytesIO
import os
import re
import twitter
from PIL import Image, ImageDraw
from colour import Color

THREAD_DEF_EXPR = r'([A-Z]+)(\d+)'
THREAD_COUNT_EXPR= '({0} )*{0}$'.format(THREAD_DEF_EXPR)
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
    Reads a threadcount definition and returns it as a list of thread coulours
    """
    threads = []
    thread_def_matcher = re.compile(THREAD_DEF_EXPR)

    for thread_def in thread_def_matcher.findall(thread_count):
        for i in range(int(thread_def[1])):
            threads.append(COLOURS[thread_def[0]])
    return threads


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
    warp = Image.new('RGBA', size)
    warp_draw = ImageDraw.Draw(warp)
    weft = Image.new('RGBA', size)
    weft_draw = ImageDraw.Draw(weft)
    total_threads = len(threads)
    for index in range(512):
        warp_draw.line((index, 0, index, 512), fill=threads[index % total_threads])
        weft_draw.line((0, index, 512, index), fill=threads[index % total_threads])

    warp.paste(weft, mask=create_alternating_mask(size))
    return warp


def threadcount_to_png(threadcount):
    return draw_weave(parse_threadcount(threadcount), (512, 512))


def login():
    return twitter.Api(consumer_key=os.environ.get('KEY'),
                  consumer_secret=os.environ.get('SECRET'),
                  access_token_key=os.environ.get('TOKEN'),
                  access_token_secret=os.environ.get('TOKEN_SECRET'))

    # auth = tweepy.OAuthHandler(os.environ.get('KEY'), os.environ.get('SECRET'))
    # auth.set_access_token(os.environ.get('TOKEN'), os.environ.get('TOKEN_SECRET'))
    # return tweepy.API(auth)

class MediaFile(BytesIO):
    mode='rb'
    name='tartan.png'

def tweet_image(api, threadcount, image, tweet_id):
    buffered = MediaFile()
    image.save(buffered, format="PNG")
    api.PostUpdate(
        media=buffered,
        status=threadcount,
        in_reply_to_status_id=tweet_id,
        trim_user=True
    )



def tweet_last_random():
    api = login()
    tweet_id, threadcount = last_random_tartan(api)
    if ('http' in threadcount):
        return
    tweet_image(api, threadcount, threadcount_to_png(threadcount), tweet_id)


def last_random_tartan(api):
    tweet = api.GetUserTimeline(screen_name='RandomTartan', count=5)[2]
    return tweet.id, tweet.text

if __name__ == '__main__':
    tweet_last_random()
