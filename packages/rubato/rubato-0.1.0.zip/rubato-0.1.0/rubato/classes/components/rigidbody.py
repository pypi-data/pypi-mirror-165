"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
import math
from typing import TYPE_CHECKING
from rubato.classes.component import Component
from rubato.utils import Vector, Configs, Time

if TYPE_CHECKING:
    from rubato.classes.components.hitbox import CollisionInfo


class RigidBody(Component):
    """
    A RigidBody implementation with built in physics and collisions.
    Rigidbodies require hitboxes.

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
        inv_mass (float): The inverse of the mass of the Rigidbody (0 if the
            mass is infinite).
        bounciness (float): How bouncy the rigidbody is (usually a value
            between 0 and 1).
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Rigidbody.

        Args:
            options: A rigidbody config. Defaults to the |default| for
                `RigidBody`
        """
        params = Configs.rigidbody_defaults | options

        super().__init__()

        self.static: bool = params["static"]

        self.gravity: Vector = params["gravity"]
        self.friction: float = params["friction"]
        self.max_speed: Vector = params["max_speed"]
        self.min_speed: Vector = params["min_speed"]

        self.velocity = Vector()

        # self.angvel: float = 0
        # self.rotation: float = params["rotation"]

        if params["mass"] == 0 or self.static:
            self.inv_mass = 0
        else:
            self.inv_mass: float = 1 / params["mass"]

        self.bounciness: float = params["bounciness"]

        self.required.append("Hitbox")

    @property
    def mass(self) -> float:
        """The mass of the Rigidbody (readonly)"""
        if self.inv_mass == 0:
            return 0
        else:
            return 1 / self.inv_mass

    def physics(self):
        """The physics calculation"""
        # Apply gravity
        self.add_force(self.gravity * self.mass)

        self.sprite.pos += self.velocity * Time.fixed_delta_time("sec")

    def add_force(self, force: Vector):
        """
        Add a force to the Rigidbody.

        Args:
            force: The force to add.
        """
        accel = force * self.inv_mass

        self.velocity += accel * Time.fixed_delta_time("sec")

    def add_cont_force(self, impulse: Vector, time: int):
        """
        Add a continuous force to the Rigidbody. A continuous force is a force
        that is continuously applied over a time period. (the force is added
        every frame for a specific duration).

        Args:
            impulse: The force to add.
            time: The time in seconds that the force should be added.
        """
        if time <= 0:
            return
        else:
            self.add_force(impulse)

            Time.delayed_frames(
                1, lambda: self.add_impulse(impulse, time - Time.delta_time()))

    @staticmethod
    def handle_collision(col: "CollisionInfo"):
        """
        Handle the collision between two rigidbodies.

        Args:
            col: The collision information.
        """
        rb_a: RigidBody = col.shape_b.sprite.get(RigidBody)
        rb_b: RigidBody = col.shape_a.sprite.get(RigidBody)

        inv_mass_a: float = (0 if rb_a is None else rb_a.inv_mass)
        inv_mass_b: float = (0 if rb_b is None else rb_b.inv_mass)

        # Relative velocity
        rv = (Vector() if rb_b is None else rb_b.velocity) - \
            (Vector() if rb_a is None else rb_a.velocity)

        # Relative velocity along collision normal
        collision_norm = col.sep.clone()
        collision_norm.normalize()
        vel_along_norm = rv.dot(collision_norm)

        if vel_along_norm > 0:
            return

        # Calculate restitution
        e = max(0 if rb_a is None else rb_a.bounciness,
                0 if rb_b is None else rb_b.bounciness)

        # Calculate impulse scalar
        j = -(1 + e) * vel_along_norm
        j /= inv_mass_a + inv_mass_b

        # Apply the impulse
        impulse = j * collision_norm

        if rb_a is not None and not rb_a.static:
            rb_a.velocity -= impulse * rb_a.inv_mass

        if rb_b is not None and not rb_b.static:
            rb_b.velocity += impulse * rb_b.inv_mass

        # Position correction
        percent = 0.2  # usually 20% to 80% interpolation
        slop = 0.01  # usually 0.01 to 0.1 correction threshold

        correction = max(col.sep.magnitude - slop, 0) / (
            inv_mass_a + inv_mass_b) * percent * collision_norm

        if rb_a is not None and not rb_a.static:
            rb_a.sprite.pos -= rb_a.inv_mass * correction

        if rb_b is not None and not rb_b.static:
            rb_b.sprite.pos += rb_b.inv_mass * correction

        # Friction

        # Relative velocity
        rv = (Vector() if rb_b is None else rb_b.velocity) - \
            (Vector() if rb_a is None else rb_a.velocity)

        # Tangent vector
        tangent = rv - rv.dot(collision_norm) * collision_norm
        tangent.normalize()

        # Solve for magnitude to apply along the friction vector
        jt = -rv.dot(tangent)
        jt /= inv_mass_a + inv_mass_b

        # Calculate mu
        if rb_a is None:
            mu = rb_b.friction
        elif rb_b is None:
            mu = rb_a.friction
        else:
            mu = math.sqrt((rb_a.friction**2) + (rb_b.friction**2))

        # Calculate friction impulse
        if abs(jt) < j * mu:
            friction_impulse = jt * tangent  # "Static friction"
        else:
            friction_impulse = -j * tangent * mu  # "Dynamic friction"

        if rb_a is not None and not rb_a.static:
            rb_a.velocity -= friction_impulse * rb_a.inv_mass

        if rb_b is not None and not rb_b.static:
            rb_b.velocity += friction_impulse * rb_b.inv_mass

    def fixed_update(self):
        """The update loop"""
        if not self.static:
            self.physics()
