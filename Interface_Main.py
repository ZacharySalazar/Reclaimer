import pygame
import Interface_Controls as IC
import Shop_Images as SI
import Panels as P

pygame.init()
update = pygame.display.update

win = pygame.display.set_mode((1400, 900))
# surfaceCreation = pygame.font.SysFont('Comic Sans MS',50)
pygame.display.set_caption("Slope Testing")
white = (255, 255, 255)

def main():
            #SI.shop.shop_screen = False
    #print(P.player.healing)
    win.blit(SI.background, (0, 0))

    IC.interface_controls()
    update()




