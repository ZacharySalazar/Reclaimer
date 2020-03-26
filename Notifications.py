import pygame


win = pygame.display.set_mode((1400, 800))
update = pygame.display.update


def load(image, directory, width = 125, height = 175):
    imageName = image + '.png'
    if directory != None:
        image = pygame.image.load(directory + imageName)
        image = pygame.transform.scale(image, (width, height))
    else:
        image = pygame.image.load(imageName)
    return image

whiteBackground = load('whiteBackground', 'images/backgrounds/', 1400, 800)
whisperWoods = load('whisper_woods', 'images/stage_titles/', 300, 300)


class Notification:
    x, y = 0, 0


    def __init__(self, img, color, x = x, y = y):
        self.img = img
        self.x = x
        self.y = y
        self.color = color

    def drawMe(self):
        win.blit(self.img, (self.x, self.y))



        #for alpha in range(0, 300):
            #self.img.set_alpha(alpha)
            #win.blit(self.img, (0, 0))
            #update()


tester = Notification(whisperWoods)

testing = True
while testing:

    event = pygame.event.poll()
    keys = pygame.key.get_pressed()

    win.blit(whiteBackground, (0, 0))
    win.blit(tester.img, (tester.x, tester.y))
    update()

    if event.type == pygame.MOUSEBUTTONDOWN:
        tester.fading_in = True
        print('can still run keys!')

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()