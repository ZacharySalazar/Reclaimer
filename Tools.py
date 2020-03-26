#import pygame
#import Stages
import HeroClassCode as HC
import random
import Sounds
red = (255, 0, 0)
blue = (0, 0, 255)

class Frame():
    iterationCounter = 0

    def __init__(self, iterationList, x, y):
        self.img = iterationList [0]
        self.iterationList = iterationList
        self.x = x
        self.y = y

def deal_damage_to_player(damage, stun_debuff = 0):
    if not HC.player.immune:

        if HC.player.overshieldAmount > 0:
            if HC.player.overshieldAmount - damage <= 0:
                damage = abs(HC.player.overshieldAmount - damage)
                HC.player.overshieldAmount = 0
                #damage = abs(HC.player.overshieldAmount - damage)
            else:
                HC.player.overshieldAmount -= damage
                text = '-' + str(damage) + ' shield'
                text = HC.player_interface_combat_text.render(text, True, blue)
                target = HC.Player_Healthbar_Interface
                HC.combatTextList.append(HC.Combat_Text(text, target, True))

                damage = 0

        if damage > 0:
            HC.player.health -= damage
            print('adding player interface')
            text = '-' + str(damage) + ' health'
            text = HC.player_interface_combat_text.render(text, True, red)
            target = HC.Player_Healthbar_Interface
            HC.combatTextList.append(HC.Combat_Text(text, target, True))

        if stun_debuff != 0:
            HC.player.stun_cooldown = stun_debuff
            HC.player.stunned = True

        if HC.player.health > 0:
            Sounds.player_damaged_sound.play()

def animateMe(self, conditionNotMet = None, conditionMet = None, givenLists = None):
    #givenLists allows a set of iterationLists to default to [list data type]


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
            print(self.iterationCounter)
            self.img = self.iterationList[self.iterationCounter]
            self.iterationCounter += 1

            if self.iterationCounter >= len(self.iterationList):
                self.iterationCounter = 0


'''Used to get specific measurements for images and outlines'''

def measureEnemy(spec):
    if Stages.stageHandler.currentStage.enemiesList != []:
        mousePosition = pygame.mouse.get_pos()
        enemy = Stages.stageHandler.currentStage.enemiesList[0]

        print(f'this is mouse X: {mousePosition[0]}, this is mouse Y: {mousePosition[1]}')
        if spec == 'midline':
            print(f'This is the enemy midline: {enemy.midLine}')
        elif spec == 'topedge':
            print(f'this is the enemy currentY: {enemy.currentY}')

"""Resets and setups between stages  (called in Stages.startNextStage()"""
def setupStage():
    HC.Piles.rechargeBattery()
    HC.Piles.recharging = True

class tester:
    helper = 1

bot = tester()
def testing():
    rand = random.randint(1, 1)
    print(rand)

testing()