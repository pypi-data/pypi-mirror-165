"""
The math module includes some helper functions for commonly used equations.
"""
from typing import Union


class Math:
    """
    A more complete math class.

    Attributes:
        INF (float): The max value of a float.
    """
    INF = float('inf')

    @classmethod
    def clamp(cls, a: Union[float, int], lower: Union[float, int], upper: Union[float, int]) -> float:
        """
        Clamps a value.

        Args:
            a: The value to clamp.
            lower: The lower bound of the clamp.
            upper: The upper bound of the clamp.

        Returns:
            float: The clamped result.
        """
        return min(max(a, lower), upper)

    @classmethod
    def sign(cls, n: Union[float, int]) -> int:
        """
        Checks the sign of n.

        Args:
            n: A number to check.

        Returns:
            int: The sign of the number. (1 for positive, 0 for 0, -1 for negative)
        """
        if n == 0:
            return 0
        return (n >= 0) - (n < 0)

    @classmethod
    def lerp(cls, a: Union[float, int], b: Union[float, int], t: float) -> float:
        """
        Linearly interpolates between lower and upper bounds by t

        Args:
            a: The lower bound.
            b: The upper bound.
            t: Distance between upper and lower (1 gives b, 0 gives a).

        Returns:
            float: The lerped value.
        """
        return a + t * (b - a)
