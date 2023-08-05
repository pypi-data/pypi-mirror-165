"""
Groups contain game objects or other groups and allow separation between game objects.
"""
from __future__ import annotations
from typing import List, Union

from . import GameObject, Hitbox, UIElement
from .. import Error, Defaults, Game


class Group:
    """The group class implementation."""

    def __init__(self, options: dict = {}) -> None:
        """
        Initializes a group object.

        Args:
            options: A group object config. Defaults to the :ref:`Group defaults <groupdef>`.
        """
        param = Defaults.group_defaults | options
        self.name: str = param["name"]
        self.groups: List[Group] = []
        self.game_objects: List[GameObject] = []
        self.z_index: int = param["z_index"]

    def add(self, *items: Union[GameObject, Group]):
        """
        Adds an item to the group.

        Args:
            items: The item(s) you wish to add to the group

        Raises:
            Error: The item being added is the group itself. A group cannot be
                added to itself.
            ValueError: The group can only hold game objects or other groups.
        """
        for item in items:
            if Game.state == Game.RUNNING:
                item.setup()
            if isinstance(item, UIElement):
                self.add_ui_element(item)
            elif isinstance(item, GameObject):
                self.add_game_obj(item)
            elif isinstance(item, Group):
                self.add_group(item)
            else:
                raise ValueError(f"The group {self.name} can only hold game objects/groups.")

    def add_group(self, g: Group):
        """Add a group to the group."""
        if self == g:
            raise Error("Cannot add a group to itself.")
        if g.name == "":
            g.name = f"Group {len(self.groups)}"
        self.groups.append(g)

    def add_game_obj(self, g: GameObject):
        """Add a game object to the group"""
        if g.name == "":
            g.name = f"Game Object {len(self.game_objects)}"
        self.game_objects.append(g)

    def add_ui_element(self, ui: UIElement):
        """Add a ui element to the group."""
        if ui.name == "":
            ui.name = f"UI {len(self.game_objects)}"
        self.game_objects.append(ui)

    def delete(self, item: Union[GameObject, Group]):
        """
        Removes an item from the group.

        Args:
            item: The item to remove from the group.

        Raises:
            ValueError: The item is not in the group and cannot be deleted.
        """
        try:
            if isinstance(item, GameObject):
                self.game_objects.remove(item)
            elif isinstance(item, Group):
                self.groups.remove(item)
        except ValueError as e:
            raise ValueError(f"The item {item.name} is not in the group {self.name}") from e

    def setup(self):
        for group in self.groups:
            group.setup()
        for game_obj in self.game_objects:
            game_obj.setup()

    def update(self):
        for group in self.groups:
            group.update()
        for game_obj in self.game_objects:
            game_obj.update()

    def fixed_update(self):
        """Runs a physics iteration on the group. Called automatically by Rubato when added to a scene."""
        for group in self.groups:
            group.fixed_update()

        hitboxes: List[Hitbox] = []
        for game_obj in self.game_objects:
            game_obj.fixed_update()

            if hts := game_obj._components.get(Hitbox, []):  # pylint: disable=protected-access
                for ht in hts:
                    for hitbox in hitboxes:
                        ht.collide(hitbox)
                hitboxes.extend(hts)

    def draw(self):
        self.groups.sort(key=lambda i: i.z_index)
        for group in self.groups:
            if group.z_index <= Game.camera.z_index:
                group.draw()

        self.game_objects.sort(key=lambda i: i.z_index)
        for game_obj in self.game_objects:
            if game_obj.z_index <= Game.camera.z_index:
                game_obj.draw()

    def count(self) -> int:
        """
        Counts all the GameObjects in this group and all groups it contains.
        Returns:
            int: The number of GameObjects in a group
        """
        children = 0
        for group in self.groups:
            children += group.count()
        return len(self.game_objects) + children
