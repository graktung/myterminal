import os

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