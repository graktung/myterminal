import pygame
from pygame.locals import*
import sys
import random

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
BLUE = 0, 0, 205
GREEN = 0, 128, 0
YELLOW = 255, 255, 0
PINK = 255, 0, 255
SCREEN = pygame.display.set_mode(SIZE, RESIZABLE)
myFont = pygame.font.SysFont("consolas", 15)
listColor = [WHITE, RED, BLUE, GREEN, YELLOW, PINK]
changeColor = 0
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
            SCREEN.blit(label, (20, (height - 120) + 20 * (bar.index(line))))

def displayText(screen, text, at, x, y, color, bg=None):
    if not 'graktung@blackrose:~# ' in text:
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
    else:
        return event.unicode

def progressCommand(cmd):
    cmd = cmd.strip()
    if cmd == '':
        return []
    elif cmd == 'exit':
        sys.exit(0)
    elif cmd == 'pwd':
        path = directory.getPWD()
        path.replace('\\', '/')
        return [path]
    elif cmd == 'ls':
        return directory.getList()
    elif cmd.startswith('cd'):
        direc = cmd.replace('cd ', '')
        isChange = directory.changePWD(direc)
        if isChange:
            return []
        else:
            path = directory.getPWD() + f'\\{direc}'
            path.replace('\\', '/')
            return ["Error!", "Cannot find path %r" %(path)]
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
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            newChar = readChar()
            if newChar not in ('backspace', 'tab', 'enter', 'esc', 'pageup', 'pagedown',\
                'shift', 'control', None, 'kright', 'kleft', 'kup', 'kdown'):
                indexListCommand = 0
                posCursor += 1
                contentLineCurrent = list(contentLineCurrent)
                contentLineCurrent.insert(posCursor - 1, newChar)
                contentLineCurrent = ''.join(contentLineCurrent)
                lstChar = list(contentLineCurrent)
                lstChar.insert(posCursor, '|')
                contentLineCurrentDisplay = ''.join(lstChar)
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
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
            elif newChar == 'kup':
                if camTop != 0:
                    if camBot - camTop == (fullLine - 1):
                        camBot -= 1
                        camTop -= 1
            elif newChar == 'kdown':
                if camBot < len(content):
                    camBot += 1
                    camTop += 1
            elif newChar == 'kright':
                if not len(contentLineCurrent) == posCursor:
                    posCursor += 1
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)
            elif newChar == 'kleft':
                if posCursor != 0:
                    posCursor -= 1
                    lstChar = list(contentLineCurrent)
                    lstChar.insert(posCursor, '|')
                    contentLineCurrentDisplay = ''.join(lstChar)
                if camBot - camTop == (fullLine - 1):
                    camBot = len(content)
                    camTop = camBot - (fullLine - 1)     
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

    SCREEN.fill(BLACK)
    changeColor += 1
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
        displayText(SCREEN, root + contentLineCurrentDisplay, 1, 0, line * 20, WHITE)
    line = 0
    pygame.display.flip()