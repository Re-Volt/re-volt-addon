# Blender Add-On for Re-Volt File Formats

* [Documentation](#documentation)
* [Features](#features)

Please download the [**dev**](https://github.com/Yethiel/re-volt-addon/tree/dev) branch for now and use it with a **nightly build of Blender 2.79** from [builder.blender.org](http://builder.blender.org).

The next stable version of the add-on will be released as soon as there is a new version of Blender that includes a [fix for the UV Reset bug](https://developer.blender.org/T52723) and the [4-value vertex color layers](https://developer.blender.org/rBaae8e211006a1d9099397727b48201b865504750).

## Documentation
The documentation can be found [here](https://yethiel.github.io/re-volt-addon/).

## Features

* **Import and Export Meshes (.prm/.m)**:  
Mesh, UV, vertex colors, texture, face properties and lods (level of detail)

* **Import Cars from parameters.txt**:  
Import the car model and wheels from parameters.txt files.

* **Import and Export World (.w)**:
Import and export Re-Volt level mesh files including boundary boxes, environment colors and texture animations.

* **Import and Export Collision (.ncp)**:
Import and export Re-Volt collision files, properties and materials.

* **Mesh Editing Tools**:  
Edit face properties and vertex colors.

* **Generate Shadows**:
Generate shadow textures and coordinates for in-game use with just one click.

* **Shade Meshes**:
Shade meshes by baking light to vertex colors with just one click.
