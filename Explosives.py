import Images
import random
import Tools
import Stages
import Sounds

class Grenade():
    speed = 3
    damage = 20
    active = True

    xCentered = False

    exploding = False
    exploded = False #determines when animation is over and damage has been delivered

    dealtDamage = False

    x_gravity = 0
    y_gravity = 0

    x_displacement = 115   #displaces the x to help adjust positioning as the grenade goes from nade to explosive
    movingRight = False

    iterationList = []
    iterationCounter = 0

    def __init__(self, sender, img = Images.grenadeImg, rotationList = Images.grenadeRotate,
                 explosionList = Images.grenadeExplode, type = 'normal'):

        self.sender = sender
        self.img = img
        self.x = sender.currentX
        self.y = sender.currentY
        self.floor = sender.bottomEdge - 25
        self.rotationList = rotationList
        self.explosionList = explosionList
        self.type = type

        if self.sender.forwardFace:
            self.movingRight = True
            self.x_displacement = -115
        else:
            self.movingRight = False
            self.x_displacement = 115

        #implementing different grenade types
        #if self.name =='normal':
            #self.travelImg = Images.grenadeRotate

    """Re-centers the explosion img to the grenade img location to center since grenade enlarges to explosion"""
    def adjustCenter(self):
        self.y = self.floor - 260
        if not self.xCentered:
            self.xCentered = True
            if self.movingRight:
                self.x += self.x_displacement
            else:
                self.x -= self.x_displacement

    """Boom Boom"""
    def explode(self):
        if not self.exploded:
            self.adjustCenter()

            self.iterationList = self.explosionList
            self.exploded = Tools.animateMe(self, False, True)

        if not self.dealtDamage:
            Sounds.explosion_sound.play()
            self.explosion_radiusX = range(round(self.x), round(self.x) + self.img.get_width())
            self.explosion_radiusY = range(round(self.y), round(self.y) + self.img.get_height())
            for enemy in Stages.stageHandler.currentStage.enemiesList:
                print(f'enemy midline: {enemy.midLine}, xRadius: {self.explosion_radiusX} yRadius: {self.explosion_radiusY}')
                if enemy.midLine in self.explosion_radiusX and enemy.midPoint in self.explosion_radiusY:
                    if self.type == 'normal':
                        enemy.health -= self.damage
                        self.dealtDamage = True
                    elif self.type == 'stun':
                        enemy.stunned = True
                        self.dealtDamage = True

            for matter in Stages.stageHandler. currentStage.matterList:
                if matter.midLine in self.explosion_radiusX and matter.midPoint in self.explosion_radiusY:
                    if self.type == 'normal':
                        matter.health -= self.damage
                        self.dealtDamage = True
                    elif self.type == 'stun':
                        matter.stunned = True
                        self.dealtDamage = True

            for wanderer in Stages.stageHandler.wanderers_list:
                if wanderer.midLine in self.explosion_radiusX and wanderer.midPoint in self.explosion_radiusY:
                    if self.type == 'normal':
                        wanderer.health -= self.damage
                        self.dealtDamage = True
                    elif self.type == 'stun':
                        wanderer.stunned = True
                        self.dealtDamage = True

            if Stages.stageHandler.currentStage.boss != None:
                if Stages.stageHandler.currentStage.boss.name == 'Who':
                    Boss = Stages.stageHandler.currentStage.boss
                    if Boss.aggression:
                        if Boss.midLine in self.explosion_radiusX and Boss.midPoint in self.explosion_radiusY:
                            if self.type == 'normal':
                                Boss.health -= self.damage
                                self.dealtDamage = True
                            elif self.type == 'stun':
                                Boss.stunned = True
                                self.dealtDamage = True

                elif Stages.stageHandler.currentStage.boss.name == 'Hollow':
                    Boss = Stages.stageHandler.currentStage.boss.head # track head of Hollow for explosion damage
                    if Boss.midLine in self.explosion_radiusX and Boss.midPoint in self.explosion_radiusY:
                        if self.type == 'normal':
                            Boss.health -= self.damage
                            self.dealtDamage = True
                        elif self.type == 'stun':
                            Boss.stunned = True
                            self.dealtDamage = True

        if self.exploded:
            self.active = False


    """Grenade will travel until it hits the ORIGINAL bottomEdge of sender which is saved as
    soon as it's thrown"""
    def travel(self):
        self.iterationList = self.rotationList
        if self.y > self.floor or self.exploding:
            self.exploding = True
            self.explode()

        else:
            if self.movingRight:
                self.x += 5 - self.x_gravity

            else:
                self.x -= 3 + self.x_gravity

            self.y += -3 + self.y_gravity
            self.x_gravity += .01
            self.y_gravity += .2

        Tools.animateMe(self)

class Stun_Grenade(Grenade):
    def __init__(self, sender, img = Images.stunGrenadeRotate[0], rotationList = Images.stunGrenadeRotate,
                 explosionList = Images.stunGrenadeExplode, type = 'stun'):
        Grenade.__init__(self, sender, img, rotationList, explosionList, type)




