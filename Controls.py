import pygame
import Dock
import Images
import HeroClassCode
import random
import Stages
import Explosives
import Bosses as B
import Interface_Main
import Shop_Images as SI
import Sounds

pygame.init()

HC = HeroClassCode
win = pygame.display.set_mode((1400, 800))


def getAttackDirection(objects, leftList, rightList):

    if objects.forwardFace:
        objects.iterationList = rightList
    else:
        objects.iterationList = leftList

def shiftPlayerAttack():
    rng = random.randint(1, 2)
    if rng == 1:
        HC.player.leftAttackList = Images.deathKnightStabLeftList
        HC.player.rightAttackList = Images.deathKnightStabRightList

    elif rng == 2:
        HC.player.leftAttackList = Images.deathKnightAttack2LeftList
        HC.player.rightAttackList = Images.deathKnightAttack2RightList

    #elif rng == 3:
        #HC.player.leftAttackList =
        #HC.player.rightAttackList =

def getCharacterSpeaking(stage):
    character = None
    if stage == Stages.stage_zero:
        character = HC.Piles
    #elif stage == Stages.stage_one:
        #character = B.HOLLOW

    if character != None:
        return character


def playerControls():
    currentStage = Stages.stageHandler.getCurrentStage()
    textBoxCharacter = getCharacterSpeaking(currentStage)
    event = pygame.event.poll()
    keys = pygame.key.get_pressed()

#Player Movement Controls
    # Shield generator timer recovery here OUTSIDE OF STUN and DEATH
    if not HC.player.shield_generator_available:
        HC.player.shield_generator_available, HC.player.shield_generator_timer = \
            HC.player.coolDown(HC.player.shield_generator_available, HC.player.shield_generator_timer, 100)

    if not HC.player.stunned and not HC.player.health <= 0:
        if not HC.player.playerAttacking and not HC.player.rolling:
            if keys[pygame.K_LEFT]:
                if HC.player.crouching:
                    HC.player.forwardFace = False
                else:
                    HC.player.move('L')


            if keys[pygame.K_RIGHT]:
                if HC.player.crouching:
                    HC.player.forwardFace = True
                else:
                    HC.player.move('R')

            if not HC.player.crouching:
                if keys[pygame.K_UP]:
                    HC.player.move('U')

                if keys[pygame.K_DOWN]:
                    HC.player.move('D')

        #Weapon Swapping Controls
        if event.type == pygame.KEYUP and not SI.shop.shop_screen:
            if event.key == pygame.K_1:
                HC.player.equip(HC.Rifle)
                    #HC.player.currentWeapon = HC.Rifle

        if event.type == pygame.KEYUP and not SI.shop.shop_screen:
            if event.key == pygame.K_2:
                if HC.player.shotgun_unlocked:
                    HC.player.equip(HC.Shotgun)

        if event.type == pygame.KEYUP and not SI.shop.shop_screen:
            if event.key == pygame.K_3:
                if HC.player.rocket_launcher_unlocked:
                    HC.player.equip(HC.Rocket_Launcher)

        #Shop Menu Controls
        if event.type == pygame.KEYUP and not SI.shop.shop_screen:
            if event.key == pygame.K_TAB:
                if not SI.shop.shop_screen:
                    SI.shop.shop_screen = True


        while SI.shop.shop_screen:
            #print(f'this is the shop_active: {SI.shop.shop_screen}')
            Interface_Main.main()

        #melee attack from player
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_b:
                if HC.player.melee_unlocked:
                    if HC.player.playerAttacking:
                        pass
                    else:
                        #shiftPlayerAttack()
                        #HC.player.getFaceDirection()
                        getAttackDirection(HC.player, HC.player.leftAttackList, HC.player.rightAttackList)
                        HC.player.playerAttacking = True
                        HC.player.resetIteration()
                        Sounds.melee_sound.play() # play melee sound
                        for target in Stages.stageHandler.currentStage.enemiesList:
                            if target.health > 0:
                                HC.player.melee(target)
                        for target in Stages.stageHandler.wanderers_list:
                            if target.health > 0:
                                HC.player.melee(target)

        #key to throw grenade
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                if HC.player.grenades_unlocked:
                    if HC.player.grenadeAmount > 0:
                        if HC.player.playerAttacking or HC.player.reloading:
                            pass

                        else:
                            print('registering grenade')
                            HC.player.shooting = False
                            HC.player.resetIteration()
                            HC.player.throw_grenade()

        #key up S for player shooting
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                if HC.player.playerAttacking:
                    pass

                else:
                   HC.player.resetIteration()
                   HC.player.throwing_grenade = False
                   HC.player.reloading = False
                   if HC.player.currentWeapon.name == 'Rocket Launcher':
                       HC.player.shoot(is_rocket=True)

                   else:
                       HC.player.shoot()

        #key up to reload
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_r:
                HC.player.shooting = False
                if HC.player.playerAttacking or HC.player.throwing_grenade:
                    pass
                else:
                    HC.player.resetIteration()
                    HC.player.reload()

    #key up X for text boxes
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_x:
                currentStage = Stages.stageHandler.getCurrentStage()
                textBoxCharacter = getCharacterSpeaking(currentStage)
                if textBoxCharacter.speechList != []:
                    textBoxCharacter.speechList[0].nextText()
                    #HC.Piles.speechList[0].nextText()



    #key up f for player heals from piles
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                HC.Piles.batteryHeal(HC.player)

                #accounting for Stage one textBox intro to healing with battery  only ran once
                if Stages.StageHandler.currentStage == Stages.stage_zero and HC.Piles.speechList[0] != []:
                    #print('changed to completed')
                    #textBoxCharacter.speechList[0].completed = True
                    HC.Piles.speechList[0].nextText()


        '''Crouching hotkey is 'c' and causes player to do more damage, but be less mobile'''
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                HC.player.resetIteration()
                if not HC.player.crouching:
                    HC.player.crouching = True
                else:
                    HC.player.crouching = False

        #rolling
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:

                if HC.player.roll_unlocked:
                    HC.player.resetIteration()
                    if HC.player.playerAttacking or HC.player.rolling:
                        pass
                    else:
                        Sounds.roll_sound.play()
                        HC.player.rolling = True


        #Activate shield generator
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                if HC.player.shield_generator_unlocked:
                    #check cooldown
                    if not HC.player.shield_generator_available:
                        pass

                        #use active
                    else:
                        Sounds.shield_sound.play()
                        HC.player.overshield = True
                        HC.player.overshieldAmount = HC.player.overshield_max_amount
                        HC.player.shield_generator_available = False # turns off the active ability and incurs its cd

    """
        if HC.player.reloading:
            getAttackDirection(HC.player, HC.player.reloadLeft, HC.player.reloadRight)
            HC.player.reloading = HC.player.animateMe(True, False)
        """



#illustrating the player attacks
    if HC.player.health <= 0:
        if HC.player.dead:
            HC.player.health = 0
            HC.death_screen.enabled = True
            win.blit(HC.player.img, (HC.player.currentX, HC.player.currentY))

        else:
            if not HC.player.death_reset:
                HC.player.resetIteration()
                HC.player.death_reset = True

            HC.player.health = 0
            HC.player.iterationList = Images.redEyesDead
            try:
                HC.player.dead = HC.player.animateMe(False, True)
            except IndexError:
                print('what?')




    elif HC.player.stunned:
        if not HC.player.stun_reset:
            HC.player.reset_for_stun()
        else:
            getAttackDirection(HC.player, Images.redEyesStunnedLeft, Images.redEyesStunned)
            #HC.player.iterationList = Images.redEyesStunned
            HC.player.animateMe()
            HC.player.stunned, HC.player.stun_timer = HC.player.coolDown(HC.player.stunned, HC.player.stun_timer,
                                                                         cooldown=HC.player.stun_cooldown)
            if not HC.player.stunned:
                HC.player.stun_reset = False
    else:

        if HC.player.playerAttacking:
            getAttackDirection(HC.player, HC.player.leftAttackList, HC.player.rightAttackList)
            HC.player.playerAttacking = HC.player.animateMe(True, False)  # When iterated through will return player attacking to False

        if HC.player.reloading:
            getAttackDirection(HC.player, HC.player.reloadLeft, HC.player.reloadRight)
            HC.player.reloading = HC.player.animateMe(conditionNotMet=True, conditionMet=False)
            #print(f'this is reloading condition: {HC.player.reloading}')
            #print(f'this is the counter: {HC.player.iterationCounter} this is the list length: {len(HC.player.iterationList)}\n should be False at 10')
            if not HC.player.reloading:
                HC.player.currentWeapon.reload()

        if HC.player.rocket_shooting:
            HC.player.crouching = False
            getAttackDirection(HC.player, Images.redEyesRocket_Launcher_Left, Images.redEyesRocket_Launcher_Right)
            HC.player.rocket_shooting = HC.player.animateMe(True, False)
            if HC.player.currentWeapon.clip <= 0:
                HC.player.rocket_shooting = False

        elif HC.player.shooting:
            if HC.player.crouching:
                getAttackDirection(HC.player, HC.player.crouchShootLeft, HC.player.crouchShootRight)
            else:
                getAttackDirection(HC.player, HC.player.shootLeft, HC.player.shootRight)
            HC.player.shooting = HC.player.animateMe(True, False)
            if HC.player.currentWeapon.clip <= 0:
                HC.player.shooting = False


        if HC.player.throwing_grenade:
            getAttackDirection(HC.player, HC.player.throwing_grenadeLeft, HC.player.throwing_grenadeRight)
            HC.player.throwing_grenade = HC.player.animateMe(True, False)
            if not HC.player.throwing_grenade:
                HC.player.grenadeAmount -= 1
                #IF SELF.STUN_GRENADE UNLOCKED APPEND THE STUN GRENADE HERE
                Stages.stageHandler.explosivesList.append(Explosives.Grenade(HC.player))

        if HC.player.rolling:
            getAttackDirection(HC.player, HC.player.rollLeft, HC.player.rollRight)
            if HC.player.forwardFace:
                HC.player.currentX += HC.player.roll_speed
            elif not HC.player.forwardFace:
                HC.player.currentX -= HC.player.roll_speed

            HC.player.rolling = HC.player.animateMe(True, False)
            HC.player.immune = True
            if not HC.player.rolling:
                HC.player.immune = False
                HC.player.resetIteration()
        else:
            HC.player.immune = False # so that mid rolls dont keep the player immune


#default to idle position
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not HC.player.playerAttacking\
                and not HC.player.shooting and not HC.player.rocket_shooting and not HC.player.throwing_grenade and not HC.player.reloading and not HC.player.rolling:        #taking out the movement key actives                                                                                                 #----- attacking animation
            HC.player.movementRight = False #updates right movement to help scrolling method

            if HC.player.forwardFace:
                if HC.player.crouching:
                    HC.player.idleList = HC.player.crouchRight
                else:
                    HC.player.idleList = HC.player.idleRightList
            else:
                if HC.player.crouching:
                    HC.player.idleList = HC.player.crouchLeft
                else:
                    HC.player.idleList = HC.player.idleLeftList

            HC.player.iterationList = HC.player.idleList
            HC.player.animateMe()
            #HC.player.img = Animator.animate(HC.player.iterationList, HC.player.iterationCounter)
            #HC.player.iterationCounter += 1

            #if HC.player.iterationCounter >= len(HC.player.iterationList):                            #idle animation
               # HC.player.iterationCounter = 0

# Exit Controls

    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        exit()








