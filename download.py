# Download texture into the supplied folder

import os.path
import urllib2

def get_link(url):
    """ Download URL data """
    try:
        u = urllib2.urlopen(url)
        meta = u.info() # Get metadata
        dl_size = int((meta.getheaders("Content-Length") or [0])[0])
        allowed = ['image/jpg','image/jpeg','image/png','image/gif'] # List of allowed file types
        dl_type = (meta.getheaders("Content-Type") or [None])[0]
        dl_name = url.split('/')[-1]


        if dl_type and dl_type not in allowed: raise IOError, "Incorrect File Type"
        print "Downloading: %s Bytes: %s" % (dl_name, dl_size or "Unknown Size")

        downloaded = 0
        block = 8192
        while True:
            buff = u.read(block)
            if not buff:
                break
            downloaded += len(buff)

            status = r"[%8d] - [%3.2f%%]" % (downloaded, (downloaded * 100.0 / dl_size) if dl_size else 100)
            print status

            yield buff

        print "Download Complete."
    except urllib2.HTTPError, e:
        raise IOError, e

if __name__ == '__main__':
    # Testing
    import tempfile
    url = "http://internetimagery.com/img/nav/challenges_button.png"
    with tempfile.TemporaryFile() as tmp:
        for data in get_link(url):
            tmp.write(data)
        tmp.seek(0)
        print "size of DL", len(tmp.read())
