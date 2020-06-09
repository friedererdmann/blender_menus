# Blender Menus
A simple menu generator for the Blender UI system

## Testing
Throw into your addon folder, activate the addon (`blender_menu_structure` or "Dynamically created Blender Menu" in the UI) - see the menu!

## Extending the menu
You can very simply just extend the dictionary `menu_hierarchy` if you just want to use the system as is.

### Menu Hierarchy
* ---: Dashes become separators (regardless how many you use)
* "menu" key is how we put in a submenu (as a dictionary value)
* "operator" becomes an operator
* Menus and Operators accept icons (either by Blender keyword or as png from the icon folder)
* Operators accept tooltips

### Functions and Parameters
Your menu entries can provide a function, but no parameters. We provide an example of using partial if you want to pass a function with parameters.

## Extending logic
The `build_menus` and the corresponding `menu_hierarchy` dictionaries are meant as example code. It should be easy from this to extend the logic and build more meaningful menu systems, e.g. checking for naming clashes with operators.

If you want to contribute to this project, please feel free to send back your pushes.

### Lack of proper register and unregister
We do not register and unregister our menu and operator classes properly, so this would be another good step to look into, if you're worried about users loading and unloading your addon or you wanting to re-run the addon with updated menus.
