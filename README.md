# Blender Add-On for Re-Volt File Formats

## Features

* **Import and Export PRM**:  
Mesh, UV, vertex colors, texture, face properties and lods (level of detail)

* **Mesh Editing Tools**:  
Edit face properties and vertex colors.

* **Generate Shadows**:
Generate shadow textures and coordinates for in-game use with just one click.

* **Shade Meshes**:
Shade meshes by baking light to vertex colors with just one click.

## Installation
Requires Blender 2.78 or newer.  
Move the `io_revolt` folder to Blender's addons folder, e.g:  
`C:\Program Files\Blender Foundation\Blender\2.79\scripts\addons\io_revolt`  
or  
`/home/marv/.config/blender/2.78/scripts/addons/io_revolt` (folder might not exist yet)

Then activate the add-on in the Blender preferences (`CTRL` `ALT` `U`),
open the _Add-Ons_ tab and search for Re-Volt. Check the checkbox in the top left.  
Optionally, click _Save User Settings_ in the bottom left.

## Known Issues
* UV Unwrap reset is broken due to a [Blender Bug](https://developer.blender.org/T52723)
