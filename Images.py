import pygame
import os

'''Creates directory and uses directory to find and transforms the image found  to a given size'''
def getPath(directory, imgFile, resizeX, resizeY):
    path = pygame.image.load(os.path.join(directory, imgFile))
    path = pygame.transform.scale(path,(resizeX, resizeY))
    return path

'''Creates and animation List given the unit and action of said unit while putting resize into the getPath function'''
def createUnitAnimation(actionFolder, unitFolder, num_of_images, xSize, ySize):
    animationList = []
    for imageNumber in range(num_of_images):
        animationList.append(getPath('images/unitImages/' + unitFolder + '/' + actionFolder, str(imageNumber) + '.png', xSize, ySize))
    return animationList



def load(image, directory, width = 125, height = 175):

    imageName = image + '.png'

    if directory != None:
        image = pygame.image.load(directory + imageName)
        image = pygame.transform.scale(image, (width, height))
    else:
        image = pygame.image.load(imageName)
    return image


#Hero Player Characters
    #redEyes-----

redEyesIdleLeft = createUnitAnimation('idleLeft', 'playerImages/redEyes2', 12, xSize=150, ySize=200)
redEyesIdleRight = createUnitAnimation('idleRight', 'playerImages/redEyes2', 12, xSize=150, ySize=200)
redEyesWalkLeft = createUnitAnimation('walkLeft', 'playerImages/redEyes2', 16, xSize=150, ySize=200)
redEyesWalkRight = createUnitAnimation('walkRight', 'playerImages/redEyes2', 16, xSize=150, ySize=200)
redEyesCrouchIdleLeft = createUnitAnimation('crouchIdleLeft', 'playerImages/redEyes2', 10, xSize=150, ySize=200)
redEyesCrouchIdleRight = createUnitAnimation('crouchIdleRight', 'playerImages/redEyes2', 10, xSize=150, ySize=200)
redEyesCrouchShootLeft = createUnitAnimation('crouchShootLeft', 'playerImages/redEyes2', 7, xSize=150, ySize=200)
redEyesCrouchShootRight = createUnitAnimation('crouchShootRight', 'playerImages/redEyes2', 7, xSize=150, ySize=200)
redEyesShootLeft = createUnitAnimation('shootLeft', 'playerImages/redEyes2', 8, xSize=150, ySize=200)
redEyesShootRight = createUnitAnimation('shootRight', 'playerImages/redEyes2', 8, xSize=150, ySize=200)
redEyesReloadLeft = createUnitAnimation('reloadLeft', 'playerImages/redEyes2', 10, xSize=150, ySize=200)
redEyesReloadRight = createUnitAnimation('reloadRight', 'playerImages/redEyes2', 10, xSize=150, ySize=200)
redEyesKnockbackLeft = createUnitAnimation('knockbackLeft', 'playerImages/redEyes2', 8, xSize=150, ySize=200)
redEyesKnockbackRight = createUnitAnimation('knockbackRight', 'playerImages/redEyes2', 8, xSize=150, ySize=200)
redEyesRocket_Launcher_Left = createUnitAnimation('rocket_launcher_shoot_left', 'playerImages/redEyes2', 8, xSize=150, ySize=200)
redEyesRocket_Launcher_Right = createUnitAnimation('rocket_launcher_shoot_right', 'playerImages/redEyes2', 8, xSize=150, ySize=200)

redEyesRollLeft = createUnitAnimation('rollLeft', 'playerImages/redEyes2', 8, xSize=150, ySize=200)
redEyesRollRight = createUnitAnimation('rollRight', 'playerImages/redEyes2', 8, xSize=150, ySize=200)

redEyesHurtLeft = createUnitAnimation('hurtLeft', 'playerImages/redEyes2', 5, xSize=150, ySize=200)
redEyesHurtRight = createUnitAnimation('hurtRight', 'playerImages/redEyes2', 5, xSize=150, ySize=200)

redEyesStunned = createUnitAnimation('stunned', 'playerImages/redEyes2', 12, xSize=150, ySize=200)
redEyesStunnedLeft = createUnitAnimation('stunnedLeft', 'playerImages/redEyes2', 12, xSize=150, ySize=200)
redEyesDead = createUnitAnimation('dead', 'playerImages/redEyes2', 15, xSize = 125, ySize = 175)
redEyesIcon = load('redEyesIcon', 'images/unitImages/playerImages/redEyes2/', 60, 60)

redEyesThrowGrenadeLeft = createUnitAnimation('ThrowGrenadeLeft', 'playerImages/redEyes2', 20, xSize=150, ySize=200)
redEyesThrowGrenadeRight = createUnitAnimation('ThrowGrenadeRight', 'playerImages/redEyes2', 20, xSize=150, ySize=200)
#ammunition
    #standard
standardBullet = createUnitAnimation('standardBullet', 'playerImages/bulletsAndflashes/bullets', 10, xSize = 8, ySize = 8)
shotgun_range_indicator = load('shotgunRangeIndicator', 'images/unitImages/playerImages/bulletsAndflashes/shotgun_range_indicator/', 15, 15)

rocket_fly = createUnitAnimation('rockets', 'playerImages/bulletsAndflashes/bullets', 2, 20, 20)

    #muzzle Flashes for shotgun
Shotgun_blast = createUnitAnimation('shotgun_flash', 'weapons/', 6, 125, 95)
Shotgun_blast_right = createUnitAnimation('shotgun_flash_right', 'weapons/', 6, 125, 95)


#standardRifleFlashRight = createUnitAnimation('standardRifleFlash', 'playerImages/bulletsAndflashes/muzzleFlashes/', 2, xSize = 90, ySize = 90)
#standardRifleFlash = createUnitAnimation('standardRifleFlash', 'playerImages/bullets and flashes/muzzleFlash', 1, xSize = 20, ySize = 20)
#attackLists DeathKnight
"""
deathKnightStabLeftList = createUnitAnimation('deathKnightStabLeftList', 'DeathKnightImages', 24, xSize = 125, ySize = 175)
deathKnightStabRightList = createUnitAnimation('deathKnightStabRightList', 'DeathKnightImages', 24, xSize = 125, ySize = 175)

deathKnightAttack2LeftList = createUnitAnimation('dkAttack2Left', 'DeathKnightImages', 24 , xSize = 125, ySize = 175)
deathKnightAttack2RightList = createUnitAnimation('dkAttack2Right', 'DeathKnightImages', 24, xSize = 125, ySize = 175)

#EnemyImages
"""
#Ghost Images
    #Ghost rise

    #Ghost die
deadPGList = createUnitAnimation('deadPG', 'enemyImages/ghosts', 7, xSize = 60, ySize = 80)

    #Ghost attack Hand Image List
pGhostAttackLeft = createUnitAnimation('attackLeft', 'enemyImages/ghosts/purpleGhost', 10, 60, 80)
pGhostAttackRight = createUnitAnimation('attackRight', 'enemyImages/ghosts/purpleGhost', 10, 60, 80)
pGhostIdleLeft = createUnitAnimation('idleLeft', 'enemyImages/ghosts/purpleGhost', 20, 60, 80)
pGhostIdleRight = createUnitAnimation('idleRight', 'enemyImages/ghosts/purpleGhost', 20, 60, 80)
pGhostHurtLeft = createUnitAnimation('hurtLeft', 'enemyImages/ghosts/purpleGhost', 7, 60, 80)
pGhostHurtRight = createUnitAnimation('hurtRight', 'enemyImages/ghosts/purpleGhost', 7, 60, 80)
pGhostHauntLeft = createUnitAnimation('hauntLeft', 'enemyImages/ghosts/purpleGhost', 28, 60, 80)
pGhostHauntRight = createUnitAnimation('hauntRight', 'enemyImages/ghosts/purpleGhost', 28, 60, 80)

#Casters

grave_keeper_teleport_in = createUnitAnimation('teleport_in', 'enemyImages/skeletons/grave_keeper', 8, 80, 90)
grave_keeper_idle = createUnitAnimation('idle', 'enemyImages/skeletons/grave_keeper', 12, 105, 125)
grave_keeper_summon = createUnitAnimation('summon_right', 'enemyImages/skeletons/grave_keeper', 24, 105, 125)
grave_keeper_death = createUnitAnimation('death', 'enemyImages/skeletons/grave_keeper', 16, 105, 125)

#SkeletonRedMage

# SkeletonRedMageWalkLeft = createUnitAnimation('WalkLeft', 'enemyImages/SkeletonRedMage', 24, 85, 105)
# SkeletonRedMageWalkRight = createUnitAnimation('WalkRight', 'enemyImages/SkeletonRedMage', 24, 85, 105)
# SkeletonRedMageIdleLeft = createUnitAnimation('IdleLeft', 'enemyImages/SkeletonRedMage', 24, 85, 105)
# SkeletonRedMageIdleRight = createUnitAnimation('IdleRight', 'enemyImages/SkeletonRedMage', 24, 85, 105)
# SkeletonRedMageHitLeft = createUnitAnimation('IdleLeft', 'enemyImages/SkeletonRedMage', 12, 85, 105)
# SkeletonRedMageHitRight = createUnitAnimation('IdleRight', 'enemyImages/SkeletonRedMage', 12, 85, 105)
# SkeletonRedMageSummonCastLeft = createUnitAnimation('cast03Left', 'enemyImages/SkeletonRedMage', 48, 85, 105)
# SkeletonRedMageSummonCastRight = createUnitAnimation('cast03Right', 'enemyImages/SkeletonRedMage', 48, 85, 105)
# SkeletonRedMageShadowCastLeft = createUnitAnimation('cast02Left', 'enemyImages/SkeletonRedMage', 30, 85, 105)
# SkeletonRedMageShadowCastRight = createUnitAnimation('cast02Right', 'enemyImages/SkeletonRedMage', 30, 85, 105)
# SkeletonRedMageDeath = createUnitAnimation('DieLeft', 'enemyImages/SkeletonRedMage', 24, 85, 105)
# SkeletonRedMageIcon = load('SkeletonRedMageIcon', 'images/unitImages/enemyImages/SkeletonRedMage/', 60, 60)

#skeletons
    #canyonSkele

"""
    #barbarian
barbarianIdleLeft = createUnitAnimation('idleLeft', 'enemyImages/skeletons/barbarian', 12, 190, 200)
barbarianIdleRight = createUnitAnimation('idleRight', 'enemyImages/skeletons/barbarian', 12, 190, 200)
barbarianWalkLeft = createUnitAnimation('walkLeft', 'enemyImages/skeletons/barbarian', 16, 190, 200)
barbarianWalkRight = createUnitAnimation('walkRight', 'enemyImages/skeletons/barbarian', 16, 190, 200)
barbarianAttackLeft = createUnitAnimation('attackLeft', 'enemyImages/skeletons/barbarian', 12, 190, 200)
barbarianAttackRight = createUnitAnimation('attackRight', 'enemyImages/skeletons/barbarian', 12, 190, 200)
barbarianHurtLeft = createUnitAnimation('hurtLeft', 'enemyImages/skeletons/barbarian', 24, 190, 200)
barbarianHurtRight = createUnitAnimation('hurtRight', 'enemyImages/skeletons/barbarian', 24, 190, 200)
barbarianDeath = createUnitAnimation('death', 'enemyImages/skeletons/barbarian', 28, 190, 200)
"""

    #marksman
"""
mmIdleLeft = createUnitAnimation('idleLeft', 'enemyImages/skeletons/marksman', 12, 120, 150)
mmIdleRight = createUnitAnimation('idleRight', 'enemyImages/skeletons/marksman', 12, 120, 150)
mmWalkLeft = createUnitAnimation('walkLeft', 'enemyImages/skeletons/marksman', 16, 120, 150)
mmWalkRight = createUnitAnimation('walkRight', 'enemyImages/skeletons/marksman', 16, 120, 150)
mmAttackLeft = createUnitAnimation('attackLeft', 'enemyImages/skeletons/marksman', 18, 120, 150)
mmAttackRight = createUnitAnimation('attackRight', 'enemyImages/skeletons/marksman', 18, 120, 150)
mmHurtLeft = createUnitAnimation('hurtLeft', 'enemyImages/skeletons/marksman', 12, 120, 150)
mmHurtRight = createUnitAnimation('hurtRight', 'enemyImages/skeletons/marksman', 12, 120, 150)
mmDeath = createUnitAnimation('death', 'enemyImages/skeletons/marksman', 24, 120, 150)
"""


fadeWalkerIdleLeft = createUnitAnimation('idleLeft', 'enemyImages/skeletons/fadeWalker', 12, 150, 165)
fadeWalkerIdleRight = createUnitAnimation('idleRight', 'enemyImages/skeletons/fadeWalker', 12, 150, 165)
fadeWalkerWalkLeft = createUnitAnimation('walkLeft', 'enemyImages/skeletons/fadeWalker', 8, 150, 165)
fadeWalkerWalkRight = createUnitAnimation('walkRight', 'enemyImages/skeletons/fadeWalker', 8, 150, 165)
fadeWalkerAttackLeft = createUnitAnimation('attackLeft', 'enemyImages/skeletons/fadeWalker', 18, 150, 165)
fadeWalkerAttackRight = createUnitAnimation('attackRight', 'enemyImages/skeletons/fadeWalker', 18, 150, 165)
fadeWalkerStealthLeft = createUnitAnimation('stealthLeft', 'enemyImages/skeletons/fadeWalker', 8, 150, 165)
fadeWalkerStealthRight = createUnitAnimation('stealthRight', 'enemyImages/skeletons/fadeWalker', 8, 150, 165)
fadeWalkerDeath = createUnitAnimation('death', 'enemyImages/skeletons/fadeWalker', 10, 150, 165)
fadeWalkerTeleportIn = createUnitAnimation('teleport_in', 'enemyImages/skeletons/fadeWalker', 6, 75, 90)

#     #Leaper Skeletons
leaperIdleLeft = createUnitAnimation('idleLeft', 'enemyImages/skeletons/leaper', 20, 130, 155)
leaperIdleRight = createUnitAnimation('idleRight', 'enemyImages/skeletons/leaper', 20, 130, 155)
leaperWalkLeft = createUnitAnimation('walkLeft', 'enemyImages/skeletons/leaper', 16, 130, 155)
leaperWalkRight = createUnitAnimation('walkRight', 'enemyImages/skeletons/leaper', 16, 130, 155)
leaperAttackLeft = createUnitAnimation('attackLeft', 'enemyImages/skeletons/leaper', 10, 130, 155)
leaperAttackRight = createUnitAnimation('attackRight', 'enemyImages/skeletons/leaper', 10, 130, 155)
leaperHurtLeft = createUnitAnimation('hurtLeft', 'enemyImages/skeletons/leaper', 4, 130, 155)
leaperHurtRight = createUnitAnimation('hurtRight', 'enemyImages/skeletons/leaper', 4, 130, 155)
leaperJumpLeft = createUnitAnimation('jumpLeft', 'enemyImages/skeletons/leaper', 7, 130, 155)
leaperJumpRight = createUnitAnimation('jumpRight', 'enemyImages/skeletons/leaper', 7, 130, 155)
leaperDeath = createUnitAnimation('die', 'enemyImages/skeletons/leaper', 12, 130, 155)

#       #captain skeletons
# captainSkeleIdleLeft = createUnitAnimation('captainSkeleIdleLeft', 'enemyImages/skeletons/captainSkele', 20, 130, 160)
# captainSkeleIdleRight = createUnitAnimation('captainSkeleIdleRight', 'enemyImages/skeletons/captainSkele', 20, 130, 160)
# captainSkeleWalkLeft = createUnitAnimation('captainSkeleWalkLeft', 'enemyImages/skeletons/captainSkele', 16, 130, 160)
# captainSkeleWalkRight = createUnitAnimation('captainSkeleWalkRight', 'enemyImages/skeletons/captainSkele', 16, 130, 160)
# captainSkeleAttackLeft = createUnitAnimation('captainSkeleAttackLeft', 'enemyImages/skeletons/captainSkele', 10, 130, 160)
# captainSkeleAttackRight = createUnitAnimation('captainSkeleAttackRight', 'enemyImages/skeletons/captainSkele', 10, 130, 160)
# captainSkeleHurtLeft = createUnitAnimation('captainSkeleHurtLeft', 'enemyImages/skeletons/captainSkele', 24, 130, 160)
# captainSkeleHurtRight = createUnitAnimation('captainSkeleHurtRight', 'enemyImages/skeletons/captainSkele', 24, 130, 160)
# captainSkeleRallyLeft = createUnitAnimation('captainSkeleRallyLeft', 'enemyImages/skeletons/captainSkele', 16, 130, 160)
# captainSkeleRallyRight = createUnitAnimation('captainSkeleRallyRight', 'enemyImages/skeletons/captainSkele', 16, 130, 160)
# captainSkeleDie = createUnitAnimation('captainSkeleDie', 'enemyImages/skeletons/captainSkele', 32, 130, 160)
#
# # #
# # #
# # #       #regular skeletons
# regSkeleIdleLeft = createUnitAnimation('idleLeft', 'enemyImages/skeletons/regSkele', 20, 110, 150) #120 165 was org sizes
# regSkeleIdleRight = createUnitAnimation('idleRight', 'enemyImages/skeletons/regSkele', 20, 110, 150)
# regSkeleWalkLeft = createUnitAnimation('walkLeft', 'enemyImages/skeletons/regSkele', 16, 110, 150)
# regSkeleWalkRight = createUnitAnimation('walkRight', 'enemyImages/skeletons/regSkele', 16, 110, 150)
# regSkeleAttackLeft = createUnitAnimation('attackLeft', 'enemyImages/skeletons/regSkele', 10, 110, 150)
# regSkeleAttackRight = createUnitAnimation('attackRight', 'enemyImages/skeletons/regSkele', 10, 110, 150)
# regSkele_rs_Left = createUnitAnimation('rsLeft', 'enemyImages/skeletons/regSkele', 16, 110, 150)  #rs is raiseShield
# regSkele_rs_Right = createUnitAnimation('rsRight', 'enemyImages/skeletons/regSkele', 16, 110, 150)
# regSkeleHurtLeft = createUnitAnimation('hurtLeft', 'enemyImages/skeletons/regSkele', 16, 110, 150)
# regSkeleHurtRight =  createUnitAnimation('hurtRight', 'enemyImages/skeletons/regSkele', 16, 110, 150)
# regSkeleDeath = createUnitAnimation('death', 'enemyImages/skeletons/regSkele', 23, 110, 150)
# regSkeleRise = createUnitAnimation('regSkeleRise', 'enemyImages/skeletons/regSkele', 20, 110, 150)



#Spell Images
plagueBoltLeft = createUnitAnimation('flyLeft', 'spellImages/plagueBolt', 31, 90, 70)
plagueBoltRight = createUnitAnimation('flyRight', 'spellImages/plagueBolt', 31, 90, 70)
# fireBallLeft = createUnitAnimation('flyLeft', 'spellImages/fireBall', 31, 80, 60)
# fireBallRight = createUnitAnimation('flyRight', 'spellImages/fireBall', 31, 80, 60)
#
# arrowLeft = createUnitAnimation('flyLeft', 'spellImages/arrow', 2, 40, 50)
# arrowRight = createUnitAnimation('flyRight', 'spellImages/arrow', 2, 20, 50)

#Piles
#risePGList = createUnitAnimation('risePG', 'enemyImages/ghosts', 16, xSize = 195, ySize = 245)    for example here
idleRightPiles = createUnitAnimation('IdlePiles', 'PilesImages', 50, xSize = 70, ySize = 120)
walkRightPiles = createUnitAnimation('WalkPiles', 'PilesImages', 36, xSize = 70, ySize = 120)
castHealPiles = createUnitAnimation('castHealPiles', 'PilesImages', 14, xSize = 190, ySize = 120)

#Icons ---------
    #enemy Icons
captainSkeleIcon = load('captainSkeleIcon', 'images/icons/enemyIcons/', 60, 60)
regularSkeletonIcon = load('regularSkeletonIcon', 'images/icons/enemyIcons/', 60, 60)
ghostIcon = load('ghostIconImg', 'images/icons/enemyIcons/', 60, 60)

#backgrounds
backGround1 = load('backGround1', 'images/backgrounds/', 1400, 800)
death_screen = load('death_screen_black', 'images/backgrounds/', 1400, 800)
reclaimer_down = load('reclaimer_down', 'images/backgrounds/', 350, 80)
c_b = pygame.image.load('images/backgrounds/c_b.jpg')
c_b = pygame.transform.scale(c_b, (1410, 800))

whiteBackground = load('whiteBackground', 'images/backgrounds/', 1410, 800)
forest1 = load('forest1', 'images/backgrounds/', 1410, 800)
forest2 = load('forest2', 'images/backgrounds/', 1410, 800)
forest_boss_background = load('forest_boss_stage', 'images/backgrounds/', 1410, 800)

cave_background = load('cave_background', 'images/backgrounds/', 1410, 800)
cave_boss_background = load('tester2', 'images/backgrounds/', 1410, 800)
cave_boss_foreground = load('boss_2_foreground', 'images/backgrounds/', 1410, 300)


#background characters
batFlyLeft = createUnitAnimation('flyLeft', 'background_characters/Bat', 8, xSize = 30, ySize = 30)
batFlyRight = createUnitAnimation('flyRight', 'background_characters/Bat', 8, xSize = 30, ySize = 30)
ghostAppear = createUnitAnimation('ghostAppear', 'background_characters/decals', 3, xSize = 40, ySize = 40)

camp_fire = createUnitAnimation('camp_fire', 'background_characters/decals', 8, xSize=70, ySize=90)

#Effect Images
damageBuff = createUnitAnimation('damageBuff', 'effects', 25, xSize=40, ySize=40)
damageBuffOrg = createUnitAnimation('damageBuffOrg', 'effects', 20, xSize = 40, ySize = 40)
purpFlame = createUnitAnimation('purpFlame', 'effects', 20, xSize = 40, ySize = 40)

#TextBox Images
textBoxImg = load('textBoxImg', 'images/textImages/', 400, 200)
pressXImg = load('pressXImg', 'images/textImages/', 110, 70)


#Interface Images
batteryPower0 = load('batteryPower0', 'images/interfaceImages/', 60, 45)
batteryPower1 = load('batteryPower1', 'images/interfaceImages/', 40, 50)
batteryPower2 = load('batteryPower2', 'images/interfaceImages/', 50, 50)
batteryPower3 = load('batteryPower3', 'images/interfaceImages/', 50, 50)

reloadBox = load('reloadBox', 'images/interfaceImages/', 30, 25)

rifle_unselected = load('rifle_unselected_img', 'images/interfaceImages/', 80, 55)
rifle_selected = load('rifle_selected_img', 'images/interfaceImages/', 80, 55)
shotgun_unselected = load('shotgun_unselected_img', 'images/interfaceImages/', 80, 55)
shotgun_selected = load('shotgun_selected_img', 'images/interfaceImages/', 80, 55)
rocket_launcher_unselected = load('rocket_launcher_unselected_img', 'images/interfaceImages/', 80, 55)
rocket_launcher_selected = load('rocket_launcher_selected_img', 'images/interfaceImages/', 80, 55)

shield_available = load('shield_available', 'images/interfaceImages/', 60, 50)
shield_unavailable = load('shield_unavailable', 'images/interfaceImages/', 60, 50)

#Consumable Images
battery = load('battery', 'images/consumables/', 40, 40)
overshieldImg = load('overshieldImg', 'images/consumables/', 40, 40)
grenadeImg = load('grenadeImg', 'images/consumables/', 30, 30)

#Currency Images
greenGem = createUnitAnimation('greenGem', 'currency', 4, 15, 25)
blueGem = createUnitAnimation('blueGem', 'currency', 4, 15, 25)
redGem = createUnitAnimation('redGem', 'currency', 4, 15, 25)
yellowGem = createUnitAnimation('yellowGem', 'currency', 4, 15, 25)

collect = createUnitAnimation('collect', 'effects', 20, 30, 30)
normalChest = createUnitAnimation('normalChest', 'currency/chests', 3, 90, 90)
chestExplosion = createUnitAnimation('chestExplosion', 'currency/chests', 20, 100, 100)
rocket_Explosion = createUnitAnimation('chestExplosion', 'currency/chests', 20, 150, 150)

parachute = load('parachute', 'images/unitImages/currency/chests/', 130, 130)
#Weapons Images
grenadeExplode = createUnitAnimation('grenadeExplode', 'weapons', 7, 350, 300)
grenadeRotate = createUnitAnimation('grenadeRotate', 'weapons', 5, 30, 30)

stunGrenadeExplode = createUnitAnimation('stunGrenadeExplode', 'weapons', 7, 350, 350)
stunGrenadeRotate = createUnitAnimation('stunGrenadeRotate', 'weapons', 5, 30, 30)

circleImg = load('circle', 'images/unitImages/', 40, 40)

#Bosses
    #HOLLOW BOSS

# hollowIdle = createUnitAnimation('idle', 'enemyImages/bosses/hollow', 4, 400, 400)
# hollowSlam  = createUnitAnimation('slamming', 'enemyImages/bosses/hollow', 2, 400, 400)
# hollowHeadlessIdle = createUnitAnimation('idle_headless', 'enemyImages/bosses/hollow', 4, 400, 400)
# hollowHeadlessSlamm = createUnitAnimation('slamming_headless', 'enemyImages/bosses/hollow', 2, 400, 400)
#
# hollowHeadWalkLeft = createUnitAnimation('walkLeft', 'enemyImages/bosses/hollow/hollow_head', 4, 150, 150)
# hollowHeadWalkRight = createUnitAnimation('walkRight', 'enemyImages/bosses/hollow/hollow_head', 4, 150, 150)
#
# hollowHeadCrashedLeft = createUnitAnimation('idleLeft', 'enemyImages/bosses/hollow/crashed_head', 2, 210, 210)
# hollowHeadCrashedRight = createUnitAnimation('idleRight', 'enemyImages/bosses/hollow/crashed_head', 2, 210, 210)
#
# hollowHeadDamagedLeft = createUnitAnimation('damagedLeft', 'enemyImages/bosses/hollow/crashed_head', 2, 210, 210)
# hollowHeadDamagedRight = createUnitAnimation('damagedRight', 'enemyImages/bosses/hollow/crashed_head', 2, 210, 210)
#
# hollowHeadWalkingDamagedLeft = createUnitAnimation('damagedLeft', 'enemyImages/bosses/hollow/hollow_head', 2, 150, 150)
# hollowHeadWalkingDamagedRight = createUnitAnimation('damagedRight', 'enemyImages/bosses/hollow/hollow_head', 2, 150, 150)
#
# hollowDeath = createUnitAnimation('hollow_death', 'enemyImages/bosses/hollow', 7, 350, 350)
#
# hollowHeart = createUnitAnimation('heart', 'enemyImages/bosses/hollow/', 3, 70, 70)
# hollowHeartSplatter = createUnitAnimation('heart_splatter', 'enemyImages/bosses/hollow/', 3, 115, 115)
#
# hollowName = load('hollowName', 'images/unitImages/enemyImages/bosses/hollow/', 200, 35)
# hollowIcon = load('hollowIcon', 'images/unitImages/enemyImages/bosses/hollow/', 70, 70)
#
#
# hollow_summon_decay = createUnitAnimation('summon_decay', 'enemyImages/bosses/hollow', 3, 400, 400)
# skele_hand_hatch = createUnitAnimation('skele_hand_hatch', 'enemyImages/bosses/hollow/skele_hand', 3, 220, 220)
# skele_hand_rise = createUnitAnimation('skele_hand_rise', 'enemyImages/bosses/hollow/skele_hand', 7, 220, 220)
# skele_hand_wave = createUnitAnimation('skele_hand_wave', 'enemyImages/bosses/hollow/skele_hand', 16, 220, 220)
# skele_hand_fall = createUnitAnimation('skele_hand_fall', 'enemyImages/bosses/hollow/skele_hand', 8, 220, 220)

    #WHO BOSS

# whoIdleLeft = createUnitAnimation('idleLeft', 'enemyImages/bosses/who', 12, 225, 255)
# whoIdleRight = createUnitAnimation('idleRight', 'enemyImages/bosses/who', 12, 225, 255)
# whoWalkLeft = createUnitAnimation('walkLeft', 'enemyImages/bosses/who', 10, 225, 255)
# whoWalkRight = createUnitAnimation('walkRight', 'enemyImages/bosses/who', 10, 225, 255)
# whoAttackLeft = createUnitAnimation('attackLeft', 'enemyImages/bosses/who', 10, 225, 255)
# whoAttackRight = createUnitAnimation('attackRight', 'enemyImages/bosses/who', 10, 225, 255)
# whoHurtLeft = createUnitAnimation('hurtLeft', 'enemyImages/bosses/who', 8, 225, 255)
# whoHurtRight = createUnitAnimation('hurtRight', 'enemyImages/bosses/who', 8, 225, 255)
#
#
# whoDeath = createUnitAnimation('death', 'enemyImages/bosses/who', 12, 225, 255)
# whoOrbImages = createUnitAnimation('orbImages', 'enemyImages/bosses/who', 6, 60, 60)
# whoOrbFlameImages = createUnitAnimation('orbFlameImages', 'enemyImages/bosses/who', 7, 60, 70)
# whoVortexImages = createUnitAnimation('whoVortexImages', 'enemyImages/bosses/who', 6, 110, 110)
# whoVortexFlameImages = createUnitAnimation('vortexFlameImages', 'enemyImages/bosses/who', 7, 60, 60)
#
# greyPortal = createUnitAnimation('greyPortal', 'enemyImages/bosses/who/portals', 4, 90, 90)
# greenPortal = createUnitAnimation('greenPortal', 'enemyImages/bosses/who/portals', 4, 90, 90)
# redPortal = createUnitAnimation('redPortal', 'enemyImages/bosses/who/portals', 4, 90, 90)
#
# #upCurrent = createUnitAnimation('upCurrent', 'enemyImages/bosses/who', 4, 90, 90)
# #downCurrent = createUnitAnimation('downCurrent', 'enemyImages/bosses/who', 4, 90, 90)
#
# marium = createUnitAnimation('Marium', 'enemyImages/bosses/who', 3, 120, 120)
# MariumShield = load('MariumShield', 'images/unitImages/enemyImages/bosses/who/', 140, 140)
# MariumShieldBreaking = load('mariumShieldBreaking', 'images/unitImages/enemyImages/bosses/who/', 140, 140)
# mariumImmuneShield = load('mariumImmuneShield', 'images/unitImages/enemyImages/bosses/who/', 140, 140)
# mariumIcon = load('mariumIcon', 'images/unitImages/enemyImages/bosses/who/', 50, 50)
# mariumName = load('mariumName', 'images/unitImages/enemyImages/bosses/who/', 75, 40)
# boss_template = load('bossTemplate', 'images/unitImages/enemyImages/bosses/who/', 650, 80)
# whoName = load('whoName', 'images/unitImages/enemyImages/bosses/who/', 200, 35)
# whoIcon = load('whoIcon', 'images/unitImages/enemyImages/bosses/who/', 50, 50)
