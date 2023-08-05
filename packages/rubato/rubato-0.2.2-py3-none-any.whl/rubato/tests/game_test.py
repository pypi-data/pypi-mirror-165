"""Test the Game class"""
from unittest.mock import Mock
import pytest

from rubato.game import Game
from rubato.classes.scene import Scene
# pylint: disable=redefined-outer-name


@pytest.fixture
def scene():
    return Scene()


def test_state(monkeypatch):
    assert Game.state == Game.STOPPED
    Game.state = Game.RUNNING
    assert Game.state == Game.RUNNING

    push_event = Mock()
    monkeypatch.setattr("sdl2.SDL_PushEvent", push_event)

    Game.state = Game.STOPPED
    assert Game.state == Game.STOPPED
    push_event.assert_called_once()


def test_camera(scene):
    # pylint: disable=unused-argument
    Game.scenes.add(scene, "main")
    assert Game.camera == Game.scenes.current.camera
