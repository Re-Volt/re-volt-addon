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
Helper functions that work closely with Blender can be found here.

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

## `rvfiles.py`
Functions for working with the Re-Volt folder structure to locate textures and
car/level files.  
Helper functions that have nothing to do with Blender can be found here.

## `rvstruct.py`
Classes for Re-Volt's binary files (reads and exports, from rvtools).  
This actually imports and exports Re-Volt files.
