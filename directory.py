import os
import shutil
import zipfile

def changePWD(newpath):
    try:
        os.chdir(newpath)
        return []
    except:
        path = getPWD() + f'\\{newpath}'
        path = path.replace('\\', '/')
        return ["1f401268Error!", "Cannot find path %r" %(path)]

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

def move(_path):
    _path = _path.strip()
    _path = _path.split()
    try:
        newpath = shutil.move(_path[0], _path[1])
        return []
    except:
        return ["1f401268Error!", "Cannot find the file or path specified"]

def rename(nameContent):
    nameContent = nameContent.strip()
    name, newname = nameContent.split()
    try:
        os.rename(name, newname)
        return []
    except:
        return ["1f401268Error!", "Cannot find the file or folder specified"]

def removeFile(file):
    file = file.strip()
    try:
        os.unlink(file)
        return []
    except:
        return ["1f401268Error!", "Cannot find the file specified"]

def removeDir(direc):
    direc = direc.strip()
    try:
        shutil.rmtree(direc)
        return []
    except:
        return ["1f401268Error!", "Cannot find the directory specified"]

def makeDir(name):
    name = name.strip('\\/:*?"<>| ')
    try:
        os.makedirs(name)
        return []
    except:
        return ["1f401268Error!"]

def makeFile(name):
    name = name.strip('\\/:*?"<>| ')
    try:
        with open(name, 'w') as f:
            f.close()
        return []
    except PermissionError:
        return ['1f401268%r is exist' %(name)]
    except:
        return ["1f401268Error!"]

def getContent(name):
    try:
        with open(name) as f:
            content = f.readlines()
            for i in range(len(content)):
                content[i] = content[i].rstrip()
        return content
    except UnicodeDecodeError:
        return ["1f401268File Error!", \
        "Something went wrong when trying to get content %r" %(name)]
    except:
        return ["1f401268Error!", "Cannot find the file specified"]

def checkPath(_path):
    try:
        if os.path.exists(r'{}'.format(_path)):
            return ["7084338aValid path"]
        else:
            return ["1f401268Invalid path"]
    except:
        return ["1f401268Invalid path"]

def checkDir(_path):
    try:
        if os.path.isdir(r'{}'.format(_path)):
            return ["7084338aDirectory is exist"]
        else:
            return ["1f401268Directory is not exist"]
    except:
        return ["1f401268Directory is not exist"]

def checkFile(_path):
    try:
        if os.path.isfile(r'{}'.format(_path)):
            return ["7084338aFile is exist"]
        else:
            return ["1f401268File is not exist"]
    except:
        return ["1f401268File is not exist"]

def unzipAll(content):
    content = content.split()
    if len(content) == 2:
        extractTo = content[1]
    else:
        extractTo = 0
    try:
        zipFile = zipfile.ZipFile(content[0])
        if extractTo == 0:
            zipFile.extractall()
        else:
            zipFile.extractall(r'{}'.format(content[1]))
        zipFile.close()
        return []
    except FileNotFoundError:
        return ['1f401268File %r Not Found' %(content[0])]
    except zipfile.BadZipFile:
        return ['1f401268File %r is not a zip file' %(content[0])]
    except:
        return ['Something went wrong when trying to unzip file %r' %(content[0])]

def unzip(content):
    content = content.split()
    if len(content) < 2:
        return unzipAll(''.join(content))
    else:
        if len(content) == 3:
            extractTo = content[-1]
        else:
            extractTo = 0
        try:
            zipFile = zipfile.ZipFile(content[1])
            if extractTo == 0:
                zipFile.extract(content[0])
            else:
                zipFile.extract(content[0], extractTo)
            zipFile.close()
            return []
        except FileNotFoundError:
            return ['1f401268File %r Not Found' %(content[1])]
        except zipfile.BadZipFile:
            return ['1f401268File %r is not a zip file' %(content[1])]
        except KeyError:
            return ['1f401268There no item named %r in the archive' %(content[0])]
        except:
            return ['Something went wrong when trying to unzip file %r' %(content[1])]