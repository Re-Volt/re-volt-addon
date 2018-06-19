---
title: Re-Volt File Structure
---

## Files
Levels are similar to “Instances”. They consist of two files:  
`level.w`, which is similar to `instance.prm`. It contains the “look” of the level.  
`level.ncp`, which is similar to `instance.ncp` (but not equal). Contains the “feel” (What you cannot see but drive on).

## Coordinate System
The positive X-Axis goes to the right, Y downwards and Z forwards.

## Basic Data Types

`rvfloat` is a 32-bit floating point number,

`rvshort` a 16-bit integer and goes from -32768 to 32767, and

`rvlong` a 32-bit floating point number. (Both `rvshort` and `rvlong` are signed unless explicit marked as unsigned)

## 3D Structures

### Mesh file (.prm)

```c
struct PRM_Mesh {

  rvshort polygon_count;
  rvshort vertex_count;

  Polygon polygons[polygon_count];
  Vertex  vertices[vertex_count];
};
```

### World file (.w)
```c
struct World {

  rvlong       mesh_count;
  Mesh         meshes[mesh_count];

  rvlong       bigcube_count;
  BigCube      bcube[bigcube_count];

  rvlong       animation_count;
  TexAnimation anim[animation_count]

  EnvList   env_list;
};
```

### Mesh (.w)
```c
struct Mesh {

  Vector       bound_ball_center;
  rvfloat      bound_ball_radius;

  BoundingBox  bbox;

  rvshort      polygon_count;
  rvshort      vertex_count;

  Polygon      polygons[polygon_count];
  Vertex       vertices[vertex_count];
};
```

### TexAnimation (.w)
```c
struct TexAnimation {

  rvlong frame_count; // the number of frames per animation
  Frame  frames[animation_count]
};
```

### Frame (.w)
```c
struct Frame {

  rvlong  texture;
  rvfloat delay; // in microseconds
  UV      uv[4];
};
```

### Polygon
```c
struct Polygon {

           rvshort  type;

           rvshort  texture;

           rvshort  vertex_indices[4];
  unsigned rvlong   colors[4];

           UV       texcoord[4];
};
```
**type** is a bit field with the following values:

| Bit-#  | Value | Purpose in .w                      | Purpose in .prm                    |
| :----- | :---- | :--------------------------------- | :--------------------------------- |
| bit 0  | 0x001 | Polygon is quadratic               | Polygon is quadratic               |
| bit 1  | 0x002 | Polygon is double-sided            | Polygon is double-sided            |
| bit 2  | 0x004 | is translucent                     | is translucent                     |
| bit 8  | 0x100 | 0: Alpha, 1: Additive transmarency | 0: Alpha, 1: Additive transmarency |
| bit 10 | 0x400 | unused                             | Disable EnvMapping                 |
| bit 11 | 0x800 | Enable EnvMapping                  | pickup.m: sparkles                 |

**texture** is the number of the texture page (0=levela.bmp, 1=levelb.bmp, …). If set to -1, the object won't have any texture.

**vertex_indices** is a list of three or four indices for the list in the mesh structure. If the polygon is not double-sided, the vertices have to be given in clockwise order. (if you look at it from its “behind”, the points will be ordered ccw, and the poly is invisible)

### Vertex
```c
struct Vertex {

  Vector position;
  Vector normal;
};
```

### Vector
```c
struct Vector {

  rvfloat x;
  rvfloat y;
  rvfloat z;
};
```

### UV
```c
struct UV {

  rvfloat u;
  rvfloat v;
};
```

### BigCube (.w)
```c
struct BigCube {

  Vector  center;
  rvfloat size;

  rvlong  mesh_count;
  rvlong  mesh_indices[mesh_count];
};
```

### NCP (.w)
```c
struct WorldNCP {

  rvshort    polyhedron_count;
  Polyhedron polyhedra[polyhedron_count];

  LookupGrid lookup;
};
```

### Polyhedron (.ncp)
```c
struct Polyhedron {

  rvlong      type;
  rvlong      surface;

  Plane       plane[5];

  BoundingBox bbox;
};
```

### Plane (.ncp)
```c
struct Plane {

  Vector  normal;
  rvfloat distance;
};
```

### Lookup Grid (.ncp)
```c
struct LookupGrid {

  rvfloat    x0;
  rvfloat    z0;

  rvfloat    x_size;
  rvfloat    z_size;

  rvfloat    raster_size;

  LookupList lists[z_size][x_size];
};
```

### Env List (.w)
```c
struct EnvList {

  unsigned rvlong env_color[number of bit-11-polys in file];
};
```

### Bounding Box (.w)
```c
struct BoundingBox {

  rvfloat xlo, xhi;
  rvfloat ylo, yhi;
  rvfloat zlo, zhi;
};
```

### Mirror file (.rim)
```c
struct RIM_File {

  rvshort   entry_count;

  RIM_Entry entries[entry_count];
};
```

### Mirror Entry (.rim)
```c
struct RIM_Entry {
  rvulong     flags;

  Vector      plane_normal;
  rvfloat     plane_distance;

  BoundingBox bbox;

  Vector      vertices[4];
};
```

## Level File Structures

### Position Node File (.pan)
```c
struct PAN {
	rvlong    number_nodes;
    rvlong	  start_node;
    rvfloat   total_distance;

    Node      pos_nodes[number_nodes];
}
```

Position nodes don't consist of much. There is the number of nodes, the ID of the node the track starts with, the total length of the track and a list of Nodes. There is a maximum number of 1024 nodes (limit is hardcoded).

### Node (.pan)
```c
struct Node {
    Vector      position;
    rvfloat     distance;
    rvlong      prev_node_ids[4];
    rvlong      next_node_ids[4];
}
```
The nodes from the Pos. node file are very straightforward. There is a regular vector for its position, a float for the distance to the finish line and two lists of 4 longs that give you the IDs of the previous and next IDs of the nodes the current node is connected to. There is a maximum of 4 links (limit due to file definition). If there is no link, the value(s) are `-1`.

### Instances (.fin)
```c
struct Fin {
    long      instance_count;
    Instance  instaces[instance_count];
}
```

### Instance (.fin)
```c
struct Instance {
    char[9]   name;
    unsigned rvlong   color[3];
    unsigned rvlong   env_rgb[4];
    Byte			  priority;
    Byte			  flag;
    Vector			  position;
    Matrix	          transformation[3f][3f];
}
```

## Sources
+ [Ali's Structure Breakdown (perror.de)](http://perror.de/rv/rvstruct.html)
+ Kay
+ Re-Volt source code