"""
THe Scene class which is a collection of groups. It also houses the current
scene camera. Scenes come with a default group that everything is added to if
no other groups are specified.
"""
from typing import List, Union, TYPE_CHECKING
from rubato.classes import Camera, Group

if TYPE_CHECKING:
    from rubato.classes import Sprite


class Scene:
    """
    A scene is a collection of groups.

    Attributes:
        root (Group): The base group of sprites in the scene.
        camera (Camera): The camera of this scene.
        id (str): The id of this scene.
    """

    def __init__(self):
        """
        Initializes a scene with an empty collection of sprites, a new camera,
        and a blank id.
        """
        self.root: Group = Group()
        self.camera = Camera()
        self.id: str = ""

    def add(
        self,
        item: Union["Sprite", "Group", List[Union["Sprite", "Group"]]]):
        """
        Adds an item to the root group.

        Args:
            item: The item or list of items to add.

        """
        self.root.add(item)

    def remove(self, item: Union["Sprite", "Group"]):
        """
        Removes an item from the root group.

        Args:
            item: The item to remove.

        """
        self.root.remove(item)

    def private_draw(self):
        self.root.draw()

    def private_update(self):
        self.update()
        self.root.update()

    def private_fixed_update(self):
        self.fixed_update()
        self.root.fixed_update()

    def private_setup(self):
        self.setup()
        self.root.setup()

    def setup(self):
        """The start loop for this scene. It is run before the first frame."""
        pass

    def update(self):
        """
        The update loop for this scene. Is empty by default an can be
        overridden.
        """
        pass

    def fixed_update(self):
        """
        The fixed update loop for this scene. Is empty by default an can be
        overridden.
        """
        pass
