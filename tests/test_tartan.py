#!/usr/bin/env python

"""Tests for `tartan` package."""
import pytest

import PIL

from tartan import tartan


def test_parse_threads():
    assert tartan.parse_threadcount('W2 B4') == [
        "#FFFFFF", "#FFFFFF", "#0000FF", "#0000FF", "#0000FF", "#0000FF"
    ]


def test_parse_symmetrical_threads():
    """
    A symmetrical pattern reflects from the back.  The reflecting thread group is not repeated
    """
    assert tartan.parse_threadcount('W/2 B1 LB/2') == [
        "#FFFFFF", "#FFFFFF", "#0000FF", "#82CFFD", "#82CFFD", "#0000FF"
    ]


ASYMMETRIC_IMAGE = tartan.threadcount_to_image('LG10 DR20 DY10', (80, 80))

@pytest.mark.parametrize("offset, expected", [
    (0, "#86C67C"),
    (9, "#86C67C"),
    (10, "#960000"),
    (29, "#960000"),
    (30, "#BC8C00"),
    (39, "#BC8C00"),
    (40, "#86C67C"),  # Back to the start again
])
def test_squares(offset, expected):
    assert PIL.ImageColor.getrgb(expected) == ASYMMETRIC_IMAGE.getpixel((offset, offset))[:3]

