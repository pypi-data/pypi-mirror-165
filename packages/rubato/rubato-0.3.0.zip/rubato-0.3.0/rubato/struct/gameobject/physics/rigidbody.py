"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
from __future__ import annotations

from .. import Component
from .... import Vector, Time, Math


class RigidBody(Component):
    """
    A RigidBody implementation with built in physics and collisions.
    Rigidbodies require hitboxes.

    Args:
        mass: The mass of the rigidbody. Defaults to -1.
        gravity: The gravity of the rigidbody. Defaults to Vector(0, 0).
        friction: The friction of the rigidbody. Defaults to 0.
        static: Whether the rigidbody is static. Defaults to False.
        bounciness: The bounciness of the rigidbody. Defaults to 0.
        max_speed: The maximum speed of the rigidbody. Defaults to Vector(INF, INF).
        velocity: The velocity of the rigidbody. Defaults to Vector(0, 0).
        ang_vel: The angular velocity of the rigidbody. Defaults to 0.
        pos_correction: The positional correction of the rigidbody. Defaults to 0.25.
        offset: The offset of the rigidbody from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The offset of the rigidbody's rotation from the gameobject. Defaults to 0.
        z_index: The z-index of the rigidbody. Defaults to 0.

    Attributes:
        static (bool): Whether or not the rigidbody is static (as in, it does
            not move).
        gravity (Vector): The acceleration of the gravity that should be
            applied.
        friction (float): The friction coefficient of the Rigidbody (usually a
            a value between 0 and 1).
        max_speed (Vector): The maximum speed of the Rigidbody.
        min_speed (Vector): The minimum speed of the Rigidbody.
        velocity (Vector): The current velocity of the Rigidbody.
        ang_vel (float): The current angular velocity of the Rigidbody.
        bounciness (float): How bouncy the rigidbody is (usually a value
            between 0 and 1).
        advanced (bool): Whether to use rotational collision resolution
            (not desired in basic platformers, for instance).
    """

    def __init__(
        self,
        mass: float = 1,
        gravity: Vector = Vector(),
        friction: float = 0,
        static: bool = False,
        bounciness: float = 0,
        max_speed: Vector = Vector(Math.INF, Math.INF),
        velocity: Vector = Vector(),
        ang_vel: float = 0,
        pos_correction: float = 0.25,
        offset: Vector = Vector(),
        rot_offset: float = 0,
        z_index: int = 0
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)

        self.static: bool = static

        self.gravity: Vector = gravity
        self.friction: float = friction
        self.max_speed: Vector = max_speed

        self.pos_correction: float = pos_correction

        self.velocity: Vector = velocity
        self.ang_vel: float = ang_vel

        self.singular = True

        if mass == 0 or self.static:
            self._inv_mass = 0
        else:
            self._inv_mass: float = 1 / mass

        self.bounciness: float = bounciness

    @property
    def inv_mass(self) -> float:
        """The inverse mass of the Rigidbody."""
        return self._inv_mass

    @inv_mass.setter
    def inv_mass(self, new: float):
        self._inv_mass = new

    @property
    def mass(self) -> float:
        """The mass of the Rigidbody."""
        if self.inv_mass == 0:
            return 0
        else:
            return 1 / self.inv_mass

    @mass.setter
    def mass(self, new: float):
        if new == 0:
            self.inv_mass = 0
        else:
            self.inv_mass: float = 1 / new

    def physics(self):
        """Applies general kinematic laws to the rigidbody."""
        self.velocity += self.gravity * Time.fixed_delta
        self.velocity.clamp(-self.max_speed, self.max_speed)

        self.gameobj.pos += self.velocity * Time.fixed_delta
        self.gameobj.rotation += self.ang_vel * Time.fixed_delta

    def add_force(self, force: Vector):
        """
        Applies a force to the Rigidbody.

        Args:
            force (Vector): The force to add.
        """
        accel = force * self.inv_mass

        self.velocity += accel * Time.fixed_delta

    def add_impulse(self, impulse: Vector):
        """
        Applies an impulse to the rigidbody.

        Args:
            impulse (Vector): _description_
        """
        self.velocity += impulse * Time.fixed_delta

    def add_cont_force(self, force: Vector, time: int):
        """
        Add a continuous force to the Rigidbody.
        A continuous force is a force that is continuously applied over a time period.
        (the force is added every frame for a specific duration).

        Args:
            force (Vector): The force to add.
            time (int): The time in seconds that the force should be added.
        """
        if time <= 0:
            return
        else:
            self.add_force(force)
            Time.delayed_frames(1, lambda: self.add_cont_force(force, time - (1000 * Time.delta_time)))

    def add_cont_impulse(self, impulse: Vector, time: int):
        """
        Add a continuous impulse to the Rigidbody.
        A continuous impulse is a impulse that is continuously applied over a time period.
        (the impulse is added every frame for a specific duration).

        Args:
            impulse (Vector): The impulse to add.
            time (int): The time in seconds that the impulse should be added.
        """
        if time <= 0:
            return
        else:
            self.add_impulse(impulse)
            Time.delayed_frames(1, lambda: self.add_cont_impulse(impulse, time - (1000 * Time.delta_time)))

    def fixed_update(self):
        """The physics loop for the rigidbody component."""
        if not self.static:
            self.physics()

    def clone(self) -> RigidBody:
        return RigidBody(
            mass=self.mass,
            gravity=self.gravity,
            friction=self.friction,
            static=self.static,
            bounciness=self.bounciness,
            max_speed=self.max_speed,
            velocity=self.velocity,
            ang_vel=self.ang_vel,
            pos_correction=self.pos_correction,
            offset=self.offset,
            rot_offset=self.rot_offset,
            z_index=self.z_index
        )
