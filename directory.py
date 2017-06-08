import os
import shutil
import zipfile

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

def makeDir(name):
    name = name.strip('\\/:*?"<>| ')
    try:
        os.makedirs(name)
        return 1
    except:
        return 0

def makeFile(name):
    name = name.strip('\\/:*?"<>| ')
    try:
        with open(name, 'w') as f:
            f.close()
        return 1
    except:
        return 0

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

def checkPath(path):
    try:
        if os.path.exists(path):
            return 1
        else:
            return 0
    except:
        return 0

def checkDir(path):
    try:
        if os.path.isdir(path):
            return 1
        else:
            return 0
    except:
        return 0

def checkFile(path):
    try:
        if os.path.isfile(path):
            return 1
        else:
            return 0
    except:
        return 0

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