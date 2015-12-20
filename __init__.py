# Download textures if URLS are found in filenames

import re
import shutil
import os.path
import urllib2
import hashlib
import tempfile
import maya.cmds as cmds

TEXTURE_FOLDER = "Online_Textures"
URL = re.compile(r"^https?://")

def get_textures():
    """ Get all textures in the scene """
    nodes = cmds.ls(exactType="file") or []
    for a in nodes:
        yield a, cmds.getAttr("%s.fileTextureName" % a)

def set_texture(node, path):
    """ Set texture """
    cmds.setAttr("%s.fileTextureName" % node, path, type="string")

def download(url, restricted_to=['image/jpg','image/jpeg','image/png','image/gif']):
    """ Download URL data """
    try:
        u = urllib2.urlopen(url)
        meta = u.info() # Get metadata
        dl_size = int((meta.getheaders("Content-Length") or [0])[0])
        dl_type = (meta.getheaders("Content-Type") or [None])[0]
        dl_name = url.split('/')[-1]


        if dl_type and dl_type not in restricted_to: raise IOError, "Incorrect File Type"
        print "Downloading: %s Bytes: %s" % (dl_name, dl_size or "Unknown Size")

        downloaded = 0
        while True:
            buff = u.read(8192)
            if not buff:
                break
            downloaded += len(buff)
            print "[%8d] - [%3.2f%%]" % (downloaded, (downloaded * 100.0 / dl_size) if dl_size else 100)
            yield buff

        print "Download Complete."
    except urllib2.HTTPError, e:
        raise IOError, e


def main():
    """ Check for files """
    scene = cmds.file(q=True, sn=True) or None
    if scene: # Don't do anything without a scene saved.
        textures = dict((a, b) for a, b in get_textures() if URL.search(b))
        if textures: # We found something!
            folder = os.path.realpath(os.path.join(os.path.dirname(scene), TEXTURE_FOLDER))
            if not os.path.isdir(folder):
                os.mkdir(folder)
            for node, url in textures.iteritems():
                try:
                    with tempfile.SpooledTemporaryFile() as tmp:
                        md5 = hashlib.md5()
                        for data in download(url):
                            md5.update(data)
                            tmp.write(data)
                        ext = url.split(".")[-1]
                        name = md5.hexdigest() + ".%s" % ext if ext else ""
                        path = os.path.join(folder, name)
                        if not os.path.isfile(path): # Doesn't exist
                            with open(path, "w") as f:
                                tmp.seek(0)
                                f.write(tmp.read())
                        set_texture(node, path.replace("\\", "/"))
                except IOError as e:
                    print "Warning:", e


if __name__ == '__main__':
    main()
