# Helpers

![Helpers Panel](./tools-panel/img/helpers.png)

## 3D View

**Texture**:  
Enables texture mode.

**Textured Solid**:  
Enables solid shading mode and enables the textured solid option. This might be better for working with only half-textured models.

## RVGL

**Launch RVGL**:
Starts RVGL in developer mode. The path has to be configured in the add-on settings.

## Texture tools

**Copy project textures**: 
Renaming and checking many image files may be monotonous. This command copies all used track textures from their source to chosen destination track folder and renames them properly for you. 
**Note:** If you chose destination directory same as actual source for textures all files with matching names will be overwritten. 

**Rename track textures**:
All used textures must be named (this is not referring file names) in numerical order in blender's image editor e.g. `0.bmp 1.bmp 2.bmp 3.bmp ... 63.bmp`. This name uniquely identifies each texture, any gap in numeration may cause an issues. Command will assign new name (ID) to each texture. 
**Note:** this may override existing (manual) numeration.
