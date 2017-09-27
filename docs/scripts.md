<!-- TOC START min:1 max:3 link:true update:true -->
- [Included scripts](#included-scripts)
  - [`__init__.py`](#__init__py)
  - [`common.py`](#commonpy)
  - [`img_in.py`](#img_inpy)
  - [`operators.py`](#operatorspy)
  - [`panels.py`](#panelspy)
  - [`parameters.py`](#parameterspy)
  - [`prm_in.py`](#prm_inpy)
  - [`prm_out.py`](#prm_outpy)
  - [`properties.py`](#propertiespy)
  - [`rvstruct.py`](#rvstructpy)
  - [`tools.py`](#toolspy)

<!-- TOC END -->

# Included scripts

## `__init__.py`
Initializes the add-on in Blender.hat way,

## `common.py`
Collection of universal constants and functions.

## `img_in.py`
Imports images and creates dummy textures if it can't find them.

Since images are also used to define the texture number of polygons,
it creates a dummy texture (e.g. dummya.bmp) so the texture can still be set,
even if the texture file doesn't exist.

## `operators.py`
Functions behind user interface buttons.  
This also includes the import and export operators so they are globally
available.  

## `panels.py`
The user interface for the add-on.

## `parameters.py`
Parses parameter files (from rvtools).

## `prm_in.py`
Imports PRM files.

## `prm_out.py`
Exports PRM files.

## `properties.py`
Blender Properties for Re-Volt Objects and getter/setter functions.

## `rvstruct.py`
Classes for Re-Volt's binary files (reads and exports, from rvtools).  
This actually imports and exports Re-Volt files.

## `tools.py`
Contains the functions behind the buttons of the tool panel.
