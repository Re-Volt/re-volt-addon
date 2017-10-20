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

---

## Animation Slots

### Slot

The animation slot to display in the panel. The actual animation is set by the
texture number/page.

### Frames

The amount of frames you want to use for the animation. For example, set this to
`32` in order to access frames `0` to `31`.

---

## Animation Frame

### Frame

The frame to display in the panel.

### Preview

Click the Preview button to preview the frame's UV on the currently selected face. The buttons next to it go back or advance one frame and then preview the UV of that frame on the currently selected face.

### Texture

The texture page number this animation frame uses.

### Duration

The duration of the frame or the delay until the next frame shows up.

## Animate

Functions for automatically generating animations.

### Transform Animation

Interpolates the UV coordinates between two given frames. (Animates from point A to B.)

#### Start Frame

The start frame the animation starts from. This frame will not be changed.

#### End Frame

The frame the animation ends on. This frame will not be changed. To achieve a perfectly looping animation, it's sometimes necessary to leave the last frame out. To do so, decrease the amount of frames of the animation by 1.

#### Frame Duration

The duration of all resulting frames.

#### Texture

The texture page applied to all resulting frames.

### Grid Animation

Lays out animation frames on a grid, much like the mars animation in Museum 2.

#### Start Frame

The frame the animation starts at.

#### X Resolution

The width of the grid.

#### Y Resolution

The height of the grid.

#### Frame Duration

The duration of all resulting frames.

#### Texture

The texture page applied to all resulting frames.

---

## UV

### UV to Frame

Takes the UV coordinates of the currently selected face and applies them to the texture animation frame.

### Coordinates

The UV mapping for the currently displayed frame. For triangular faces, UV3 will
be ignored.