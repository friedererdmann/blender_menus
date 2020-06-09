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

import bpy
from functools import partial


def add_menu(name, parent_name="TOPBAR_MT_editor_menus"):
    """Adds a menu class and adds it to any menu.

    Args:
        name (str): Name of the menu
        parent_name (str, optional): What Blender menu should this be added into. Defaults to "TOPBAR_MT_editor_menus".
    """

    def draw(self, context):
        pass

    def menu_draw(self, context):
        self.layout.menu(my_menu_class.bl_idname)

    bl_idname = "MENU_MT_{0}".format(name.replace(" ", ""))
    full_parent_name = "bpy.types.{0}".format(parent_name)

    parent = eval(full_parent_name)

    my_menu_class = type(
        "DynamicMenu{0}".format(name),
        (bpy.types.Menu,),
        {
            "bl_idname": bl_idname,
            "bl_label": name
        })

    bpy.utils.register_class(my_menu_class)
    parent.append(menu_draw)

    return bl_idname


def add_operator(name, callback, parent_name="TOPBAR_MT_editor_menus"):
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
        self.layout.operator(my_operator_class.bl_idname)

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
        menu_dict (dict): A dictionary with keys for menu entries and callables or dictionarys as values.
        parent_name (str, optional): What Blender menu should this be nested into. Defaults to "TOPBAR_MT_editor_menus".
    """
    for entry in menu_dict:
        if type(menu_dict[entry]) is dict:
            bl_idname = add_menu(entry, parent_name)
            build_menus(menu_dict[entry], bl_idname)
        if entry.count("-") == len(entry):
            add_separator(parent_name)
        if callable(menu_dict[entry]):
            add_operator(entry, menu_dict[entry], parent_name)


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
        "A Menu Entry": an_example,
        "Another": partial(an_example_with, "This works!"),
        "----------": "This is a separator indicated by a -",
        "A Sub Menu": {
            "With One More Entry": partial(an_example_with, "This works too!")
        }
    }
}


build_menus(menu_hierarchy)


def register():
    pass


def unregister():
    pass
