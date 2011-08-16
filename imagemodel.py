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
    
    def __init__(self, startdir, width=None, height=None, noexit=True):
        self.width = width
        self.height = height
        self.dirnav = filenav.FileNav(startdir)
        self.imagenav = filenav.FileNav(startdir.children()[0])
        self.clock = pygame.time.Clock()
        self.noexit = noexit


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
                file = self.imagenav.previous
                self.view.viewImage(file)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.time = 0
                file = self.imagenav.next
                self.view.viewImage(file)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.time = 0
                newdir = self.dirnav.previous
                file = newdir.children()[0]
                self.imagenav.current = file
                self.view.viewImage(file)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.time = 0
                newdir = self.dirnav.next
                file = newdir.children()[0]
                self.imagenav.current = file
                self.view.viewImage(file)
        if self.play:
            self.time = self.time + self.clock.tick()
            if self.time > self.waittime:
                self.time = 0
                file = self.imagenav.next
                self.view.viewImage(file)


    def run(self):
        self.view = ImageView(self.width, self.height)
        self.view.viewImage(self.imagenav.current)
        self.play = True
        self.time = self.clock.tick()
        self.waittime = 30000
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

