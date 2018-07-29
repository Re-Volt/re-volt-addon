# Instances

![Instances Panel](./tools-panel/img/instances.png)

The Instances Panel provides some helper tools to make working with instances easier.

---

**Select by data**: Selects all objects with the same object data (mesh) as the currently selected object. You could, for example, place objects around the scene using `ALT`+`D` to create duplicates with shared mesh data and then select all of them.

---

**Rename selected**: Instances that have the same mesh should also have the same name. This renames all selected objects to the name entered in the text field above.

**Select by name**: Selects all objects that contain the name entered in the text field above.

---

**Mark as Instance**: Sets the _is instance_ property for all selected objects. These objects will then be exported when exporting to `.fin`.

**Remove Instance property**: Removes the _is instance_ property for all selected objects so they won't be exported when exporting to `.fin`.