#reload(__import__('remote-texture'))

# Modify textures to use remote destinations.
import maya.cmds as cmds
import re, os, hashlib, urllib2, datetime, json

def cache_file(dest):
	#ensure Cache exists
	base = os.path.dirname(os.path.realpath(__file__))
	cache = os.path.join( base, "cache")
	if not os.path.exists(cache):
		os.makedirs(cache)
	uid = hashlib.sha224(dest).hexdigest()
	uidPath = os.path.join( cache, uid) # Unique path for the file to sit in
	fileName = dest.split('/')[-1]
	filePath = os.path.join( uidPath, fileName ) # Path to the cache file
	metaPath = os.path.join( uidPath, "meta.txt") # Path for file information
	if os.path.isfile(filePath):
		return filePath
	else:
		try:
			# Create unique directory for our files
			if not os.path.exists(uidPath):
				os.makedirs(uidPath)
			# Download File
			u = urllib2.urlopen(dest)
			f = open(filePath, "wb")
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
				# Store meta information from the file
				metaData = { "downloaded" : datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), "url" : dest, "name" : fileName }
				m = open(metaPath, "w")
				m.write(json.dumps(metaData))
				m.close()
				return filePath
		except urllib2.HTTPError, e:
			print "Url does not work. Sorry. :(", e
	return False

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
		if cachePath:
			cmds.setAttr("%s.fileTextureName" % node, cachePath, type="string")
		else:
			cmds.setAttr("%s.fileTextureName" % node, "", type="string")

cmds.scriptJob( ie=check_last_action)
print "Remote Texture is watching for http files..."
