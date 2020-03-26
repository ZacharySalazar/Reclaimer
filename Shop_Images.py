import pygame
import os

def load(image, directory, width = 125, height = 175):

    imageName = image + '.png'

    if directory != None:
        image = pygame.image.load(directory + imageName)
        image = pygame.transform.scale(image, (width, height))
    else:
        image = pygame.image.load(imageName)
    return image

def transform(givenImage, xSize, ySize):
    creatingImage = pygame.image.load(givenImage)
    creatingImage = pygame.transform.scale(creatingImage, (xSize, ySize))
    return creatingImage

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

class Shop():
    shop_screen = False
shop = Shop()

background = load('shop_background', 'images/shopImages/', 1400, 800)
shotgun_icon = load('shotgun_core', 'images/shopImages/Panels/un_selected/', 80, 80)
shotgun_selected_icon = load('shotgun_core', 'images/shopImages/Panels/selected/', 80, 80)


rocket_icon = load('rocket_launcher_core', 'images/shopImages/Panels/un_selected/', 80, 80)
rocket_selected_icon = load('rocket_launcher_core', 'images/shopImages/Panels/selected/', 80, 80)


roll_icon = load('roll_icon', 'images/shopImages/Panels/un_selected/', 80, 80)
roll_selected_icon = load('roll_icon', 'images/shopImages/Panels/selected/', 80, 80)

sprint_icon = load('sprint_icon', 'images/shopImages/Panels/un_selected/', 80, 80)
sprint_selected_icon = load('sprint_icon', 'images/shopImages/Panels/selected/', 80, 80)

melee_icon = load('melee_icon', 'images/shopImages/Panels/un_selected/', 80, 80)
melee_selected_icon = load('melee_icon', 'images/shopImages/Panels/selected/', 80, 80)

throw_grenade_icon = load('tg_icon', 'images/shopImages/Panels/un_selected/', 80, 80)
throw_grenade_selected_icon = load('tg_icon', 'images/shopImages/Panels/selected/', 80, 80)

shield_generator_icon = load('shield_generator_icon', 'images/shopImages/Panels/un_selected/', 80, 80)
shield_generator_selected_icon = load('shield_generator_icon', 'images/shopImages/Panels/selected/', 80, 80)

#upgrades
bullet_icon = load('bullet_upgrade', 'images/shopImages/Panels/un_selected/', 80, 80)
bullet_selected_icon = load('bullet_upgrade', 'images/shopImages/Panels/selected/', 80, 80)

explosion_icon = load('explosion_icon', 'images/shopImages/Panels/un_selected/', 80, 80)
explostion_selected_icon = load('explosion_icon', 'images/shopImages/Panels/selected/', 80, 80)

health_icon = load('health_icon', 'images/shopImages/Panels/un_selected/', 70, 70)
health_selected_icon = load('health_icon', 'images/shopImages/Panels/selected/', 70, 70)

battery_icon = load('battery_icon', 'images/shopImages/Panels/un_selected/', 70, 70)
battery_selected_icon = load('battery_icon', 'images/shopImages/Panels/selected/', 70, 70)

shield_upgrade_icon = load('shield_upgrade', 'images/shopImages/Panels/un_selected/', 70, 70)
shield_upgrade_selected_icon = load('shield_upgrade', 'images/shopImages/Panels/selected/', 70, 70)

mag_icon = load('mag_icon', 'images/shopImages/Panels/un_selected/', 80, 80)
mag_selected_icon = load('mag_icon', 'images/shopImages/Panels/selected/', 80, 80)


green_buy_button = load('green_buy_button', 'images/shopImages/Panels/', 160, 115)
red_buy_button = load('red_buy_button', 'images/shopImages/Panels/', 160, 115)
buy_button = load('buy_button', 'images/shopImages/Panels/', 160, 115)

purchased_image = load('purchased_image', 'images/shopImages/Panels/', 70, 30)

level_1 = load('level_1', 'images/shopImages/Panels/upgrade_levels/', 50, 50)
level_2 = load('level_2', 'images/shopImages/Panels/upgrade_levels/', 50, 50)
level_max = load('level_max', 'images/shopImages/Panels/upgrade_levels/', 50, 50)

redEyesKnockbackRight = createUnitAnimation('knockbackRight', 'playerImages/redEyes2', 8, xSize=150, ySize=200)
redEyesRollRight = createUnitAnimation('rollRight', 'playerImages/redEyes2', 8, xSize=150, ySize=200)
redEyesThrowGrenadeRight = createUnitAnimation('ThrowGrenadeRight', 'playerImages/redEyes2', 20, xSize=150, ySize=200)
redEyesRocketLauncherRight = createUnitAnimation('rocket_launcher_shoot_right', 'playerImages/redEyes2', 12, xSize=150, ySize=200)
redEyesShotgunShootRight = createUnitAnimation('shotgun_shoot_right', 'playerImages/redEyes2', 8, xSize=130, ySize=175)
redEyesIdleRight = createUnitAnimation('idleRight', 'playerImages/redEyes2', 12, xSize=150, ySize=200)
redEyesShieldActive = createUnitAnimation('shieldActive', 'playerImages/redEyes2', 8, xSize=125, ySize=175)
#load('redEyesIcon', 'images/unitImages/playerImages/redEyes2/', 60, 60)