import os
from .parameters import read_parameters

def get_texture_path(filepath, tex_num):
    """ Gets the full texture path when given a file and its
        polygon texture number.
    """
    path, fname = filepath.rsplit(os.sep, 1)

    if not os.path.isdir(path):
        return None

    # The file is part of a car
    if "parameters.txt" in os.listdir(path):
        params = read_parameters(os.path.join(path, "parameters.txt"))
        tpage = params["tpage"].replace("\\", os.sep).split(os.sep)[-1]
        return os.path.join(path, tpage)
    # The file is part of a track
    else:
        tpage = filepath.split(os.sep)[-2].lower() + chr(97 + tex_num) + ".bmp"
        return os.path.join(path, tpage)
