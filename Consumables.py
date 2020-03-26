import pygame
import Stages
import Images
import Colors
import Tools
import HeroClassCode
import Stages
import Effects
import random
import Sounds

HC = HeroClassCode

win = pygame.display.set_mode((1400, 800))
consumableText = pygame.font.SysFont('algerian', 10)
yellow = (255, 255, 0)
#text = combatTextBold.render(target_name.combatText, True, green)

#print(HC.player.name)

def spawnRandomGems(for_chest = False):
    if not for_chest:
        rng = random.randint(1, 100)
        if rng >= 90:
            return Yellow_Gem
        elif rng < 90 and rng >= 70:
            return Red_Gem
        elif rng < 70 and rng >= 40:
            return Blue_Gem
        else:
            return Green_Gem
    else:
        num_of_gems = random.randint(3, 6)
        containmentList = []
        for gem in range(num_of_gems):
            rng = random.randint(1, 100)
            if rng >= 90:
                containmentList.append(Yellow_Gem)
            elif rng < 90 and rng >= 70:
                containmentList.append(Red_Gem)
            elif rng < 70 and rng >= 40:
                containmentList.append(Blue_Gem)
            else:
                containmentList.append(Green_Gem)

        return containmentList

def spawnRandomConsumables():
    rng = random.randint(1, 100)
    if rng > 90:
        return Overshield
    elif rng <= 90 and rng > 60:
        return Battery
    else:
        return spawnRandomGems()

"""Items that may be picked up by the player including healing, shields, damage, etc...
they are appended to stageHandler.consumablesList when the enemy they are stored in dies
and thus begin to drop."""
class Consumable():
    active = True
    name = ''

    def __init__(self, name, img, corpse, x, y, animate=False):
        self.name = name
        self.img = img
        self.corpse = corpse
        self.x = x
        self.y = y

        self.animate = animate
        if self.animate:
            self.iterationCounter = 0
            self.iterationList = []

        self.landing = self.corpse.bottomEdge - 15  #adjusts a buffer since the img is drawn FROM the currentX

    def showLabel(self):
        text = consumableText.render(self.name, True, Colors.green)
        win.blit(text, (self.x, self.y - 10)) #buffered higher

    def fall(self):
        self.showLabel()
        if self.y < self.landing:
            self.y += 1
        else:
            #print(self.y, self.landing)
            pass

        if self.animate:
            Tools.animateMe(self)

"""Increases Piles batteryPower by 1"""
class Battery(Consumable):

    def __init__(self, corpse, x, y, name = 'battery', img = Images.battery):
        Consumable.__init__(self, name, img, corpse, x, y)

    def pickup(self):
        #Sounds.collect_gem_sound.play()
        if HC.Piles.batteryPower < HC.Piles.batteryClip:
            Sounds.collect_gem_sound.play()
            HC.Piles.batteryPower += 1
            Stages.stageHandler.consumablesList.remove(self)

'''Gives player a shield equal to his current max health.'''
class Overshield(Consumable):
    energy = HC.player.overshield_max_amount

    def __init__(self, corpse, x, y, name = 'overshield', img = Images.overshieldImg):
        Consumable.__init__(self, name, img, corpse, x, y)

    def pickup(self):
        Sounds.shield_sound.play()
        HC.player.overshield = True
        HC.player.overshieldAmount = self.energy
        Stages.stageHandler.consumablesList.remove(self)

class Grenade_drop(Consumable):
    amount = 1

    def __init__(self, corpse, x, y, name = 'grenade', img = Images.grenadeImg):
        Consumable.__init__(self, name, img, corpse, x, y)

    def pickup(self):
        Sounds.collect_gem_sound.play()
        HC.player.grenadeAmount += self.amount
        self.active = False


class Gem(Consumable):
    discovered = False
    amount = 0

    def __init__(self, corpse, x, y, name='', img=None, animate=True):
        Consumable.__init__(self, name, img, corpse, x, y, animate)

        self.effect = Effects.Effect(HC.player, Images.collect)

    def pickup(self):
        Sounds.collect_gem_sound.play()
        HC.player.gems += self.amount
        #Stages.stageHandler.effectsList.append(self.effect)
        pickupText = HC.creditText.render('+' + str(self.amount), True, yellow)
        HC.combatTextList.append(HC.Combat_Text(pickupText, HC.Credit_Interface, slowed=False))
        Stages.stageHandler.consumablesList.remove(self)

class Green_Gem(Gem):
    amount = 1

    def __init__(self, corpse, x, y):
        Gem.__init__(self, corpse, x, y)

        self.img = Images.greenGem[0]
        self.iterationList = Images.greenGem

class Blue_Gem(Gem):
    amount = 5
    def __init__(self, corpse, x, y):
        Gem.__init__(self, corpse, x, y)

        self.img = Images.blueGem[0]
        self.iterationList = Images.blueGem

class Red_Gem(Gem):
    amount = 10
    def __init__(self, corpse, x, y):
        Gem.__init__(self, corpse, x, y)

        self.img = Images.redGem[0]
        self.iterationList = Images.redGem

class Yellow_Gem(Gem):
    amount = 50
    def __init__(self, corpse, x, y):
        Gem.__init__(self, corpse, x, y)

        self.img = Images.yellowGem[0]
        self.iterationList = Images.yellowGem



"""Destructable Objects or Chests (ITERATIONLISTS are animated when taking damage only)"""
class Matter():
    iterationCounter = 0
    iterationList = []
    takingDamage = False

    def __init__(self, x, y, img, health, iterationList, sizeX, sizeY):
        self.img = img
        self.x = x
        self.y = y
        self.health = health
        self.originalHealth = self.health
        self.iterationList = iterationList

        self.sizeX = sizeX
        self.sizeY = sizeY
        self.midLine = x + sizeX
        self.midPoint = y + sizeY

        self.leftEdge = self.midLine - sizeX
        self.rightEdge = self.midLine + sizeX
        self.topEdge = self.midPoint - sizeY
        self.bottomEdge = self.midPoint + sizeY

        self.Xbubble = range(self.leftEdge, self.rightEdge)
        self.Ybubble = range(self.topEdge, self.bottomEdge)

        self.headshotRange = (-500, -501) #Disables headshots
        self.immune = False
        self.humanoidName = 'matter'

        self.combatStatus = ''

    def checkHealth(self):
        if self.health < self.originalHealth:
            self.takingDamage = True
            self.originalHealth = self.health
        self.showDamageTaken()

    def showDamageTaken(self):
        if self.takingDamage:
            self.takingDamage = Tools.animateMe(self, True, False)
            if not self.takingDamage:
                self.img = self.iterationList[0]

    def update_position(self):
        self.midLine = self.x + self.sizeX
        self.midPoint = self.y + self.sizeY
        self.leftEdge = self.midLine - self.sizeX
        self.rightEdge = self.midLine + self.sizeX
        self.topEdge = self.midPoint - self.sizeY
        self.bottomEdge = self.midPoint + self.sizeY

        self.Xbubble = range(self.leftEdge, self.rightEdge)
        self.Ybubble = range(self.topEdge, self.bottomEdge)



class Chest(Matter):

    gemsAdded = False
    broken = False
    has_parachute = False

    speed = 1

    def __init__(self, x, y, containmentList, img = Images.normalChest[0], health = 100, iterationList = Images.normalChest, sizeX = 35, sizeY=45):
        Matter.__init__(self, x, y, img, health, iterationList, sizeX, sizeY)

        self.containmentList = containmentList

    def sky_fall(self):
        self.y += self.speed
        self.update_position()
        if self.y >= 800: #800 is max screen Y size
            Stages.stageHandler.currentStage.matterList.remove(self)

    def cycle(self):
        if self.health <= 0:
            self.explode()
        else:
            if self.has_parachute:
                self.sky_fall()
                win.blit(Images.parachute, (self.x - 20, self.y - 65))

            self.checkHealth()


    def explode(self):
        '''
        if not self.gemsAdded:
            for gem in range(self.amount_of_gems):
                self.containmentList.append(spawnRandomGems())
        '''
        if not self.gemsAdded:
            for gem in self.containmentList:
                rngX = random.randint(-100, 100)
                rngY = random.randint(-200, 0)
                print('appending gem here')
                Stages.stageHandler.consumablesList.append(gem(self, self.x + rngX, self.y + rngY))
            self.gemsAdded = True

        self.iterationList = Images.chestExplosion
        self.broken = Tools.animateMe(self, False, True)
        if self.broken:
            Stages.stageHandler.currentStage.matterList.remove(self)

class Care_Package(Chest):
    has_parachute = True

    def __init__(self, x, y, containmentList, speed, img = Images.normalChest[0], health = 100, iterationList = Images.normalChest, sizeX = 35, sizeY=45):
        Chest.__init__(self, x, y, containmentList, img, health, iterationList, sizeX, sizeY)

        self.speed = speed





    #def pickup(self):

