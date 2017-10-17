[$\leftarrow$ Back](../index.html)

---

# Texture Animation

[TOC]

An edit panel for texture animations. The animations themselves are saved in the
scene, not the selected object. It is only accessible in edit mode to provide
tools to use existing polygons and UV mapping to create an animation.

## Total Slots

The total amount of texture animations you would like to use.  
For example, set this to `3` to use slots `0`, `1` and `2`.

The maximum amount is 10 since a polygon's animation is determined by the
texture number.

## Animation Slots

### Slot

The animation slot to display in the panel. The actual animation is set by the
texture number/page.

### Frames

The amount of frames you want to use for the animation. For example, set this to
`32` in order to access frames `0` to `31`.

## Animation Frame

### Frame

The frame to display in the panel.

### Texture

The texture page number this animation frame uses.

### Duration

The duration of the frame or the delay until the next frame shows up.

## UV

### UV to Frame

Takes the UV coordinates of the currently selected face and applies them to the texture animation frame.

### Frame to UV

Takes the UV coordinates of the current frame and applies them to the currently selected face.

### Coordinates

The UV mapping for the currently displayed frame. For triangular faces, UV3 will
be ignored.