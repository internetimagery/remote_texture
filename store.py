# Store file and get link

import shutil
import os.path
import hashlib

def save(file_path, folder_path):
    """ Save file into folder without duplicate """
    md5 = hashlib.md5()
    with open(file_path, "r") as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            md5.update(data)
    name = md5.hexdigest()

if __name__ == '__main__':
    import tempfile
    path = os.path.realpath(__file__)
    tmp_dir = tempfile.t
