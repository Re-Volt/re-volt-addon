# Blender Add-On for Re-Volt File Formats

* [Features](#features)
* [Installation](#installation)
* [Documentation](#documentation)
* [Known Issues](#known-issues)

## Features

* **Import and Export PRM**:  
Mesh, UV, vertex colors, texture, face properties and lods (level of detail)

* **Import Cars from parameters.txt**:  
Import the car model and wheels from parameters.txt files.

* **Import World (.w)**:
Import Re-Volt level mesh files.

* **Mesh Editing Tools**:  
Edit face properties and vertex colors.

* **Generate Shadows**:
Generate shadow textures and coordinates for in-game use with just one click.

* **Shade Meshes**:
Shade meshes by baking light to vertex colors with just one click.

## Installation
Find a detailed guide [here](https://yethiel.github.io/re-volt-addon/installation).  
Requires Blender 2.78 or newer.  
Move the `io_revolt` folder to Blender's addons folder, e.g:  
`C:\Program Files\Blender Foundation\Blender\2.79\scripts\addons\io_revolt`  
or  
`/home/marv/.config/blender/2.78/scripts/addons/io_revolt` (folder might not exist yet)

Then activate the add-on in the Blender preferences (`CTRL` `ALT` `U`),
open the _Add-Ons_ tab and search for Re-Volt. Check the checkbox in the top left.  
Optionally, click _Save User Settings_ in the bottom left.

## Documentation
The documentation can be foud [here](https://yethiel.github.io/re-volt-addon/).

## Known Issues
* UV Unwrap reset is broken due to a [Blender Bug](https://developer.blender.org/T52723). Get Blender 2.79 from [here](https://builder.blender.org/download/) to solve the issue.
