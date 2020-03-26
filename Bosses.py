import HeroClassCode as HC
import Images
import pygame
import Stages
import Sounds
import Consumables as C
import random
import Tools
import Spells

win = pygame.display.set_mode((1400, 800))
yellow = (255, 255, 0)


def coolDown(action, timer, cooldown):
    timer += 1
    if timer > cooldown:
        action = not action
        timer = 0


    else:
        action = action
    return action, timer

# class Vortex(HC.Frame):
#     flame_spawn_timer = 0
#
#     def __init__(self, x=0, y=0, iterationList=Images.whoVortexImages):
#         HC.Frame.__init__(self, iterationList, x, y)
#
#     def spin(self):
#         win.blit(self.img, (self.x, self.y))
#         Tools.animateMe(self)
#         self.flame_spawn_timer += 1
#         if self.flame_spawn_timer > 80:
#             self.spawn_flames()
#             self.flame_spawn_timer = 0
#
#     def spawn_flames(self):
#         WHO.flame_list.append(Flame(orb = 'vortex', x = self.x, y = self.y, vortexFlame=True))
#
# summonedVortex = Vortex(1150, 125)
#
# class Flame(HC.Frame):
#     name = 'Flame'
#     damage = 1
#     flame_timer = 0
#
#     def __init__(self, orb, x=0, y=0, iterationList=Images.whoOrbFlameImages, vortexFlame = False):
#         HC.Frame.__init__(self, iterationList, x, y)
#
#         self.orb = orb
#         self.vortexFlame = vortexFlame
#         if vortexFlame:
#             rng = random.randint(1, 4)
#             self.iterationList = Images.whoVortexFlameImages
#             self.momentumnX = -rng
#             self.momentumnY = 0
#
#     """Updates the x and y of the flame based off line's x and y from orb"""
#     def update_position(self):
#         self.x = self.orb.line1X - 25
#         self.y = self.orb.line1Y - 45
#         self.explosion_radiusX = range(round(self.x + 10), round(self.x) + self.img.get_width())
#         self.explosion_radiusY = range(round(self.y - 10), round(self.y) + self.img.get_height() + 5)
#
#     def burn(self):
#         if HC.player.midPoint in self.explosion_radiusY:
#             if HC.player.midLine in self.explosion_radiusX:
#                 Tools.deal_damage_to_player(self.damage)
#
#     def draw(self):
#         win.blit(self.img, (self.x, self.y))
#         Tools.animateMe(self)
#
#     def move(self):
#         """
#         if self.vortexFlame:
#             print('WE ARE MOVING IN THE CORRECT SPOT SHOULD WORK?')
#             self.x -= 1
#             self.y += 1
#             self.draw()
#         """
#         if not self.vortexFlame:
#             self.update_position()
#             self.draw()
#             self.burn()
#
#     """Used specifially by flames spawned by the vortex to float around map"""
#     def float(self):
#         self.explosion_radiusX = range(round(self.x + 10), round(self.x) + self.img.get_width())
#         self.explosion_radiusY = range(round(self.y), round(self.y) + self.img.get_height())
#         if self.y < 610:
#             rngY = random.randint(1, 4)
#             self.momentumnY = rngY
#
#         elif self.y > 750:
#             rngY = random.randint(1, 4)
#             self.momentumnY = -rngY
#
#         if self.x <= 15:
#             rngX = random.randint(1, 4)
#             self.momentumnX = rngX
#
#         elif self.x >= 1200:
#             rngX = random.randint(1, 4)
#             self.momentumnX = -rngX
#
#         self.x += self.momentumnX
#         self.y += self.momentumnY
#
#         self.flame_timer += 1
#         if self.flame_timer > 1000:
#             WHO.flame_list.remove(self)
#         else:
#             self.draw()
#             self.burn()
#
#     """Used specifically by flames spawned from orbs that stay in place"""
#     def idle(self):
#         self.explosion_radiusX = range(round(self.x + 10), round(self.x) + self.img.get_width())
#         self.explosion_radiusY = range(round(self.y), round(self.y) + self.img.get_height())
#         self.flame_timer += 1
#         if self.flame_timer > 350:
#             WHO.flame_list.remove(self)
#         else:
#             self.draw()
#             self.burn()
#
#
#
# class Orb(HC.Frame):
#     name = 'orb'
#     speed = 2
#
#     casting_lazer = False           #determine if orb is actively sending lazers
#     lazer_timer = 0
#     casting_lazer_increment = 0     #resets lazer to false to create breaks between lazer creation
#     lazer_drag = 'L'                #determines which direction the lazer drags as it goes
#
#     flame_added = False             #determines if the flame caused by the line has been added
#     line1X = random.randint(100, 1050)  #random X for lazer target location
#     line1Y = random.randint(610, 790)   #random Y for lazer target location
#
#     def __init__(self, sender, iterationList = Images.whoOrbImages, x = 0 , y = 0):
#         HC.Frame.__init__(self, iterationList, x, y)
#
#         self.sender = sender
#         self.x = self.sender.currentX + 10
#         self.y = self.sender.midPoint
#         self.flame = Flame(orb = self)
#
#     def burnout(self):
#         WHO.flame_list.append(Flame(orb='idle', x=self.flame.x, y=self.flame.y))
#
#     def cast_lazer(self):
#         if not self.casting_lazer:
#             self.casting_lazer, self.lazer_timer = coolDown(self.casting_lazer, self.lazer_timer, cooldown=50)
#             if self.casting_lazer:
#                 self.lazer_drag = random.choice(['L', 'R'])
#                 self.line1X = random.randint(HC.player.midLine - 100, HC.player.midLine + 100)
#                 self.line1Y = random.randint(HC.player.midPoint - 50, HC.player.midPoint + 50)
#                 #self.line1X = random.randint(100, 1050)
#                 #self.line1Y = random.randint(610, 790)
#
#         if self.casting_lazer:
#             if not self.flame_added:
#                 WHO.orb_list.append(self.flame)
#                 self.flame_added = True
#
#             self.casting_lazer_increment += 1
#             pygame.draw.line(win, yellow, (self.x + 40, self.y + 40), (self.line1X, self.line1Y), 2)
#             if self.lazer_drag == 'L':
#                 self.line1X -= 4
#             elif self.lazer_drag == 'R':
#                 self.line1X += 2
#             if self.casting_lazer_increment > 100:
#                 self.casting_lazer = False
#                 self.casting_lazer_increment = 0
#                 self.flame_added = False
#                 self.burnout()
#                 if self.flame in WHO.orb_list:
#                     WHO.orb_list.remove(self.flame)
#
#             #print('sending lazer')
#
#
#     def move(self):
#         self.x -= self.speed
#         win.blit(self.img, (self.x, self.y))
#         Tools.animateMe(self)
#
#         self.cast_lazer()
#
# class Marium(C.Matter):
#     shieldImg = Images.MariumShield
#     shieldBreaking = Images.MariumShieldBreaking
#
#     downed = False  # turned on when marium needs to be attended to after her health reaches 0
#     snapped = False # snaps marium to location to be dragged onto screen by WHO
#
#     def __init__(self, x=-500, y=0, img=Images.marium[0], health=300, iterationList=Images.marium, sizeX=35, sizeY=45):
#         C.Matter.__init__(self, x, y, img, health, iterationList, sizeX, sizeY)
#
#         self.maxHealth = health
#
#     def drawShield(self):
#         if self.immune:
#             win.blit(Images.mariumImmuneShield, (self.x, self.y))
#         elif self.health >= self.maxHealth / 2:
#             win.blit(self.shieldImg, (self.x, self.y))
#         elif self.health < self.maxHealth / 2:
#             win.blit(self.shieldBreaking, (self.x, self.y))
#
#     def snap_to_location(self):
#         self.x = WHO.currentX + 70
#         self.y = WHO.currentY + 110
#
#     def cycle(self):
#         if WHO.health <= 0:
#             Stages.stageHandler.currentStage.matterList.remove(self)
#             pass
#             #marium is done and over with
#         else:
#             if self.health <= 0:
#                 self.health = 0
#                 self.downed = True
#                 #print('Marium needs to re-shield')
#             else:
#                 self.drawShield()
#                 self.checkHealth()
#
# MARIUM = Marium()
#
#
# class Position():
#
#     taken = False
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#
#     def take(self):
#         self.taken = True
#
# pos_1 = Position(x=25, y=535)
# pos_2 = Position(x=75, y=625)
# pos_3 = Position(x=25, y=715)
#
#
# class Portal(HC.Frame):
#     def __init__(self, iterationList, x=100, y=700):
#         HC.Frame.__init__(self, iterationList, x, y)
#
#
#     """Makes the portals become assigned to random positioning"""
#     def dance(self):
#         if not pos_1.taken:
#             self.x = pos_1.x
#             self.y = pos_1.y
#             pos_1.taken = True
#
#         elif not pos_2.taken:
#             self.x = pos_2.x
#             self.y = pos_2.y
#             pos_2.taken = True
#
#         else:
#             self.x = pos_3.x
#             self.y = pos_3.y
#             pos_3.taken = True
#
#
#
#     def teleport(self):
#         if HC.player.midLine in range(self.x, self.x + self.img.get_width()):
#             if HC.player.midPoint in range(self.y, self.y + self.img.get_height()):
#                 if self.iterationList == endPortal.iterationList:
#                     HC.player.currentX = endPortal.x
#                     HC.player.currentY = endPortal.y
#                     HC.player.falling = True
#                 else:
#                     HC.player.currentX = 700
#                     #print('do failure here.')
#
#
#
#
# greenPortal = Portal(iterationList=Images.greenPortal)
# greyPortal = Portal(iterationList=Images.greyPortal)
# redPortal = Portal(iterationList=Images.redPortal)
#
# endPortal = Portal(iterationList=Images.greenPortal, x=770, y=205)
#
# portal_seq_1 = [greyPortal, greenPortal, redPortal]
# portal_seq_2 = [redPortal, greenPortal, greyPortal]
# portal_seq_3 = [greenPortal, redPortal, greyPortal]


class Boss(HC.Humanoid):
    taunted = False
    taunt = Sounds.your_fate_is_sealed # sound that plays from boss when the player is dead.

    dead_sound = Sounds.my_fate_is_sealed # sound played when boss is dead
    dead_sound_played = False
    def __init__(self, stage, startingX, startingY, sizeX, sizeY, findMid, xBuffer, yBuffer, health, dmg, img, iterationList, idleLeftList, idleRightList, leftWalkList, rightWalkList, leftAttackList, rightAttackList, leftHurtList,
                 rightHurtList, deathList, speed=1, iconImg = None):

        HC.Humanoid.__init__(self, stage, iconImg, startingX, startingY, sizeX, sizeY, findMid,
                              xBuffer, yBuffer, health, dmg, speed, img, iterationList,
                              idleLeftList, idleRightList, leftWalkList,
                              rightWalkList, leftAttackList, rightAttackList,
                              leftHurtList, rightHurtList, deathList)



        self.stage = stage
        self.maxHealth = health
        self.humanoidName = 'Boss' # added this in before recording


    def taunt_player(self):
        if HC.player.health <= 0:
            if not self.taunted:
                self.taunt.play()
                self.taunted = True
    """Places Bosses for after custscnes to their engagement starting points."""
    def set_start_placement(self, x, y):
        self.currentX = x
        self.currentY = y

"""The Cave's Sorrow Boss
This is the BODY of the boss"""
# class Hollow(Boss):
#     name = 'Hollow' # identified for damage projectile collisions and explosion tracking for the self.head
#     risen_from_foreground = False # when ready to speak and done with first part of introduce()
#     y_placed = False # starting point for current Y to rise from foreground
#
#     rampaging = False # rampage is the process of all slams in a sequence
#     rampage_timer = 0
#     rampage_cooldown = 50
#
#     slam_ready = False
#     slam_area = 0  # x location for slam to be done
#     slam_range = range(0, 0) # range in which if player is in the slam will deal damage
#     slam_timer = 0
#     slam_cooldown = 60
#
#     speaking_sound = False
#     speaking_sound_timer = 0
#     scream_ready = False
#
#     headless = False
#     current_target_iteration = 0 # iteration in slam_area_list that is currently being traveled to
#
#     slamming = False # becomes True if Boss in slam_area and starts the slam
#
#     phase = 1 # determines boss difficulty / ability/ actions (changes based off health percentages of the boss)
#
#     heart = None
#
#     casted_decay = False # determines if decay has been casted when the head reattatches
#     casted_decay_timer = 0
#     decay_list = [] # undead hands being summoned to slow and damage player
#     decay_flipper = 0 # flips between 0 and 1 to make Hollow body shake when casting decay
#     played_decay_audio = False # determines if the summoning decay sound phrase has already been said once
#
#     dead_rising = False  # If True, undead hands rise from the ground
#     dead_rising_timer = 0
#     dead_rising_cooldown = 500
#
#     death_iteration_counter = 0 # determines death img iteration for boss
#
#     def __init__(self, stage, startingX, startingY):
#
#         Boss.__init__(self, stage, iconImg=Images.regularSkeletonIcon, startingX=startingX, startingY=startingY,
#                                      sizeX=50, sizeY=141, findMid=129,
#                                      xBuffer=55, yBuffer=88, health=580, dmg=5, speed=6, img=Images.hollowIdle[0],
#                                      iterationList=Images.hollowIdle,
#                                      idleLeftList=Images.hollowIdle, idleRightList=Images.hollowIdle,
#                                      leftWalkList=Images.hollowIdle,
#                                      rightWalkList=Images.hollowIdle, leftAttackList=Images.hollowIdle,
#                                      rightAttackList=Images.hollowIdle,
#                                      leftHurtList=Images.hollowIdle, rightHurtList=Images.hollowIdle,
#                                      deathList=Images.hollowIdle)
#
#         self.anchorY = startingY # anchor for reference to retreat back to after dipping into slams
#
#     def cutscene_complete(self):
#         self.stage.cutsceneAvailable = 'completed'
#
#     """Introduces Lord Hollow to the player and upon completion
#     of dialogue will begin the encounter. Also references head
#     to the body"""
#     def introduce(self):
#         print(self.name, 'this should be Hollow as the bosses name')
#         self.head = HOLLOW_HEAD
#         if not self.y_placed:
#             self.currentY = self.currentY + 400
#             self.y_placed = True
#         if not self.risen_from_foreground:
#             Sounds.hollow_rising.play()
#             if self.currentY > self.anchorY:
#                 self.currentY -= 2
#                 self.animateMe()
#                 win.blit(self.img, (self.currentX, self.currentY))
#                 win.blit(Images.cave_boss_foreground, (0, 600))  # draw foreground
#             else:
#                 pygame.mixer.stop()
#                 Sounds.fear_wrath_of_dead.play()
#                 self.risen_from_foreground = True
#         else:
#             print('this is if he has risen yet: ',self.risen_from_foreground)
#             self.speakText('H1', 'text/Hollow_introduce_textbox.txt', function_at_end=self.cutscene_complete)
#             self.animateMe()
#             win.blit(self.img, (self.currentX, self.currentY))
#             print('introducing')
#
#     """Upon being done with rampaging sequence
#     if head not dettatched it becomes dettatched."""
#     def dettatch_head(self):
#         if not self.headless:
#             rng = random.randint(1,2)
#             if rng == 1:
#                 Sounds.i_hunger.play() #(Sound played when head dettatched)
#             elif rng == 2:
#                 Sounds.feast_on_flesh.play()
#             self.headless = True
#             #self.head.float()
#
#     def draw_slam_aoe(self):
#         if self.slam_area == 95:
#             self.slam_range = range(0, 498)
#             #print('drawing rectangle')
#             pygame.draw.rect(win, [255, 0, 0], [0, 605, 498, 400])
#         elif self.slam_area == 550:
#             self.slam_range = range(480, 940)
#             #print('drawing rectangle')
#             pygame.draw.rect(win, [255, 0, 0], [498, 605, 442, 400])
#         elif self.slam_area == 1000:
#             self.slam_range = range(940, 1410)
#             #print('drawing rectangle')
#             pygame.draw.rect(win, [255, 0, 0], [940, 605, 480, 400])
#
#                                                 #150 550 1000
#
#
#     """Slams the ground with fists. If sequence is complete
#     rampaging is put on cooldown."""
#     def slam(self):
#         if not self.slam_ready:
#             if self.headless:
#                 self.iterationList = Images.hollowHeadlessSlamm
#             else:
#                 self.iterationList = Images.hollowSlam
#             self.slam_ready, self.slam_timer = self.coolDown(self.slam_ready, self.slam_timer, self.slam_cooldown)
#             self.draw_slam_aoe()
#
#         elif self.slam_ready:
#             Sounds.slam_sound.play()
#             print('slammed')
#             self.currentY += 70
#             self.slam_ready = False
#             if HC.player.midLine in self.slam_range:
#                 Tools.deal_damage_to_player(damage = 125)
#
#             try:
#                 self.current_target_iteration += 1
#                 self.slam_area = self.slam_area_list[self.current_target_iteration]
#
#             except:
#                 print('done with slamming')
#                 self.rampaging = False
#                 self.current_target_iteration = 0
#                 self.dettatch_head()
#             #self.slam_ready = False
#
#
#     """Moves to slam area based off self.midLine"""
#     def move_to_slam_area(self):
#         self.slam_area = self.slam_area_list[self.current_target_iteration]
#         #print(f'this is the slam area location {self.slam_area}')
#         if self.midLine in range(self.slam_area - 10, self.slam_area + 10):
#             self.slam()
#             #print('in slam area')
#
#         else:
#             if self.midLine < self.slam_area:
#                 self.move('R')
#
#             elif self.midLine > self.slam_area:
#                 self.move('L')
#
#     """Determines slam sequence order of slams"""
#     def select_slam_area(self):
#         #if in phase 1 or phase 2          (slam 3 different spots)
#         rng = random.randint(1, 3)
#         if rng == 1:
#             self.slam_area_list = [95, 550, 1000] #left / mid/ right
#         elif rng == 2:
#             self.slam_area_list = [1000, 95, 550] #right / left / mid
#         elif rng == 3:
#             self.slam_area_list = [550, 1000, 95] #mid / right/ left
#
#     """Starts checks self.rampaging and goes on slamming sequences."""
#     def rampage(self):
#         if self.rampaging:
#             self.move_to_slam_area()
#
#         elif not self.rampaging:
#             #print(self.rampage_timer, ' this is the rampage timer')
#             self.rampaging, self.rampage_timer = self.coolDown(self.rampaging, self.rampage_timer, self.rampage_cooldown)
#             if self.rampaging:
#                 self.select_slam_area()
#
#     """Checks the body state if the head is attatched or not"""
#     def check_headless_state(self):
#         if self.headless:
#             self.iterationList = Images.hollowHeadlessIdle
#             self.leftWalkList = Images.hollowHeadlessIdle
#             self.rightWalkList = Images.hollowHeadlessIdle
#         else:
#             self.iterationList = Images.hollowIdle
#             self.leftWalkList = Images.hollowIdle
#             self.rightWalkList = Images.hollowIdle
#
#     def draw_boss_bar(self):
#         win.blit(Images.hollowName, (735, 20))
#         win.blit(Images.hollowIcon, (940, -8))
#
#         pygame.draw.rect(win, [169, 169, 169], [510, 60, self.maxHealth, 35])
#         pygame.draw.rect(win, [255, 128, 0], [510, 60, self.head.health, 35])
#         win.blit(Images.boss_template, (480, 45))
#
#     """Upgrades boss abilities based off the current phase."""
#     def get_upgrade(self):
#         #phase 1 is speed: 6    slam_cooldown: 60   self.head.speed = 6
#         if self.phase == 2:
#             print('in phase 2')
#             self.speed = 8 # up from 7  (increase speed)
#             self.slam_cooldown = 45 # down from 60  (slam occurs quicker)
#             self.head.speed = 9
#             self.dead_rising_cooldown = 750 # increased to give more spawns to undead hands
#
#         elif self.phase == 3:
#             print('in phase 3')
#             self.speed = 10
#             self.slam_cooldown = 30
#             self.head.speed = 10
#             self.dead_rising_cooldown = 900
#
#     """Adds undead adds to the decay list and shakes
#     the Hollow Body"""
#     def cast_decay(self):
#         self.dead_rising = True
#         print('casting decay')
#         #if self.phase > 1:
#         self.iterationList = Images.hollow_summon_decay
#         self.casted_decay, self.casted_decay_timer = self.coolDown(self.casted_decay, self.casted_decay_timer, 100)
#
#         if self.decay_flipper == 0:
#             self.decay_flipper = 1
#             self.currentX = self.currentX + 15
#         elif self.decay_flipper == 1:
#             self.decay_flipper = 0
#             self.currentX = self.currentX - 15
#         self.outlineSelf()
#
#
#     """Determines phase based off current Health.
#        Each phase increases the speed of both the body and head actions."""
#     def determine_phase(self):
#         if self.head.health > self.maxHealth * .80:
#             self.phase = 1
#
#         elif self.head.health > self.maxHealth * .50:
#             self.phase = 2
#
#         else:
#             self.phase = 3
#
#     """Determines random audio output from the boss"""
#     def speak_sound(self):
#         rng = random.randint(1, 3)
#         if rng == 1:
#             Sounds.death_bell_tolls.play()
#         elif rng == 2:
#             Sounds.i_cant_stand_the_living.play()
#         elif rng == 3:
#             Sounds.hatred_devours_all.play()
#         self.speaking_sound = True
#
#     """Controls automated management for sound audio phrases given by boss."""
#     def script(self):
#         #Allows time for sound to speak without interuption
#         if self.speaking_sound:
#             self.speaking_sound, self.speaking_sound_timer = self.coolDown(self.speaking_sound, self.speaking_sound_timer,
#                                                                            500)
#         else:
#             rng = random.randint(1, 10)
#             if rng == 1:
#                 self.speak_sound()
#
#     """Flow of the bosses sequences. (The Main) of the boss"""
#     def cycle(self):
#         if HC.player.health <= 0:
#             self.taunt_player()
#
#         if self.head.health > 0:
#             self.script()
#             self.determine_phase()
#             self.get_upgrade()
#             self.check_headless_state()
#
#             #return to y as priority after slamming in self.rampage()
#             if self.currentY > self.anchorY:
#                 self.move('U')
#
#                 #draw body before head
#                 self.animateMe()
#                 win.blit(self.img, (self.currentX, self.currentY))
#
#                 if self.headless:
#                     self.head.float()
#
#             else:
#                 if not self.current_target_iteration == 0 and not self.casted_decay:
#                     if not self.played_decay_audio:
#                         self.stage.enemiesList.append(HC.Fade_Walker(startingX=random.choice([0, 1300]), startingY=random.choice([600, 780]), droppedConsumable=C.Battery, aggression=True))
#                         Sounds.dead_shall_serve.play()
#                         self.played_decay_audio = True
#
#                     self.cast_decay()
#                     self.animateMe()
#                     win.blit(self.img, (self.currentX, self.currentY))
#                 else:
#                     self.played_decay_audio = False
#                     self.rampage()
#
#                     #draw body before head
#                     self.animateMe()
#                     win.blit(self.img, (self.currentX, self.currentY)) #always drawn after rampage and head drawn after this
#
#                     if self.headless:
#                         self.head.float()
#
#             #checking for / managing / spawning Decay
#             for decay in self.decay_list:
#                 decay.form()
#                 #print(decay.x, ' this is decayX', decay.y, 'this is decay Y')
#             if self.dead_rising:
#                 #print('casting dead_rising')
#                 rng = random.randint(1, 60)
#                 if rng == 1:
#                     if len(self.decay_list) <= 16: #delete after testing
#                         self.decay_list.append(Decay(x=random.randint(50, 1305), y=random.randint(500, 655), iterationList=Images.skele_hand_hatch))
#                 self.dead_rising, self.dead_rising_timer = self.coolDown(self.dead_rising, self.dead_rising_timer, self.dead_rising_cooldown)
#
#
#             #draw heart and health bar
#             self.heart.transfer_damage()
#             self.draw_boss_bar()
#
#         elif self.head.health <= 0:
#             if not self.dead_sound_played:
#                 self.dead_sound.play()
#                 Sounds.hollow_rising.play()
#                 self.dead_sound_played = True
#
#             self.iterationList = Images.hollowDeath
#             self.img = self.iterationList[self.iterationCounter]
#             self.death_iteration_counter += 1
#             if self.death_iteration_counter > 35:
#                 if self.iterationCounter >= len(self.iterationList) - 1:
#                     self.iterationCounter = 0
#                     self.stage.boss = None
#                     print('stage done')
#                 else:
#                     self.iterationCounter += 1
#                     self.death_iteration_counter = 0
#             win.blit(self.img, (self.currentX, self.currentY + 50))
#
#
#
#
# HOLLOW = Hollow(stage = Stages.stage_one, startingX=580, startingY=235)
# HOLLOW.name = "Hollow"
#
# def getAttackDirection(objects, leftList, rightList):
#
#     if objects.forwardFace:
#         objects.iterationList = rightList
#     else:
#         objects.iterationList = leftList
#
# """This is the head of the boss"""
# class Hollow_Head(Boss):
#     aggression = True
#     dettatched = False
#     charge_ready = False
#
#     applied_bite = False
#
#     crashed = False # determines if colided with wall or not
#
#     return_to_body = False
#     return_to_body_timer = 0
#
#
#     def __init__(self, stage, startingX, startingY):
#
#         Boss.__init__(self, stage, iconImg=Images.regularSkeletonIcon, startingX=startingX, startingY=startingY,
#                                      sizeX=58, sizeY=92, findMid=66,
#                                      xBuffer=55, yBuffer=55, health=580, dmg=5, speed=8, img=Images.hollowHeadWalkLeft[0],
#                                      iterationList=Images.hollowHeadWalkLeft,
#                                      idleLeftList=Images.hollowHeadWalkLeft, idleRightList=Images.hollowHeadWalkLeft,
#                                      leftWalkList=Images.hollowHeadWalkLeft,
#                                      rightWalkList=Images.hollowHeadWalkRight, leftAttackList=Images.hollowHeadWalkLeft,
#                                      rightAttackList=Images.hollowHeadWalkLeft,
#                                      leftHurtList=Images.hollowHeadWalkLeft, rightHurtList=Images.hollowHeadWalkLeft,
#                                      deathList=Images.hollowHeadWalkLeft)
#
#         self.body = HOLLOW # This is the body reference for the head object to send damage to
#         self.headshotRange = (-500, -500) # disables headshots for this Boss since all would be headshot damage
#
#     def adjust_size(self):
#         self.outlineSelf()
#         #print(f'{self.findMid} this is the findMid, {self.sizeY} this is the sizeY')
#         #print(f'{self.currentX}, {self.currentY} this is the currentX and currentY')
#         #print(f'{self.leftEdge}, {self.rightEdge}, left to right')
#         #print(f'{self.topEdge}, {self.bottomEdge} top to bottom')
#
#         if self.crashed:
#             self.sizeY = 122
#
#             if self.forwardFace:
#                 self.findMid = 95
#             else:
#                 self.findMid = 125
#
#         else:
#             self.findMid = 66
#             self.sizeY = 92
#
#     def get_body_location(self):
#         self.currentX = self.body.currentX + 20
#         self.currentY = self.body.currentY
#
#     def get_side_destination(self):
#         rng = random.randint(1, 4)
#         if rng == 1:
#             self.side_position = (0, 560) # puts Skele on left / upper lane side
#         elif rng == 2:
#             self.side_position = (0, 660) # puts Skele on left / lower lane side
#         elif rng == 3:
#             self.side_position = (1250, 560) # puts Skele on right/ upper lane side
#         elif rng == 4:
#             self.side_position = (1250, 660) # puts Skele on right / lower lane side
#
#     """Check if a bite has been applied to the player during each charge!"""
#     def check_bite(self):
#         if not self.applied_bite:
#             if HC.player.midLine in range(self.leftEdge, self.rightEdge):
#                 if HC.player.midPoint in range(self.topEdge, self.bottomEdge):
#
#                     # SOUND: PLAY BITE SOUND
#                     Sounds.bite_sound.play()
#                     self.applied_bite = True
#                     Tools.deal_damage_to_player(damage = 100, stun_debuff=100)
#
#     """Head returns to body to reattatch itself
#     to safety and enable different abilities."""
#     def reconnect(self):
#         self.takingDamage = False
#         self.leftWalkList = Images.hollowHeadWalkLeft
#         self.rightWalkList = Images.hollowHeadWalkRight
#
#         if self.currentX in range(self.body.currentX - 20, self.body.currentX + 20) and\
#             self.currentY in range(self.body.currentY - 20, self.body.currentY + 20):
#                 self.body.headless = False # reset head on body
#                 self.dettatched = False # confirms head back on body
#
#                 self.charge_ready = False # resets for next charge
#                 self.applied_bite = False # reset for next bite
#
#                 self.body.casted_decay = False # reset the cast_decay for body to cast
#                 self.crashed = False
#                 self.return_to_body = False
#                 self.return_to_body_timer = 0
#
#                 #reset slamming rotation to make sure 3 slams happen before head dettatches again
#                 if self.body.current_target_iteration >= 1:
#                     self.body.current_target_iteration = 0
#                 print('reconnected to body')
#
#
#         else:
#             if self.currentX not in range(self.body.currentX - 20, self.body.currentX + 20):
#                 if self.currentX > self.body.currentX:
#                     self.move('L')
#
#                 elif self.currentX < self.body.currentX:
#                     self.move('R')
#
#             if self.currentY not in range(self.body.currentY - 20, self.body.currentY + 20):
#                 if self.currentY < self.body.currentY:
#                     self.move('D')
#
#                 elif self.currentY > self.body.currentY:
#                     self.move('U')
#
#             self.headshotRange = (-500, -500) # make headshots not possible for this boss
#         #reset for next dettatchment
#
#
#     """Head charges across lane attempting to bite player.
#     Collides with left and right stage boundary for damage.
#     Then returns to the body for reattatchment."""
#     def charge(self):
#         if self.health < self.originalHealth:
#             self.takingDamage = True
#             self.originalHealth = self.health
#         #print(f'{self.currentY} currentY of skull head!')
#         # crashed is true if collided with wall
#         if self.crashed:
#             self.return_to_body, self.return_to_body_timer = self.coolDown(self.return_to_body, self.return_to_body_timer, 80)
#             if self.return_to_body:
#                 self.reconnect()
#
#             else:
#                 if self.takingDamage:
#                     if self.iterationCounter > 1:
#                         self.resetIteration()
#                     getAttackDirection(self, Images.hollowHeadDamagedLeft, Images.hollowHeadDamagedRight)
#                     if self.iterationList[self.iterationCounter] == self.iterationList[-1]:
#                         self.takingDamage = False
#                 else:
#                     getAttackDirection(self, Images.hollowHeadCrashedLeft, Images.hollowHeadCrashedRight)
#
#                 self.animateMe()
#             #print('crashed')
#
#         else:
#             if self.takingDamage:
#                 if self.iterationCounter >= 3:
#                     self.resetIteration()
#                 self.leftWalkList = Images.hollowHeadWalkingDamagedLeft
#                 self.rightWalkList = Images.hollowHeadWalkingDamagedRight
#
#                 if self.iterationList[self.iterationCounter] == self.iterationList[-1]:
#                     self.takingDamage = False
#                     self.leftWalkList = Images.hollowHeadWalkLeft
#                     self.rightWalkList = Images.hollowHeadWalkRight
#
#             if self.forwardFace:
#                 #print(f'{self.currentX} this is the currentX')
#                 if self.currentX > 1290:
#                     self.currentX = 1235
#                     self.currentY -= 50
#                     #self.outlineSelf()
#                     self.crashed = True
#
#                 else:
#                     self.move('R')
#
#             elif not self.forwardFace:
#                 #print(f'{self.currentY} this is the currentY')
#                 if self.currentX < -50:
#                     self.currentX = -30
#                     self.currentY -= 50
#                     #self.outlineSelf()
#                     self.crashed = True
#
#                 else:
#                     self.move('L')
#
#             self.headshotRange = (-500, -500) # disables headshot range for boss after movements
#             self.check_bite()
#
#     def move_to_lane(self):
#         print(f'this is the skele side position destinattion: {self.side_position[0], self.side_position[1]}')
#         print(f'this is the head locations: {self.currentX, self.currentY}')
#         if self.currentX in range(self.side_position[0] - 10, self.side_position[0] + 10)\
#             and self.currentY in range(self.side_position[1] - 10, self.side_position[1] + 10):
#             self.charge_ready = True
#
#         else:
#
#             if self.currentX < self.side_position[0]:
#                 self.move('R')
#             if self.currentX > self.side_position[0]:
#                 self.move('L')
#
#             #starts y movement after X locaiton has been reached
#             if self.currentX in range(self.side_position[0] - 10, self.side_position[0] + 10):
#                 if self.side_position[0] < 500:  # if on left side  face right
#                     self.forwardFace = True
#                 else:
#                     self.forwardFace = False
#
#                 if self.currentY < self.side_position[1]:
#                     self.move('D')
#                 if self.currentY > self.side_position[1]:
#                     self.move('U')
#
#             self.headshotRange = (-500, -500) #disables headshot range for boss after movements
#
#
#
#     def float(self):
#         #adjusts for different tilt when floating or crashed
#         self.adjust_size()
#
#         if self.body.headless:
#             if not self.dettatched:
#                 self.get_body_location()  # snaps head to body location to start self.float() from
#                 self.get_side_destination() # selects which side and lane position to travel to
#                 self.dettatched = True
#
#             if not self.charge_ready:
#                 self.move_to_lane()
#             else:
#                 self.charge()
#             win.blit(self.img, (self.currentX, self.currentY))
#
# HOLLOW_HEAD = Hollow_Head(stage=Stages.stage_one, startingX=HOLLOW.currentX, startingY= HOLLOW.currentY)
#
#
# HOLLOW.head = HOLLOW_HEAD # attatches head to body
#
#
# class Decay(HC.Frame):
#     hatched = False # only shadow of hand showing warning player of rising hand incoming
#     hatch_timer = 0
#
#     risen = False # hand rises to do slow / damage above the ground
#     risen_timer = 0
#
#     falling = False
#     falling_timer = 0
#     fall_complete = False
#
#     def __init__(self, x, y, iterationList=Images.skele_hand_hatch):
#         HC.Frame.__init__(self, iterationList, x, y)
#
#     """If player in range of hand movement the hand will deal
#     damage to the player and stun him."""
#     def grasp(self):
#         #print('grasping')
#         if HC.player.midLine in range(self.x + 62, self.x + 62 + 47)\
#             and HC.player.midPoint in range(self.y + 60, self.y + 60 + 80):
#                 if not HC.player.immune:
#                     Sounds.stun_sound.play()
#                     Tools.deal_damage_to_player(damage=20, stun_debuff=100)
#                     #HC.player.stunned = True
#                     HOLLOW.decay_list.remove(self)
#
#     """Part 4 and final part of form() The hand falls
#     back into the ground and removes itself from the
#     decay_list."""
#     def fall(self):
#         self.iterationList = Images.skele_hand_fall
#         self.fall_complete = Tools.animateMe(self, False, True)
#         if self.fall_complete:
#             self.iterationCounter = 0
#         else:
#             HOLLOW.decay_list.remove(self)
#
#
#     """Part 3 of the form() where the hand is waving around
#     and is actively trying to grasp() player."""
#     def wave(self):
#         self.iterationList = Images.skele_hand_wave
#         self.grasp()
#         self.falling_timer += 1
#         if self.falling_timer > 400: # change to 125
#             self.falling = True
#             self.iterationCounter = 0
#
#
#         # if HC.player.midLine in range(self.x, self.x + 60)\
#         #     and HC.player.midPoint in range(self.y, self.y + 60):
#         #     HC.player.health -= 1
#
#     """Part 1 of the form() where the hand is a shadow about
#     to rise after the hatch timer expires."""
#     def check_hatch(self):
#         if not self.hatched:
#             self.hatch_timer += 1
#
#             if self.hatch_timer > 100:
#                 self.hatched = True
#                 self.iterationCounter = 0
#
#     """Part 2 of form() allowing hand to rise from ground
#     before dealing slow / damage to player."""
#     def check_rise(self):
#         if not self.risen:
#             self.iterationList = Images.skele_hand_rise
#             self.risen = Tools.animateMe(self, False, True)
#             if self.risen:
#                 self.iterationCounter = 0
#
#
#     """Cycle for forming the hand above the ground"""
#     def form(self):
#         if self.falling:
#             self.fall()
#         else:
#             self.check_hatch()
#             if self.hatched:
#                 self.check_rise()
#             if self.risen:
#                 self.wave()
#
#         self.animateMe()
#         win.blit(self.img, (self.x, self.y))
#
#
# class Blood_Splatter(HC.Frame):
#     def __init__(self, iterationList=Images.hollowHeartSplatter, x=700, y=660):
#         HC.Frame.__init__(self, iterationList, x, y)
#
#
# blood = Blood_Splatter()
# """The heart of the boss Hollow which transfers 1/4
# of the damage it takes back to Hollow_Head."""
# class Heart(C.Matter):
#     head = HOLLOW_HEAD # attatches the head to the heart
#
#     splatter_ready = True # pumps blood animation when damaged
#     splatter_timer = 0
#     def __init__(self, x, y, img, health, iterationList, sizeX, sizeY):
#         C.Matter.__init__(self, x, y, img, health, iterationList, sizeX, sizeY)
#
#     """Draws / animates heart and transfers damage
#     to boss"""
#     def transfer_damage(self):
#         #print(self.splatter_ready, 'this is splatter ready')
#
#         if self.health < self.originalHealth:
#             transfer_damage = .5
#             self.head.health -= transfer_damage
#             self.originalHealth = self.health
#
#             if not self.splatter_ready:
#                 self.splatter_timer += 1
#                 if self.splatter_timer > 20:
#                     self.splatter_ready = True
#             else:
#                 #draw blood
#                 self.splatter_ready = Tools.animateMe(blood, True, False)
#                 win.blit(blood.img, (self.x - 15, self.y - 10))
#
#         Tools.animateMe(self)
#         win.blit(self.img, (self.x, self.y))
#
# HEART = Heart(x=700, y= 650, img = Images.hollowHeart[0], health = 10000, iterationList= Images.hollowHeart, sizeX=31, sizeY=34)
# HOLLOW.heart = HEART # attatches the heart to the body
#

#class
"""Lord of the forest"""
# class Who(Boss):
#     name = 'Who'
#     phase = 1
#
#     myMarium = MARIUM
#
#     minionsReady = False
#     minionsTimer = 600 # starts at 600 to get an earlier starting summon
#     minionList = [HC.Skeleton,
#                   HC.Skeleton,
#                   HC.Skeleton]
#
#     vortex_sounded = False # indicates if the vortex has already made its sound during each cast
#
#     #start_pos_x =
#     flying_y_pos = 140
#
#     flying = False
#     first_ascend = True
#
#     orb_ready = False
#     orb_timer = 0
#     orb_cooldown = 250
#     orb_list = []
#     flame_list = []
#
#     casting_vortex = False
#     vortex_timer = 0
#
#     portals_active = False
#     portals_assigned = False
#
#
#     grunt_damage = False
#     grunt_damage_timer = 0
#
#     voice = Sounds.who_damage_taken_1
#
#     def __init__(self, stage, startingX, startingY):
#         Boss.__init__(self, stage, iconImg=Images.regularSkeletonIcon, startingX=startingX, startingY=startingY,
#                              sizeX=50, sizeY=141, findMid=129,
#                              xBuffer=55, yBuffer=88, health=580, dmg=5, speed=3, img=Images.whoIdleLeft[0],
#                              iterationList=Images.whoIdleLeft,
#                              idleLeftList=Images.whoIdleLeft, idleRightList=Images.whoIdleRight,
#                              leftWalkList=Images.whoWalkLeft,
#                              rightWalkList=Images.whoWalkRight, leftAttackList=Images.whoAttackLeft,
#                              rightAttackList=Images.whoAttackRight,
#                              leftHurtList=Images.whoHurtLeft, rightHurtList=Images.whoHurtRight,
#                              deathList=Images.whoDeath)
#
#         self.stage.matterList.append(self.myMarium)  # injects self into self.stage.matterlist upon initialization
#         self.maxHealth = self.health
#         self.ground_y_pos = startingY
#         self.humanoidName = 'Boss'
#
#     """Makes a grunt sound when grunt_damage is true."""
#     def grunt(self):
#
#         if self.health < self.originalHealth and not self.grunt_damage:
#             self.grunt_damage = True
#             self.grunt_sound = random.choice(
#                 [Sounds.who_damage_taken_1, Sounds.who_damage_taken_2, Sounds.who_damage_taken_3])
#
#             self.voice = self.grunt_sound
#             self.voice.stop()
#             self.voice.play()
#             self.originalHealth = self.health
#
#         if self.grunt_damage:
#             self.grunt_damage, self.grunt_damage_timer = self.coolDown(self.grunt_damage, self.grunt_damage_timer, 100)
#
#     """Progresses the stage to the boss partition after the enemiesList and cutscene intro"""
#     def cutscene_complete(self):
#         self.stage.cutsceneAvailable = 'completed'
#
#     '''Used as the cutscene intro'''
#     def introduce(self):
#         if not self.myMarium.snapped:
#             self.myMarium.snap_to_location()
#             self.myMarium.snapped = True
#         #print('introducing')
#
#         #print(f'this is the stage: {self.stage.name}')
#         #print(f'this is the stageBoss: {self.stage.boss}')
#        # print(f'this is enemieslist: {self.stage.enemiesList}')
#        # print(self.stage.cutsceneAvailable)
#         if self.currentX > 1050:
#             self.move('L')
#             #self.speakText('Who_S1', 'text/Who_cutscene_TextBox.txt')
#             #HeroClassCode.Piles.speakText('S0F1', 'text/PilesStageZeroTextBox.txt')
#         if self.myMarium.x > 1280:
#             self.myMarium.x -= 2
#             self.myMarium.update_position()
#         else:
#             self.speakText('Who_S2', 'text/Who_cutscene_TextBox.txt', function_at_end=self.cutscene_complete, specifiedDimensions=(50, 100))
#             self.iterationList = self.idleLeftList
#             self.player_line_x = HC.player.currentX
#             print(self.stage.name)
#         win.blit(self.img, (self.currentX, self.currentY))
#         self.animateMe()
#
#     def draw_boss_bars(self):
#         if self.health > 0:
#             win.blit(Images.whoName, (735, 20))
#             win.blit(Images.whoIcon, (940, 6))
#             win.blit(Images.mariumName, (795, 100))
#             win.blit(Images.mariumIcon, (940, 95))   #dont draw marium
#
#
#             pygame.draw.rect(win, [169, 169, 169], [510, 60, self.maxHealth, 35])
#             pygame.draw.rect(win, [255, 128, 0], [510, 60, self.health, 35])
#             win.blit(Images.boss_template, (480, 45))
#
#         #marium Shield health
#             pygame.draw.rect(win, [127, 128, 255], [510, 145, self.myMarium.health * 2, 25])
#
#     def reset_vortex(self):
#         self.casting_vortex = False
#         self.vortex_timer = 0
#         self.portals_active = False
#         self.portals_assigned = False
#
#         #reset positions being taken
#         pos_1.taken = False
#         pos_2.taken = False
#         pos_3.taken = False
#
#
#
#     def cast_vortex(self):
#
#         if not self.casting_vortex:
#             if self.phase > 1:
#                 self.vortex_sounded = False
#                 #print('NOT CASTING VORTEX')
#                 self.myMarium.immune = False
#                 self.casting_vortex, self.vortex_timer = self.coolDown(self.casting_vortex, self.vortex_timer, 500)
#                 if not self.takingDamage:
#                     self.iterationList = self.idleLeftList
#
#         elif self.casting_vortex:
#             if not self.vortex_sounded:
#                 Sounds.vortex_sound.play(loops=1)
#                 self.vortex_sounded = True
#             #print('STILL IS CASTING VORTEX')
#             self.img = self.leftAttackList[1]
#             self.myMarium.immune = True
#             self.casting_vortex, self.vortex_timer = self.coolDown(self.casting_vortex, self.vortex_timer, 500)
#             summonedVortex.spin()
#
#             #portals manipulation and management
#             self.portals_active = True
#             if self.portals_active:
#                 if not self.portals_assigned:
#                     endPortal.iterationList = random.choice([Images.greenPortal, Images.redPortal, Images.greyPortal])
#                     self.portal_sequence = random.choice([portal_seq_1, portal_seq_2, portal_seq_3])
#                     for portal in self.portal_sequence:
#                         portal.dance()
#
#                     self.portals_assigned = True
#
#             #draw portals
#
#                 Tools.animateMe(greenPortal)
#                 win.blit(greenPortal.img, (greenPortal.x, greenPortal.y))
#                 Tools.animateMe(greyPortal)
#                 win.blit(greyPortal.img, (greyPortal.x, greyPortal.y))
#                 Tools.animateMe(redPortal)
#                 win.blit(redPortal.img, (redPortal.x, redPortal.y))
#                 Tools.animateMe(endPortal, (endPortal.x, endPortal.y))
#                 win.blit(endPortal.img, (endPortal.x, endPortal.y))
#
#                 greenPortal.teleport()
#                 greyPortal.teleport()
#                 redPortal.teleport()
#
#
#     def summonMinions(self):
#         if not self.minionsReady:
#             self.minionsReady, self.minionsTimer = self.coolDown(self.minionsReady, self.minionsTimer, 1000)
#             if self.minionsTimer == 800:
#                 Sounds.minions_rise_sound.play(loops=0)
#
#         elif self.minionsReady:
#             if self.phase == 1:
#                 randomX = random.choice([100, 1000])
#                 randomY = random.choice([500, 700])
#                 self.stage.enemiesList.append(
#                     HC.Skeleton('regularSkeleton', randomX, randomY, droppedConsumable=C.spawnRandomConsumables(),
#                                 aggression=True))
#
#             if self.phase > 1:
#                 for pick in range(2):
#                     randomX = random.choice([100, 1000])
#                     randomY = random.choice([500, 700])
#                     self.stage.enemiesList.append(HC.Skeleton('regularSkeleton', randomX, randomY, droppedConsumable=C.spawnRandomConsumables(), aggression=True))
#
#
#             if self.phase > 2:
#                 randomX = random.choice([100, 1000])
#                 randomY = random.choice([500, 700])
#                 self.stage.enemiesList.append(HC.Skeleton('captainSkeleton', randomX, randomY, droppedConsumable=C.Battery, aggression=True))
#
#
#             self.minionsReady = False
#
#
#             #Sounds.minions_rise_sound.play(loops=0)
#         #print(f'this is the mininos timer: {self.minionsTimer}')
#
#     def useAbility(self):
#         pass
#
#     """Awaits for player to step forward 25 pixels to start engagement"""
#     def await_engage(self):
#         self.animateMe()
#         if HC.player.currentX > self.player_line_x + 25 or HC.player.shooting:
#             self.aggression = True
#
#
#
#     def attend_marium(self):
#         self.myMarium.health += 1
#         self.forwardFace = True
#
#
#     def descend(self):
#         if self.currentY < self.ground_y_pos:
#             self.move('D')
#         else:
#             if not self.takingDamage:
#                 self.iterationList = self.idleRightList
#
#             self.attend_marium()
#             if self.myMarium.health >= self.myMarium.maxHealth:
#                 self.flying = False
#                 self.myMarium.downed = False
#
#     def ascend(self):
#         self.forwardFace = False
#         if self.first_ascend:
#             Sounds.fine_sound.play(loops=0)
#             self.first_ascend = False
#
#         self.speed = 3
#         if self.currentY > self.flying_y_pos:
#             self.move('U')
#         else:
#             self.flying = True
#             self.iterationList = self.idleLeftList
#
#     def manage_abilities(self):
#         for orb in self.orb_list:
#             orb.move()
#             if orb.x < Stages.stageHandler.currentStage.leftBoundary and orb.name == 'orb':
#                 self.orb_list.remove(orb)
#                 if orb.flame in WHO.orb_list:
#                     WHO.orb_list.remove(orb.flame)
#
#         for flame in self.flame_list:
#             if flame.vortexFlame:
#                 flame.float()
#             else:
#                 flame.idle()
#
#
#
#
#
#     def cast_orb(self):
#
#         if self.phase == 2:
#             self.orb_cooldown = 200
#
#         if not self.orb_ready:
#             if not self.takingDamage:
#                 self.orb_ready, self.orb_timer = self.coolDown(self.orb_ready, self.orb_timer, self.orb_cooldown)
#                 if self.orb_cooldown == 250:
#                     rng = random.randint(1, 3)
#                     if self.orb_timer == 150:
#                         if rng == 1:
#                             Sounds.stop_wasting_time.play(loops=0)
#
#                 elif self.orb_cooldown == 200:
#                     rng = random.randint(1, 4)
#                     if self.orb_timer == 100:
#                         if rng == 1:
#                             Sounds.stop_wasting_time.play(loops=0)
#
#         elif self.orb_ready:
#             self.iterationList = self.leftAttackList
#             self.orb_ready = self.animateMe(True, False)
#             self.casting_orb = True
#             if not self.orb_ready:
#                 self.iterationList = self.idleLeftList
#                 self.orb_list.append(Orb(self))
#                 self.casting_orb = False
#
#
#     def flyingCycle(self):
#
#         print(self.orb_list)
#         try:
#             self.cast_orb()
#         except IndexError:
#             self.iterationCounter = 0
#
#         if self.phase > 0:   #== 3
#
#             self.cast_vortex()
#
#
#
#     """Changes the phase based off the bosses current Health. Phases adjust the difficulty and power
#     of boss abilities"""
#     def get_phase(self):
#
#         print(f'this is the current phase: {self.phase}')
#         if self.health >= self.maxHealth * .80:
#             self.phase = 1
#         elif self.health >= self.maxHealth *.50:
#             self.phase = 2
#         else:
#             self.phase = 3
#
#     def cycle(self):
#         #print(f'this is the boss taking damage: {self.takingDamage}')
#         #waits for player aggression
#         if self.dead:
#             HC.combatTextList = [] # clears all stun debuffs from adds
#             Spells.activeSpells = [] #clears all buffs from adds
#             Stages.stageHandler.currentStage.boss = None
#             Stages.stageHandler.currentStage.enemiesList = []
#             print('stage completed')
#
#         self.grunt()
#
#         if not self.aggression:
#             self.await_engage()
#
#         #flys to starting position when starting aggression
#         elif self.aggression:
#             self.get_phase()
#             self.draw_boss_bars()
#
#             self.reportHealth()
#
#
#             self.summonMinions()
#             self.manage_abilities()   #manages and moves orbs and flames
#
#             #print(f'this is the matter list is marium in here? {self.stage.matterList}')
#             if self.takingDamage:
#                 self.reset_vortex()
#                 self.animateDamageTaken()
#
#             else:
#                 self.animateMe()
#                 if not self.showDamage:
#                     self.showDamage, self.showDamageTimer = self.coolDown(self.showDamage, self.showDamageTimer, 30)
#
#                 if not self.flying and not self.myMarium.downed:
#                     self.ascend()
#
#                 #when reached will start offical boss encounter
#                 elif self.flying:
#                     if self.flying and not self.myMarium.downed:
#                         self.flyingCycle()
#
#                     else:
#                         self.reset_vortex()
#                         self.descend()
#                     #print('battle ready and starting')
#
#             #print(f'this is myMarium health: {self.myMarium.health}')
#
#
#            # if self.casting_vortex:
#                # if not self.takingDamage:
#                     #self.img = self.leftAttackList[1]
#                 #else:
#                     #self.reset_vortex()
#
#
#         win.blit(self.img, (self.currentX, self.currentY))
#         win.blit(self.myMarium.img, (self.myMarium.x, self.myMarium.y))
#         self.headshotRange = (-500, -500) # disables headshots on the boss
#
#         #speaks to player
#         rng = random.randint(1, 600)
#         if rng == 1:
#             self.voice.stop()
#             self.voice = random.choice([Sounds.whoLaugh, Sounds.no_place_for_living])
#             self.voice.play()
#
#
#         #if not self.takingDamage:
#             #self.animateMe()
#         #print('in cycle!')
#
# WHO = Who(Stages.stage_one, 1450, 550) # currently set to stage 3




