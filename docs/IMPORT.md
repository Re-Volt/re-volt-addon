# Import

## Importing Files
Re-Volt files can be imported via the File menu (File -> Import -> Re-Volt).

## Imported Meshes (PRM)

### Mesh Data
An object with the mesh will be linked to the current scene. Meshes consist of
quads and tris.

### UV Map
The UV map of the mesh can be found on the default UV layer (UVMap).

### Vertex Colors
The vertex colors can be found on the Col and Alpha layers.  
On the alpha channel, white is fully transparent while black is opaque.

### Level of Detail (LOD)
If a PRM file includes mulitple meshes, all of them will be imported.  
A suffix will be appended to the mesh name ("|q0" is the highest quality,
"|q3 is a lower quality").  
A fake user will be assigned to them so they're not lost when saving the
file.
