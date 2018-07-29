# Instance Properties

![Instance Properties](./properties/img/props-instance.png)

**Is Instance**: If enabled, the object will be exported to `.fin`. If a `.prm` file with the name of the object doesn't yet exist, it will also be exported to `.prm`.

**Model Color**: Additional or subtractive RGB color. Default is (0.5, 0.5, 0.5). Setting this to 1.0 erases the existing vertex color, 0.5 leaves it where it is and anything closer to 0 darkens the instance.

**EnvColor**: Environment map color and intensity (alpha).

**Hide**: Hides the instances (only collision).

**Don't show in Mirror Mode**: The instance won't be shown if the level is played in mirror mode.

**Is affected by Light**: In-game lights affect the instance.

**No Camera Collision**: The camera will clip through the instance.

**No Object Collision**: The instance won't collide with cars and other moving objects.

**Priority**: If set to anything other than `0`, the instance cannot be turned off using the video options.

**LoD Bias**: Unused