# Changelog 

## 2018-06-

Version [`rva_18.06`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_18.06)

**Topics**: Bugfixes, Tools

- **Fixes**
    - Batch bake should not crash anymore
    - Import and export of .fin properties
- **Additions**
    - Batch Bake section in the Light and Shadow tool panel
    - RVGL Launcher in the Helpers panel. The RVGL path (folder) has to be set in the add-on settings.
- **Modifications**
    - 

## 2018-06-19

Version [`rva_18.0619`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_18.0619)

**Topics**: Bugfixes

- **Fixes**
    - Support loading files with uppercase letters
    - Throw an error message when exceeding polygon/vertex limits for meshes
    - Activate NCP no-collision flag (reported by Kiwi)
- **Modifications**
    - Inverted alpha vertex color layer: Black is translucent, white is opaque. I've done this to resemble the behavior of pure black on textures.

## 2018-04-30

Version [`rva_18.0430`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_18.0430)

**Topics**: Instance (.fin), UI, Bugfixes

- **Additions**
    - **Instances (.fin)**: Export (full support)
    - *Select by name* button in the Instances panel that allows users to select all objects with a similar name
    - *Mark as Instance* button in the Instances panel that sets the instance properties on all selected objects
    - *Batch baking* feature for instance RGB in the Instances panel
    - **Initial hull support**: Import (unfinished)
- **Fixes**
    - Textures are now loaded when importing a mesh from the custom folder (reported by Gotolei)
    - Ensure that NCP layers exist when exporting: All Material layers and Type layers are now kept. This fixes missing materials when exporting NCP. (reported by LoScassatore, Gorgonzola)
    - Export of textures with suffixes like .bmp.001 (reported by Boy80)
- **Modifications**
    - Moved the instances helper section to a dedicated Instances panel.
    - Objects marked as instance (*Is Instance*) will no longer be exported when exporting to .w, use .fin instead
    - Fixed all Re-Volt panels to the top (object and scene properties) so they're easier to find. This makes the add-on a lot more intrusive but most people using this add-on use Blender exclusively for Re-Volt.
    - Message boxes for confirming actions in the helpers panel
    - Texture number face property only shows when *Use Number for Textures* option is enabled
    - *Prefer Solid Textured Mode* is now disabled by default

## 2018-02-25
Version [`rva_18.0225`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_18.0225)

- **Additions**
    - NCP: *Only export selected* option added (check the documentation for details)
- **Fixes**
    - Rewrote the parameters.txt parser, should now load all cars
    - The light panel now only shows up if at least one object is selected
- **Misc**
    - New system for handling import and export errors

## 2018-02-19
Version [`rva_18.0219`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_18.0219)

- **Additions**
    - Instance (.fin) import
    - Batch-rename feature (Helpers panel)
    - *No collision* flag for NCP (face properties)
- **Fixes**
    - Prepared the add-on for 2.79a. All features should now work as expected.
    - Various Import/Export fixes
- **Misc.**
    - Improved UI
    - Documentation is now generated with Ivy

## 2017-11-12

Version [`rva_17.1112`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_17.1112)

- **Fixes**
    - Fixed the following crash: Import mesh, clear .blend, import mesh again (reported by Zorbah)
    - Shadowtable not added to the UI (reported by Mladen)
    - Required vertex color layers weren't created on export ([Issue #16](https://github.com/Yethiel/re-volt-addon/issues/16), reported by progwolff)
- **Additions**
    - NCP: Setting for collision grid size (requested by Zorbah). Higher values = faster export (might slow down the game in return)


## 2017-10-25

Version [`rva_17.1025`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_17.1025)

- **Fixes** (reported by Gotolei)
    - Animation slot count can now be set to 10
    - Frame count for animations reset itself
    - Animation export didn't work in some cases


## 2017-10-24

Version [`rva_17.1024`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_17.1024)

- **Additions**
    - **Texture Animation**: Transform animation feature (animates from frame A to frame B), Grid animation feature (for creating animations like the mars animation found in Museum 2). Added a [resources](http://learn.re-volt.io/tracks-blender/resources) link to the documentation which will include texture animation sheets ready to be used with the add-on.
    - **Re-Export Button**: Press the button next to the Export button to export to the same file again.
- **Fixes**
    - The vertex color picker now picks from selected faces *or* vertices. (Contribution by Boy80)
    - Fixed persisting QUAD flag by removing it from the export mask. (Reported by Boy80)
    - Importing cars with the same texture name resulted in them having the same texture. (Reported by Gotolei)
- **UI**
    - Added icons to panels
    - Moved add-on settings to a separate panel
    - The settings, texture animation and the helpers panel are now collapsed by default
    - Fixed the import/export panel to the top
    - Notifications now have an icon
- **Misc.**
    - Huge code refactoring and some fixes
    - Restructured the documentation

## 2017-10-17

Version [`rva_17.1017`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_17.1017)

- **Additions**
    - **NCP** (collision): Import and export is now supported. The face properties panel has a section for NCP now (face flags and materials).
    - **Settings**: *Prefer Textured Solid mode* setting, enabled by default. This makes the add-on use textured solid mode (easier for editing NCP/untextured meshes).
    - **Import/Export**: Import and export operators now show the matching settings in the bottom left.
    - **Vertex Colors**: Button for getting the color from the active face (requested by Boy80)
- **Fixes**
    - The y coordinates of bounding boxes were swapped.
    - Faces can now be exported with no texture (reported by Boy80).

## 2017-10-10

Version [`rva_17.1010`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_17.1010)

* Added Re-Volt file structure specifications to the documentation
- **Fixes**
    - **Light Baking Tool**: Reverse horizontal X direction (light was shining from the wrong direction)
    - **Export .w**, **export .prm**: Apply scale and rotation correctly. Parented objects should now be exported correctly.
- **Debug**
    - Rename bound spheres to cubes
    - Import cubes instead of spheres

## 2017-10-09

Version [`rva_17.1009`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_17.1009)

- **Export .w**
    - Export complete .w files with meshes, boundary boxes/spheres, env colors and texture animation
- **Texture animation panel**
    - Added buttons for copying UV from and to selected faces.
- **Settings panel completed**
    - *Parent .w meshes to Empty* now disabled by default to avoid confusion
    - New layout
- **Misc**
    - Decreased shadow table accuracy to 4 decimal places

## 2017-10-07

Version `rva_17.1007`

- **Tool panels**
    - Fixed a bug where the tool panels became unusable after CTRL Z.
- **Import .w**
    - Bound boxes, bound spheres and big cubes, each of which can be imported on different layers
    - Env colors with GUI implementation
- **Import .prm completed**
    - Apply scale and rotation on export by default (no need for manual apply, can be disabled in the options)
