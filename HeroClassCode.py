import pygame
import random
import Images
import Stages
import random
import Text
import Spells
import Explosives
import Sounds
import Shop_Images as SI

pygame.init()
win = pygame.display.set_mode((1400, 800))
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (138, 43, 226)
grey = (169, 169, 169)
white = (0, 0, 0)

def checkCollision(ob1, ob2):
    #ob1 is the moving object by default
    #print(f'ghost midpoint: {ob1.midPoint}, player bubble {ob2.Ybubble}')
    if ob1.midPoint in ob2.Ybubble:
        if ob1.leftEdge + ob1.xBuffer in ob2.Xbubble or ob1.rightEdge - ob1.xBuffer in ob2.Xbubble:
            return True

    else:
        #print('no detection')
        return False

"""Specifically used for basic animations"""
class Frame():
    iterationCounter = 0

    def __init__(self, iterationList, x, y):
        self.img = iterationList[0]
        self.iterationList = iterationList
        self.x = x
        self.y = y

    def animateMe(self, shotgun_use=None, explosive = False):
        if self.iterationCounter >= len(self.iterationList):
            self.iterationCounter = 0

            if explosive:
                self.active = False


            #used to reset the muzzle flash for player shotgun animation
            if shotgun_use == True:
                player.shotgun_muzzle_flash = False

        else:
            self.img = self.iterationList[self.iterationCounter]
            self.iterationCounter += 1

class explosive_frame(Frame):
    active = True

    def __init__(self, iterationList=Images.rocket_Explosion, x=0, y=0):
        Frame.__init__(self, iterationList, x, y)

    def travel(self):
        self.animateMe(explosive=True)

shotgun_blast_left = Frame(iterationList=Images.Shotgun_blast, x=0, y=0)
shotgun_blast_right = Frame(iterationList=Images.Shotgun_blast_right, x=0, y=0)
shield_shell = Frame(iterationList=SI.redEyesShieldActive, x=0, y=0)

#rocket_explode = explosive_frame(iterationList=Images.chestExplosion, x=0, y=0)


combatTextList = []
player_interface_combat_text = pygame.font.SysFont('yugothicregularyugothicuisemilight', 20)
combatTextFont = pygame.font.SysFont('yugothicregularyugothicuisemilight', 15) # used for damage texts
combatTextHeadshot = pygame.font.SysFont('algerian', 16)  # used for headshots.... obviously
combatTextBold = pygame.font.SysFont('segoeuisemibold', 16)  # used for casting and buffing
ammoText = pygame.font.SysFont('yugothicregularyugothicuisemilight', 12)
creditText = pygame.font.SysFont('segoeuisemibold', 14)


def deal_damage_to_player(damage, stun_debuff=0):
    if not player.immune:

        if player.overshieldAmount > 0:
            if player.overshieldAmount - damage <= 0:
                damage = abs(player.overshieldAmount - damage)
                player.overshieldAmount = 0
                # damage = abs(HC.player.overshieldAmount - damage)
            else:
                player.overshieldAmount -= damage
                text = '-' + str(damage) + ' shield'
                text = player_interface_combat_text.render(text, True, blue)
                target = Player_Healthbar_Interface
                combatTextList.append(Combat_Text(text, target, True))

                damage = 0

        if damage > 0:
            player.health -= damage
            print('adding player interface')
            text = '-' + str(damage) + ' health'
            text = player_interface_combat_text.render(text, True, red)
            target = Player_Healthbar_Interface
            combatTextList.append(Combat_Text(text, target, True))

        if stun_debuff != 0:
            player.stun_cooldown = stun_debuff
            player.stunned = True

        if player.health > 0:
            Sounds.player_damaged_sound.play()

class Combat_Text:
    decriment = 20

    def __init__(self, text, char, slowed = False, idle = None):
        self.text = text
        self.char = char
        self.x = self.char.midLine
        self.y = self.char.topEdge - self.decriment      #20 starting is 5 up from 15 for healthbars



        self.yAnchor = self.y    #anchors the Y so that it dissapears after certain distance from anchor Y
        self.slowed = slowed        # used for buffs or important information to be read easier
        self.idle = idle

    '''Creates a floating combatText from anchor position that dissapates after specified distance is over.
    the yLocation is usually the topEdge of image which needs to be decrimented due to images being drawn
    at lower than the image currentY instead of higher than the currentY'''
    def drawText(self):
        if self.idle:
           pass

        else:
            if self.slowed:
                self.decriment += .5
            elif not self.slowed:
                self.decriment += 4

        self.x = self.char.midLine
        self.y = self.char.topEdge - self.decriment
        #adjusts here specificall for being above player healthbar
        if self.char.humanoidName == 'Player':
            self.x, self.y = 200, 100

        win.blit(self.text, (self.x, self.y - 30))

        if self.decriment >= 50:
            combatTextList.remove(self)

        if self.char.combatStatus == '' and self.idle == True:
            combatTextList.remove(self)
"""Object for Credit Text in bottom Left reference so that It can update
using the Combat_Text Class"""
class Credit_Interface():
    midLine = 95
    topEdge = 790
    humanoidName = 'Credit_Menu'
    combatStatus = ''

"""Object for reference of Combat Text updating player health changes"""
class Player_Healthbar_Interface():
    midLine = 220
    topEdge = 100
    humanoidName = 'Player Healthbar Interface'
    combatStatus = ''

class Humanoid:
    ranged = False   #determines how the object interacts with the player
    usedAbility = False  #determines if the object has used their ability yet
    autoCastingReady = True #for casters to use castthis functions
    autoCastingReadyTimer = 0

    stealth = False # determines if the image is harder to see (used primarly by the FadeWalker)

    #attackSpeed = 30  #determines the cd for melee and ranged auto attacks. larger number; slower attacks


    risen = True #determines if the enemy is summoned or rises to battle from the ground

    attacking = False  # determines if melee attacking animation and damage deliverance enabled
    takingDamage = False  # determines if damage was taken by the character
    takingDamageTimer = 0
    showDamage = True #determines if the object may be interuppted by damage
    showDamageTimer = 0

    startAction = False
    inAction = True
    inActionTimer = 0

    humanoidName = None
    combatText = ''
    combatStatus = '' #status is debuff conditions like stuns

    dead = False    # determines if the healthbar has fallen below zero AND death iteration has gone to end

    forwardFace = True   # gets the direction of the humanoid fdyingTimeror img processing (left or right)
    iterationCounter = 0

#active events
    speaking = False
    speechList = []
    falling = False
    movingLeft = False  # detects directional movement for automated hover function

    #animation variables
    aggression = False   # determines if the object has left hover function and is showing tracking/ aggresion towards player location
    chill = False
    chillTimer = 0
    usingAbility = False
    #cooldowns
        #  melee Cooldown is how long in between each auto attack in melee range from object
    meleeCooldown = False  # detects if melee auto attack on cooldown
    meleeCooldownTimer = 0   # tracks time since start time
    melee_sound = Sounds.scythe_sound
    melee_sound_reset = True

    #meleeCooldownTimer = 2    # add this to change the melee cd for different enemies !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    #debuffs
    stunned = False
    stunCooldownTimer = 0

    frozen = False

    immune = False

    #def __init__(self, name, iconImg, startingX, startingY, sizeX, sizeY, health, dmg, speed, img, iterationList, idleLeftList, idleRightList, leftWalkList, rightWalkList,
                 #leftAttackList, rightAttackList, leftHurtList, rightHurtList, deathList):  original

    def __init__(self, name, iconImg, startingX, startingY, findMid, sizeX, sizeY, xBuffer, yBuffer, health, dmg, speed, img, iterationList, idleLeftList, idleRightList, leftWalkList, rightWalkList,
                 leftAttackList, rightAttackList, leftHurtList, rightHurtList, deathList, droppedConsumable = None, attackSpeed = 30):  #can choose to make npcs aggressive on spawn

        self.name = name
        self.iconImg = iconImg
        self.currentX = startingX
        self.currentY = startingY
        self.findMid = findMid #given amount to find the midline
        self.sizeX = sizeX # subtracted and added from the midline to find the left and right edges of an image
        self.sizeY = sizeY # The full distance from the topEdge of the img to the bottom Edge of the img
        self.xBuffer = xBuffer #Added distance from midLine to determine attackRange of image                         #round(sizeX / 2)  # allows image to match player hitbox based off its size   (Primmarily for enemies to make them closer proximity estimations to player conflicts
        self.yBuffer = yBuffer #added to the img to find the distance after invis background from actual top Y of the img
        self.midLine = self.currentX + findMid   # declares the middle center between left and right dimensions of the image

        self.attackRange = range(self.midLine - self.xBuffer, self.midLine + self.xBuffer)

        self.leftEdge = self.midLine - sizeX   # declares left edge of the img
        self.rightEdge = self.midLine + sizeX  # declares the right edge of the img
        self.midPoint = self.currentY + self.yBuffer + (round(self.sizeY / 2))#self.currentY + sizeY  # finds center mass of img
        self.topEdge = self.currentY + self.yBuffer #self.midPoint - sizeY   # finds top edge of img
        self.bottomEdge = self.topEdge + self.sizeY #self.midPoint + sizeY #finds bottom edge of img
        self.centerPoint = range(self.midPoint - 20, self.midPoint + 20)
        self.Xbubble = range(self.leftEdge, self.rightEdge)  # declares the personal X bubble dimensions of the img
        self.Ybubble = range(self.topEdge, self.bottomEdge) # declares the personal Y bubble dimensions of the img
        self.headshotRange = range(self.topEdge, round(self.topEdge + (self.sizeY / 3)))

        if startingX > 800:
            self.leftAnchor = startingX - 300
            self.rightAnchor = startingX
        else:
            self.leftAnchor = startingX
            self.rightAnchor = startingX + 300

        self.originalHealth = health # comparative numeral to current health to detect changes in health
        self.maxHealth = health    # gets the max health based off their starting health and for healing percentages in game
        self.health = health
        self.dmg = dmg
        self.speed = speed
        self.slow_speed = round(speed / 2)
        self.img = img
        self.iterationList = iterationList
        self.idleLeftList = idleLeftList
        self.idleRightList = idleRightList
        self.leftWalkList = leftWalkList
        self.rightWalkList = rightWalkList
        self.leftAttackList = leftAttackList
        self.rightAttackList = rightAttackList
        self.leftHurtList = leftHurtList
        self.rightHurtList = rightHurtList
        self.deathList = deathList
        self.attackSpeed = attackSpeed

        self.droppedConsumable = droppedConsumable


    def sayName(self):
        print(f'Your name is {self.name}')


    def castThis(self, spell_name, spell_type, topRng, spellImageList, target_name, amount_given, combat_text_given,
                leftIteration, rightIteration, summoned_enemy_class = None, summoned_enemy_name = None, spellImageRightList = None,
                speed = None, autoCasting = None, spellYBuffer = None, spellImgXBuffer = 0, spellImgYBuffer = 0, cyclic = False):  #end condition must be preset to True (ready to go)
        #target_name can be a string if iterating through lists searching for name matching
            #or it can be an object for single target manipulations.
                                                                                                                                      #buffs only need a spellImageList since they are circles
                                                                                                                                      #desturctionspells use 'spellImageRightList due to them having
                                                                                                                                      #two directions
        #spellYBuffer adds to the spells currentY when drawn to shoot from hands or mid of characters casting it.



        #print(self.autoCastingReady)
        if autoCasting:
            if not self.autoCastingReady:
                self.autoCastingReady, self.autoCastingReadyTimer = self.coolDown(self.autoCastingReady, self.autoCastingReadyTimer, 100)

        #create cd for usedAbility  IN THIS FUNCTION since its always being called / otherwise autocasting going at it for ranged attackers

        #if not self.usedAbility or self.autoCastingReady:
        if autoCasting and not self.autoCastingReady:   #check is autoCasting and if the cd isnt over
            self.getFaceDirection(player)
            self.animateMe(givenLists=[self.idleLeftList, self.idleRightList])

        elif self.usedAbility and not autoCasting:     #check if ability already used and user isn't autoCasting
            pass

        else:               #continue
            if not self.startAction:
                #print('in order 1')
                rng = random.randint(1, topRng)
                if rng == 1:
                    self.startAction = True
                    self.resetIteration()

                    if not autoCasting and spell_name != '':
                        self.combatText = 'Casted ' + str(spell_name)
                        text = combatTextBold.render(self.combatText, True, purple)
                        combatTextList.append(Combat_Text(text, self, slowed=True))   #alerts combat Text spell is casted

            if self.startAction:
                #print('in order 2')
                if self.inAction:
                    #check for spell or autoCast for ranged classes   if autoCast usingAbility cant be messed with due to it shutting down the hover that leads to it
                    if autoCasting:
                        pass
                    else:
                        self.usingAbility = True


                    self.getFaceDirection(player)

                    if self.forwardFace:
                        self.iterationList = rightIteration
                    elif not self.forwardFace:
                        self.iterationList = leftIteration

                    if self.iterationCounter < len(self.iterationList) - 1:
                        self.iterationCounter += 1
                    else:
                        self.iterationCounter = len(self.iterationList) - 1

                        if autoCasting:
                            self.inAction = False
                        else:
                            self.inAction, self.inActionTimer = self.coolDown(self.inAction, self.inActionTimer, 20)

                self.img = self.iterationList[self.iterationCounter]
                #print(self.inAction)

            if not self.inAction:
                print('in order 3')
                if self.usingAbility or autoCasting:
                #decide spell type here (the type determines the combat text color here after casting animation ends
                #Will append the spell to the active spells list unless it is a summon spell which is deal with here. ------------

                    if spell_type == 'Buff':
                        #Finding player to heal (player is always and object not a name
                        #SPECIFICALLY FOR HEALING WHICH IS NOT CYCLIC
                        if target_name != str(target_name):
                            target_name.combatText = combat_text_given
                            text = combatTextBold.render(target_name.combatText, True, green)
                            combatTextList.append(Combat_Text(text, target_name, slowed=True))
                            print('appending the heal')
                            Spells.activeSpells.append(
                                Spells.Buff('heal', amount_given, spellImageList[0], spellImageList, target_name, cycles=cyclic)
                            )
                        else:

                            for enemy in Stages.stageHandler.currentStage.enemiesList:
                                if enemy.name == target_name:
                                    enemy.combatText = combat_text_given             #ex: 'damage given'
                                    text = combatTextBold.render(enemy.combatText, True, yellow)
                                    combatTextList.append(Combat_Text(text, enemy, slowed = True))
                                    Spells.activeSpells.append(
                                        Spells.Buff('damage', amount_given, spellImageList[0], spellImageList, enemy, cycles=cyclic)) #change to cyclic with input

                    #this spellType uses the normal spellImageList as it's left iteration and the optional 'spellImageRightList as its right iteration List
                    #unique IDs in parameters used are [leftIteration, rightIteration, movingRight, speed]
                    elif spell_type == 'Destruction':
                        print('casted destro')
                        self.getFaceDirection(player)
                        if not self.forwardFace:
                            movingRight = False
                        else:
                            movingRight = True

                        if spellYBuffer != None:
                            Spells.activeSpells.append(Spells.Destruction(amount=amount_given, img=spellImageList[0], iterationList=spellImageList, char=self, target=target_name,
                                                                          leftIteration=spellImageList, rightIteration=spellImageRightList, movingRight=movingRight, speed=speed, yBuffer=spellYBuffer,
                                                                          spellImgXBuffer=spellImgXBuffer, spellImgYBuffer=spellImgYBuffer))
                        else:
                            Spells.activeSpells.append(Spells.Destruction(amount=amount_given, img=spellImageList[0],iterationList=spellImageList, char=self, target=target_name,
                                                                          leftIteration=spellImageList, rightIteration=spellImageRightList, movingRight=movingRight, speed=speed,
                                                                          yBuffer=spellYBuffer, spellImgXBuffer=spellImgXBuffer, spellImgYBuffer=spellImgYBuffer))



                    #Adds specified amount of enemies to currentStage enemies within the stage boundaries here
                    #without using the spells class
                    elif spell_type == 'Summon':
                        for enemy_being_summoned in range(amount_given):
                            xRng = random.randint(self.currentX - 300, self.currentX + 300)
                            yRng = random.randint(Stages.stageHandler.currentStage.topBoundary, Stages.stageHandler.currentStage.bottomBoundary - 100) #draws at the currentY so needs to be lowered to stay in bounds

                            if summoned_enemy_name == 'regularSkeleton':
                                Stages.stageHandler.currentStage.enemiesList.insert(0, summoned_enemy_class('regularSkeleton', xRng, yRng, summoned = True, aggression = True))
                            else:
                                Stages.stageHandler.currentStage.enemiesList.insert(0, summoned_enemy_class(xRng, yRng))


                    self.usingAbility = False
                    self.startAction = False
                    self.inAction = True

                    if autoCasting:
                        self.autoCastingReady = False

                    else:
                        self.usedAbility = True


    def speakText(self, ID, textFile, function_at_end = None, parameters_for_function = None, specifiedDimensions = None):
        #print('we are still speaking')
        if self.speechList == []:
            #print('we appending an empty list')
            if specifiedDimensions != None:
                self.speechList.append(Text.TextBox(ID, self, specifiedDimensions))
            else:
                self.speechList.append(Text.TextBox(ID, self))
            self.speaking = True

        else:
            if self.speechList[0].completed and self.speechList[0].ID != ID:
                #print('we are emptying the list')
                self.speechList = []

                if specifiedDimensions != None:
                    self.speechList.append(Text.TextBox(ID, self, specifiedDimensions))
                else:
                    self.speechList.append(Text.TextBox(ID, self))

                self.speechList[0].nextText() #####!!!! have to reset next Text when transfering to a different text file
                self.speaking = True

            elif self.speechList[0].ID != ID:
                #print('ID doesnt match')
                self.speechList[0].completed = True

            elif self.speechList[0].completed:
                self.speaking = False

            else:
                if self.speaking:
                    for speech in self.speechList:
                        speech.runFile(self, textFile, function_at_end, parameters_for_function)


    def showHealth(self):
        self.health = round(self.health, 2)
        print(f'{self.name} health is {self.health}')



    '''Used for damage applications (utilized by player and enemies) parameters may specify headshots for player
    and debuffs for player / enemies'''
    def dealDamage(self, target, amount, headshot = False, debuff = None):
        if debuff != None:
            if not target.immune:
                if target.humanoidName != 'Boss':
                    if debuff == 'stun' or debuff == 'frozen':
                        target.stunned = True
                        stunText = 'STUNNED'
                        stunText = combatTextBold.render(stunText, True, yellow)
                        target.combatStatus = Combat_Text(stunText, target, idle=True)
                        combatTextList.append(target.combatStatus)

                        if debuff == 'frozen':
                            print('Drawing frozen image here.')

                    if debuff =='knockbackRight':
                        target.currentX += 100
                    elif debuff == 'knockbackLeft':
                        target.currentX -= 100

                    target.stunned = True
                    stunText = 'STUNNED'
                    stunText = combatTextBold.render(stunText, True, yellow)
                    target.combatStatus = Combat_Text(stunText, target, idle=True)
                    combatTextList.append(target.combatStatus)

        if not target.immune:
            if headshot:
                amount = amount * 2
                target.health -= amount
                target.combatText = str(amount) + ' HEADSHOT'
                text = combatTextHeadshot.render(target.combatText, True, red)

            elif not headshot:
                target.health -= amount
                target.combatText = str(amount) + ' damage'
                text = combatTextFont.render(target.combatText, True, red)

            if target.humanoidName != 'Player':
                print('still obv referencing text')
                combatTextList.append(Combat_Text(text, target, slowed=False))

            elif target.humanoidName == 'Player':
                print('adding player interface')
                text = '-' + str(amount) + ' health'
                text = combatTextFont.render(text, True, red)
                target = Player_Healthbar_Interface
                combatTextList.append(Combat_Text(text, target, True))

        elif target.immune:
            if target.humanoidName == 'Skeleton':
                target.combatText = 'Blocked'
                text = combatTextFont.render(target.combatText, True, blue)
                combatTextList.append(Combat_Text(text, target))
            else:
                text = combatTextFont.render('Immune', True, white)
                combatTextList.append(Combat_Text(text, target))


#'''Determines if the character is facing the right direction or not based
#off comparison to other objects midline'''
    '''Takes and action and a timer. When the timer increases to an amount larger than the cooldown
    parameter the action becomes its opposite. If affectOther is present the affectOther becomes its
    opposite when the cooldown is over'''
    def coolDown(self, action, timer, cooldown, affectOther = None):

        timer += 1
        if timer > cooldown:
            action = not action
            timer = 0
            self.iterationCounter = 0
            if affectOther != None:
                affectOther = not affectOther

        else:
            action = action
            if affectOther != None:
                affectOther = affectOther

        if affectOther != None:
            return action, timer, affectOther
        else:
            return action, timer

    def getFaceDirection(self, comparedObj):
        if self.midLine <= comparedObj.midLine:
            self.forwardFace = True
        elif self.midLine > comparedObj.midLine:
            self.forwardFace = False

    def applyDebuff(self, debuff, target):
        if debuff == 'stun':
            target.stunned = True

        elif debuff == 'slow':
            target.slowed = True


    '''Reports the health of the character to see if the original health has changed
     since the updated health (if it has it creates aggro in the self)'''
    def reportHealth(self):
        if self.health < self.originalHealth:
            self.aggression = True
            print(f'{self.name} took damage and is now at {self.health}')
            print(f'this is showDamage bool: {self.showDamage} this is showDamageTimer: {self.showDamageTimer}')
            self.originalHealth = self.health

            if self.showDamage or self.health <= 0:
                self.takingDamage = True
                self.showDamage = False
                self.resetIteration()

        else:
            self.originalHealth = self.health

        #if self.midPoint in range(target.topEdge,target.bottomEdge - self.yBuffer) and self.leftEdge + self.xBuffer in target.Xbubble or \
                #self.midPoint in range(target.topEdge, target.bottomEdge - self.yBuffer) and self.rightEdge - self.xBuffer in target.Xbubble:

    '''Used specifically by Player'''
    def melee(self, target):
        if self.midPoint in range(target.topEdge, target.bottomEdge): #- self.yBuffer):
            #print('lined up with enemies')
            #if target.midLine in range(self.midLine - self.xBuffer) or target.midLine in range(self.midLine + self.xBuffer):

            #self.xBuffer = 40

            if self.midLine < target.midLine:
                if target.midLine in range(self.midLine, self.midLine + self.xBuffer):
                    if self.forwardFace:
                        print('player hit enemies to the right of him')
                        self.dealDamage(target, self.dmg, debuff='knockbackRight')


            elif self.midLine >= target.midLine:
                if target.midLine in range(self.midLine - self.xBuffer, self.midLine):
                    if not self.forwardFace:
                        print('player hit enemies to the left of him')
                        self.dealDamage(target, self.dmg, debuff='knockbackLeft')

                                                                                                                                                #self.leftEdge + self.xBuffer in target.Xbubble or \
                    #self.midPoint in range(target.topEdge, target.bottomEdge - self.yBuffer) and self.rightEdge - self.xBuffer in target.Xbubble:
                #self.dealDamage(target)

    '''Allows all characters to auto attack when in melee range of given target'''
    def meleeAttack(self, target):

        '''Checks for stun or debuffs depending on the attacking NPC's autoAttack'''
        def checkMeleeAttackType(self, target):
            if self.name == 'barbarian':
                print('deal special damage here!')
                self.dealDamage(target, self.dmg, debuff = 'stun')
            else:
                deal_damage_to_player(self.dmg)
                #target.health -= self.dmg



        if self.meleeCooldown:

            self.meleeCooldown, self.meleeCooldownTimer = self.coolDown(
                self.meleeCooldown, self.meleeCooldownTimer, self.attackSpeed)

            if target.midLine >= self.midLine:
                self.iterationList = self.idleRightList

            if target.midLine < self.midLine:
                self.iterationList = self.idleLeftList
            self.getFaceDirection(player)
            self.animateMe()

        elif not self.meleeCooldown:
            if self.melee_sound_reset:
                self.melee_sound.play()
                self.melee_sound_reset = False

            if target.midLine >= self.midLine:
                self.iterationList = self.rightAttackList

            if target.midLine < self.midLine:
                self.iterationList = self.leftAttackList
            self.getFaceDirection(player)

            self.meleeCooldown = self.animateMe(False, True)
            if self.meleeCooldown:
                self.melee_sound_reset = True
                checkMeleeAttackType(self, target)


    '''Animates a given image with a given sprite iteration List'''
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

            elif givenLists != None:

                if not self.forwardFace:
                    self.iterationList = givenLists[0]
                elif self.forwardFace:
                    self.iterationList = givenLists[1]

                if self.iterationCounter >= len(self.iterationList):
                    self.resetIteration()

                self.img = self.iterationList[self.iterationCounter]
                self.iterationCounter += 1

                if self.iterationCounter >= len(self.iterationList):
                    self.iterationCounter = 0

            else:
                #if self.iterationCounter > len(self.iterationList):
                    #self.resetIteration()

                if self.iterationCounter >= len(self.iterationList):
                    self.iterationCounter = 0

                self.img = self.iterationList[self.iterationCounter]
                self.iterationCounter += 1

                if self.iterationCounter >= len(self.iterationList):
                    self.iterationCounter = 0


#update and reset fucntions
    '''Constantly redefines character edges and position. Redefined with all changes in position'''
    def outlineSelf(self):

        self.leftEdge = self.midLine - self.sizeX
        self.midLine = self.currentX + self.findMid
        self.attackRange = range(self.midLine - self.xBuffer, self.midLine + self.xBuffer)
        self.rightEdge = self.midLine + self.sizeX
        self.topEdge = self.currentY + self.yBuffer
        self.midPoint = self.currentY + self.yBuffer + (round(self.sizeY / 2))#self.currentY + self.sizeY
        self.bottomEdge = self.topEdge + self.sizeY
        self.centerPoint = (self.midPoint - 20, self.midPoint + 20)

        self.Xbubble = range(self.leftEdge, self.rightEdge)
        self.Ybubble = range(self.topEdge, self.bottomEdge)
        self.headshotRange = range(self.topEdge, round(self.topEdge + (self.sizeY / 3)))

        if self.humanoidName == 'Player':
            if player.currentWeapon.name == 'Shotgun':
                player.currentWeapon.update_shotgun_range()



    def resetIteration(self):
        self.iterationCounter = 0
####
#'''The character will stop chasing and become idle for variation'''
    def calm(self, permanent = None):
        if permanent != None:
            self.chill = True

        if not self.chill:
            if not self.stealth:
                rng = random.randint(1, 350)
                if rng == 1:
                    self.chill = True

        elif self.chill:
            if permanent != None:
                self.chill, self.chillTimer = self.coolDown(self.chill, self.chillTimer, 500)
            else:
                self.chill, self.chillTimer = self.coolDown(self.chill, self.chillTimer, random.randint(80, 120))
                if not self.chill:
                    self.resetIteration()

    def move(self, direction):


        if self.attacking:
            self.iterationCounter = 0
            self.attacking = False

        if self.humanoidName == 'Player':
            if player.shooting:
                self.resetIteration()
                player.shooting = False

            if player.rocket_shooting:
                self.resetIteration()
                player.rocket_shooting = False

            if player.reloading:
                self.resetIteration()
                player.reloading = False

            if player.throwing_grenade:
                self.resetIteration()
                player.throwing_grenade = False

        #print(self.bottomEdge)
        # Function constantly updates the outline and center of model as it moves
        #print(f'left: {self.leftEdge}, middle X: {self.midLine}, right: {self.rightEdge}, Xbubble: {self.Xbubble}')
        #print(f'top: {self.topEdge}, middle Y: {self.midPoint}, bottom: {self.bottomEdge}, Ybubble: {self.Ybubble}')
        self.outlineSelf()
        #if Stages.stageHandler.currentStage.scrolling:
            #player.currentX -= Stages.stageHandler.currentStage.scrollSpeed

        if direction == 'L':
            self.forwardFace = False
           # Stages.StageHandler.currentStage.checkBoundaries(self)
            self.currentX -= self.speed

        if direction == 'R':
            self.forwardFace = True
            if self.humanoidName == 'Player':
                self.movementRight = True
                #if Stages.stageHandler.currentStage.scrolling:
                    #pass
                #else:
                self.currentX += self.speed
            else:
                self.currentX += self.speed

        if direction == 'U':
            if not self.falling:
                self.currentY -= self.speed
            #Stages.StageHandler.currentStage.checkBoundaries(self)
        if direction == 'D':
            self.currentY += self.speed
            #Stages.StageHandler.currentStage.checkBoundaries(self)

        if not self.usingAbility:
            if self.forwardFace:
                self.iterationList = self.rightWalkList

            elif not self.forwardFace:
                self.iterationList = self.leftWalkList

        self.animateMe()

    def followTarget(self, target):
        #print('NOT IN BUFFER?')
        self.calm()  # provides rng chance to stand still to allow chase manipulation
        if not self.chill:

            if target.midLine <= self.midLine - self.xBuffer:  # The normal xBuffer is 55 for a player hitbox. Each enemy size and xBuffer is unique
                self.move('L')

            if target.midLine >= + self.midLine + self.xBuffer:  # Have to pad for hero displacement  (maybe change later based off performance)
                self.move('R')

            if self.midPoint not in range(target.topEdge,
                                          target.bottomEdge) and self.midPoint <= target.midPoint:  # pad the 20 to help seek closer between top and bottom of player
                self.move('D')

            if self.midPoint not in range(target.topEdge,
                                          target.bottomEdge) and self.midPoint >= target.midPoint:
                self.move('U')
        else:
            self.getFaceDirection(target)
            if self.forwardFace:
                self.iterationList = self.idleRightList
            elif not self.forwardFace:
                self.iterationList = self.idleLeftList

            self.animateMe()

    def chase(self, target, rangedObject = None):

        if not self.usingAbility:
            if self.midPoint in range(target.topEdge, target.bottomEdge) and target.midLine in self.attackRange:

                if not self.attacking:
                    self.iterationCounter = 0
                    self.attacking = True
                                                    #check if attacking Npc is ranged or not
                if rangedObject != None:
                    #print('actually autocasting')
                    rangedObject.autoCast(target)

                elif rangedObject == None:
                    self.meleeAttack(target)
                    #print('still melee attacking')
            else:
                self.followTarget(target)

    '''Checks if the player has entered between the 2 anchors of an enemy, if so the enemy
    will begin to track the player and attack rather than patrol between anchors.'''
    def checkThreat(self):
        if player.currentX in range(self.leftAnchor, self.rightAnchor):
            self.aggression = True


    '''Checks if the self has taken damage and will animate a hit animation if so.'''
    def animateDamageTaken(self):

        if self.health <= 0:
            #self.dead, self.dyingTimer = self.coolDown(self.dead, self.dyingTimer, 25)
            self.iterationList = self.deathList
            self.dead = self.animateMe(False, True)
        else:
            #self.takingDamage, self.takingDamageTimer = self.coolDown(self.takingDamage, self.takingDamageTimer, 25)  # can make this variable to make different humanoids have different hit downtime timers
            if self.forwardFace:
                self.iterationList = self.rightHurtList
            else:
                self.iterationList = self.leftHurtList
            # print('here')
            self.takingDamage = self.animateMe(True, False)
            #self.determineIfAnimation()
            #create the showDamage here?
            #make the showDamage instantly make the taking damage off if stall is on cd otherwise progress down
            #showDamage makes it so that the damage taken may only be animated every so often instead of stunlocking targets
            #taking damage makes it so that there is animation when the showDamage is off


    def hover(self, aggressionStart = False, rangedObject = None):
        #instantly tracks if the character has been damaged per iteration
        #print(f'this is the risen condition: {self.risen}')
        #if not self.risen:
            #self.iterationList = Images.regSkeleRise
            #self.risen = self.animateMe(False, True)

        #if self.risen:

            self.reportHealth()
            if self.stunned:
                self.stunned, self.stunCooldownTimer = self.coolDown(self.stunned, self.stunCooldownTimer, 100)

                if self.health <= 0:
                    self.stunned = False


            else:
                self.combatStatus = ''

                if not self.usingAbility: # and show damage:
                    if self.takingDamage:
                        self.animateDamageTaken()

                    else:
                        #start resetting showDamage so that the enemy can stutter when hit again after specified
                        #period of time.
                        if not self.showDamage:
                            self.showDamage, self.showDamageTimer = self.coolDown(self.showDamage, self.showDamageTimer, 30)

                        if aggressionStart:
                            self.aggression = True

                        if not self.aggression:
                            self.checkThreat()
                            if self.currentX >= self.rightAnchor:
                                self.movingLeft = True

                            if self.currentX <= self.leftAnchor:
                                self.movingLeft = False

                            if self.movingLeft:
                                self.move('L')
                            if not self.movingLeft:
                                self.move('R')
                        else:
                            if rangedObject != None:
                                #print('sending ranged object')
                                self.chase(player, rangedObject)

                            elif rangedObject == None:
                                self.chase(player)

    def drawHealthBar(self):
        if self.health >= self.maxHealth / 2:
            color_of_health = green
        elif self.health >= round(self.maxHealth / 4):
            color_of_health = yellow
        else:
            color_of_health = red


        if self.health > 0:
            if self.forwardFace:
                pygame.draw.rect(win, color_of_health, (self.currentX + round(self.sizeX / 2), self.topEdge - 15, self.health, 7))
            else:
                pygame.draw.rect(win, color_of_health, (self.currentX + round(self.sizeX), self.topEdge - 15, self.health, 7))

    '''constantly draws enemies Alive in the current stages enemiesList and removes those who are dead
        as long as alive they also display their health bars, also will drop any consumables attatched to them'''
    def drawMe(self):
        if not self.dead:
            win.blit(self.img, (self.currentX, self.currentY))
            if self.humanoidName != 'Player' and self.humanoidName != 'Piles' and not self.stealth:
                self.drawHealthBar()

        else:
            if self.droppedConsumable != None:
                #if self.droppedConsumable.name == '':
                    #Stages.stageHandler.consumablesList.append(
                        #self.droppedConsumable(type='green', corpse=self, x=self.currentX, y=self.currentY))
                #else:
                Stages.stageHandler.consumablesList.append(self.droppedConsumable(corpse=self, x=self.currentX, y=self.currentY))

            if self not in Stages.stageHandler.currentStage.enemiesList:
                Stages.stageHandler.wanderers_list.remove(self)
            else:
                Stages.stageHandler.currentStage.enemiesList.remove(self)

'''Creates specific destruction spells/ arrows for ranged attackers'''
class Auto_Cast:

    def __init__(self, spell_name,spell_type, top_rng, spellImageList, amount, combat_text_given,
                 leftIteration, rightIteration, spellImageRightList, speed, autoCasting, spellYBuffer, spellImgYBuffer = 0,
                 spellImgXBuffer = 0):

        self.spell_name = spell_name
        self.spell_type = spell_type
        self.top_rng = top_rng
        self.spellImageList = spellImageList
        self.amount = amount
        self.combat_text_given = combat_text_given
        self.leftIteration = leftIteration
        self.rightIteration = rightIteration
        self.spellImageRightList = spellImageRightList
        self.speed = speed
        self.autoCasting = autoCasting
        self.spellYBuffer = spellYBuffer

        self.spellImgYBuffer = spellImgYBuffer
        self.spellImgXBuffer = spellImgXBuffer

# rsAutocast = Auto_Cast(spell_name='PlagueBolt', spell_type='Destruction', top_rng=2,
#                       spellImageList=Images.plagueBoltLeft,
#                       amount=20, combat_text_given='', leftIteration=Images.SkeletonRedMageShadowCastLeft,
#                       rightIteration=Images.SkeletonRedMageShadowCastRight, spellImageRightList=Images.plagueBoltRight,
#                       speed=4, autoCasting=True, spellYBuffer=10, spellImgXBuffer=10, spellImgYBuffer= 38)

# mmAutocast = Auto_Cast(spell_name='ArrowShot', spell_type='Destruction', top_rng=2,
#                       spellImageList=Images.arrowLeft,
#                       amount=10, combat_text_given='', leftIteration=Images.mmAttackLeft,
#                       rightIteration=Images.mmAttackRight, spellImageRightList=Images.arrowRight,
#                       speed=8, autoCasting=True, spellYBuffer=40, spellImgXBuffer= 10, spellImgYBuffer = 67) #spellXImgBuffer = )

#rsAutocast.target_name = player

class Caster(Humanoid):

    def __init__(self, name, iconImg, startingX, startingY, findMid, sizeX, sizeY, xBuffer,
                 yBuffer, health, dmg, speed, img, iterationList, idleLeftList, idleRightList,
                leftWalkList, rightWalkList,leftAttackList, rightAttackList, leftHurtList, rightHurtList, deathList, ac,
                 castOneLeftList=None, castOneRightList=None, castTwoLeftList=None, castTwoRightList=None, droppedConsumable = None):   #ac is the autoCaster object

        #allows two casting ability slots for casters
        self.castOneLeftList = castOneLeftList
        self.castOneRightList = castOneRightList
        self.castTwoLeftList = castTwoLeftList
        self.castTwoRightList = castTwoRightList
        self.ac = ac


        Humanoid.__init__(self, name, iconImg, startingX, startingY, findMid, sizeX, sizeY, xBuffer,
                 yBuffer, health, dmg, speed, img, iterationList, idleLeftList, idleRightList,
                leftWalkList, rightWalkList,leftAttackList, rightAttackList, leftHurtList, rightHurtList, deathList, droppedConsumable)

        self.ranged = True

    def autoCast(self, target):
        self.castThis(spell_name=self.ac.spell_name, spell_type=self.ac.spell_type, topRng=self.ac.top_rng, spellImageList=self.ac.spellImageList,
                      target_name=target, amount_given=self.ac.amount, combat_text_given=self.ac.combat_text_given, leftIteration=self.ac.leftIteration,
                      rightIteration=self.ac.rightIteration, spellImageRightList=self.ac.spellImageRightList,
                      speed=self.ac.speed, autoCasting=self.ac.autoCasting, spellYBuffer=self.ac.spellYBuffer, spellImgXBuffer=self.ac.spellImgXBuffer, spellImgYBuffer = self.ac.spellImgYBuffer)

"""
class Marksman(Caster):
    def __init__(self, startingX, startingY, droppedConsumable = None):
        Caster.__init__(self, name='marksman', iconImg=Images.mmIdleLeft[0], startingX=startingX, startingY=startingY,
                        sizeX=60, sizeY=127, findMid=60, xBuffer=400, yBuffer=12, health=60, dmg=20, speed=3,
                        img=Images.mmIdleLeft[0], iterationList=Images.mmIdleLeft,
                        idleLeftList=Images.mmIdleLeft, idleRightList=Images.mmIdleRight,
                        leftWalkList=Images.mmWalkLeft, rightWalkList=Images.mmWalkRight,
                        leftAttackList=Images.mmAttackLeft,
                        rightAttackList=Images.mmAttackRight,
                        leftHurtList=Images.mmHurtLeft, rightHurtList=Images.mmHurtRight,
                        deathList=Images.mmDeath, ac=mmAutocast)

        self.droppedConsumable = droppedConsumable


    def useAbility(self):
        pass
        #print('ability for marksman not added yet')
"""
'''Summons skeletons and cast shadowBolts'''

# class Red_Skeleton(Caster):
#
#     def __init__(self, startingX, startingY, droppedConsumable = None, aggresssion = False):     # what do i name this lul
#
#         #This caster doesnt melee showing the NONE leftattack and rightattack lists
#         #xBuffer was originally 25
#         Caster.__init__(self, name='red_skeleton', iconImg=Images.SkeletonRedMageIcon , startingX=startingX, startingY=startingY,
#                         sizeX=30, sizeY=80, findMid=30, xBuffer=600, yBuffer=18, health=60, dmg=20, speed=3, img=Images.SkeletonRedMageIdleLeft[0], iterationList=Images.SkeletonRedMageIdleLeft,
#                         idleLeftList=Images.SkeletonRedMageIdleLeft, idleRightList=Images.SkeletonRedMageIdleRight, leftWalkList=Images.SkeletonRedMageWalkLeft, rightWalkList=Images.SkeletonRedMageWalkRight ,
#                         leftAttackList=Images.SkeletonRedMageShadowCastLeft, rightAttackList=Images.SkeletonRedMageShadowCastRight, leftHurtList= Images.SkeletonRedMageIdleLeft, rightHurtList=Images.SkeletonRedMageIdleRight ,
#                         deathList=Images.SkeletonRedMageDeath, castOneLeftList = Images.SkeletonRedMageSummonCastLeft, castOneRightList = Images.SkeletonRedMageSummonCastRight,
#                         castTwoLeftList=Images.SkeletonRedMageShadowCastLeft, castTwoRightList= Images.SkeletonRedMageShadowCastRight, ac=rsAutocast)
#
#         self.humanoidName = 'Red_Skeleton'
#         self.droppedConsumable = droppedConsumable
#         self.aggression = aggresssion
#
#     '''Summons 2 regular skeletons to the screen'''
#     def summon_skeletons(self):
#         #print('casted the summons')
#         self.castThis(spell_name='Summon Skeletons', spell_type='Summon', topRng=5, spellImageList=self.castOneLeftList, target_name=None, amount_given=2, combat_text_given='Summoned',
#                       leftIteration=self.castOneLeftList, rightIteration=self.castOneRightList, summoned_enemy_class=Skeleton, summoned_enemy_name='regularSkeleton')
#
#     def useAbility(self):
#         self.summon_skeletons()


'''Skeletons specific to the canyon Stages'''

class Canyon_Skeleton(Humanoid):
    def __init__(self, name, startingX, startingY, aggress = False, droppedConsumable = None):
        self.name = name
        self.startingX = startingX
        self.startingY= startingY
        self.aggress = aggress
        self.droppedConsumable = droppedConsumable

        if self.aggress:
            self.aggression = True


        """
        elif name == 'barbarian':
            Humanoid.__init__(self, name, iconImg=Images.regularSkeletonIcon, startingX=startingX, startingY=startingY,
                              sizeX=70, sizeY=135,
                              xBuffer=80, yBuffer=67, health=75, dmg=5, speed=3, img=Images.barbarianIdleLeft[0],
                              iterationList=Images.barbarianIdleLeft,
                              idleLeftList=Images.barbarianIdleLeft, idleRightList=Images.barbarianIdleRight,
                              leftWalkList=Images.barbarianWalkLeft,
                              rightWalkList=Images.barbarianWalkRight, leftAttackList=Images.barbarianAttackLeft,
                              rightAttackList=Images.barbarianAttackRight,
                              leftHurtList=Images.barbarianHurtLeft, rightHurtList=Images.barbarianHurtRight,
                              deathList=Images.barbarianDeath, attackSpeed=150) #slower attack speed than others, but stuns when hits!
        
        """
    def useAbility(self):
        if self.name == 'canyonSkele':
            print('this skele doesnt have an ability')


"""Stealth invis reaper class that will stun player if in melee range and still stealthed.
(only way they become unstealthed is being damaged below 50% health)"""

class Fade_Walker(Humanoid):
    ranged = 'non combative'
    gut_shot = False # stuns the player if in melee range and stealthed [boolean indidcates if delievered or not]
    done_porting = False
    porting_timer = 0
    #stealth = True # keeps the fade_walker stealthed and harder to see/target

    def __init__(self, startingX, startingY, name = 'fade_walker', summoned = False, aggression = False, droppedConsumable = None):
        #self.name = name
    
        Humanoid.__init__(self, name, iconImg=Images.regularSkeletonIcon, startingX=startingX, startingY=startingY,
                          sizeX=52, sizeY=83, findMid=68,
                          xBuffer=55, yBuffer=50, health=75, dmg=5, speed=3, img=Images.fadeWalkerIdleLeft[0],
                          iterationList=Images.fadeWalkerIdleLeft,
                          idleLeftList=Images.fadeWalkerIdleLeft, idleRightList=Images.fadeWalkerIdleRight,
                          leftWalkList=Images.fadeWalkerStealthLeft,
                          rightWalkList=Images.fadeWalkerStealthRight, leftAttackList=Images.fadeWalkerAttackLeft,
                          rightAttackList=Images.fadeWalkerAttackRight,
                          leftHurtList=Images.fadeWalkerIdleLeft, rightHurtList=Images.fadeWalkerIdleRight,
                          deathList=Images.fadeWalkerDeath)

        self.stealth = True
        self.startingX = startingX
        self.startingY = startingY
        self.summoned = summoned
        self.aggression = aggression
        self.droppedConsumable = droppedConsumable
        self.meleeCooldown = True # allows the stun to land before melee attack specifially for this class
        self.meleeCooldownTimer = 25 # 5 less than self.attack_speed to make the first attack follow up quickly from stun

    def port_first(self):
        if self.done_porting:
            self.hover(aggressionStart=True)
        else:
            self.iterationList = Images.fadeWalkerTeleportIn
            self.done_porting, self.porting_timer = self.coolDown(self.done_porting, self.porting_timer, 100)
            self.animateMe()
            win.blit(self.img, (self.currentX, self.currentY))

    def useAbility(self):
        self.sneak()

    def deliver_gut_shot(self):
        Sounds.stun_sound.play()
        deal_damage_to_player(self.dmg * 2, stun_debuff=150)
        #Sounds.stun_sound.play()
        print('ok')
        #player.stunned = True
        #play gut_shot sound here (SOUND INPUT GOES HERE)

    """Updates based off current health if the walker has retained it's stealth capabilities"""

    def check_stealth(self):
        if self.health >= round(self.maxHealth / 2):
            self.leftWalkList = Images.fadeWalkerStealthLeft
            self.rightWalkList = Images.fadeWalkerStealthRight
            self.stealth = True
        else:
            self.stealth = False
            self.gut_shot = True # makes the gutshot be used without applying to player since no stealth available
            self.leftWalkList = Images.fadeWalkerWalkLeft
            self.rightWalkList = Images.fadeWalkerWalkRight

    def sneak(self):
        if not self.gut_shot:
            self.check_stealth()
            if self.stealth:
                if self.midPoint in range(player.topEdge, player.bottomEdge) and player.midLine in self.attackRange:
                    self.deliver_gut_shot()
                    self.gut_shot = True
                    self.stealth = False
                    self.leftWalkList = Images.fadeWalkerWalkLeft
                    self.rightWalkList = Images.fadeWalkerWalkRight



"""Summons ghosts constantly until Killed"""
class Grave_Keeper(Humanoid):
    teleported_in = False #determines if unit has teleported in (can still be damaged)
    tele_timer = 0

    summoning_ghost = False
    summoning_ghost_timer = 0
    humanoidName = 'grave_keeper'


    def __init__(self, startingX, startingY, droppedConsumable=None):
        Humanoid.__init__(self, name='grave_keeper', iconImg=Images.regularSkeletonIcon, startingX=startingX, startingY=startingY,
                          sizeX=45, sizeY=64, findMid=62,
                          xBuffer=55, yBuffer=40, health=75, dmg=5, speed=3, img=Images.grave_keeper_teleport_in[0],
                          iterationList=Images.grave_keeper_teleport_in,
                          idleLeftList=Images.grave_keeper_idle, idleRightList=Images.grave_keeper_idle,
                          leftWalkList=Images.grave_keeper_idle,
                          rightWalkList=Images.grave_keeper_idle, leftAttackList=Images.grave_keeper_idle,
                          rightAttackList=Images.grave_keeper_summon,
                          leftHurtList=Images.grave_keeper_idle, rightHurtList=Images.grave_keeper_idle,
                          deathList=Images.grave_keeper_death)

        self.ranged = 'non combative'
        self.aggression = True
        self.droppedConsumable = droppedConsumable

    def hover_keeper(self):
        if not self.teleported_in:
            self.tele_timer += 1
            self.animateMe()
            if self.tele_timer > 150:
                self.teleported_in = True

        else:
            if self.health > 0:
                self.summon_ghosts()
                self.animateMe()

            else:
                self.combatStatus = ''
                self.iterationList = self.deathList
                self.dead = self.animateMe(False, True)






    def summon_ghosts(self):

        if self.summoning_ghost_timer >= 150:
            self.summoning_ghost = True
            self.summoning_ghost_timer = 0

        if self.summoning_ghost:
            self.iterationList = Images.grave_keeper_summon
            if self.iterationList[self.iterationCounter] == self.iterationList[-1]:
                self.summoning_ghost = False
                Stages.stageHandler.currentStage.enemiesList.append(Ghost(startingX = self.currentX + 50, startingY= self.currentY))
        else:
            self.iterationList = Images.grave_keeper_idle
            self.summoning_ghost_timer += 1




        #print(self.name, 'is summoning ghosts!')

    def useAbility(self):
        pass


'''Skeletons specific to the graveyard stages'''
class Skeleton(Humanoid):
    shieldRaised = False  # if shield raised  >>>>>> skele gains immunity or defence!
    humanoidName = "Skeleton"
    # Allow skeletons unique abilities based off their names / ID   so normal ones have no access  while advanced ones may access abilities
    def __init__(self, name, startingX, startingY, summoned = False, aggression = False, droppedConsumable = None):
        self.name = name


        # if name == 'regularSkeleton':
        #
        #     Humanoid.__init__(self, name, iconImg = Images.regularSkeletonIcon, startingX = startingX, startingY = startingY, sizeX = 50, sizeY = 83, findMid=45,
        #                       xBuffer = 55, yBuffer = 50, health = 75, dmg = 5, speed = 4, img = Images.regSkeleIdleLeft[0], iterationList = Images.regSkeleIdleLeft,
        #                       idleLeftList = Images.regSkeleIdleLeft, idleRightList = Images.regSkeleIdleRight, leftWalkList = Images.regSkeleWalkLeft,
        #                       rightWalkList =  Images.regSkeleWalkRight, leftAttackList = Images.regSkeleAttackLeft, rightAttackList = Images.regSkeleAttackRight,
        #                       leftHurtList = Images.regSkeleHurtLeft, rightHurtList = Images.regSkeleHurtRight, deathList = Images.regSkeleDeath)

        if name == 'leaper':
            self.leap_ready = False
            self.leapTimer = 0
            self.leaping = False

            self.amount_traveled = 0 # used to track how far in the jump the leaper is
            Humanoid.__init__(self, name, iconImg = Images.regularSkeletonIcon, startingX = startingX, startingY = startingY, sizeX = 40, sizeY = 94, findMid=55,
                              xBuffer = 65, yBuffer = 44, health = 75, dmg = 10, speed = 3, img = Images.leaperIdleLeft[0], iterationList = Images.leaperIdleLeft,
                              idleLeftList = Images.leaperIdleLeft, idleRightList = Images.leaperIdleRight, leftWalkList = Images.leaperWalkLeft,
                              rightWalkList =  Images.leaperWalkRight, leftAttackList = Images.leaperAttackLeft, rightAttackList = Images.leaperAttackRight,
                              leftHurtList = Images.leaperHurtLeft, rightHurtList = Images.leaperHurtRight, deathList = Images.leaperDeath)

        # elif name == 'captainSkeleton':
        #     self.rallied = False
        #     self.inRally = True  #will remain False until done rallying and then rallied becomes true
        #     self.rallyTimer = 0
        #
        #     Humanoid.__init__(self, name, iconImg=Images.captainSkeleIcon, startingX=startingX, startingY=startingY,
        #                       sizeX=65, sizeY=82, findMid=60, xBuffer=60, yBuffer=58, health=75, dmg=10, speed=2,
        #                       img=Images.captainSkeleIdleLeft[0],
        #                       iterationList=Images.captainSkeleIdleRight, idleLeftList=Images.captainSkeleIdleLeft,
        #                       idleRightList=Images.captainSkeleIdleRight, leftWalkList=Images.captainSkeleWalkLeft,
        #                       rightWalkList=Images.captainSkeleWalkRight,
        #                       leftAttackList=Images.captainSkeleAttackLeft,
        #                       rightAttackList=Images.captainSkeleAttackRight, leftHurtList=Images.captainSkeleHurtLeft,
        #                       rightHurtList=Images.captainSkeleHurtRight, deathList=Images.captainSkeleDie)


        self.humanoidName = 'Skeleton'
        self.startingX = startingX
        self.startingY = startingY
        self.droppedConsumable = droppedConsumable


        if aggression:
            self.aggression = True
        if summoned:
            self.risen = False


    def useAbility(self):
        if self.name == 'regularSkeleton':
            self.raiseShield()
        elif self.name == 'captainSkeleton':
            self.rally()
        elif self.name == 'leaper':
            self.leap()


    """Used by Leapers to jump to player location"""
    #elif self.orb_ready:
        #self.iterationList = self.leftAttackList
        #self.orb_ready = self.animateMe(True, False)
        #self.casting_orb = True
        #if not self.orb_ready:
            #self.iterationList = self.idleLeftList
            #self.orb_list.append(Orb(self))
            #self.casting_orb = False

    def travel(self):
        if self.midLine not in range(self.leap_desintation - 3, self.leap_desintation + 3):
            if self.midLine > self.leap_desintation:
                self.currentX -= self.speed * 2

            elif self.midLine < self.leap_desintation:
                self.currentX += self.speed * 2

            self.outlineSelf()
            self.amount_traveled += self.speed * 2

            if self.amount_traveled <= round(self.travel_distance / 2):
                self.currentY -= 8
            else:
                self.currentY += 3
        else:
            self.usingAbility = False
            self.leap_ready = False
            self.leaping = False

            self.amount_traveled = 0


    def leap(self):
        if not self.leap_ready:
            self.leap_ready, self.leapTimer = self.coolDown(self.leap_ready, self.leapTimer, 100)
            if self.leap_ready:
                self.resetIteration()
                self.leap_desintation = player.midLine
                self.travel_distance = abs(player.midLine - self.midLine)
                Sounds.leaper_s1.play() # play learper leap sound

        elif self.leap_ready:
            self.usingAbility = True
            self.leaping = True

            if self.iterationCounter < len(self.iterationList) - 1:
                self.animateMe(givenLists=[Images.leaperJumpLeft, Images.leaperJumpRight])

            else:
                self.img = self.iterationList[-1]              #UNDO
                self.travel()
                print('go to air')






    '''Used to determine cast direction/target/face of caster/effect'''
    def rally(self):
        print('captain is rallying!')

        print(self.rallied)
        if self.health > 0:
        #main change is the startAction = self.castThis when returning different values
            self.castThis(spell_name='Rally', spell_type='Buff', topRng=500, spellImageList=Images.damageBuffOrg,             #UNDO
                        target_name='regularSkeleton', amount_given=5,combat_text_given= 'Damage Buffed',
                        leftIteration=Images.captainSkeleRallyLeft, rightIteration=Images.captainSkeleRallyRight, cyclic=True)

        else:
            self.usingAbility = False

    #Only done by regular skeletons where they raise shield
    def raiseShield(self):

        if not self.shieldRaised:
            if self.health > 0:
                self.immune = False
                rng = random.randint(1, 400)
                if rng == 1:
                    print('hit')
                    self.shieldUptimeStart = pygame.time.get_ticks()
                    self.usingAbility = True
                    self.shieldRaised = True



        if self.shieldRaised:
            if self.health > 0:
                self.immune = True      # This attribute will make the object immune to all incoming damage
                self.getFaceDirection(player)
                #provicde defensive stats here

                if self.forwardFace:

                    self.iterationList = Images.regSkele_rs_Right
                    #print('raisingShield')                                #UNDO

                elif not self.forwardFace:
                    self.iterationList = Images.regSkele_rs_Left
                #print('raisingShield')

                if self.iterationCounter < len(self.iterationList) - 1:
                    self.iterationCounter += 1

                else:
                    self.iterationCounter = len(self.iterationList) - 1
                    self.shieldCooldown = (pygame.time.get_ticks() - self.shieldUptimeStart) / 1000
                    if self.shieldCooldown > 3:
                        self.resetIteration()
                        self.shieldRaised = False
                        self.usingAbility = False

                self.img = self.iterationList[self.iterationCounter]
            else:
                self.resetIteration()
                self.shieldRaised = False
                self.usingAbility = False
            #self.animateMe()



"""
randomEdgeX = random.choice([random.randint(100, 300), random.randint(1100, 1300)])
#regularSkeleton = Skeleton('regularSkeleton', startingX = 1000, startingY = 500)
#regSkeleton2SZero = Skeleton('regularSkeleton', startingX = 800, startingY = 540)
#Stages.stage_zero.enemiesList = [Red_Skeleton(1250, 500, droppedConsumable=Consumables.Battery)] #Canyon_Skeleton('peon', 700, 500), Canyon_Skeleton('trooper', 800, 550), Canyon_Skeleton('barbarian', 800, 600)] #Marksman(800, 600)]#Canyon_Skeleton('trooper', 800, 600)] #Canyon_Skeleton('barbarian', 800, 600)]  Canyon_Skeleton('peon', 700, 500), Canyon_Skeleton('trooper', 800, 600)
#Stages.stage_one.enemiesList =  [Canyon_Skeleton('trooper', 1250, 500, True), Canyon_Skeleton('peon', 1250, 600, True)]#[Skeleton('regularSkeleton', 800, 540), Skeleton('regularSkeleton', 1000, 500), Skeleton('captainSkeleton', 1000, 600), Red_Skeleton(1000, 600)]
#Stages.stage_two.enemiesList = [Canyon_Skeleton('trooper', 1250, 500, True), Canyon_Skeleton('peon', 1250, 700, True)]
#Stages.stage_zero.enemiesList = [Red_Skeleton(1000, 600)] # Skeleton('regularSkeleton', 800, 540) Ghost(850, 520)] Skeleton('regularSkeleton', 1000, 500) Skeleton('captainSkeleton', 1000, 600) Black_Mage(1000, 600) Ghost(800, 600)
Stages.stage_zero.possibleEnemies = ['regularSkeleton', 'ghost', 'captainSkeleton']
"""

class Ghost(Humanoid):
    aggression = True
    def __init__(self, startingX, startingY):            #xBuffer was 55 for ghost
        Humanoid.__init__(self, name = 'ghost', iconImg = Images.ghostIcon, startingX = startingX, startingY = startingY, findMid= 32, sizeX = 25, sizeY = 49, xBuffer = 45, yBuffer = 23, health = 25, dmg = 5, speed = 3, img = Images.pGhostIdleLeft[0],
                          iterationList = Images.pGhostIdleLeft, idleLeftList = Images.pGhostIdleLeft, idleRightList = Images.pGhostIdleRight, leftWalkList =  Images.pGhostIdleLeft,
                          rightWalkList =  Images.pGhostIdleRight, leftAttackList = Images.pGhostAttackLeft,rightAttackList = Images.pGhostAttackRight, leftHurtList = Images.pGhostHurtLeft,
                          rightHurtList = Images.pGhostHurtRight, deathList = Images.deadPGList)

        #self.name = 'ghost'
        self.currentX = startingX
        self.currentY = startingY


    def useAbility(self):
        pass



#ghost1 = Ghost(name = 'ghost',startingX = 1000, startingY = 500)

class Piles(Humanoid):
    placed = False
    idleAnimate = False
    idleTimer = 0

    inPlay = False  #Allows Piles to be constantly drawn to travel with you


    batteryImg = None
    batteryActive = True
    recharging = False #turned on an animates when piles is recharging his battery
    batteryPower = 1   #how many heals are available
    batteryClip = 3    #indicates how many heals are available
    healAmount = 20    #power of the heals amount

    castingHeal = False #Indicates if Piles is casting a heal on Player

    def __init__(self):
        Humanoid.__init__(self, name = 'Piles', iconImg = Images.regularSkeletonIcon, startingX = 600, startingY = 500, findMid=10, sizeX = 10, sizeY = 85, xBuffer = 10, yBuffer = 42, health = 550, dmg = 15, speed = 4, img = Images.idleRightPiles, iterationList = Images.idleRightPiles,
                          idleLeftList = Images.idleRightPiles, idleRightList = Images.idleRightPiles, leftWalkList = Images.idleRightPiles, rightWalkList = Images.walkRightPiles,
                          leftAttackList = Images.idleRightPiles, rightAttackList = Images.idleRightPiles, leftHurtList = None, rightHurtList = None, deathList = None)

        self.humanoidName = 'Piles'

    '''Setting Placement for Piles before cutscenes'''
    def setPlacement(self, placeX, placeY):
        self.currentX = placeX
        self.currentY = placeY

    def followPlayer(self):
        if self.inPlay:
            self.showBattery()

            if Stages.stageHandler.currentStage.scrolling:
                self.currentX -= Stages.stageHandler.currentStage.scrollSpeed

            #animates casting Piles heal
            if self.castingHeal:
                self.iterationList = Images.castHealPiles
                self.castingHeal = self.animateMe(True, False)

            elif not self.castingHeal:
                if self.currentX < 70:
                    self.currentX += self.speed
                    self.iterationList = self.rightWalkList
                else:
                    self.iterationList = self.idleRightList

                self.animateMe()

            self.drawMe()

    '''Stalling the animation before iterating through it again (avoided spamming images into memory'''
    def stall(self):
        self.idleAnimate, self.idleTimer = self.coolDown(self.idleAnimate, self.idleTimer, random.randint(120, 180))

    def checkBatteryLevel(self):
        if self.batteryPower > 0:
            self.batteryActive = True
        else:
            self.batteryActive = False

    def batteryHeal(self, target):
        self.resetIteration()
        self.checkBatteryLevel()

        if self.batteryActive:
            Sounds.healing_sound.play()
            #self.resetIteration()
            text = '+' + str(self.healAmount) + ' health'
            text = combatTextFont.render(text, True, green)
            combatTextList.append(Combat_Text(text, Player_Healthbar_Interface, True))
            self.castingHeal = True

            if target.health + self.healAmount >= target.maxHealth:
                target.health = target.maxHealth
            else:
                target.health += self.healAmount

            self.batteryPower -= 1

        else:
            #self.castingHeal = True
            print('Battery is to low')


    """Resets battery power to its max capacity"""
    def rechargeBattery(self):
        self.batteryPower = self.batteryClip
        self.batteryActive = True

    """Draws the battery insignia below Player healthBar"""
    def showBattery(self):
        #print(self.batteryPower)
        self.checkBatteryLevel()
        if self.batteryActive:
            if self.batteryPower == 1:
                self.batteryImg = Images.batteryPower1
            elif self.batteryPower == 2:
                self.batteryImg = Images.batteryPower2
            elif self.batteryPower == 3:
                self.batteryImg = Images.batteryPower3

            #win.blit(self.batteryImg, (80, 65))

        else:
            self.batteryImg = Images.batteryPower0

        win.blit(self.batteryImg, (95, 100))


    #def marker_for_scene(self):
        #self.batteryActive = True

Piles = Piles()


class Player():
    damage_iteration_counter = 0

    playerAttacking = False
    attackDmg = None
    overshield = False
    overshield_max_amount = 100
    overshieldAmount = 0

    gems = 3000

def draw_player_interface():
    # Player Icon Img
    win.blit(player.iconImg, (30, 45))

    #Grenade Count and Icon
    win.blit(Images.grenadeImg, (100, 25))
    grenadeText = combatTextFont.render(str(player.grenadeAmount), True, grey)
    win.blit(grenadeText, (125, 30))

    #RELOAD WEAPON BOX
    ammunitionText = ammoText.render(str(player.currentWeapon.clip), True, player.currentWeapon.getAmmoColor())

    #Draw Shotgun range indicators
    if player.currentWeapon.name == 'Shotgun':
        win.blit(Images.shotgun_range_indicator,
                 (player.midLine - Shotgun.x_range, player.midPoint))
        win.blit(Images.shotgun_range_indicator,
                 (player.midLine + Shotgun.x_range, player.midPoint))

    if player.forwardFace:
        win.blit(Images.reloadBox, (player.currentX + 40 * 2 - 8, player.currentY + 14 + 41))
        if player.currentWeapon.clip < 10:
            win.blit(ammunitionText, (player.currentX + 40 * 2 + 8, player.currentY + 14 + 46))
        else:
            win.blit(ammunitionText, (player.currentX + 40 * 2 + 4, player.currentY + 14 + 46))

    elif not player.forwardFace:
        win.blit(Images.reloadBox, (player.currentX + 51, player.currentY + 14 + 41))
        win.blit(ammunitionText, (player.currentX + 55, player.currentY + 14 + 46))

    credit_text = creditText.render('CREDITS:', True, green)
    credit_number = creditText.render(str(player.gems), True, green)
    win.blit(credit_text, (30, 750))
    win.blit(credit_number, (100, 750))

    #shield icon
    if player.shield_generator_available:
        win.blit(Images.shield_available, (145, 100))
    elif not player.shield_generator_available:
        win.blit(Images.shield_unavailable, (145, 100))

    #player weapon icons
    if player.currentWeapon.name == 'Rifle':
        win.blit(Images.rifle_selected, (50, 175))
    else:
        win.blit(Images.rifle_unselected, (50, 175))

    if player.currentWeapon.name == 'Shotgun':
        win.blit(Images.shotgun_selected, (140, 175))
    else:
        win.blit(Images.shotgun_unselected, (140, 175))

    if player.currentWeapon.name == 'Rocket Launcher':
        win.blit(Images.rocket_launcher_selected, (230, 175))
    else:
        win.blit(Images.rocket_launcher_unselected, (230, 175))


'''draws player healthbar and icon in top left of screen'''
def draw_player_healthbar_Icon():
    pygame.draw.rect(win, [169, 169, 169], [100, 75, player.maxHealth / 2, 25]) #grey bar
    pygame.draw.rect(win, [0, 255, 0], [100, 75, player.health / 2, 25]) #green current health bar
    if player.overshield:
        pygame.draw.rect(win, [0, 0, 255], [100, 60, player.overshieldAmount / 2, 12]) #blue bar when overshield
        #player.overshieldAmount -= .5  #constantly takes away from the overshield
        if player.overshieldAmount <= 0:
            player.overshield = False

    if player.immune:
        pygame.draw.rect(win, [255, 255, 255], [100, 75, player.health / 2, 25]) #immune white bar when rolling

def report_player_health():
    #For updating healing
    if player.health > player.originalHealth:
        player.originalHealth = player.health

    #For updating damage
    elif player.health < player.originalHealth:
        player.takingDamage = True
        player.originalHealth = player.health



activeProjectiles = []
class Projectile(Humanoid): #potenitally a humanoid to use animateMe function
    iterationCounter = 0
    exploded = False


    def __init__(self, origin, img, iterationList, damage, speed, x, y, movingRight, explodes=False):
        self.origin = origin     #determines if friendly fire or not
        self.img = img
        self.iterationList = iterationList
        self.damage = damage
        self.speed = speed
        self.x = x
        self.y = y
        self.movingRight = movingRight
        self.explodes = explodes

    '''Checks for collision between projectile and current stage enemies
    if collided; will remove itself from active projectiles list and deal damage to target hit'''
    def checkDamageCollision(self, givenList):
        if type(givenList) == list:
            pass
        else:
            givenList = [givenList]


        for enemy in givenList:
            if self in activeProjectiles:
                if self.y in enemy.Ybubble:
                    if self.x in range(enemy.leftEdge - 10, enemy.rightEdge + 10):#(round(enemy.midLine - (enemy.sizeX - 10)), round(enemy.midLine + (enemy.sizeX + 10))): #padding the 10 for point blank shots
                        if self.movingRight:
                            if self.x > enemy.midLine:
                                explosion_added = 0
                                if enemy.health > 0:
                                    if self.y in enemy.headshotRange:
                                        self.dealDamage(enemy, self.damage, headshot=True)
                                    else:
                                        self.dealDamage(enemy, self.damage)

                                    #enemy.health -= self.damage
                                    print(f'hitting {enemy}')
                                    activeProjectiles.remove(self)
                                    if self.explodes:
                                        if not self.exploded:
                                            Stages.stageHandler.explosivesList.append(explosive_frame(x=self.x - 90, y=self.y -60)) #displacement for the projectile
                                            self.exploded = True
                                            Sounds.explosion_sound.play()

                                    #print(f'{enemy.name} took {self.damage} damage!')

                        elif not self.movingRight:
                            if self.x < enemy.midLine:
                                if enemy.health > 0:
                                    if self.y in enemy.headshotRange:
                                        self.dealDamage(enemy, self.damage, headshot=True)
                                    else:
                                        self.dealDamage(enemy, self.damage)

                                    # enemy.health -= self.damage
                                    activeProjectiles.remove(self)
                                    if self.explodes:
                                        if not self.exploded:
                                            Stages.stageHandler.explosivesList.append(explosive_frame(x=self.x - 45, y=self.y -60)) #displacement for the projectile
                                            self.exploded = True
                                            Sounds.explosion_sound.play()



                if not Stages.stageHandler.currentStage.completed:
                    if self.x <= Stages.stageHandler.currentStage.leftBoundary or self.x >= Stages.stageHandler.currentStage.rightBoundary:
                        activeProjectiles.remove(self)


class Soldier(Humanoid, Player):
    stun_reset = False # used to cancel all current actions and reset iteraiton
    death_reset = False # used to reset iteration for death animation in Controls Module
    stun_timer = 0  # used to increment until higher than stun cd for becoming un-stunned
    stun_cooldown = 0 # number created when a stun is applied for the 'stun_timer' to increment above and un-stun player

    currentWeapon = None
    crouching = False
    shooting = False
    rocket_shooting = False # determines if the player is shooting the rocket launcher or not
    reloading = False

    rolling = False
    movementRight = False # Helps scroll window when stages are complete and player is progressing

    grenadeAmount = 2
    throwing_grenade = False

    roll_speed = 25

    #player unlocks
    shotgun_unlocked = False
    shotgun_muzzle_flash = False # determines when the shotgun animation is active (independent of player sprites)

    rocket_launcher_unlocked = False

    roll_unlocked = False
    melee_unlocked = False
    grenades_unlocked = False

    shield_generator_unlocked = False # unlocked in store.
    shield_generator_available = False # cooldown for on use.
    shield_generator_timer = 0 # cooldown timer for on use.

    def __init__(self, name, hero):
        self.hero = hero

        if self.hero == 'redEyes':
            Humanoid.__init__(self, name, iconImg = Images.redEyesIcon, startingX = 600, startingY = 550, findMid=69, sizeX = 26, sizeY = 96, xBuffer = 60, yBuffer = 45, health = 225, dmg = 4, speed = 7, img = Images.redEyesIdleRight[0], iterationList = Images.redEyesIdleRight,
                              idleLeftList = Images.redEyesIdleLeft, idleRightList = Images.redEyesIdleRight, leftWalkList = Images.redEyesWalkLeft, rightWalkList = Images.redEyesWalkRight,
                              leftAttackList = Images.redEyesKnockbackLeft, rightAttackList = Images.redEyesKnockbackRight, leftHurtList = None, rightHurtList = None, deathList = Images.redEyesDead)

            self.crouchLeft = Images.redEyesCrouchIdleLeft
            self.crouchRight = Images.redEyesCrouchIdleRight
            self.crouchShootLeft = Images.redEyesCrouchShootLeft
            self.crouchShootRight = Images.redEyesCrouchShootRight
            self.shootRight = Images.redEyesShootRight
            self.shootLeft = Images.redEyesShootLeft
            self.throwing_grenadeLeft = Images.redEyesThrowGrenadeLeft
            self.throwing_grenadeRight = Images.redEyesThrowGrenadeRight
            self.reloadLeft = Images.redEyesReloadLeft
            self.reloadRight = Images.redEyesReloadRight
            self.rollLeft = Images.redEyesRollLeft
            self.rollRight = Images.redEyesRollRight

            self.name = name
            #self.attackDmg = 5
            self.humanoidName = 'Player'
            self.health -= 20
            #self.equip(Rifle)      #auto equips rifle as the starting weapon
        #if hero == 'redEyes':
            #self.crouchLeft = Images.redEyesCrouchLeft
            #self.crouchRight = Images.redEyesCrouchRight

    def draw_player(self):
        if not self.dead:
            if self.takingDamage:
                if player.forwardFace:
                    self.iterationList = Images.redEyesHurtRight
                elif not player.forwardFace:
                    self.iterationList = Images.redEyesHurtLeft

                self.img = self.iterationList[self.damage_iteration_counter]
                self.damage_iteration_counter += 1
                if self.damage_iteration_counter >= len(self.iterationList) - 1:
                    self.takingDamage = False
                    self.damage_iteration_counter = 0
                    self.iterationCounter = 0
                    self.img = self.iterationList[self.iterationCounter]

            win.blit(self.img, (self.currentX, self.currentY))
            if self.shotgun_muzzle_flash:
                self.muzzle_flash()

            if self.overshield:
                shield_shell.animateMe()
                if self.forwardFace:
                    win.blit(shield_shell.img, (self.currentX, self.currentY))
                elif not self.forwardFace:
                    win.blit(shield_shell.img, (self.currentX + 25, self.currentY)) #adjusting for image displacement
                                                                                    #from the xBuffers


    def reset_for_stun(self):
        self.resetIteration()
        self.shooting = False
        self.throwing_grenade = False
        self.reloading = False
        self.rolling = False

        self.stun_reset = True


    '''Starts throwing animation, logic and flow in Player Controls module'''
    def throw_grenade(self):
        self.throwing_grenade = True

    def checkPickup(self):
        for consumables in Stages.stageHandler.consumablesList:
            if consumables.y in range(self.topEdge, self.bottomEdge):
                if self.midLine in range(consumables.x, consumables.x + consumables.img.get_width()):
                    consumables.pickup()

    """Adds current weapon to self and adds self to the Weapon objects 'user' attribute!"""
    def equip(self, weapon):
        self.currentWeapon = weapon
        self.currentWeapon.user = self
        #silly me!

        #def getWeapon(self):
            #if self.current

    '''Determines weapon type and then applies the correct muzzle flash image and adjustments
    to nozzle position'''
    def muzzle_flash(self):
        #Draw this in main with the rest of the player attributes!

        if self.currentWeapon.name == 'Shotgun':
            print('confirmed')
            if self.forwardFace:
                img = shotgun_blast_right.img #for right facing
                shotgun_blast_right.animateMe(shotgun_use=True)
                if self.crouching:
                    win.blit(img, (self.currentX + 90, self.currentY + 72))
                else: #if standing
                    win.blit(img, (self.currentX + 90, self.currentY + 50))

            else: #not forwardFace
                img = shotgun_blast_left.img
                shotgun_blast_left.animateMe(shotgun_use=True)
                if self.crouching:
                    win.blit(img, (self.currentX - 60, self.currentY + 72))
                else:  #if standing
                    win.blit(img, (self.currentX - 65, self.currentY + 50))

            #self.chamberBullet('x'), self.chamberBullet('y')

    '''Adds buffer to x and y position of bullet spawn to match hero's weapon skin nozzle.'''
    def chamberBullet(self, x_or_y):

        if self.hero == 'redEyes':
            if x_or_y == 'x':
                if self.forwardFace:
                    x = self.midLine + 35
                elif not self.forwardFace:
                    x = self.midLine - 35
                """
                if self.forwardFace:
                    x = self.currentX + 105 # was +115
                else:
                    x = self.currentX + 7 # was -3
                """
                return x

            elif x_or_y == 'y':
                if self.crouching:
                    y = self.currentY + 110
                else:
                    y = self.currentY + 92
                return y

            elif x_or_y == 'rocket_y':
                y = self.currentY + 70
                return y

    """Tests to see if the target is within shotgun
    x_range and deals damage to first target in range."""
    def shotgun_sights(self, target):
        if not self.currentWeapon.damage_dealt:
            if target.midPoint in self.currentWeapon.full_y_range:
                if target.health > 0:
                    if self.forwardFace:
                        if target.midLine in self.currentWeapon.right_x_range:
                            self.dealDamage(target, self.currentWeapon.damage, headshot=False)
                            self.currentWeapon.damage_dealt = True

                    else:
                        if target.midLine in self.currentWeapon.left_x_range:
                            self.dealDamage(target, self.currentWeapon.damage, headshot=False)
                            self.currentWeapon.damage_dealt = True


    '''Adds projectile to activeList with the player's current weapons bullet image, bulletspeed, and bulletdamage.
    Activates when the player presses the 's' Key.'''
    def shoot(self, is_rocket = False):

        if self.currentWeapon.clip > 0:
            #self.muzzleFlash()
            self.currentWeapon.clip -= 1
            if self.currentWeapon.name == 'Rifle':
                activeProjectiles.append(Projectile('Player', self.currentWeapon.bulletImg, self.currentWeapon.bulletIteration, self.currentWeapon.damage,
                                                    self.currentWeapon.bulletSpeed, self.chamberBullet('x'), self.chamberBullet('y'), self.forwardFace))
                Sounds.rifle_fire.play()

            elif self.currentWeapon.name == 'Rocket Launcher':
                activeProjectiles.append(
                    Projectile('Player', self.currentWeapon.bulletImg, self.currentWeapon.bulletIteration,
                               self.currentWeapon.damage,
                               self.currentWeapon.bulletSpeed, self.chamberBullet('x'), self.chamberBullet('rocket_y'),
                               self.forwardFace, explodes=True))
                Sounds.RL_fire.play()

            elif self.currentWeapon.name == 'Shotgun':
                self.shotgun_muzzle_flash = True
                self.currentWeapon.update_shotgun_range() # updates shotgun range location based off player location
                Sounds.shotgun_fire.play()

                for enemy in Stages.stageHandler.currentStage.enemiesList:
                    self.shotgun_sights(enemy)
                    # if not self.currentWeapon.damage_dealt:
                    #     if enemy.midPoint in self.currentWeapon.full_y_range:
                    #         if self.forwardFace:
                    #             if enemy.midLine in self.currentWeapon.right_x_range:
                    #                 self.dealDamage(enemy, self.currentWeapon.damage, headshot=False)
                    #                 self.currentWeapon.damage_dealt = True
                    #                 print(f'hitting {enemy.name}')
                    #         else:
                    #             if enemy.midLine in self.currentWeapon.left_x_range:
                    #                 self.dealDamage(enemy, self.currentWeapon.damage, headshot=False)
                    #                 self.currentWeapon.damage_dealt = True
                    #                 print(f'hitting {enemy.name}')

                for matter in Stages.stageHandler.currentStage.matterList:
                    self.shotgun_sights(matter)
                    # if not self.currentWeapon.damage_dealt:
                    #     if matter.midPoint in self.currentWeapon.full_y_range:
                    #         if self.forwardFace:
                    #             if matter.midLine in self.currentWeapon.right_x_range:
                    #                 self.dealDamage(matter, self.currentWeapon.damage, headshot=False)
                    #                 self.currentWeapon.damage_dealt = True
                    #                 print(f'hitting')
                    #         else:
                    #             if matter.midLine in self.currentWeapon.left_x_range:
                    #                 self.dealDamage(matter, self.currentWeapon.damage, headshot=False)
                    #                 self.currentWeapon.damage_dealt = True
                    #                 print(f'hitting')
                    #
                    #             #matter.health -= self.currentWeapon.damage
                    #             print(f'hitting')

                for wanderer in Stages.stageHandler.wanderers_list:
                    self.shotgun_sights(wanderer)

                if Stages.stageHandler.currentStage.boss != None:
                    if Stages.stageHandler.currentStage.boss.name == 'Hollow':
                        self.shotgun_sights(Stages.stageHandler.currentStage.boss.head)
                        self.shotgun_sights(Stages.stageHandler.currentStage.boss.heart)
                    else:
                        self.shotgun_sights(Stages.stageHandler.currentStage.boss)


            Shotgun.damage_dealt = False

            #determine if rocket is being shot to animate the player into firing the rocket launcher
            #found in the Controls Module under key press 'S'
            if not is_rocket:
                self.shooting = True
            else:
                self.rocket_shooting = True

        else:
            print(f'(in shoot() function: Out of ammo')
        #self.shooting = True
        #activeProjectiles.append(self)

    """Swaps reloading boolean condition.
    (Animation and logic handled in controls)"""
    def reload(self):
        if self.currentWeapon.name == 'Rifle':
            Sounds.rifle_reload.play()
        elif self.currentWeapon.name == 'Shotgun':
            Sounds.shotgun_reload.play()
        elif self.currentWeapon.name == 'Rocket Launcher':
            Sounds.rifle_reload.play()

        self.reloading = True

'''Draws/moves/collids projectiles while also determining their origin and operations'''
def drawProjectiles():
    if activeProjectiles != []:

        for projectiles in activeProjectiles:
            projectiles.animateMe()
            win.blit(projectiles.img, (projectiles.x, projectiles.y))
            if projectiles.movingRight:
                projectiles.x += projectiles.speed
            else:
                projectiles.x -= projectiles.speed

            projectiles.checkDamageCollision(Stages.stageHandler.currentStage.enemiesList)
            projectiles.checkDamageCollision(Stages.stageHandler.currentStage.matterList)
            projectiles.checkDamageCollision(Stages.stageHandler.wanderers_list)

            if Stages.stageHandler.currentStage.boss != None:
                # checking for boss 2
                if Stages.stageHandler.currentStage.boss.name == 'Hollow':
                    #print('checking projectiles for boss head')
                    #the stage boss is connected as the body which has a head and heart
                    projectiles.checkDamageCollision(Stages.stageHandler.currentStage.boss.head)
                    projectiles.checkDamageCollision(Stages.stageHandler.currentStage.boss.heart)

                # checking collisions for boss 1 and other bosses
                else:
                    if Stages.stageHandler.currentStage.boss.aggression:
                        projectiles.checkDamageCollision(Stages.stageHandler.currentStage.boss)

            if not Stages.stageHandler.currentStage.scrolling:
                if projectiles.x > Stages.stageHandler.currentStage.rightBoundary + 100\
                    or projectiles.x < Stages.stageHandler.currentStage.leftBoundary - 100:
                    if projectiles in activeProjectiles:
                        activeProjectiles.remove(projectiles)

player = Soldier('Fiends', 'redEyes')


class Weapon():
    user = player

    def __init__(self, name, bulletImg, bulletIteration, bulletSpeed, damage, clipSize, weaponSound, fireType, ammo_color):
        self.name = name
        self.bulletImg = bulletImg
        self.bulletIteration = bulletIteration
        self.bulletSpeed = bulletSpeed
        self.damage = damage
        self.clip = clipSize
        self.clipSize = clipSize
        self.weaponSound = weaponSound
        self.fireType = fireType  # for single Fire we use KEYUP for automatic we use KEYDOWN
        self.ammo_color = ammo_color

    def getAmmoColor(self):
        return self.ammo_color

    def reload(self):
        print('reloading weapon')
        self.clip = self.clipSize

"""Uses specific range from user midLine instead of projectiles list to deal damage!"""

class Shotgun(Weapon):
    damage_dealt = False

    def __init__(self, name, damage, clipSize, weaponSound, fireType, ammo_color, bulletImg=None, bulletIteration=None,
                 bulletSpeed=None, x_range=140):
        Weapon.__init__(self, name, bulletImg, bulletIteration, bulletSpeed, damage, clipSize, weaponSound, fireType,
                        ammo_color)

        self.x_range = x_range  # used as personal extension from self.users midLine in both directions to determine range of shotgun Blast
        self.full_y_range = self.user.Ybubble
        self.left_x_range = [] #range(self.user.midLine - self.x_range, self.user.midLine) # use midLine is updated by user movement in 'outlineSelf()'
        self.right_x_range = range(self.user.midLine, self.user.midLine + self.x_range)

    def update_shotgun_range(self):
        self.full_y_range = range(self.user.topEdge - 10, self.user.bottomEdge + 10)
        self.left_x_range = range(self.user.midLine - self.x_range, self.user.midLine) #range(self.user.midLine - self.x_range, self.user.midLine)
        self.right_x_range = range(self.user.midLine, self.user.midLine + self.x_range)


Rifle = Weapon(name='Rifle', bulletImg=Images.standardBullet[0], bulletIteration=Images.standardBullet, bulletSpeed=30, damage=3,       # damage was originally 5
               clipSize=12, weaponSound=None, fireType='single', ammo_color=green)

Shotgun = Shotgun(name='Shotgun', damage=10, clipSize=5, weaponSound=None, fireType='single', ammo_color=red)

# modify this later #####################################################################
Rocket_Launcher = Weapon(name='Rocket Launcher', bulletImg=Images.rocket_fly[0], bulletIteration=Images.rocket_fly,
                         bulletSpeed=30, damage=20, clipSize=4, weaponSound=None, fireType='single', ammo_color=blue)


# setup player with weapons after weapon creations
player.equip(Rifle)


class Death_Screen():
    enabled = False

    def draw_screen(self):
        win.blit(Images.death_screen, (0, 0))
        win.blit(Images.reclaimer_down, (600, 300))

death_screen = Death_Screen()
'''
for enemy in Stages.stageHandler.currentStage.enemiesList:
    if projectiles.y in enemy.Ybubble:
        if projectiles.x in range(round(enemy.midLine - (enemy.xBuffer)), round(enemy.midLine + (enemy.xBuffer))):
            if projectiles.movingRight:
                if projectiles.x > enemy.midLine:
                    enemy.health -= projectiles.damage
                    activeProjectiles.remove(projectiles)
                    print(f'{enemy.name} took {projectiles.damage} damage!')

            elif not projectiles.movingRight:
                if projectiles.x < enemy.midLine:
                    enemy.health -= projectiles.damage
                    activeProjectiles.remove(projectiles)
                    print(f'{enemy.name} took {projectiles.damage} damage!')
#print(f'this is the bullet damage that has made it into the loop!: {projectiles.currentWeapon.damage}')
'''


'''
class DeathKnight(Humanoid, Player):
    runeOfFallen = False
    pillarOn = False
    killingMachine = None
    strength = 1
    baseStrength = 1
    maxHealth = 400
    classhero = 'DeathKnight'

    def __init__(self, name):
        Humanoid.__init__(self, name, iconImg = Images.redEyesIcon, startingX = 600, startingY = 550, sizeX = 62, sizeY = 85, health = 550, dmg = 15, speed = 7, img = Images.idleR1DkImg, iterationList = Images.rightIdleDeathKnightList,
                          idleLeftList = Images.leftIdleDeathKnightList, idleRightList = Images.rightIdleDeathKnightList, leftWalkList = Images.leftWalkDeathKnightList, rightWalkList = Images.rightWalkDeathKnightList,
                          leftAttackList = Images.deathKnightStabLeftList, rightAttackList = Images.deathKnightStabRightList, leftHurtList = None, rightHurtList = None, deathList = None)
        self.name = name
        #self.attackDmg = 5
        self.humanoidName = 'Player'


    #    def __init__(self, name = input('Enter your name: ')):     //// to be used for allowing player to input their own name
           # Humanoid.__init__(self, name, 400)
            #self.attackDmg = 5

    def pillarOfFrost(self):
        print(f'{self.name} used Pillar of Frost!')
        self.strength = self.baseStrength * .15 + self.baseStrength
        self.pillarOn = True

    def runeOfFallenCrusader(self):
        rng = random.randint(1, 10)
        if rng == 1:
            if not self.runeOfFallen:
                print('Rune of Fallen Crusader Procs!')
                self.strength = self.baseStrength * .20 + self.baseStrength
                self.runeOfFallen = True

            else:
                # This is where you restart the buff timer
                pass
        else:
            pass

    def chanceKillingMachine(self):
        rng = random.randint(1, 5)
        if rng == 1:
            print(f'{self.name} gained a Killing Machine Proc!')
            self.killingMachine = True

    def obliterate(self, target):
        print(f'{self.name} used Obliterate! on {target.name}')
        self.runeOfFallenCrusader()
        self.chanceKillingMachine()

        self.attackDmg = self.critChance('Obliterate', 15 * self.strength, None)
        target.health -= self.attackDmg

    def frostStrike(self, target):
        self.runeOfFallenCrusader()

        if self.killingMachine:
            print(f'{self.name} used Frost Strike (Auto Crit - Killing Machine)')
            self.attackDmg = self.critChance('Frost Strike', 5 * self.strength, True)
            self.killingMachine = False

        else:
            print('No killing Machine')
            self.attackDmg = self.critChance('Frost Strike', 5 * self.strength, None)

    def deathStrike(self, target):
        print(f'{self.name} used Death Strike and healed for {self.maxHealth * .10}')
        self.runeOfFallenCrusader()

        self.attackDmg = self.critChance('Death Strike', 3 * self.strength, None)
        self.health = self.maxHealth * .10 + self.health

    def clockBuffs(self):
        if self.runeOfFallen:
            # Start countdown timer for the rune of fallen crusader
            pass

        if self.pillarOn:
            # This is where you start the timer for the use to buff to fall
            pass

    def masterAttack(self, target):
        if not self.pillarOn:
            self.pillarOfFrost()

        elif self.health <= self.maxHealth / 2:
            self.deathStrike(target)

        elif self.killingMachine:
            self.frostStrike(target)

        else:
            self.obliterate(target)
'''

#bot = Humanoid('bot', 100,Images.idleRightDeathKnightImg,Images.rightWalkDeathKnightList,Images.rightWalkDeathKnightList)


#player = DeathKnight('Fiends')


