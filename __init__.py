#reload(__import__('remote-texture'))

# Modify textures to use remote destinations.
import maya.cmds as cmds
import re, os, md5, urllib2

def cache_file(dest):
	#ensure Cache exists
	base = os.path.dirname(os.path.realpath(__file__))
	cache = os.path.join( base, "cache")
	if not os.path.exists(cache):
		os.makedirs(cache)
	uid = md5.new(dest).hexdigest()
	uidPath = os.path.join( cache, uid)
	if not os.path.isfile(uidPath):
		try:
			# Download File
			fileName = dest.split('/')[-1]
			u = urllib2.urlopen(dest)
			#f = open(uidPath, "wb")
			meta = u.info()
			fileSize = int(meta.getheaders("Content-Length")[0])
			allowed = ['image/jpg','image/jpeg','image/png','image/gif']
			fileType = meta.getheaders("Content-Type")[0]
			#if fileType in allowed:
			
#			print "Downloading: %s Bytes: %s" % (file_name, file_size)
	
#			file_size_dl = 0
#			block_sz = 8192
#			while True:
#				buffer = u.read(block_sz)
#				if not buffer:
#					break
#				file_size_dl += len(buffer)
#				f.write(buffer)
#				status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
#				status = status + chr(8)*(len(status)+1)
#				print status,
		except urllib2.HTTPError, e:
			print "Url does not work. Sorry. :(", e
#f.close()	
		

def check_last_action():
	# Looking for: setAttr -type "string" file1.fileTextureName "filename";
	#data = re.findall("^setAttr.*(file\d+)\.fileTextureName\\s\"(https?://.*)\"", cmds.undoInfo( q=True, un=True ), re.S)
	#if data:
	#	node = data[0][0]
	#	path = data[0][1]
	#	print node, path
	cache_file("http://icons.iconarchive.com/icons/artdesigner/gentle-romantic/512/heart-icon.pngg")	



cmds.scriptJob( runOnce=True, ie=check_last_action )