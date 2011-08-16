#!/usr/bin/python

import os, pygame, filenav
import pygame.locals

images = ['jpg', 'jpeg', 'png', ]

def isImage(file):
    index = file.rfind('.')
    ext = file[index+1:]
    if ext in images:
        return True
    return False

class ImageModel:

    waittime = 30000

    def __init__(self, startdir, width=None, height=None,
                 noexit=True, switchKeys=False):
        self.width = width
        self.height = height
        print "startdir is", startdir
        self.dirnav = filenav.FileNav(startdir, sortbyname=True)
        self.momentum = self.right

        newdir = self.dirnav.current
        s = filenav.similarChild(None, newdir)
        self.imagenav = s

        self.clock = pygame.time.Clock()
        self.noexit = noexit
        self.switchKeys = switchKeys

    def dispatch_events(self):
        time = self.time
        play = self.play
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.time = 0
                self.exit = True
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.time = 0
                self.exit = True
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.time = -self.waittime
                play = not play
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.time = 0
                self.up()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.time = 0
                self.down()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.time = 0
                self.left()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.time = 0
                self.right()
        if self.play:
            self.time = self.time + self.clock.tick()
            if self.time > self.waittime:
                self.time = 0
                self.momentum()

    def down(self):
        if self.switchKeys:
            self.nextDir()
        else:
            self.nextImage()
        self.momentum = self.down

    def up(self):
        if self.switchKeys:
            self.prevDir()
        else:
            self.prevImage()
        self.momentum = self.up

    def left(self):
        if self.switchKeys:
            self.prevImage()
        else:
            self.prevDir()
        self.momentum = self.left

    def right(self):
        if self.switchKeys:
            self.nextImage()
        else:
            self.nextDir()
        self.momentum = self.right

    def nextImage(self):
        file = self.imagenav.next
        self.view.viewImage(file)

    def prevImage(self):
        file = self.imagenav.previous
        self.view.viewImage(file)


    def prevDir(self):
        newdir = self.dirnav.previous
        self.imagenav = filenav.similarChild(self.imagenav, newdir)
        self.view.viewImage(self.imagenav.current)


    def nextDir(self):
        newdir = self.dirnav.next
        self.imagenav = filenav.similarChild(self.imagenav, newdir)
        self.view.viewImage(self.imagenav.current)


    def run(self):
        self.view = ImageView(self.width, self.height)
        self.view.viewImage(self.imagenav.current)
        self.play = True
        self.time = self.clock.tick()
        self.exit = False
        while 1:
            self.dispatch_events()
            if self.noexit == True:
                continue
            else:
                if self.exit == True:
                    break

class ImageView:

    def __init__(self, width, height):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.res = (width, height)
        self.screen = pygame.display.set_mode(self.res, pygame.locals.DOUBLEBUF)
        background = pygame.Surface(self.res)
        self.background = background.convert()
        self.background.fill( (0,0,0) )

    def viewImage(self, fp):
        print fp
        fullpath = fp.path
        try:
            image = pygame.image.load(fullpath)
        except pygame.error, message:
            print 'Cannot load image %s' % file
            raise SystemExit, message
        self.screen.blit(self.background, (0,0) )
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
