"""Console script for tartan."""
import argparse
import sys
from tartan.tartan import threadcount_to_image

def main():
    """Console script for tartan."""
    parser = argparse.ArgumentParser()
    parser.add_argument('threadcount')
    parser.add_argument('--width', default=512, type=int)
    parser.add_argument('--height', default=512, type=int)
    args = parser.parse_args()
    img = threadcount_to_image(args.threadcount, (args.width, args.height))
    img.save(sys.stdout.buffer, format="PNG")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
