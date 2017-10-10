[$\leftarrow$ Back](../index.html)

---

# Changelog

## 2017-10-10

Version [`rva_17.1010`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_17.1010)

* Added Re-Volt file structure specifications to the documentation
* **Fixes**
  * **Light Baking Tool**: Reverse horizontal X direction (light was shining from the wrong direction)
  * **Export .w**, **export .prm**: Apply scale and rotation correctly. Parented objects should now be exported correctly.
* **Debug**
  * Rename bound spheres to cubes
  * Import cubes instead of spheres

## 2017-10-09

Version [`rva_17.1009`](https://github.com/Yethiel/re-volt-addon/releases/tag/rva_17.1009)

* **Export .w**
  * Export complete .w files with meshes, boundary boxes/spheres, env colors and texture animation
* **Texture animation panel**
  * Added buttons for copying UV from and to selected faces.
* **Settings panel completed**
  * *Parent .w meshes to Empty* now disabled by default to avoid confusion
  * New layout
* **Misc**
  * Decreased shadow table accuracy to 4 decimal places

## 2017-10-07

Version `rva_17.1007`

+ **Tool panels**
  + Fixed a bug where the tool panels became unusable after CTRL Z.


+ **Import .w**
  + Bound boxes, bound spheres and big cubes, each of which can be imported on
    different layers
  + Env colors with GUI implementation
+ **Import .prm completed**
  + Apply scale and rotation on export by default (no need for manual apply,
    can be disabled in the options)