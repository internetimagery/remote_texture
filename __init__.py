#reload(__import__('remote-texture'))

# Modify textures to use remote destinations.
import maya.cmds as cmds
import re, os, hashlib, urllib2

def cache_file(dest):
	#ensure Cache exists
	base = os.path.dirname(os.path.realpath(__file__))
	cache = os.path.join( base, "cache")
	if not os.path.exists(cache):
		os.makedirs(cache)
	uid = hashlib.sha224(dest).hexdigest()
	uidPath = os.path.join( cache, uid)
	if not os.path.isfile(uidPath):
		try:
			# Download File
			fileName = dest.split('/')[-1]
			u = urllib2.urlopen(dest)
			f = open(uidPath, "wb")
			meta = u.info()
			fileSize = int(meta.getheaders("Content-Length")[0])
			allowed = ['image/jpg','image/jpeg','image/png','image/gif'] # List of allowed file types
			fileType = meta.getheaders("Content-Type")[0]
			if fileType in allowed: # Only allow certain files
				print "Downloading: %s Bytes: %s" % (fileName, fileSize)
				fileSizeDL = 0
				block_sz = 8192
				while True:
					buffer = u.read(block_sz)
					if not buffer:
						break
					fileSizeDL += len(buffer)
					f.write(buffer)
					status = r"[%8d] - [%3.2f%%]" % (fileSizeDL, fileSizeDL * 100. / fileSize)
					status = status + chr(8)*(len(status)+1)
					print status
				print "Download Complete."
				f.close()
		except urllib2.HTTPError, e:
			print "Url does not work. Sorry. :(", e
	return uidPath

global preparedRegex
preparedRegex = re.compile("^setAttr.*(file\d+)\.fileTextureName\\s\"(https?://.*)\"")
# Check the most recent action for filename changes
def check_last_action():
	global preparedRegex
	# Looking for: setAttr -type "string" file1.fileTextureName "filename";
	# data = re.findall("^setAttr.*(file\d+)\.fileTextureName\\s\"(https?://.*)\"", cmds.undoInfo( q=True, un=True ), re.S)
	data = preparedRegex.findall(cmds.undoInfo( q=True, un=True ))
	if data:
		node = data[0][0]
		path = data[0][1]
		cachePath = cache_file(path)
		cmds.setAttr("%s.fileTextureName" % node, cachePath, type="string")
		print "%s's path changed to %s from %s" %( node, cachePath, path )

cmds.scriptJob( ie=check_last_action, ro=True )
print "Remote Texture is watching for http files..."