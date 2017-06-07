import os
import shutil

def changePWD(newpath):
    try:
        os.chdir(newpath)
        return 1
    except:
        return 0

def getPWD():
    return os.getcwd()

def getList():
    ls = list(os.walk(getPWD()))[0][1:]
    lss = []
    for fol in ls[0]:
        lss.append("Folder: " + fol)
    for file in ls[1]:
        lss.append("File  : " + file)
    return lss

def move(path):
    path = path.strip()
    path = path.split()
    try:
        newpath = shutil.move(path[0], path[1])
        return 1
    except:
        return 0

def rename(nameContent):
    nameContent = nameContent.strip()
    name, newname = nameContent.split()
    try:
        os.rename(name, newname)
        return 1
    except:
        return 0

def removeFile(file):
    file = file.strip()
    try:
        os.unlink(file)
        return 1
    except:
        return 0

def removeDir(direc):
    direc = direc.strip()
    try:
        shutil.rmtree(direc)
        return 1
    except:
        return 0