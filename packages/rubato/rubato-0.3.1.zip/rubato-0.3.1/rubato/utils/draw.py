"""A static draw class for drawing things directly to the renderer."""
from __future__ import annotations
from ctypes import c_int16
from typing import TYPE_CHECKING, Optional, Callable
import cython

import sdl2, sdl2.sdlgfx, sdl2.ext

from . import Vector, Color, Font, Display, Math, InitError

if TYPE_CHECKING:
    from .. import Surf, Camera


@cython.cclass
class DrawTask:
    priority: cython.int = cython.declare(cython.int, visibility="public")
    func: Callable = cython.declare(object, visibility="public")

    def __init__(self, priority: cython.int, func: Callable):
        self.priority = priority
        self.func = func


# THIS IS A STATIC CLASS
class Draw:
    """Draws things to the renderer. Don't instantiate, instead use it as a static class."""
    _queue: list[DrawTask] = []

    def __init__(self) -> None:
        raise InitError(self)

    @classmethod
    def clear(cls, background_color: Color = Color.white, border_color: Color = Color.black):
        """Clears the renderer and draws the background of the frame.

        Args:
            background_color (Color): The background color. Defaults to white.
            border_color (Color): The border color. Defaults to black.
                Shown when the aspect ratio of the game does not match the aspect ratio of the window.
        """
        Display.renderer.clear(border_color.to_tuple())
        Display.renderer.fill(
            (0, 0, *Display.renderer.logical_size),
            background_color.to_tuple(),
        )

    @classmethod
    def push(cls, z_index: int, callback: Callable):
        """
        Add a custom draw function to the frame queue.

        Args:
            z_index (int): The z_index to call at (lower z_indexes get called first).
            callback (Callable): The function to call.
        """
        cls._queue.append(DrawTask(z_index, callback))

    @classmethod
    def dump(cls):
        """Draws all queued items. Is called automatically at the end of every frame."""
        if not cls._queue:
            return

        cls._queue.sort(key=lambda x: x.priority)

        for task in cls._queue:
            task.func()

        cls._queue.clear()

    @classmethod
    def queue_point(cls, pos: Vector, color: Color = Color.cyan, z_index: int = Math.INF):
        """
        Draw a point onto the renderer at the end of the frame.

        Args:
            pos (Vector): The position of the point.
            color (Color): The color to use for the pixel. Defaults to Color.cyan.
            z_index (int): Where to draw it in the drawing order. Defaults to Math.INF.
        """
        cls.push(z_index, lambda: cls.point(pos, color))

    @staticmethod
    def point(pos: Vector, color: Color = Color.cyan):
        """
        Draw a point onto the renderer immediately.

        Args:
            pos (Vector): The position of the point.
            color (Color): The color to use for the pixel. Defaults to Color.cyan.
        """
        sdl2.sdlgfx.pixelRGBA(Display.renderer.sdlrenderer, round(pos.x), round(pos.y), *color.to_tuple())

    @classmethod
    def queue_line(
        cls, p1: Vector, p2: Vector, color: Color = Color.cyan, width: int | float = 1, z_index: int = Math.INF
    ):
        """
        Draw a line onto the renderer at the end of the frame.

        Args:
            p1: The first point of the line.
            p2: The second point of the line.
            color: The color to use for the line. Defaults to Color.cyan.
            width: The width of the line. Defaults to 1.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
        """
        cls.push(z_index, lambda: cls.line(p1, p2, color, width))

    @staticmethod
    def line(p1: Vector, p2: Vector, color: Color = Color.cyan, width: int | float = 1):
        """
        Draw a line onto the renderer immediately.

        Args:
            p1: The first point of the line.
            p2: The second point of the line.
            color: The color to use for the line. Defaults to Color.cyan.
            width: The width of the line. Defaults to 1.
        """
        sdl2.sdlgfx.thickLineRGBA(
            Display.renderer.sdlrenderer, round(p1.x), round(p1.y), round(p2.x), round(p2.y), round(width), color.r,
            color.g, color.b, color.a
        )

    @classmethod
    def queue_rect(
        cls,
        center: Vector,
        width: int | float,
        height: int | float,
        border: Color = Color.clear,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        angle: float = 0,
        z_index: int = Math.INF
    ):
        """
        Draws a rectangle onto the renderer at the end of the frame.

        Args:
            center: The center of the rectangle.
            width: The width of the rectangle.
            height: The height of the rectangle.
            border: The border color. Defaults to Color.clear.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            angle: The angle in degrees. Defaults to 0.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
        """
        cls.push(z_index, lambda: cls.rect(center, width, height, border, border_thickness, fill, angle))

    @staticmethod
    def rect(
        center: Vector,
        width: int | float,
        height: int | float,
        border: Color = Color.clear,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        angle: float = 0
    ):
        """
        Draws a rectangle onto the renderer immediately.

        Args:
            center: The center of the rectangle.
            width: The width of the rectangle.
            height: The height of the rectangle.
            border: The border color. Defaults to Color.clear.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            angle: The angle in degrees. Defaults to 0.
        """
        x, y = width // 2, height // 2
        verts = (Vector(-x, -y), Vector(x, -y), Vector(x, y), Vector(-x, y))

        Draw.poly([center + v.rotate(angle) for v in verts], border, border_thickness, fill)

    @classmethod
    def queue_circle(
        cls,
        center: Vector,
        radius: int = 4,
        border: Color = Color.clear,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        z_index: int = Math.INF
    ):
        """
        Draws a circle onto the renderer at the end of the frame.

        Args:
            center: The center.
            radius: The radius. Defaults to 4.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
        """
        cls.push(z_index, lambda: cls.circle(center, radius, border, border_thickness, fill))

    @staticmethod
    def circle(
        center: Vector,
        radius: int | float = 4,
        border: Color = Color.clear,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None
    ):
        """
        Draws a circle onto the renderer immediately.

        Args:
            center: The center.
            radius: The radius. Defaults to 4.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
        """
        if fill:
            sdl2.sdlgfx.filledCircleRGBA(
                Display.renderer.sdlrenderer,
                int(center.x),
                int(center.y),
                int(radius),
                fill.r,
                fill.g,
                fill.b,
                fill.a,
            )

        for i in range(int(border_thickness)):
            sdl2.sdlgfx.aacircleRGBA(
                Display.renderer.sdlrenderer,
                int(center.x),
                int(center.y),
                int(radius) + i,
                border.r,
                border.g,
                border.b,
                border.a,
            )

    @classmethod
    def queue_poly(
        cls,
        points: list[Vector],
        border: Color = Color.clear,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None,
        z_index: int = Math.INF
    ):
        """
        Draws a polygon onto the renderer at the end of the frame.

        Args:
            points: The list of points to draw.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
        """
        cls.push(z_index, lambda: cls.poly(points, border, border_thickness, fill))

    @staticmethod
    def poly(
        points: list[Vector],
        border: Color = Color.clear,
        border_thickness: int | float = 1,
        fill: Optional[Color] = None
    ):
        """
        Draws a polygon onto the renderer immediately.

        Args:
            points: The list of points to draw.
            border: The border color. Defaults to green.
            border_thickness: The border thickness. Defaults to 1.
            fill: The fill color. Defaults to None.
        """
        x_coords, y_coords = zip(*(coord.tuple_int() for coord in points))

        vx = (c_int16 * len(x_coords))(*x_coords)
        vy = (c_int16 * len(y_coords))(*y_coords)
        if fill:
            sdl2.sdlgfx.filledPolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(points),
                fill.r,
                fill.g,
                fill.b,
                fill.a,
            )

        if border_thickness <= 0:
            return
        elif border_thickness == 1:
            sdl2.sdlgfx.aapolygonRGBA(
                Display.renderer.sdlrenderer,
                vx,
                vy,
                len(points),
                border.r,
                border.g,
                border.b,
                border.a,
            )
        else:
            for i in range(len(points)):
                Draw.line(
                    Vector(
                        points[i].x,
                        points[i].y,
                    ),
                    Vector(
                        points[(i + 1) % len(points)].x,
                        points[(i + 1) % len(points)].y,
                    ),
                    border,
                    border_thickness,
                )

    @classmethod
    def queue_text(
        cls,
        text: str,
        font: Font,
        pos: Vector = Vector(),
        justify: str = "left",
        align: Vector = Vector(),
        width: int | float = 0,
        z_index: int = Math.INF
    ):
        """
        Draws some text onto the renderer at the end of the frame.

        Args:
            text: The text to draw.
            font: The Font object to use.
            pos: The position of the text. Defaults to Vector(0, 0).
            justify: The justification of the text. (left, center, right). Defaults to "left".
            align: The alignment of the text. Defaults to Vector(0, 0).
            width: The maximum width of the text. Will automatically wrap the text. Defaults to -1.
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
        """
        cls.push(z_index, lambda: cls.text(text, font, pos, justify, align, width))

    @staticmethod
    def text(
        text: str,
        font: Font,
        pos: Vector = Vector(),
        justify: str = "left",
        align: Vector = Vector(),
        width: int | float = 0
    ):
        """
        Draws some text onto the renderer immediately.

        Args:
            text: The text to draw.
            font: The Font object to use.
            pos: The position of the text. Defaults to Vector(0, 0).
            justify: The justification of the text. (left, center, right). Defaults to "left".
            align: The alignment of the text. Defaults to Vector(0, 0).
            width: The maximum width of the text. Will automatically wrap the text. Defaults to -1.
        """
        tx = sdl2.ext.Texture(Display.renderer, font.generate_surface(text, justify, width))
        Display.update(tx, pos + (align - 1) * Vector(*tx.size) / 2)

    @classmethod
    def queue_texture(
        cls,
        texture: sdl2.ext.Texture,
        pos: Vector = Vector(),
        z_index: int = Math.INF,
        scale: Vector = Vector(1, 1),
        angle: float = 0,
    ):
        """
        Draws an texture onto the renderer at the end of the frame.

        Args:
            texture: The texture to draw.
            pos: The position of the texture. Defaults to Vector(0, 0).
            z_index: Where to draw it in the drawing order. Defaults to Math.INF.
            scale: The scale of the texture. Defaults to Vector(1, 1).
            angle: The clockwise rotation of the texture. Defaults to 0.
        """
        cls.push(z_index, lambda: cls.texture(texture, pos, scale, angle))

    @staticmethod
    def texture(
        texture: sdl2.ext.Texture,
        pos: Vector = Vector(),
        scale: Vector = Vector(1, 1),
        angle: float = 0,
    ):
        """
        Draws an SDL Texture onto the renderer immediately.

        Args:
            texture: The texture to draw.
            pos: The position to draw the texture at. Defaults to Vector().
            scale: The scale of the texture. Defaults to Vector(1, 1).
            angle: The clockwise rotation of the texture. Defaults to 0.
        """
        Display.update(texture, pos, scale, angle)

    @classmethod
    def queue_surf(cls, surf: Surf, pos: Vector = Vector(), z_index: int = Math.INF, camera: Camera | None = None):
        """
        Draws an surf onto the renderer at the end of the frame.

        Args:
            surf: The surf to draw.
            pos: The position to draw the surf at. Defaults to Vector(0, 0).
            z_index: The z-index of the surf. Defaults to 0.
            camera: The camera to use. Set to None to ignore the camera. Defaults to None.
        """
        cls.push(z_index, lambda: cls.surf(surf, pos, camera))

    @staticmethod
    def surf(surf: Surf, pos: Vector = Vector(), camera: Camera | None = None):
        """
        Draws an surf onto the renderer immediately.

        Args:
            surf: The surf to draw.
            pos: The position to draw the surf at. Defaults to Vector().
            camera: The camera to use. Set to None to ignore the camera. Defaults to None.
        """
        if not surf.surf:
            return
        if not surf.uptodate:
            surf.generate_tx()

        if camera is None:
            pos -= surf.get_size() / 2
        else:
            pos = camera.transform(pos - (surf.get_size() / 2))

        Draw.texture(surf.tx, pos, surf.scale, surf.rotation)
