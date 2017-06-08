# standard modules
import pygame
import time
from pygame.locals import*
import sys
import random
try:
    import pyperclip
    canCopy = 1
except:
    canCopy = 0

# my modules
import directory

pygame.init()
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)
pygame.display.set_caption('Gr^k-T\'s Python Terminal')

SIZE = width, height = 800, 480
fullLine = 18
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
ERRORCOLOR = 204, 0, 0
BLUE = 0, 0, 205
GREEN = 0, 128, 0
YELLOW = 255, 255, 0
PINK = 255, 0, 255
SCREEN = pygame.display.set_mode(SIZE, RESIZABLE)
myFont = pygame.font.SysFont("consolas", 15)
listColor = [WHITE, RED, BLUE, GREEN, YELLOW, PINK]
changeColor = 0
showCur = 0
colorCur = listColor.pop(listColor.index(random.choice(listColor)))

content = []
contentDisplay = []
listCommand = []
indexListCommand = 0
contentLineCurrent = ''
contentLineCurrentDisplay = '|'
posCursor = 0
currentLine = True
root = 'graktung@blackrose:~# '
camTop = 0
camBot = 0
line = 0

def displayGrakT(colorCur):
    bar = ["  ____     /\ _       _____        _____ _      __         _       _____",
" / ___|_ _|/\| | __  |_   _|      |_   _| |__   \_\_ _ __ | |__   |_   _| __ _   _ _ __   __ _ ",
"| |  _| '__| | |/ /____| |          | | | '_ \ / _` | '_ \| '_ \    | || '__| | | | '_ \ / _` |",
"| |_| | |    |   <_____| |          | | | | | | (_| | | | | | | |   | || |  | |_| | | | | (_| |",
" \____|_|    |_|\_\    |_|  Nguyễn  |_| |_| |_|\__,_|_| |_|_| |_|   |_||_|   \__,_|_| |_|\__, |",
"                                                                                         |___/"]
    for line in bar:
        label = myFont.render(line, 1, colorCur)
        SCREEN.blit(label, (20, (fullLine * 20) + 20 * (bar.index(line))))        

def displayText(text, at, x, y, color, bg=None):
    if text.startswith('1f401268'):
        text = text.replace('1f401268', '')
        label = myFont.render(text, at, ERRORCOLOR, bg)
        SCREEN.blit(label, (x, y))
    elif text.startswith('7084338a'):
        text = text.replace('7084338a', '')
        label = myFont.render(text, at, GREEN, bg)
        SCREEN.blit(label, (x, y))
    elif not 'graktung@blackrose:~# ' in text:
        label = myFont.render(text, at, WHITE, bg)
        SCREEN.blit(label, (x, y))    
    else:
        labelUser = myFont.render('graktung@blackrose', at, (RED), bg)
        labelColon = myFont.render(':', at, (WHITE), bg)
        labelNS = myFont.render('#', at, (WHITE), bg)
        labelTilde = myFont.render('~', at, (BLUE), bg)
        SCREEN.blit(labelUser, (0, y))
        SCREEN.blit(labelColon, (145, y))
        SCREEN.blit(labelTilde, (153, y))
        SCREEN.blit(labelNS, (165, y))
        text = text.replace('graktung@blackrose:~#', '')
        labelText = myFont.render(text, at, color, bg)
        SCREEN.blit(labelText, (170, y))

def readChar():
    if event.key == pygame.K_BACKSPACE:
        return 'backspace'
    elif event.key == pygame.K_PAGEUP:
        return 'pageup'
    elif event.key == pygame.K_PAGEDOWN:
        return 'pagedown'
    elif event.key == pygame.K_TAB:
        return 'tab'
    elif event.key == pygame.K_RETURN:
        return 'enter'
    elif event.key == pygame.K_ESCAPE:
        return 'esc'
    elif event.key in (pygame.K_RSHIFT, pygame.K_LSHIFT):
        return 'shift'
    elif event.key in (pygame.K_RCTRL, pygame.K_LCTRL):
        return 'control'
    elif event.key == pygame.K_RIGHT:
        return 'kright'
    elif event.key == pygame.K_LEFT:
        return 'kleft'
    elif event.key == pygame.K_UP:
        return 'kup'
    elif event.key == pygame.K_DOWN:
        return 'kdown'
    elif event.key == pygame.K_CAPSLOCK:
        return None
    elif event.key == 282:
        return 'paste'
    elif event.key == 283:
        return 'begincur'
    elif event.key == 284:
        return 'endcur'
    elif event.key == 285:
        return 'delall'
    else:
        return event.unicode

def helpCommand():
    lstHelp = [[]]
    lstHelp.append(["7084338aTerminal Working"])
    lstHelp.append(['"exit" -> stop Terminal from working'])
    lstHelp.append(['"clear" -> clear all command lines which is displayed in Terminal'])
    lstHelp.append([])
    lstHelp.append(["7084338aDirectory Working"])
    lstHelp.append(['"ls" -> List all the folders and the files at current working directory'])
    lstHelp.append(['"pwd" -> Print the current working directory'])
    lstHelp.append(['"cd new_working_directory" -> Change current working directory to new_working_directory'])
    lstHelp.append([])
    lstHelp.append(["7084338aFiles And Folders Working"])
    lstHelp.append(['"move file_name/folder_name new_place" -> move the file or the folder to new_place'])
    lstHelp.append(['"rename file_name/folder_name new_name" -> rename the file or the folder to new_name'])
    lstHelp.append(['"rmf file_name" -> remove the file file_name'])
    lstHelp.append(['"rmdir folder_name" -> remove the folder folder_name'])
    lstHelp.append([])
    return lstHelp

def progressCommand(cmd):
    cmd = cmd.strip()
    if cmd == '':
        return []
    elif cmd == 'exit':
        sys.exit(0)
    elif cmd == 'help':
        return helpCommand()
    elif cmd == 'pwd':
        path = directory.getPWD()
        path = path.replace('\\', '/')
        return [path]
    elif cmd == 'ls':
        return directory.getList()
    elif cmd.startswith('cd '):
        direc = cmd[3:]
        direc = direc.strip(' ')
        isOK = directory.changePWD(direc)
        if isOK:
            return []
        else:
            path = directory.getPWD() + f'\\{direc}'
            path = path.replace('\\', '/')
            return ["1f401268Error!", "Cannot find path %r" %(path)]
    elif cmd.startswith('move '):
        cmd = cmd[5:]
        isOK = directory.move(cmd)
        if isOK:
            return []
        else:
            return ["1f401268Error!", "Cannot find the file or path specified"]
    elif cmd.startswith('rename '):
        cmd = cmd[7:]
        isOK = directory.rename(cmd)
        if isOK:
            return []
        else:
            return ["1f401268Error!", "Cannot find the file or folder specified"]
    elif cmd.startswith('rmf '):
        cmd = cmd[4:]
        isOK = directory.removeFile(cmd)
        if isOK:
            return []
        else:
            return ["1f401268Error!", "Cannot find the file specified"]
    elif cmd.startswith('rmdir '):
        cmd = cmd[6:]
        isOK = directory.removeDir(cmd)
        if isOK:
            return []
        else:
            return ["1f401268Error!", "Cannot find the directory specified"]
    elif cmd.startswith('mkdir '):
        cmd = cmd[6:]
        isOK = directory.makeDir(cmd)
        if isOK:
            return []
        else:
            return ["1f401268Error!"]
    elif cmd.startswith('mkf '):
        cmd = cmd[4:]
        isOK = directory.makeFile(cmd)
        if isOK:
            return []
        else:
            return ["1f401268Error!"]
    elif cmd.startswith('get content '):
        cmd = cmd[12:]
        isOK = directory.getContent(cmd)
        if type(isOK) is list:
            return isOK
        elif isOK == -1:
            return ["1f401268File Error!", "Something went wrong when trying to get content %r" %(cmd)]
        else:
            return ["1f401268Error!", "Cannot find the file specified"]
    elif cmd.startswith('checkpath '):
        cmd = cmd[10:]
        isOK = directory.checkPath(cmd)
        if isOK:
            return ["7084338aValid path"]
        else:
            return ["1f401268Invalid path"]
    elif cmd.startswith('checkdir '):
        cmd = cmd[9:]
        isOK = directory.checkDir(cmd)
        if isOK:
            return ["7084338aDirectory is exist"]
        else:
            return ["1f401268Directory is not exist"]
    elif cmd.startswith('checkf '):
        cmd = cmd[7:]
        isOK = directory.checkFile(cmd)
        if isOK:
            return ["7084338aFile is exist"]
        else:
            return ["1f401268File is not exist"]
    else:
        return ['%r not found.' %(cmd)]

while 1:
    fullLine = (height - 120) // 20
    if currentLine:
        if camBot - camTop == (fullLine - 1):
            camBot = len(contentDisplay)
            camTop = camBot - (fullLine - 1)
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            SCREEN = pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            width, height = pygame.display.get_surface().get_size()
            if width < 400:
                width = 400
                SCREEN = pygame.display.set_mode((width,height), HWSURFACE|DOUBLEBUF|RESIZABLE)
            if height < 400:
                height = 400
                SCREEN = pygame.display.set_mode((width,height), HWSURFACE|DOUBLEBUF|RESIZABLE)
            fullLine = (height - 120) // 20
            if len(contentDisplay) >= fullLine:
                camBot = len(contentDisplay)
                camTop = camBot - (fullLine - 1)
            else:
                camBot = len(contentDisplay)
                camTop = 0
            currentLine = True
        elif event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            newChar = readChar()
            if newChar not in ('delall', 'begincur', 'endcur', 'backspace', 'tab', 'enter', 'esc', 'pageup', 'pagedown',\
                'shift', 'control', None, 'kright', 'kleft', 'kup', 'kdown', 'paste'):
                try:
                    contentLineCurrent = list(contentLineCurrent)
                    contentLineCurrent.insert(posCursor, newChar)
                    contentLineCurrent = ''.join(contentLineCurrent)
                    posCursor += 1
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                except:
                    posCursor = 0
                    if camBot - camTop == (fullLine - 1):
                        camTop += 1
                    camBot += 1
                    content.append([root])
                    contentLineCurrent = ''
                    contentLineCurrentDisplay = '|'    
                indexListCommand = 0
                showCur = 0   
                currentLine = True
            elif newChar == 'delall':
                contentLineCurrent = ''
                posCursor = 0
                contentLineCurrentDisplay = '|'
                currentLine = True
            elif newChar == 'begincur':
                posCursor = 0
                contentLineCurrentDisplay = '|' + contentLineCurrent
                currentLine = True
            elif newChar == 'endcur':
                posCursor = len(contentLineCurrent)
                contentLineCurrentDisplay = contentLineCurrent + '|'
                currentLine = True
            elif newChar == 'paste':
                if canCopy:
                    paste = pyperclip.paste()
                    showCur = 0
                    contentLineCurrent = list(contentLineCurrent)
                    contentLineCurrent.insert(posCursor, paste)
                    contentLineCurrent = ''.join(contentLineCurrent)
                    posCursor += len(paste)
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                else:
                    print('Require Pyperclip module for Paste.')
                currentLine = True
            elif newChar == 'pageup':    
                if not len(listCommand) == 0:
                    if -len(listCommand) != indexListCommand:
                        indexListCommand -= 1
                        contentLineCurrent = listCommand[indexListCommand]
                        contentLineCurrentDisplay = contentLineCurrent + '|'
                        posCursor = len(contentLineCurrent)
                currentLine = True
                showCur = 0
            elif newChar == 'pagedown':
                if not len(listCommand) == 0:
                    if indexListCommand < -1:
                        indexListCommand += 1
                        contentLineCurrent = listCommand[indexListCommand]
                        contentLineCurrentDisplay = contentLineCurrent + '|'
                        posCursor = len(contentLineCurrent)
                currentLine = True
                showCur = 0
            elif newChar == 'kup':
                if camTop != 0:
                    if camBot - camTop == (fullLine - 1):
                        camBot -= 1
                        camTop -= 1
                        currentLine = False
                showCur = 0
            elif newChar == 'kdown':
                if camBot < len(contentDisplay):
                    camBot += 1
                    camTop += 1
                showCur = 0
            elif newChar == 'kright':
                if not len(contentLineCurrent) == posCursor:
                    posCursor += 1
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                currentLine = True
                showCur = 0
            elif newChar == 'kleft':
                if posCursor != 0:
                    posCursor -= 1
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                currentLine = True
                showCur = 0
            elif newChar == 'backspace':
                if len(contentLineCurrent) != 0 and posCursor != 0:
                    try:
                        contentLineCurrent = list(contentLineCurrent)
                        wordPoped = contentLineCurrent.pop(posCursor - 1)
                        contentLineCurrent = ''.join(contentLineCurrent)
                        posCursor -= 1
                    except:
                        contentLineCurrent = contentLineCurrent[1:]
                        posCursor = len(contentLineCurrent)
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                    currentLine = True
                showCur = 0
            elif newChar == 'enter':
                currentLine = True
                indexListCommand = 0
                if camBot - camTop == (fullLine - 1):
                    camTop += 1
                camBot += 1
                content.append([root + contentLineCurrent])
                if contentLineCurrent.strip() == 'clear':
                    camTop = 0
                    camBot = 0
                    posCursor = 0
                    content = []
                    contentLineCurrent = ''
                    contentLineCurrentDisplay = '|'
                else:
                    contentAppend = progressCommand(contentLineCurrent)
                    for eachLine in contentAppend:
                        if camBot - camTop == (fullLine - 1):
                            camTop += 1
                        camBot += 1
                        content.append(eachLine)
                if len(contentLineCurrent.strip(' ')) != 0:
                    listCommand.append(contentLineCurrent)
                posCursor = 0
                contentLineCurrent = ''
                contentLineCurrentDisplay = '|'
                showCur = 0
    SCREEN.fill(BLACK)
    changeColor += 1
    showCur += 1
    if changeColor > 500:
        changeColor = 0
        appColorAgain = colorCur
        colorCur = listColor.pop(listColor.index(random.choice(listColor)))
        listColor.append(appColorAgain)
        displayGrakT(colorCur)
    else:
        displayGrakT(colorCur)
    contentDisplay = []
    for i in range(len(content)):
        text = ''.join(content[i])
        if len(text) * 8 > width:
            while len(text) * 8 > width:
                textMini = text[:width // 8 - 1]
                contentDisplay.append(textMini)
                text = text[width // 8 - 1:]
            contentDisplay.append(text)
        else:
            contentDisplay.append(text)
    if currentLine:
        if len(contentDisplay) >= fullLine:
            camBot = len(contentDisplay)
            camTop = camBot - (fullLine - 1)
        else:
            camBot = len(contentDisplay)
            camTop = 0
    for i in range(camTop, camBot):
        displayText(contentDisplay[i], 1, 0, line * 20, WHITE)
        line += 1
    if camBot == len(contentDisplay):
        if showCur < 500:
            displayText(root + contentLineCurrentDisplay, 1, 0, line * 20, WHITE)
        else:
            displayText(root + contentLineCurrent, 1, 0, line * 20, WHITE)
        if showCur > 1000:
            showCur = 0
    else:
        displayText(''.join(contentDisplay[camBot]), 1, 0, line * 20, WHITE)
    line = 0
    pygame.display.flip()