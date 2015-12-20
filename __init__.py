# Download textures if URLS are found in filenames
# Created By Jason Dixon. http://internetimagery.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import re
import time
import shutil
import os.path
import urllib2
import hashlib
import tempfile
import threading
import maya.cmds as cmds
import maya.utils as utils

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
            cmds.refresh()

        print "Download Complete."
    except urllib2.HTTPError, e:
        raise IOError, e

def background(func, interval=2):
    """ Run function over and over in background """
    block = threading.Semaphore() # Don't throttle Maya

    def run():
        while True:
            time.sleep(interval)
            block.acquire()
            utils.executeDeferred(lambda: cmds.scriptJob(ro=True, ie=(lambda: block.release(), func())))

    threading.Thread(target=run).start()
    print "Running %s" % repr(func)

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
                set_texture(node, "") # Keep broken urls from continuous checking
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
