# standard modules
import pygame
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
listCommand = []
indexListCommand = 0
contentLineCurrent = ''
contentLineCurrentDisplay = '|'
posCursor = 0
root = 'graktung@blackrose:~# '
camTop = 0
camBot = 0
line = 0

def displayGrakT(colorCur):
    bar = ["  ____     /\ _       ______       _____ _      __         _       _____",
" / ___|_ _|/\| | __  |_   _|      |_   _| |__   \_\_ _ __ | |__   |_   _| __ _   _ _ __   __ _ ",
"| |  _| '__| | |/ /____| |          | | | '_ \ / _` | '_ \| '_ \    | || '__| | | | '_ \ / _` |",
"| |_| | |    |   <_____| |          | | | | | | (_| | | | | | | |   | || |  | |_| | | | | (_| |",
" \____|_|    |_|\_\    |_|  Nguyễn  |_| |_| |_|\__,_|_| |_|_| |_|   |_||_|   \__,_|_| |_|\__, |",
"                                                                                         |___/"]
    if not height < 140:
        for line in bar:
            label = myFont.render(line, 1, colorCur)
            SCREEN.blit(label, (20, (fullLine * 20) + 20 * (bar.index(line))))
    elif height > 20:
        for line in bar:
            if bar.index(line) * 20 + 20 > height:
                break
            label = myFont.render(line, 1, colorCur)
            SCREEN.blit(label, (20, 20 + 20 * (bar.index(line))))        

def displayText(screen, text, at, x, y, color, bg=None):
    if text.startswith('1f401268'):
        text = text.replace('1f401268', '')
        label = myFont.render(text, at, ERRORCOLOR, bg)
        screen.blit(label, (x, y))
    elif text.startswith('7084338a'):
        text = text.replace('7084338a', '')
        label = myFont.render(text, at, GREEN, bg)
        screen.blit(label, (x, y))
    elif not 'graktung@blackrose:~# ' in text:
        label = myFont.render(text, at, WHITE, bg)
        screen.blit(label, (x, y))    
    else:
        labelUser = myFont.render('graktung@blackrose', at, (RED), bg)
        labelColon = myFont.render(':', at, (WHITE), bg)
        labelNS = myFont.render('#', at, (WHITE), bg)
        labelTilde = myFont.render('~', at, (BLUE), bg)
        screen.blit(labelUser, (0, y))
        screen.blit(labelColon, (145, y))
        screen.blit(labelTilde, (153, y))
        screen.blit(labelNS, (165, y))
        text = text.replace('graktung@blackrose:~#', '')
        labelText = myFont.render(text, at, color, bg)
        screen.blit(labelText, (170, y))

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
    lstHelp.append(['"exit" -> stop Terminal from working.'])
    lstHelp.append(['"clear" -> clear all command lines which is displayed in Terminal.'])
    lstHelp.append([])
    lstHelp.append(["7084338aDirectory Working"])
    lstHelp.append(['"ls" -> List all the folders and the files at current working directory.'])
    lstHelp.append(['"pwd" -> Print the current working directory.'])
    lstHelp.append(['"cd new_working_directory" -> Change current working directory to new_working_directory.'])
    lstHelp.append(['"move file_name/folder_name new_place" -> move the file or the folder to new_place.'])
    lstHelp.append(['"rename file_name/folder_name new_name" -> rename the file or the folder to new_name.'])
    lstHelp.append(['"rmf file_name" -> remove the file file_name.'])
    lstHelp.append(['"rmdir folder_name" -> remove the folder folder_name.'])
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
    else:
        return ['%r not found.' %(cmd)]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            SCREEN = pygame.display.set_mode(event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            width, height = pygame.display.get_surface().get_size()
            fullLine = (height - 120) // 20
            if len(content) >= fullLine:
            	camBot = len(content)
            	camTop = camBot - (fullLine - 1)
            else:
            	camBot = len(content)
            	camTop = 0
        elif event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            newChar = readChar()
            if newChar not in ('delall', 'begincur', 'endcur', 'backspace', 'tab', 'enter', 'esc', 'pageup', 'pagedown',\
                'shift', 'control', None, 'kright', 'kleft', 'kup', 'kdown', 'paste'):
                indexListCommand = 0
                showCur = 0
                contentLineCurrent = list(contentLineCurrent)
                contentLineCurrent.insert(posCursor, newChar)
                contentLineCurrent = ''.join(contentLineCurrent)
                posCursor += 1
                lstChar = list(contentLineCurrent)
                lstChar.insert(posCursor, '|')
                contentLineCurrentDisplay = ''.join(lstChar)
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
            elif newChar == 'delall':
                contentLineCurrent = ''
                posCursor = 0
                contentLineCurrentDisplay = '|'
            elif newChar == 'begincur':
                posCursor = 0
                contentLineCurrentDisplay = '|' + contentLineCurrent
            elif newChar == 'endcur':
                posCursor = len(contentLineCurrent)
                contentLineCurrentDisplay = contentLineCurrent + '|'
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
            elif newChar == 'pageup':            
                if not len(listCommand) == 0:
                    if -len(listCommand) != indexListCommand:
                        indexListCommand -= 1
                        contentLineCurrent = listCommand[indexListCommand]
                        contentLineCurrentDisplay = contentLineCurrent + '|'
                        posCursor = len(contentLineCurrent)
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
                showCur = 0
            elif newChar == 'pagedown':
                if not len(listCommand) == 0:
                    if indexListCommand < -1:
                        indexListCommand += 1
                        contentLineCurrent = listCommand[indexListCommand]
                        contentLineCurrentDisplay = contentLineCurrent + '|'
                        posCursor = len(contentLineCurrent)
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
                showCur = 0
            elif newChar == 'kup':
                if camTop != 0:
                    if camBot - camTop == (fullLine - 1):
                        camBot -= 1
                        camTop -= 1
                showCur = 0
            elif newChar == 'kdown':
                if camBot < len(content):
                    camBot += 1
                    camTop += 1
                showCur = 0
            elif newChar == 'kright':
                if not len(contentLineCurrent) == posCursor:
                    posCursor += 1
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
                showCur = 0
            elif newChar == 'kleft':
                if posCursor != 0:
                    posCursor -= 1
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
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
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
                showCur = 0
            elif newChar == 'enter':
                indexListCommand = 0
                if camBot - camTop == (fullLine - 1):
                    camTop += 1
                camBot += 1
                content.append([root, contentLineCurrent])
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
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
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
    for i in range(camTop, camBot):
        displayText(SCREEN,''.join(content[i]), 1, 0, line * 20, WHITE)
        line += 1
    if camBot == len(content):
        if showCur < 500:
            displayText(SCREEN, root + contentLineCurrentDisplay, 1, 0, line * 20, WHITE)
        else:
            displayText(SCREEN, root + contentLineCurrent, 1, 0, line * 20, WHITE)
        if showCur > 1000:
            showCur = 0
    else:
        displayText(SCREEN,''.join(content[camBot]), 1, 0, line * 20, WHITE)
    line = 0
    pygame.display.flip()