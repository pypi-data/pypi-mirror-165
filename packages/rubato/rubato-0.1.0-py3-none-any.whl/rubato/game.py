"""
The main game class. It controls everything in the game.
The Display is where your game lives at a certain aspect ratio,
The Screen is the actual size of the window which the user interacts with.

Attributes:
    scenes (SceneManager): The global scene manager.
    radio (Radio): The global radio system.
    name (str): The title of the game window.
    fps (int): The target fps of the game.
    reset_display (bool): Controls whether or not the display should reset
        every frame.
    state (STATE): The current state of the game.
"""
import sys
import pygame
from pygame.transform import scale
from typing import TYPE_CHECKING, Tuple
from rubato.classes.sprite import Sprite
from rubato.utils import Display, Vector, Time, Configs, Math
from rubato.classes import SceneManager
from enum import Enum

if TYPE_CHECKING:
    from rubato.radio import Radio


class STATE(Enum):
    """
    An enum to keep track of the state things

    RUNNING: will run everything normally
    STOPPED: will quit the window
    PAUSED: will pause physics time calls. Please do not use this feature.
    """
    RUNNING = 1
    STOPPED = 2
    PAUSED = 3


pygame.init()

name: str = ""
_window_width: int = 0
_window_height: int = 0
resolution: Vector = Vector()
fps_cap: int = 0
physics_timestep: int = 0
reset_display: bool = True
_use_better_clock: bool = True

_physics_count: float = 0

_state = STATE.STOPPED

scenes = SceneManager()
radio: "Radio" = None

_saved_dims = [_window_width, _window_height]

_clock = pygame.time.Clock()
Time.set_clock(_clock)

_max_screen_size: Tuple[int, int] = (0, 0)

_screen = None
_display = None

is_init = False


def init(options: dict = {}):
    """
    Initializes a game. Should only be called by :meth:`rubato.init`.

    Args:
        options: A game config.
            Defaults to the |default| for `Game`.
    """
    global name, _window_width, _window_height, resolution, fps_cap, \
        reset_display, _use_better_clock, _saved_dims, _max_screen_size, \
        _screen, _display, is_init

    is_init = True

    params = Configs.game_defaults | options

    name = params["name"]
    _window_width = params["window_size"].x
    _window_height = params["window_size"].y
    resolution = params["resolution"]

    fps_cap = params["fps_cap"]
    Time.fdt = params["physics_timestep"]
    reset_display = params["reset_display"]
    _use_better_clock = params["better_clock"]

    _screen = pygame.display.set_mode(
        (_window_width, _window_height),
        pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.SCALED)
    _display = pygame.Surface(resolution.to_tuple(), pygame.SRCALPHA)

    pygame.display.set_caption(name)
    if options.get("icon"):
        pygame.display.set_icon(pygame.image.load(options.get("icon")))

    Display.set_display(_display)

    _saved_dims = [_window_width, _window_height]

    infos = pygame.display.Info()
    _max_screen_size = (infos.current_w, infos.current_h)


def constant_loop():
    """
    The constant game loop. Should only be called by :meth:`rubato.begin`.
    """
    global _state
    _state = STATE.RUNNING
    while True:
        update()


def update():
    """
    The update loop for the game. Called automatically every frame.
    Handles the game states.
    Will always process timed calls.
    """
    global _saved_dims, _screen, _physics_count, _display
    dnd_if_paused = get_state() != STATE.PAUSED
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            radio.broadcast("EXIT", {})
            pygame.quit()
            sys.exit(1)
        if event.type == pygame.VIDEORESIZE:
            global _window_height, _window_width
            _window_width, _window_height = event.size
        if event.type == pygame.KEYDOWN:
            radio.broadcast(
                "keydown",
                {
                    "key": pygame.key.name(event.key),
                    "unicode": event.unicode,
                    "code": event.key,
                    "modifiers": event.mod,
                },
            )
        if event.type == pygame.KEYUP:
            radio.broadcast(
                "keyup",
                {
                    "key": pygame.key.name(event.key),
                    "unicode": event.unicode,
                    "code": event.key,
                    "modifiers": event.mod,
                },
            )

    # Window resize handling
    if (_saved_dims[0] != _window_width or _saved_dims[1] != _window_height):
        _screen = pygame.display.set_mode(
            (_window_width, _window_height),
            pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.SCALED)

    aspect_ratio = resolution.x / resolution.y
    ratio = (_window_width / _window_height) < aspect_ratio
    width = (_window_height * aspect_ratio, _window_width)[ratio]
    height = (_window_height, _window_width / aspect_ratio)[ratio]
    top_left = (((_window_width - width) // 2, 0),
                (0, (_window_height - height) // 2))[ratio]

    _saved_dims = [_window_width, _window_height]

    # Delayed calls handling
    if dnd_if_paused and get_state():
        Time.process_calls()

    # Fixed Update Loop
    _physics_count += Time.delta_time()

    _physics_count = Math.clamp(_physics_count, 0, Time.fdt * 100)

    while dnd_if_paused and _physics_count > Time.fdt:
        scenes.fixed_update()
        _physics_count -= Time.fdt

    # Regular Update Loop
    if dnd_if_paused:
        scenes.update()

    # Draw Loop
    if dnd_if_paused:
        _screen.fill((0, 0, 0))
        if reset_display: _display.fill((255, 255, 255))
        scenes.draw()

    # Update Screen
    _display = Display.global_display

    frame = pygame.transform.smoothscale(_display, (width, height))

    _screen.blit(frame, top_left)

    pygame.display.flip()
    radio.events = []
    if dnd_if_paused:
        if _use_better_clock:
            _clock.tick_busy_loop(fps_cap)
        else:
            _clock.tick(fps_cap)
    else:
        pygame.time.delay(int(Time.delta_time()))


def render(sprite: Sprite, surface: pygame.Surface):
    if sprite.z_index <= scenes.current_scene.camera.z_index:
        width, height = surface.get_size()

        new_size = (
            round(width * scenes.current_scene.camera.zoom),
            round(height * scenes.current_scene.camera.zoom),
        )

        Display.update(
            scale(surface, new_size),
            scenes.current_scene.camera.transform(
                Sprite.center_to_tl(sprite.pos, Vector(width, height)) *
                scenes.current_scene.camera.zoom),
        )


def get_state() -> STATE:
    return _state


def set_state(new_state: STATE):
    global _state
    _state = new_state

    if _state == STATE.STOPPED:
        pygame.event.post(pygame.event.Event(pygame.QUIT))


def get_window_width():
    """
    Returns:
        The height of the actual window (screen).
    """
    return _window_width


def set_window_width(window_width: int) -> None:
    """
    Sets width of actual window (screen).
    Args:
        window_width:
            width clamped between the max display size initialized
            rubato.init()
    """
    global _window_width
    if _max_screen_size[0] > window_width > 0:
        _window_width = window_width


def get_window_height():
    """
    Returns:
        The width of the actual window (screen).
    """
    return _window_height


def set_window_height(window_height: int) -> None:
    """
    Sets height of actual window (screen).
    Args:
        window_height:
            height clamped between the max display size initialized
            rubato.init()
    """
    global _window_height
    if _max_screen_size[1] > window_height > 0:
        _window_height = window_height


def get_window_size():
    """
    The current size of the window

    Returns:
        Vector: A vector with x representing the width and
        y representing the height
    """
    return Vector(_window_width, _window_height)


def set_window_size(window_size: Vector):
    set_window_width(window_size.x)
    set_window_height(window_size.y)
