# GUI
# Tools Panel
Open/Close the tools panel using `T`. The Re-Volt tab can be found at the very
bottom.

The tools panel will show different tools and properties depending on the mode.

* [Object Mode](#object-mode)
* [Edit Mode](#edit-mode)

## Object Mode

In Object Mode, the following panels are available:

+ [Import/Export](#import-export)
+ [Light and Shadow](#light-and-shadow)

### Import/Export

#### Buttons
There are two buttons, one for import and one for export. They have the same
functions as the menu entries in the File -> Import/Export menus.

#### Settings
Import and Export settings can be found right beneath the buttons.

##### Triangulate n-gons
Triangulates faces with more than 4 vertices (also called n-gons).  
This will only affect the exported object, the mesh itself will not be
triangulated.  
Deselecting this might result in broken exports.

### Light and Shadow

#### Shade Object
Shades a mesh by baking light to the vertex color layer.

##### Orientation
Sets the orientation of the lights. The following options are available:  
**Z (Vertical)**: Places lights above and beneath the selected object.  
**Y (Horizontal)**: Places lights in the front and the back of the selected
object  
**X (Horizontal)**: Places lights on the left and right of the selected object.

##### Direction
Shows where the lights will be placed, depending on the chosen orientation.

##### Light
Three options: Hard (sun, more contrast), Soft (hemisphere, smoother) and None.  
The **hard** option emits light in a distinct direction
([Blender docs](https://docs.blender.org/manual/de/dev/render/blender_render/lighting/lamps/sun/introduction.html)).  
The **soft** option emits light from a hemisphere which makes the model evenly lit
([Blender docs](https://docs.blender.org/manual/de/dev/render/blender_render/lighting/lamps/hemi.html)).

##### Intensity
This defines the intensity of the light sources. This is the same setting as the lamp's energy.

#### Generate Shadow Texture

With this feature you can create shadows that are ready for use in-game. The shadows are negative which is a requirement by the game.  
The add-on creates the shadows with ray-tracing and then baking them to an automatically sized textured plane (takes child objects into account).  
To save the shadows, go into the UV/Image Editor, select the shadow (most recenty try has the highest number, e.g. Shadow.420) and then click Image -> Save as Image.

**Warning**: Start with low-quality settings first as Blender might hang a while during the creation of a shadow. If it appears to freeze, wait a few minutes. Depending on the settings you chose, it might take a while.

##### Method
There are two options:  
_Default_ (Adaptive QMC), which is the faster option. I recommend this for testing the shadow settings.  
_High Quality_ (Constant QMC), which is the slower and less-grainy option. I recommend using this when you're done tweaking your shadow settings.

##### Quality
The amount of samples the shadow is rendered with (number of samples taken extra).

##### Softness
Light size for ray shadow sampling.

##### Resolution
The resolution of the resulting texture (height and width).

##### Table
Shadow coordinates for use in parameters.txt of cars. Click to select all, then CTRL C to copy.

## Edit Mode

### Face Properties
The list of properties is put together as follows:  
#### Checkbox
Enable or disable the property for all selected faces. The checkbox is checked when _all_ selected faces have this property.  
#### Number
Indicates how many of the selected faces have this property.  
#### Property Name
Hover the property name to find out more about the property.
#### Select (sel) button
Click to select/deselect all faces with this property.  
#### Texture
Sets the texture number for all selected faces. `-1` if numbers of selected faces don't match.

### Vertex Colors
Vertex colors will be set depending on the selection mode.  
Vertex, edge and face select modes each have different effects.
#### Color Wheel
An easy to access color selector to select the color hue and shade.  
The _Color_ button sets the color to the selected faces.  
Click on the color preview to the left of the _Color_ button to get a more detailed color wheel that supports RBG, HSV and Hex values and a color picker.

#### Shade buttons
These buttons can be used for easily shading a mesh. They range from black to white.
