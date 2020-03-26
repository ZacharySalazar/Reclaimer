
import Tools
import pygame


"""Finds a target and copies its imgX and imgY then draws
the given effect list over it"""
class Effect():
    iterationCounter = 0
    active = True

    def __init__(self, target, iterationList):
        self.target = target
        self.x, self.y = target.currentX, target.currentY
        self.iterationList = iterationList
        self.img = iterationList[0]


    def drawMe(self):
        self.x, self.y = self.target.currentX, self.target.currentY
        self.active = Tools.animateMe(self, True, False)
        self.img = pygame.transform.scale(self.img, (self.target.img.get_width(), self.target.img.get_height()))

