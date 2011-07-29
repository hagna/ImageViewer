#!/usr/bin/python

import os, pygame

images = ['jpg', 'jpeg', 'png', ]

def isImage(file):
    index = file.rfind('.')
    ext = file[index+1:]
    if ext in images:
        return True
    return False

class ImageModel:
    
    def __init__(self, dirs):
        self.dirs = dirs
        self.index = 0
        self.dirIndex = 0
        self._setFiles()

    def _setFiles(self):
        self.files = [file for file in os.listdir(self.getCurrentDir()) if isImage(file)]

    def getCurrentDir(self):
        return self.dirs[self.dirIndex]

    def getCurrentImage(self):
        return self.files[self.index]

    def getNextImage(self):
        self.index = self.index + 1
        if self.index == len(self.files):
            self.index = 0
        return self.getCurrentImage()

    def getPrevImage(self):
        if self.index == 0:
            self.index = len(self.files)
        self.index = self.index - 1
        return self.getCurrentImage()

    def getNextDir(self):
        self.dirIndex = self.dirIndex + 1
        if self.dirIndex == len(self.dirs):
            self.dirIndex = 0
        self._setFiles()
        self.index = 0
        return self.getCurrentImage()

    def getPrevDir(self):
        if self.dirIndex == 0:
            self.dirIndex = len(self.dirs)
        self.dirIndex = self.dirIndex - 1
        self._setFiles()
        self.index = 0
        return self.getCurrentImage()

    def run(self):
        self.view = ImageView()
        self.view.viewImage(self.getCurrentDir(), self.getCurrentImage())

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    file = self.getPrevImage()
                    self.view.viewImage(self.getCurrentDir(), file)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    file = self.getNextImage()
                    self.view.viewImage(self.getCurrentDir(), file)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                    file = self.getPrevDir()
                    self.view.viewImage(self.getCurrentDir(), file)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                    file = self.getNextDir()
                    self.view.viewImage(self.getCurrentDir(), file)

class ImageView:

    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.res = (info.current_w, info.current_h)
        self.screen = pygame.display.set_mode(self.res)
        background = pygame.Surface(self.res)
        self.background = background.convert()
        self.background.fill( (0,0,0) )

    def viewImage(self, dir, file):
        fullpath = os.path.join(dir, file)
        try:
            image = pygame.image.load(fullpath)
        except pygame.error, message:
            print 'Cannot load image %s' % file
            raise SystemExit, message
        self.screen.blit(self.background, (0,0) )
        pygame.display.flip()
        pos = self._getPos(image)
        self.screen.blit(image, pos)
        pygame.display.flip()

    def _getPos(self, image):
        imageW, imageH = image.get_size()
        screenW, screenH = self.res
        startX = int((screenW - imageW) / 2)
        if startX < 0:
            startX = 0
        startY = int((screenH - imageH) / 2)
        if startY < 0:
            startY = 0
        return (startX, startY)

