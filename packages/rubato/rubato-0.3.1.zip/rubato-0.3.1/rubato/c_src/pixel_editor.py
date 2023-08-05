# distutils: language = c++
# cython: language_level = 3
"""Loader for PixelEditor.cpp"""
import cython
from .. import Vector
if cython.compiled:
    from cython.cimports.rubato.c_src import cPixelEditor as PE  # pyright: ignore
    from cython.cimports.cpython import array  # pyright: ignore
else:
    PE = None
    import array


def set_pixel(pixels: int, width: int, height: int, x: int, y: int, color: int, blending: bool = True):
    PE.setPixel(pixels, width, height, x, y, color, blending)


def get_pixel(pixels: int, width: int, height: int, x: int, y: int):
    return PE.getPixel(pixels, width, height, x, y)


def clear_pixels(pixels: int, width: int, height: int):
    PE.clearPixels(pixels, width, height)


def draw_line(
    pixels: int,
    width: int,
    height: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: int,
    aa: bool = False,
    blending: bool = True,
    thickness: int = 1,
):
    PE.drawLine(pixels, width, height, x1, y1, x2, y2, color, aa, blending, thickness)


def draw_circle(
    pixels: int,
    width: int,
    height: int,
    xc: int,
    yc: int,
    radius: int,
    border_color: int,
    fill_color: int,
    aa: bool = False,
    blending: bool = True,
    thickness: int = 1
):
    PE.drawCircle(pixels, width, height, xc, yc, radius, border_color, fill_color, aa, blending, thickness)


def draw_rect(
    pixels: int,
    width: int,
    height: int,
    x: int,
    y: int,
    w: int,
    h: int,
    border_color: int,
    fill_color: int,
    blending: bool = True,
    thickness: int = 1,
):
    PE.drawRect(pixels, width, height, x, y, w, h, border_color, fill_color, blending, thickness)


def draw_poly(
    pixels: int,
    width: int,
    height: int,
    points: list[Vector],
    border_color: int,
    fill_color: int,
    aa: bool = False,
    blending: bool = True,
    thickness: int = 1,
):
    vxt = []
    vyt = []
    for v in points:
        x, y = v.tuple_int()
        vxt.append(x)
        vyt.append(y)
    vx: array.array = array.array("i", vxt)
    vy: array.array = array.array("i", vyt)
    PE.drawPoly(
        pixels,
        width,
        height,
        vx.data.as_voidptr,
        vy.data.as_voidptr,
        len(points),
        border_color,
        fill_color,
        aa,
        blending,
        thickness,
    )
