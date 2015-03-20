#reload(__import__('remote-texture'))

# Modify textures to use remote destinations.
import maya.cmds as cmds
import re, os

def cache_file(path):
	#ensure Cache exists
	base = os.path.dirname(os.path.realpath(__file__))
	cache = os.path.join( base, "cache")
	if not os.path.exists(cache):
		os.makedirs(cache)

def check_last_action():
	# Looking for: setAttr -type "string" file1.fileTextureName "filename";

	data = re.findall("^setAttr.*(file\d+)\.fileTextureName\\s\"(https?://.*)\"", cmds.undoInfo( q=True, un=True ), re.S)
	#if data:
	#	node = data[0][0]
	#	path = data[0][1]
	#	print node, path
	cache_file("stuff")	



cmds.scriptJob( runOnce=True, ie=check_last_action )