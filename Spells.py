import pygame
import HeroClassCode as HC
import Stages
import Tools
import Sounds

win = pygame.display.set_mode((1400, 800))
red = (255, 0, 0)








activeSpells = []
'''Spells are used for Buffs/Damage/Healing'''
class Spell:
    iterationCounter = 0
    active = True

    def __init__(self, amount, img, iterationList, char):
        self.amount = amount
        self.img = img
        self.iterationList = iterationList
        self.char = char
        #self.x = char.currentX
        #self.y = char.currentY



        #self.x = char_using_effect.currentX
        #self.y = char_using_effect.currentY
        #self.width = width
        #self.height = height
        #self.cycles = cycles

        #self.img = pygame.transform.scale(self.img, (char_using_effect.img.get_size()[0], char_using_effect.img.get_size()[1]))
        #self.xWidth = char_using_effect.img.get_width()

    def updateLocation(self):
        self.x = self.char.currentX
        self.y = self.char.currentY

    def resetIteration(self):
        self.iterationCounter = 0

    def animateMe(self, conditionNotMet = None, conditionMet = None):
        if self.iterationCounter > len(self.iterationList):
            self.resetIteration()

        else:
            if conditionNotMet != None:
                self.img = self.iterationList[self.iterationCounter]
                self.iterationCounter += 1

                if self.iterationCounter >= len(self.iterationList):
                    self.iterationCounter = 0
                    return conditionMet
                else:
                    return conditionNotMet

            else:
                self.img = self.iterationList[self.iterationCounter]
                self.iterationCounter += 1

                if self.iterationCounter >= len(self.iterationList):
                    self.iterationCounter = 0

#rally = Effects(rallyImg, rallyImgList)

'''Buffs specifically may cycle for continual expression
note: char"s are also the targets of buffs and their attributes
are used so acordingly'''
class Buff(Spell):
    buffed = False
    school = 'Buff'

    def __init__(self, buff_type, amount, img, iterationList, char, cycles, specifiedX = None, specifiedY = None):
        Spell.__init__(self, amount, img, iterationList, char)

        #These poistition the x and y of buff on their char in intialization
        #char in buffs are the TARGETS of the buff
        self.buff_type = buff_type
        self.x = self.char.currentX
        self.y = self.char.currentY
        self.cycles = cycles
        self.specifiedX = specifiedX
        self.specifiedY = specifiedY

'''These are the offensive flying across map spells
char are the casters in this spell school and the targets
are the spells focus'''

class Destruction(Spell):
    school = 'Destruction'

    def __init__(self, amount, img, iterationList, char, target, leftIteration, rightIteration, movingRight, speed, yBuffer=None, spellImgYBuffer = None,
                 spellImgXBuffer = None):
        Spell.__init__(self, amount, img, iterationList, char)

        #defaults the starting position of a destruction spell at it's caster
        self.x = self.char.midLine
        self.y = self.char.topEdge
        self.yBuffer = yBuffer


        self.target = target
        self.leftIteration = leftIteration
        self.rightIteration = rightIteration
        self.movingRight = movingRight
        self.speed = speed

        self.spellImgXBuffer = spellImgXBuffer  # added to X to find left side and subtracted from x.width() to find right side Point ends
        self.spellImgYBuffer = spellImgYBuffer #adds to Y to find midPoint

        self.frontEnd = self.x + self.spellImgXBuffer
        self.midPoint = self.y + self.spellImgYBuffer + round(self.img.get_height() / 2)

    # def dealDamage(self, target):
    #     if not target.immune:
    #         target.health -= self.amount
    #         activeSpells.remove(self)
    #
    #         text = HC.combatTextFont.render('-' + str(self.amount) + ' health', True, red)
    #         HC.combatTextList.append(HC.Combat_Text(text, HC.Player_Healthbar_Interface, slowed=True))
    #     else:
    #         pass

    def impact(self):
        print('destruction spell has landed!')
        Tools.deal_damage_to_player(self.amount)
        if not HC.player.immune:
            activeSpells.remove(self)
            Sounds.plaguebolt_hit.play()
        #self.dealDamage(self.target)


    #maybe add an explosion on impact
    '''Flys towards the player until colliding with midLine for damage of flying off screen
    upon impact will deal damage and remove itself from activeSpells List (Also draws the image)'''
    def fly(self):
        #print(f'this is the arrow midLine: {self.midLine}')
        print(f'this is the arrow midPoint: {self.midPoint}')
        self.midPoint = self.y + self.spellImgYBuffer

        if not self.movingRight:

            self.frontEnd = self.x + self.spellImgXBuffer #finding the close (left facing) point
            print(f'this is fireball frontEnd: {self.frontEnd}')
            self.iterationList = self.leftIteration
            self.x -= self.speed

            if self.midPoint in self.target.Ybubble:
                if self.frontEnd in self.target.Xbubble:
                    self.impact()

            if Stages.stageHandler.currentStage.scrolling:
                self.x -= Stages.stageHandler.currentStage.scrollSpeed

        elif self.movingRight:
            self.frontEnd = (self.x + self.img.get_width()) - self.spellImgXBuffer  #finding the far (right facing) point
            self.iterationList = self.rightIteration
            self.x += self.speed

            if self.midPoint in self.target.Ybubble:
                if self.frontEnd in self.target.Xbubble:
                    self.impact()



        self.animateMe()
        win.blit(self.img, (self.x, self.y + self.yBuffer))


'''Finds effects in activeSpells and updates their location before drawing them.'''
def showSpells():
    #make conditionals like if effect is a temporary or continual also ones that determine when they end
    #also where they are to be positioned
    for spell in activeSpells:
        if spell.school == 'Destruction':
            spell.fly()



        #if spell.school == 'Heal':

        if spell.school == 'Buff':
            if not spell.buffed:
                if spell.buff_type == 'damage':
                    spell.char.dmg += spell.amount
                    #spell.char.combatText
                    spell.buffed = True

                elif spell.buff_type == 'heal':
                    if spell.char.health + spell.amount >= spell.char.maxHealth:
                        spell.char.health = spell.char.maxHealth
                    else:
                        spell.char.health += spell.amount
                    spell.buffed = True

            #spell.updateLocation()

            if not spell.cycles:
                print('spell running')
                #only for spells that cycle through animation once
                spell.updateLocation()
                spell.animateMe()
                spell.active = spell.animateMe(True, False)
                spell.img = pygame.transform.scale(spell.img, (round(spell.char.img.get_size()[0]),
                                                               round(spell.char.img.get_size()[1])))

                win.blit(spell.img, (spell.char.midLine - round(spell.char.sizeX),
                                     spell.char.midPoint - round(spell.char.sizeY)))

            elif spell.cycles:
                spell.updateLocation()
                spell.animateMe()

                #sets specific dimensions to find center of enemies, make this a function if needed repeatedly
                if spell.char.name == 'regularSkeleton':
                    spell.img = pygame.transform.scale(spell.img, (round(spell.char.img.get_size()[0] - 50),
                                                                   round(spell.char.img.get_size()[1] - 50)))

                    if spell.char.forwardFace:
                        win.blit(spell.img, (spell.char.currentX - 10, spell.char.currentY + 35))
                    elif not spell.char.forwardFace:
                        win.blit(spell.img, (spell.char.currentX + 45, spell.char.currentY + 35))


        #if cycles; only continues so long as char is alive
        if spell.school == 'Buff':
            if spell.char.health <= 0:
                spell.active = False

        if not spell.active:
            activeSpells.remove(spell)

