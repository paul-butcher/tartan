"""Console script for tartan."""
import argparse
import sys
from tartan.tartan import threadcount_to_image, COLOURS

def main():
    """Console script for tartan."""
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'threadcount',
        help='A space-separated list of stripe values e.g. DB2 W4 P10, use "/" to make symmetrical, e.g. DB/2 W4 P/10'
    )
    parser.add_argument('--width', default=512, type=int)
    parser.add_argument('--height', default=512, type=int)
    parser.add_argument_group(
        'Available colours',
        'Colours are specified using a one or two letter abbreviation: \n\n' + format_colour_table()
    )
    args = parser.parse_args()
    img = threadcount_to_image(args.threadcount, (args.width, args.height))
    img.save(sys.stdout.buffer, format="PNG")
    return 0


def format_colour_table():
    return '\n'.join('{} - {}'.format(key, value[1]) for key, value in COLOURS.items())


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
