import os
from .parameters import read_parameters

def get_texture_path(filepath, tex_num):
    """ Gets the full texture path when given a file and its
        polygon texture number.
    """
    path, fname = filepath.rsplit(os.sep, 1)
    folder = filepath.split(os.sep)[-2]

    if not os.path.isdir(path):
        return None

    # The file is part of a car
    if "parameters.txt" in os.listdir(path):
        params = read_parameters(os.path.join(path, "parameters.txt"))
        tpage = params["tpage"].replace("\\", os.sep).split(os.sep)[-1]
        return os.path.join(path, tpage)
    # The file is part of a track
    elif is_track_folder(path):
        tpage = filepath.split(os.sep)[-2].lower() + chr(97 + tex_num) + ".bmp"
        return os.path.join(path, tpage)
    else:
        return os.path.join(path, "dummy{}.bmp".format(chr(97 + tex_num)))

def is_track_folder(path):
    for f in os.listdir(path):
        if ".inf" in f:
            return True
