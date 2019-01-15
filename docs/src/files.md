# File Specifications

The following files are supported by the add-on:

- [World (`.w`)](#world)
- [Mesh (`.prm`)](#mesh)
- [Collision (`.ncp`)](#collision)
- [Instances (`.fin`)](#instances)
- [Mirror Planes (`.rim`)](#mirror-planes)
- [Hulls (`.hul`)](#hull)
- [Texture Animation Spreadsheets (`.ta.csv`)](#texture-animation-spreadsheets)
- [Car Parameters (`parameters.txt`)](#car-parameters)

## World

File extension: `.w`

See [Mesh](#mesh). The only addition is the environment color list that defines a specularity color for certain polygons if the flag is enabled for them.  

The **environment color** is accessible on a **vertex color layer** called `Env`.
The alpha value of the color is only accessible via the face property editing panel since it's written to a per-face float layer (`EnvAlpha`).

Do note that environment colors are per-polygon. The average color will be sampled from the vertex color layer when an env-enabled polygon is selected.

**Debug**:  
There are [debug options](./tools-panel/settings.html#import-world-w) in the add-on settings (bounding boxes). They are for debug purposes only and they will not affect the export in any way.

---

## Mesh

File extension: `.prm`

**Vertex Color Layers**:  
- `Col`: Color layer
- `Alpha`: Alpha layer (black: translucent, white: opaque)

**UV**:  
Only the uv map called `UVMap` will be exported.

**Textures**:  
The texture file name is used by the game engine to determine the texture number for exported faces. Make sure it's named correctly (e.g. `tracka.bmp`, `car.bmp`). Currently one car texture and up to 64 track textures are supported, all present files must be named in order using scheme presented bellow. Example: `tracka.bmp ... trackk.bmp trackl.bmp` is correct set but `tracka.bmp ... trackk.bmp trackm.bmp` is incorrect - the last file and any further will be not loaded.

- `0       tracka `
- `1       trackb `
- `2       trackc `
- `3       trackd `
- `...            `
- `25      trackz `
- `26      trackaa`
- `27      trackba`
- `...            `
- `51      trackza`
- `52      trackab`
- `53      trackbb`

*Important note*: for convenience add-on changes the imported image names (not file names) in blender's image editor to `<number>.bmp`, please use same convention when adding a new images.

If the imported mesh is a **car mesh**, the texture path will be taken from `parameters.txt`.  
If it's a **level file**, the texture name will be generated from the polygon's texture number and taken from the level folder.  
If a texture file cannot be found, a 512x512 dummy texture will be generated.  
If a texture with the same path already exists, it will be used instead.  

The texture number is also written onto a bmesh integer layer. This layer can be used instead of the texture on the tex layer for exporting (see add-on settings).


**Level of Detail**:  
If a PRM file includes mulitple meshes all of them will be imported.  
A suffix will be appended to the mesh name (`|q0` is the highest quality, `|q3` is a lower quality).  
A fake user will be assigned to them so they're not lost when saving the file.

**Note**: Only car wheels support LoD.

---

## Collision

File extension: `.ncp`

NCP flags and materials are written to the integer layers `NCPFlags` and `Material`. A preview color for the materials is written to the `NCPPreview` vertex color layer.

All objects of the scene will be merged into one mesh and then exported to the file. Objects will be ignored if they're a debug object or have the *ignore* object property set ([Properties Editor](./properties/object/ncp.html)).  
Faces that have the material `NONE` assigned to them will not be exported.  
The vertex color layer called `NCPPreview` will be ignored since it's only for previewing purposes.

A lookup grid will be automatically exported. This can be turned off in the export settings.

---

## Instances

File extension: `.fin`

Instances are [PRM meshes](#mesh) placed around a level. An instance file contains metadata about multiple instances.

**ModelRGB**: Each RGB value ranges from -128 to 127. The color picker in Blender likes values from 0.0 to 1.0 most, that's why the default ModelRGB is (0.5, 0.5, 0.5).

---

## Mirror Planes

TODO

---

## Hull

File extension: `.hul`

**Note**: For importing hull files `qhull` needs to be installed on GNU/Linux (macOS too) in order to import Hulls (on Arch, install it with `sudo pacman -S qhull`, package name may be similar on your distro). The add-on is shipped with qhull.exe for Windows systems, nothing needs to be installed additionally.

Hull files are mainly used for car collision and some other moving objects (some of which can be found in the `models` folder).

Importing a hull file results several Blender objects:  
One (sometimes more) **convex hull** which resembles the car body.  
The **interior** (one per convex hull) consisting of spheres.

**Note**: Vertex and edge data is ignored when importing but written to exported files. Many custom `.hul`s don't include vertex and edge data, apparently the game works without them.

---

## Texture Animation Spreadsheets

TODO

---

## Car Parameters

The add-on currently imports the car's body and wheels and their positions.  
If a wheel file cannot be found, it will be represented with an empty object.

