# Light and Shadow

![Light and Shadow Panel](./tools-panel/img/light-shadow.png)

## Shade Object
Shades a mesh by baking light to the vertex color layer.

**Orientation**:  
Sets the orientation of the lights. The following options are available:  
- **Z (Vertical)**: Places lights above and beneath the selected object.  
- **Y (Horizontal)**: Places lights in the front and the back of the selected
object  
- **X (Horizontal)**: Places lights on the left and right of the selected object.

**Direction**:  
Shows where the lights will be placed, depending on the chosen orientation.

**Light**:  
Three options: Hard (sun, more contrast), Soft (hemisphere, smoother) and None.  
- The **hard** option emits light in a distinct direction
([Blender docs](https://docs.blender.org/manual/de/dev/render/blender_render/lighting/lamps/sun/introduction.html)).  
- The **soft** option emits light from a hemisphere which makes the model evenly lit
([Blender docs](https://docs.blender.org/manual/de/dev/render/blender_render/lighting/lamps/hemi.html)).

**Intensity**:  
This defines the intensity of the light sources. This is the same setting as the lamp's energy.

---

## Generate Shadow Texture

With this feature you can create shadows that are ready for use in-game. The shadows are negative which is a requirement by the game.

The add-on creates the shadows with ray-tracing and then baking them to an automatically sized textured plane (takes child objects into account).

To **save the shadows**, go into the _UV/Image Editor_, select the shadow (most recenty try has the highest number, e.g. Shadow.420) and then click _Image -> Save as Image_.

**Warning**: Start with low-quality settings first as Blender might hang a while during the creation of a shadow. If it appears to freeze, wait a few minutes. Depending on the settings you chose, it might take a while.

**Method**:  
There are two options:  
- **Default** (Adaptive QMC), which is the faster option. I recommend this for testing the shadow settings.  
- **High Quality** (Constant QMC), which is the slower and less-grainy option. I recommend using this when you're done tweaking your shadow settings.

**Quality**:  
The amount of samples the shadow is rendered with (number of samples taken extra).

**Softness**:  
Light size for ray shadow sampling.

**Resolution**:  
The resolution of the resulting texture (height and width).

**Table**:  
Shadow coordinates for use in parameters.txt of cars. Click to select all, then CTRL C to copy. 

## Batch Bake Lights

This feature allows you to bake lights in the current scene to instance objects.

**Bake to Model RGB**:  
Whether to bake the color to the Model RGB value. This can be used to darken or tint the instance.

**Bake to Model Env**:  
Whether to bake the color to the Model Env value. This can be used to alter the reflection color of the instance.

**Bake all selected**  
Bakes a full render to all selected objects. This usually takes a long time, Blender freezes until the action is done. A popup will show up when the baking process is complete.
