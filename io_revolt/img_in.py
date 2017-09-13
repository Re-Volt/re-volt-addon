import bpy
import os

def load_image(filepath):
    # Guess texture name and path
    texture_name = os.path.basename(filepath)

    # Get image if it already exists
    image = bpy.data.images.get(texture_name)
    # Loads image if it doesn't exit yet
    if not image:
        if os.path.exists(filepath):
            image = bpy.data.images.load(filepath)
            # Sets a fake user because it doesn't get automatically set
            image.use_fake_user = True
        else:
            print("Texture not found: ", filepath)
            # Creates a dummy texture
            bpy.ops.image.new(name=texture_name, width=512, height=512,
                              generated_type="UV_GRID")
            image = bpy.data.images.get(texture_name)

    return image

def import_file(filepath):
    return load_image(filepath)
