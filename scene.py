# Get scene information

import maya.cmds as cmds

def get_textures():
    """ Get all textures in the scene """
    nodes = cmds.ls(exactType="file") or []
    return dict((a, cmds.getAttr("%s.fileTextureName" % a)) for a in nodes)

def set_texture(node, path):
    """ Set texture """
    cmds.setAttr("%s.fileTextureName" % node, path, type="string")


if __name__ == '__main__':
    print get_textures()
