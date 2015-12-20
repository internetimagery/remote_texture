# Simple file downloader
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

import os.path
import urllib2

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

if __name__ == '__main__':
    # Testing
    import tempfile
    url = "http://internetimagery.com/img/nav/challenges_button.png"
    with tempfile.TemporaryFile() as tmp:
        for data in download(url):
            tmp.write(data)
        tmp.seek(0)
        print "size of DL", len(tmp.read())
