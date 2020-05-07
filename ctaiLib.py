import os

def joinPath(path1,path2):
    return os.path.join(path1,path2)

def executeCmd(cmd):
    return os.system(cmd)

def listDirCont(path):
    return os.listdir(path)

def userHomeDirPath():
    return os.path.expanduser('~')