"""
A static time class to monitor time and to call functions in the future.

"""
from dataclasses import dataclass, field
from typing import Callable
import heapq
import sdl2
from . import InitError


@dataclass(order=True)
class DelayedTask:
    """A task that is run after a specified number of milliseconds."""
    delay: int
    task: Callable = field(compare=False)
    is_stopped: bool = field(default=False, compare=False)

    def stop(self):
        """Stop the DelayedTask from invoking."""
        self.is_stopped = True


@dataclass(order=True)
class FramesTask:
    """A task that is run after a specified number of frames."""
    delay: int
    task: Callable = field(compare=False)
    is_stopped: bool = field(default=False, compare=False)

    def stop(self):
        """Stop the FramesTask from invoking."""
        self.is_stopped = True


@dataclass(order=True)
class ScheduledTask:
    """A task that is run every specified number of milliseconds."""
    interval: int = field(compare=False)
    task: Callable = field(compare=False)
    delay: int = field(default=0)
    is_stopped: bool = field(default=False, compare=False)

    def stop(self):
        """Stop the ScheduledTask from invoking."""
        self.is_stopped = True


# THIS IS A STATIC CLASS
class Time:
    """
    The time class.
    """

    frames: int = 0
    """The total number of elapsed frames since the start of the game."""

    _frame_queue: list[FramesTask] = []
    _task_queue: list[DelayedTask] = []
    _schedule_queue: list[ScheduledTask] = []

    delta_time: float = 0.001
    fixed_delta: float = 0
    """The number of seconds since the last fixed update."""
    normal_delta: float = 0
    fps = 60
    """The current fps of thi frame."""
    _frame_start: int = 0

    physics_counter: float = 0

    _fps_history: int = 120
    _past_fps = [0] * _fps_history
    _fps_index: int = 0

    target_fps = 0  # this means no cap
    """The fps that the game should try to run at. 0 means that the game's fps will not be capped. Defaults to 0."""
    capped: bool = False

    physics_fps = 30
    """The fps that the physics should run at. Defaults to 30."""

    def __init__(self) -> None:
        raise InitError(self)

    @classmethod
    @property
    def smooth_fps(cls) -> int:
        """The average fps over the past 120 frames. This is a get-only property."""
        return int(sum(cls._past_fps) / cls._fps_history)

    @classmethod
    def now(cls) -> int:
        """The time since the start of the game, in milliseconds."""
        return sdl2.SDL_GetTicks64()

    @classmethod
    @property
    def frame_start(cls) -> int:
        """The time since the start of the game, in milliseconds, taken at the start of the frame.
        This is a get-only property."""
        return cls._frame_start

    @classmethod
    def schedule(cls, task: DelayedTask | FramesTask | ScheduledTask):
        """
        Schedules a task for delayed execution based on what type of task it is.

        Args:
            task (DelayedTask | FramesTask | ScheduledTask): The task to queue.
        """
        if isinstance(task, DelayedTask):
            task.delay += cls.now()
            heapq.heappush(cls._task_queue, task)
        elif isinstance(task, FramesTask):
            task.delay += cls.frames
            heapq.heappush(cls._frame_queue, task)
        elif isinstance(task, ScheduledTask):
            task.delay += cls.now()
            heapq.heappush(cls._schedule_queue, task)
        else:
            raise TypeError("Task argument must of of type DelayedTask, FramesTask or ScheduledTask.")

    @classmethod
    def delayed_call(cls, delay: int, func: Callable):
        """
        Calls the function func at a later time.

        Args:
            delay: The time from now (in milliseconds) to run the function at.
            func: The function to call.
        """

        heapq.heappush(cls._task_queue, DelayedTask(delay + cls.now(), func))

    @classmethod
    def delayed_frames(cls, delay: int, func: Callable):
        """
        Calls the function func at a later frame.

        Args:
            delay: The number of frames to wait.
            func: The function to call
        """

        heapq.heappush(cls._frame_queue, FramesTask(cls.frames + delay, func))

    @classmethod
    def scheduled_call(cls, interval: int, func: Callable):
        """
        Calls the function func at a scheduled interval.

        Args:
            interval: The interval (in milliseconds) to run the function at.
            func: The function to call.
        """

        heapq.heappush(cls._schedule_queue, ScheduledTask(interval, func, interval + cls.now()))

    @classmethod
    def milli_to_sec(cls, milli: int) -> float:
        """
        Converts milliseconds to seconds.

        Args:
            milli: A number in milliseconds.
        Returns:
            float: The converted number in seconds.
        """
        return milli / 1000

    @classmethod
    def sec_to_milli(cls, sec: int) -> float:
        """
        Converts seconds to milliseconds.

        Args:
            sec: A number in seconds.
        Returns:
            float: The converted number in milliseconds.
        """
        return sec * 1000

    @classmethod
    def process_calls(cls):
        """Processes the delayed function call as needed"""
        cls.frames += 1
        cls.fps = 1 / cls.delta_time

        cls._past_fps[cls._fps_index] = int(cls.fps)
        cls._fps_index = (cls._fps_index + 1) % cls._fps_history

        while cls._frame_queue:
            if cls._frame_queue[0].delay <= cls.frames:
                timer_task = heapq.heappop(cls._frame_queue)
                if not timer_task.is_stopped:
                    timer_task.task()
            else:
                break

        while cls._task_queue:
            if cls._task_queue[0].delay <= cls.now():
                timer_task = heapq.heappop(cls._task_queue)
                if not timer_task.is_stopped:
                    timer_task.task()
            else:
                break

        while cls._schedule_queue:
            if cls._schedule_queue[0].delay <= cls.now():
                scheduled_task = heapq.heappop(cls._schedule_queue)

                if not scheduled_task.is_stopped:
                    scheduled_task.task()

                if not scheduled_task.is_stopped:
                    scheduled_task.delay += scheduled_task.interval
                    heapq.heappush(cls._schedule_queue, scheduled_task)
            else:
                break
