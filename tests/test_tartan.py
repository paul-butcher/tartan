#!/usr/bin/env python

"""Tests for `tartan` package."""

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
