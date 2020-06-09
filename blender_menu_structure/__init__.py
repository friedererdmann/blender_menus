bl_info = {
    "name": "Dynamically created Blender Menu",
    "author": "Frieder Erdmann, Boris Ignjatovic",
    "blender": (2, 80, 3),
    "location": "Menu > Submenus",
    "description": "A test to create dynamic menus",
    "warning": "",
    "wiki_url": "",
    "category": "UI"
}

import os
from functools import partial
import bpy
from bpy.utils import previews


imageloader = None


class ImageLoader():
    """ImageLoader to wrap previews into a singleton.
    Heavily inspired by Embark tools - thanks!
    """

    def __init__(self):
        self.preview_handler = previews.new()

    def blender_icon(self, icon="NONE"):
        if icon.lower().endswith(".png"):
            icon = self.load_icon(icon)
        return self.preview_handler[icon].icon_id

    def load_icon(self, filename="image.png"):
        script_dir = os.path.dirname(__file__)
        icon_dir = os.path.join(script_dir, "icons")
        filepath = os.path.join(icon_dir, filename)
        name = os.path.splitext(filename)[0]
        self.preview_handler.load(name, filepath, 'IMAGE')
        return name

    def unregister(self):
        previews.remove(self.preview_handler)
        self.preview_handler = None


def add_menu(name, icon_value=0, parent_name="TOPBAR_MT_editor_menus"):
    """Adds a menu class and adds it to any menu.

    Args:
        name (str): Name of the menu
        parent_name (str, optional): What Blender menu should this be added into. Defaults to "TOPBAR_MT_editor_menus".
    """

    def draw(self, context):
        pass

    def menu_draw(self, context):
        self.layout.menu(my_menu_class.bl_idname, icon_value=icon_value)

    bl_idname = "MENU_MT_{0}".format(name.replace(" ", ""))
    full_parent_name = "bpy.types.{0}".format(parent_name)

    parent = eval(full_parent_name)

    my_menu_class = type(
        "DynamicMenu{0}".format(name),
        (bpy.types.Menu,),
        {
            "bl_idname": bl_idname,
            "bl_label": name,
            "draw": draw
        })

    bpy.utils.register_class(my_menu_class)
    parent.append(menu_draw)

    return bl_idname


def add_operator(name, callback, icon_value=0, tooltip='Dynamic Operator', parent_name="TOPBAR_MT_editor_menus"):
    """Adds a dummy operator to be able to add your callback into any menu.

    Args:
        name (str): Name of the menu entry
        callback (function): What method do you want to callback to from here
        parent_name (str, optional): What Blender menu should this be added into. Defaults to "TOPBAR_MT_editor_menus".
    """

    def execute(self, context):
        my_operator_class.func()
        return {"FINISHED"}

    def operatator_draw(self, context):
        self.layout.operator(my_operator_class.bl_idname, icon_value=icon_value)

    bl_idname = "menuentry.{0}".format(name.replace(" ", "").lower())
    full_parent_name = "bpy.types.{0}".format(parent_name)
    parent = eval(full_parent_name)
    my_operator_class = type(
        "DynamicOperator{0}".format(name),
        (bpy.types.Operator,),
        {
            "bl_idname": bl_idname,
            "bl_label": name,
            "func": callback,
            "execute": execute,
            "__doc__": tooltip
        })
    bpy.utils.register_class(my_operator_class)
    parent.append(operatator_draw)

    return bl_idname


def add_separator(parent_name="TOPBAR_MT_editor_menus"):
    """Adds a separator to the menu identified in parent_name

    Args:
        parent_name (str, optional): What Blender menu should this be added into. Defaults to "TOPBAR_MT_editor_menus".
    """

    def draw_separator(self, context):
        self.layout.row().separator()

    full_parent_name = "bpy.types.{0}".format(parent_name)
    parent = eval(full_parent_name)
    parent.append(draw_separator)


def build_menus(menu_dict, parent_name="TOPBAR_MT_editor_menus"):
    """A simple recursive menu builder without too much logic or extra data.

    Args:
        menu_dict (dict): A dictionary with entries for submenus and operators.
        parent_name (str, optional): What Blender menu should this be nested into. Defaults to "TOPBAR_MT_editor_menus".
    """

    for key in menu_dict:
        if key.count("-") == len(key):
            add_separator(parent_name)
        entry = menu_dict[key]
        icon = 0
        tooltip = ""
        if "icon" in entry:
            icon = imageloader.blender_icon(entry["icon"])
        if "tooltip" in entry:
            tooltip = entry["tooltip"]
        if "menu" in entry:
            bl_idname = add_menu(
                name=key,
                icon_value=icon,
                parent_name=parent_name)
            build_menus(entry["menu"], bl_idname)
        elif "operator" in entry:
            add_operator(
                name=key,
                callback=entry["operator"],
                icon_value=icon,
                tooltip=tooltip,
                parent_name=parent_name)


def an_example():
    """A simple example method to call in our example menu.
    """

    print("An Example!")


def an_example_with(parameter):
    """A simple example method with a parameter to showcase
    how to add it in our menu.

    Args:
        parameter (str, int, float): We will call print() on this.
    """

    print(parameter)


menu_hierarchy = {
    "My Menu": {
        "icon": "heart.png",
        "menu": {
            "A Menu Entry": {
                "icon": "arrow.png",
                "tooltip": "An example of a menu entry",
                "operator": an_example},
            "Another": {
                "icon": "arrowBlue.png",
                "tooltip": "An example of a menu entry with parameters",
                "operator": partial(an_example_with, "This works!")},
            "----": {},
            "A Sub Menu": {
                "menu": {
                     "With One More Entry": {
                        "operator": partial(an_example_with, "This works too!"),
                        "tooltip": "I even have a tooltip"}
                        }
                    }
                }
            }
}


def register():
    global imageloader
    if imageloader is None:
        imageloader = ImageLoader()
    build_menus(menu_hierarchy)


def unregister():
    global imageloader
    if imageloader is not None:
        imageloader.unregister()
        imageloader = None


if __name__ == "__main__":
    register()
