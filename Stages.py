import pygame
import Images
import random
import CutScenes
import Tools

pygame.init()
win = pygame.display.set_mode((1400, 800))
update = pygame.display.update

stageCompletionFont = pygame.font.SysFont('castellar', 30)
yellow = (255, 255, 0)

def animateMe(character):

    if character.iterationCounter > len(character.iterationList):
        character.iterationCounter = 0

    else:
        character.img = character.iterationList[character.iterationCounter]
        character.iterationCounter += 1

        if character.iterationCounter >= len(character.iterationList):
            character.iterationCounter = 0

class BG_Characters:
    iterationCounter = 0

    img = None

    def __init__(self, leftIteration, rightIteration, startingX=random.randint(0, 1400), startingY=400, speed=5):

        self.iterationList = leftIteration
        self.leftIteration = leftIteration
        self.rightIteration = rightIteration
        self.currentX = startingX
        self.currentY = startingY
        self.speed = speed


        if startingX == 1400:
            self.movingRight = False
        elif startingX == 0:
            self.movingRight = True

    def move(self):
        #print(self.speed)
       # print(self.currentX)

        if self.movingRight:
            self.iterationList = self.rightIteration
            if not stageHandler.currentStage.scrolling:
                self.currentX += self.speed
            else:
                pass
            #print(f'this is my currentX {self.currentX}')

        elif not self.movingRight:
            self.iterationList = self.leftIteration

            if stageHandler.currentStage.scrolling:
                #'is detecint scrolling')
                self.currentX -= stageHandler.currentStage.scrollSpeed + self.speed
            elif not stageHandler.currentStage.scrolling:
                self.currentX -= self.speed

        animateMe(self)
        win.blit(self.img, (self.currentX, self.currentY))

class Camp_Fire(Tools.Frame):
    def __init__(self, x, y, iterationList=Images.camp_fire):
        Tools.Frame.__init__(self, iterationList, x, y)

class Bat(BG_Characters):
    def __init__(self, startingX, startingY, leftIteration=Images.batFlyLeft, rightIteration=Images.batFlyRight):
        BG_Characters.__init__(self, leftIteration, rightIteration, startingX, startingY)


class Decals(BG_Characters):
    timer = 0  # used to timeout decals

    def __init__(self, uptime, leftIteration, rightIteration, startingX, startingY):
        BG_Characters.__init__(self, leftIteration, rightIteration, startingX, startingY)

        self.uptime = uptime # how long the image will animate for

    def timeout(self):
        #print(self.timer)
        self.timer += 1
        if self.timer > self.uptime:
            stageHandler.currentStage.decalsList.remove(self)

    def drawMe(self):
        if stageHandler.currentStage.scrolling:
            self.currentX -= stageHandler.currentStage.scrollSpeed
        self.iterationList = self.leftIteration
        animateMe(self)
        win.blit(self.img, (self.currentX, self.currentY))


        self.timeout()

#Bat = BG_Characters(Images.batFlyLeft, Images.batFlyRight, startingX=random.choice([0, 1400]), startingY=random.choice([200, 300]), speed=4)

class StageDisplay:
    slotLocation = (1100, 50)



enemyInterface = StageDisplay()

class Stage():
    completed = False  #determines when enemies or bosses have been cleared from the stage and player has walked on
    scrolling = False# condition indicating the stage screen is in mtion or scrolling

    enemiesList = [] #enemies loaded in DOCK module to spawn when stages are STARTED
                        # operated on in the MAIN module

    wanderers = [] #enemies loaded in DOCK module to spawn after stages are COMPLETED and fight when scrolling
                    # operated on in the MAIN module
    added_wanderers = False

    reinforcementsList = [] #enemies loaded in DOCK module to spawn when the enemiesList is emptied as reinforcements
    reinforcementsAdded = False

    matterList = []

    enemiesIconList = []
    enemyDisplay = []
    enemyDisplayX = 1200
    enemyDisplayY = 150
    CS1 = False
    CS2 = False

    introduced = False #introduces the stage with a floating title (used primarily when entering new themed stages).
    scrollSpeed = 5 # determines how fast the stage screen will scroll left


    background_characters = []   #to make the background more alive these are characters that do things in background

    boss = None # bosses are loaded in the Dock Module

    def __init__(self, name, img, leftBoundary, rightBoundary, topBoundary, bottomBoundary, bg_character,
                 nextStage, reinforcementsTrigger, cutsceneAvailable = None, layered=None, decals=None, decalsYspawnRng=(20, 240), decalsList=[],
                 foreground_characters=[], imgX = 1400, imgY = 0,
                 stage_title_img = None):

        self.name = name
        self.img = img
        self.leftBoundary = leftBoundary
        self.rightBoundary = rightBoundary
        self.topBoundary = topBoundary
        self.bottomBoundary = bottomBoundary
        self.bg_character = bg_character     #specific background character Img to spawn and make stage more alive
        self.layered = layered  # A background image for transpearent foregrounds. Allows comprised dualistic backgrounds
        self.decals = decals
        self.decalsList = decalsList
        self.decalsYspawnRng = decalsYspawnRng  # determines the Y on decals spontaneous spawning
        self.cutsceneAvailable = cutsceneAvailable

        self.imgX = imgX  #keeps it offscreen to the right
        self.imgY = imgY  #defaults always to the top left corner of screen
        self.nextStage = nextStage
        self.reinforcementsTrigger = reinforcementsTrigger  # if enemies list is less than this number the enemies in reinforcements list are added
        self.foreground_characters = foreground_characters

        self.stage_title_img = stage_title_img


    def play_cutscene(self):
        CutScenes.play_cutscene(self)


    def scroll(self):
        self.scrolling = True
        self.comeAlive(True)
        #if next stage hasnt docked at 0 or below it
        """
        if self.nextStage.imgX > 0:
            if self.layered:
                win.blit(self.layered, (self.imgX, self.imgY))
                self.nextStage.comeAlive()
            self.imgX -= self.scrollSpeed
            win.blit(self.img, (self.imgX, self.imgY))

            self.nextStage.imgX = self.imgX + self.img.get_width()

            if self.nextStage.layered:
                win.blit(self.nextStage.layered, (self.nextStage.imgX, self.nextStage.imgY))
                for char in self.background_characters:
                    if char.currentX >= self.nextStage.imgX - 40:                          #40 is the size of the image so that the right edge detects the next stage early from its currentX
                        win.blit(char.img, (char.currentX, char.currentY))
            win.blit(self.nextStage.img, (self.nextStage.imgX, self.nextStage.imgY))
            self.add_decals(True)
        else:
            print('started next stage')
            stageHandler.startNextStage()
        """
    def updateStageText(self):
        if stageHandler.currentStage.enemiesList == []:
            stageCompleteText = stageCompletionFont.render('Stage Complete', True, yellow)
            win.blit(stageCompleteText, (1090, 90))
            stageHandler.currentStage.completed = True
        else:
            stage_name = stageCompletionFont.render(self.name, True, (255, 0, 0))
            win.blit(stage_name, (1090, 90))
    """
    def introduce(self):
        if self.stage_title_img != None:
            if not self.introduced:
                self.introduced = Tools.animateMe(False, True)
    """
    def drawStageBackground(self, focus):
        #self.introduce()
        #print(stageHandler.currentStage.scrolling)
        #print(f'this is the background character list: {self.background_characters}')
        if len(self.enemiesList) <= self.reinforcementsTrigger and not self.reinforcementsAdded:
            self.enemiesList += self.reinforcementsList
            self.reinforcementsAdded = True

        if self.enemiesList == []:
            self.completed = True
            if self.cutsceneAvailable != None:
                if self.cutsceneAvailable != 'completed':
                    self.comeAlive()
                    self.play_cutscene()


        if not self.completed:
            self.comeAlive()



        if self.completed and self.cutsceneAvailable in ['completed', None]:
            #mp = pygame.mouse.get_pos()
            #print('confirmed to move on!')
            if self.boss == None:
                if not self.added_wanderers:
                    stageHandler.wanderers_list += self.wanderers
                    self.added_wanderers = True
                #if self.wanderers != []:
                    #stageHandler.wanderers_list += self.wanderers

                if focus.currentX > 600: #and focus.movementRight:  700
                    self.scrolling = True
                    self.comeAlive(True)
                    #self.scroll()
                else:
                    self.comeAlive()
                    self.scrolling = False
            else:
                #self.boss.cycle()
                self.comeAlive()
                self.boss.cycle()

        if self.boss == None:
            self.updateStageText()

            #self.comeAlive()
            #print('go to half of screen to scroll!')

    """Adds non enemies images to foreground that are idle and simple"""
    def add_foreground(self):
        for item in self.foreground_characters:
            animateMe(item)
            win.blit(item.img, (self.imgX + item.x, item.y)) #accounts for scrolling and loading

    '''Adds non enemies/images to foreGround and front for decorative animation that is moving or complex'''
    def add_decals(self):
        if self.decals != None:
            rng = random.randint(1, 100)

            #hardcoded for ghost stage zero decals  (fix this later!)
            if rng == 1:
                self.decalsList.append(Decals(uptime=50, leftIteration=self.decals, rightIteration=self.decals, startingX=random.randint(0, 1400),
                startingY=random.randint(self.decalsYspawnRng[0], self.decalsYspawnRng[1])))

        if self.decalsList != []:
            for decal in self.decalsList:
                animateMe(decal)
                decal.drawMe()

    '''Animates the background of the stage with background characters
    AND initiates the next stage'''
    def comeAlive(self, isScrolling=False):
        # not self.completed:
        if self.nextStage != None:
            if self.nextStage.imgX <= 0:
                self.nextStage.imgX = 0
                stageHandler.startNextStage()

        if self.nextStage == None:
            if self.enemiesList == []:
                print('completed')


        #print(f'this is the current stage imgx : {self.imgX}')
        if self.layered != None:
            win.blit(self.layered, (self.imgX, self.imgY))
        if self.nextStage != None:
            if self.nextStage.layered != None:
                win.blit(self.nextStage.layered, (self.nextStage.imgX, self.nextStage.imgY))

        #print(self.background_characters)
        #print(f'This is the stage name: {stageHandler.currentStage.name}, this is the active bats: {stageHandler.currentStage.background_characters}')
        if self.bg_character != None:
            for char in self.background_characters:
                #print(f'This is the bats currentX: {char.currentX}')
                if self.nextStage != None:
                    if char.currentX in range(self.imgX, self.nextStage.imgX + self.nextStage.img.get_width()):
                        char.move()
                else:
                    if char.currentX in range(self.imgX, self.imgX + self.img.get_width()):
                        char.move()

        win.blit(self.img, (self.imgX, self.imgY)) #THIS IS DRAWING THE ACTUAL GAME IMAGE

        if self.nextStage != None:
            win.blit(self.nextStage.img, (self.nextStage.imgX, self.nextStage.imgY))
            self.nextStage.add_foreground()

        self.add_foreground()
        self.add_decals()

        #print(range(self.imgX, self.imgX + self.img.get_width()))
        #print(range(self.nextStage.imgX, self.nextStage.imgX + self.nextStage.img.get_width()))
        if isScrolling:

            self.imgX -= self.scrollSpeed

            if self.nextStage != None:
                self.nextStage.imgX = self.imgX + self.img.get_width()
            else:
                print('completed')



        rng = random.randint(1, 200)
        if rng == 1:
            if self.bg_character != None:
                print('added bats!')
                #IF SELF.NAME == STAGE_ZERO:
                    #leftIteraiton = Images.batFlyLeft  rightIteration = Images.batFlyRight
                xRng = random.choice([0, 1400])
                yRng = random.randint(350, 580)
                stageHandler.currentStage.background_characters.append(self.bg_character(xRng, yRng))

        if self.bg_character != None:
            for char in stageHandler.currentStage.background_characters:
                if char.currentX < 0 or char.currentX > 1400:
                    stageHandler.currentStage.background_characters.remove(char)
                #BG_Characters(Images.batFlyLeft, Images.batFlyRight, startingX=random.choice([0, 1400]), startingY=random.randint(350, 600), speed=4))

        #if self.background_characters != []:
            #for character in self.background_characters:
                #print(character.currentX)
                #character.move()


    def finalize(self):
        self.completed = True

    '''Keep player in vision of camera and ground boundaries'''
    def checkBoundaries(self, objects):

        if round(objects.currentX + objects.speed) in range(self.leftBoundary, self.rightBoundary) \
                and round(objects.currentX - objects.speed) in range(self.leftBoundary, self.rightBoundary):
            pass

        else:
            if objects.leftEdge - 15 < self.leftBoundary:
                print(f'this is player left edge: {objects.leftEdge}')
                objects.currentX += objects.speed

            if not self.completed or self.cutsceneAvailable not in ['completed', None] or self.boss != None:
                if objects.rightEdge > self.rightBoundary:
                    objects.currentX -= objects.speed


        objects.outlineSelf()
        if round(objects.bottomEdge) in range(self.topBoundary, self.bottomBoundary) \
                and round(objects.bottomEdge) in range(self.topBoundary, self.bottomBoundary):
            objects.falling = False

        else:
            if objects.bottomEdge <= self.topBoundary:
                if objects.falling:
                    objects.currentY += 1
                else:
                    objects.currentY += objects.speed


            if objects.bottomEdge >= self.bottomBoundary:  #5 is a global padding since the bottomEdge is so precise
                print('bottom edge working?')
                objects.currentY -= objects.speed

stage_three = Stage(name = 'stage_three', img = Images.forest2, leftBoundary = -20, rightBoundary = 1400, topBoundary = 610, bottomBoundary = 800,
                   bg_character=Bat,
                   nextStage=None, reinforcementsTrigger=2, layered=Images.whiteBackground, decals=Images.ghostAppear)

#original stage two
# stage_two = Stage(name = 'stage_two', img = Images.forest2, leftBoundary = -20, rightBoundary = 1400, topBoundary = 610, bottomBoundary = 800,
#                    bg_character=Bat,
#                    nextStage=stage_three, reinforcementsTrigger=2, layered=Images.whiteBackground, decals=Images.ghostAppear, foreground_characters=[Camp_Fire(300, 700)])

stage_two = Stage(name = 'stage_six', img = Images.c_b, leftBoundary = -20, rightBoundary = 1400, topBoundary = 610, bottomBoundary = 800,
                   bg_character=Bat,
                   nextStage=stage_three, reinforcementsTrigger=2, layered=None, decals=Images.ghostAppear, foreground_characters=[Camp_Fire(300, 700)])

#changed stage name
stage_one = Stage(name = 'stage_five', img = Images.c_b, leftBoundary = -20, rightBoundary = 1400, topBoundary = 640, bottomBoundary = 800,   #changed the topboundary
                    bg_character=None,
                    nextStage=stage_two, reinforcementsTrigger=1, decals=None, layered=None)



#Lord Hollow Stage Setup
# stage_one = Stage(name = 'stage_one', img = Images.cave_boss_background, leftBoundary = -20, rightBoundary = 1400, topBoundary = 610, bottomBoundary = 800,
#                    bg_character=None,
#                    nextStage=stage_two, reinforcementsTrigger=2, decals=None, cutsceneAvailable=True)

#ready and original stage_one
# stage_one = Stage(name = 'stage_one', img = Images.forest2, leftBoundary = -20, rightBoundary = 1400, topBoundary = 610, bottomBoundary = 800,
#                    bg_character=Bat, foreground_characters=[Camp_Fire(300, 700)],
#                    nextStage=stage_two, reinforcementsTrigger=2, layered=Images.whiteBackground, decals=Images.ghostAppear, cutsceneAvailable=False)

stage_zero = Stage(name = 'stage_zero', img = Images.forest2, leftBoundary = -20, rightBoundary = 1400, topBoundary = 610, bottomBoundary = 800,
                   bg_character=Bat,
                   nextStage=stage_one, reinforcementsTrigger=0, layered=Images.whiteBackground, decals=Images.ghostAppear, imgX=0, cutsceneAvailable=True) #defaults the first stage imgX to 0 to start it from the left part of the screen (Images.batFlyLeft, Images.batFlyRight, startingX=random.choice([0, 1400])


stageList = [stage_zero, stage_one, stage_two, stage_three]


class StageHandler:
    currentStage = stage_zero
    currentIter = 0
    effectsList = []
    consumablesList = []
    explosivesList = []
    wanderers_list = [] #list used to create enemies after stages have been completed and move them while scrolling

    def startNextStage(self):
        try:
            self.currentIter += 1
            self.currentStage = stageList[self.currentIter]
            if self.currentStage.bg_character == None:
                self.currentStage.background_characters = []
            Tools.setupStage()

        except IndexError:
            print('that was end of stage')
        #print(self.currentStage.name)

    def getCurrentStage(self):
        return self.currentStage


    def drawMatter(self):
        #print(stage_one.matterList)

        for matter in self.currentStage.matterList:
            #print(f'this is the matter"s midline: {matter.midLine}')
            #print(f'this si the matter"s midPoint: {matter.midPoint}')
            matter.cycle()
            win.blit(matter.img, (matter.x, matter.y))

            #print(f'this is how many gems it contains: {matter.amount_of_gems}')
            #print(f'this is the consumables list: {self.consumablesList}')
            if stageHandler.currentStage.scrolling:
                matter.x -= stageHandler.currentStage.scrollSpeed
                matter.update_position()

    def drawConsumables(self):
        for consumables in self.consumablesList:

                #detects if gem or not
                #if consumables.name == '':
                    #if not consumables.discovered:
                        #consumables.discover_gem()
            consumables.fall()
            win.blit(consumables.img, (consumables.x, consumables.y))

            if stageHandler.currentStage.scrolling:
                consumables.x -= stageHandler.currentStage.scrollSpeed



    def drawEffects(self):
        for effects in self.effectsList:
            if not effects.active:
                self.effectsList.remove(effects)
            else:
                effects.drawMe()
                win.blit(effects.img, (effects.x, effects.y))

                if stageHandler.currentStage.scrolling:
                    effects.x -= stageHandler.currentStage.scrollSpeed

    def drawExplosives(self):

        for explosives in self.explosivesList:
            if not explosives.active:
                self.explosivesList.remove(explosives)
            else:
                explosives.travel()
                win.blit(explosives.img, (explosives.x, explosives.y))

                if stageHandler.currentStage.scrolling:
                    explosives.x -= stageHandler.currentStage.scrollSpeed


stageHandler = StageHandler()

def testBackground(player):
    testing = True
    while testing:
        #print(stageHandler.currentStage.name)
        event = pygame.event.poll()
        #print(stageHandler.currentStage.scrolling)
        #keys = pygame.key.get_pressed()
        #print(stageHandler.currentStage.name)
        #print(stageHandler.currentStage.completed)
        #for char in stage_zero.background_characters:
            #pass
            #print(f'this is the char currentX: {char.currentX}')
        #print(stageHandler.currentStage.decalsList)
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('filler')
            stageHandler.currentStage.finalize()


        stageHandler.currentStage.drawStageBackground()
        #stageHandler.currentStage.finalize()


        update()

#testBackground()

'''
def checkFalling(self, unitsList):
    # make this for only those 'in air'  or those in the process of jumping, will make the jump allow the user to move left and right but not up or down as they return to ground
    for i in unitsList:
        if round(i.currentX) in range(self.startingX, self.width) and i.currentY < self.currentY:
            i.falling = False
        else:
            i.falling = True

        if i.falling:
            i.currentY += 6
'''
