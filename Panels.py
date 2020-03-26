import pygame
import HeroClassCode as HC
import Shop_Images as SI
import Explosives as E
pygame.init()




win = pygame.display.set_mode((1400, 900))
interfaceText = pygame.font.SysFont('yugothicregularyugothicuisemilight', 32)
informationText = pygame.font.SysFont('yugothicregularyugothicuisemilight', 16)

def coolDown(action, timer, cooldown):
    timer += 1
    if timer > cooldown:
        action = not action
        timer = 0


    else:
        action = action
    return action, timer

class Cart:
    runningTotal = 0
    cart_list = []

    def update_running_total(self):
        if self.cart_list != []:
            if self.cart_list[0].tag == 'Morpher':
                self.runningTotal = self.cart_list[0].current_cost
            elif self.cart_list[0].tag == 'Panel':
                self.runningTotal = self.cart_list[0].cost

    def add_item(self, item):
        self.cart_list.append(item)


    def remove_item(self, item):
        self.cart_list.remove(item)


shopping_cart = Cart()


class Weapons:
    clipSize = 0
    damage = 0

shotgun = Weapons()
m4 = Weapons()

class Player:
    maxHealth = 100
    healing = 0
    shields = 0

    shotgun_unlocked = False
    bullet_damage = 0
    explosive_damage = 0
    gems = 1000

player = Player()

class Button():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

        self.x_width = range(self.x, self.x + self.img.get_width())
        self.y_height = range(self.y, self.y + self.img.get_height())

class Buy_Button(Button):
    def __init__(self, x, y, img):
        Button.__init__(self, x, y, img)

    """Calculates player gems subtractions/ runs Panel unlock functions/
    removes the panels from the cart and resets the cart runningTotal to 0"""
    def purchase_cart(self):
        for panels in shopping_cart.cart_list:
            panels.purchase()

            #only removes panel if it isnt a morpher(upgradable) item
            if panels.tag == 'Panel':
                shopping_cart.remove_item(panels)

        shopping_cart.runningTotal = 0

buy_button = Buy_Button(x=731, y=305, img=SI.buy_button)

"""Contains unlocks for player at a cost and self maintains selection visuals 
and availability"""
class Panel(Button):
    selected = False  # determines if the player has the panel selected or not
    bought = False  # determines the the player has already bought the item or not
    animated = False # determines if the preview screen will animate an img for the panel or not
    iterationList = []
    iterationCounter = 0
    iteration_img = None

    animation_ready = True
    animation_timer = 0

    tag = 'Panel'

    def __init__(self, x, y, cost, img, selectedImg, unselectedImg):
        Button.__init__(self, x, y, img)
        self.cost = cost  # price of gems to buy
        self.selectedImg = selectedImg
        self.unselectedImg = unselectedImg

    def animateMe(self):
        if self.animation_ready:
            self.iteration_img = self.iterationList[self.iterationCounter]
            self.iterationCounter += 1

            if self.iterationCounter >= len(self.iterationList):
                self.animation_ready = False
                self.iterationCounter = 0


        elif not self.animation_ready:
            self.iteration_img = self.iterationList[0]
            self.animation_ready, self.animation_timer = coolDown(self.animation_ready, self.animation_timer, 30)


    """Turns the panel item to bought/ subtracts the cost from player gems/
    sets the image to unavailable img"""
    def confirm_purchase(self):
        self.bought = True
        HC.player.gems -= self.cost
        #draw 'bought' over img

"""A panel that is upgradable and may be bought multiple times
(Uses 'confirm_morpher_purchase' instead of panel's class: confirm purchase(in Panels class)'
dealing with upgradable variables)"""
class Morpher(Panel):
    current_upgrade_display = 0
    current_upgrade_level = 0


    def __init__(self, cost2, cost3, x, y, cost, img, selectedImg, unselectedImg):
        Panel.__init__(self, x, y, cost, img, selectedImg, unselectedImg)

        self.current_cost = cost
        self.cost2 = cost2 #cost for 2nd upgrade level
        self.cost3 = cost3 #cost for 3rd upgrade level

        self.current_upgrade_display_location = (self.x, self.y - 25)
        self.tag = 'Morpher' #creates a unique id upon initialization when iterating through panels

        #notes  create a function to draw the current_upgrade_level on or next to the icons so they know the level
        #so long as the level is above 0

    """Runs in Interface_Controls for all morphers that
    are maxed out"""
    def update_max_reached(self):
        self.information_text = 'Max upgrade reached!'
        self.information_text2 = ''
        self.img = self.unselectedImg

    """Draws and displays the current upgrade level of the Morpher.
    constantly updated in (Interface Controls)"""
    def display_upgrade_level(self):
        if self.current_upgrade_level == 1:
            win.blit(SI.level_1, self.current_upgrade_display_location)

        elif self.current_upgrade_level == 2:
            win.blit(SI.level_2, self.current_upgrade_display_location)

        elif self.current_upgrade_level == 3:
            win.blit(SI.level_max, self.current_upgrade_display_location)

    def progress_cost(self):
        if self.current_cost == self.cost:
            self.current_cost = self.cost2

        elif self.current_cost == self.cost2:
            self.current_cost = self.cost3

    def progress_morpher(self, maxed=False):

        HC.player.gems -= self.current_cost
        self.current_upgrade_level += 1
        self.current_upgrade_display = 1
        self.progress_cost()

        #self.img = self.unselectedImg
        #self.selected = False

        if maxed:
            self.bought = True
    """When purchased upgrades to next tier. Used by all Morphers on purchase.
    (Also upgrades the cost)"""
    def confirm_morpher_purchase(self):

        if self.current_upgrade_level == 0:
            self.progress_morpher()

        elif self.current_upgrade_level == 1:
            self.progress_morpher()

        elif self.current_upgrade_level == 2:
            self.progress_morpher(maxed=True)



class Magazine_Capacity(Morpher):
    information_text = 'Increases magazine clip size of weapons.'
    information_text2 = '(Rifle clip +2, shotgun clip +1)'

    def __init__(self, cost, cost2, cost3, x=1215, y=355, img=SI.mag_icon,
                 selectedImg=SI.mag_selected_icon, unselectedImg=SI.mag_icon):
        Morpher.__init__(self, cost2, cost3, x, y, cost, img, selectedImg, unselectedImg)

    def purchase(self):
        if self.current_upgrade_level == 0:
            HC.Rifle.clipSize += 2
            HC.Shotgun.clipSize += 1
            #self.information_text = 'Increases All bullet damage by 10%'

        elif self.current_upgrade_level == 1:
            HC.Rifle.clipSize += 2
            HC.Shotgun.clipSize += 1

        elif self.current_upgrade_level == 2:
            HC.Rifle.clipSize += 2
            HC.Shotgun.clipSize += 1

        self.confirm_morpher_purchase()


magazine_capacity_Morpher = Magazine_Capacity(cost=50, cost2=75, cost3=100)

class Explosive_Damage(Morpher):
    information_text = 'Increases All explosive damage'
    information_text2 = '(Grenades and Rocket Launcher deal (50 Damage)'

    def __init__(self, cost, cost2, cost3, x=1215, y=255, img=SI.explosion_icon,
                 selectedImg=SI.explostion_selected_icon, unselectedImg=SI.explosion_icon):
        Morpher.__init__(self, cost2, cost3, x, y, cost, img, selectedImg, unselectedImg)

    def purchase(self):
        if self.current_upgrade_level == 0:
            E.Grenade.damage = 50
            HC.Rocket_Launcher.damage = 50
            self.information_text2 = '(Grenades and Rocket Launcher deal (60 Damage)'

        elif self.current_upgrade_level == 1:
            E.Grenade.damage = 60
            HC.Rocket_Launcher.damage = 60
            self.information_text2 = '(Grenades and Rocket Launcher deal (80 Damage)'

        elif self.current_upgrade_level == 2:
            E.Grenade.damage = 80
            HC.Rocket_Launcher.damage = 80
            self.information_text2 = '(Grenades and Rocket Launcher deal (80 Damage)'

        self.confirm_morpher_purchase()

explosive_damage_Morpher = Explosive_Damage(cost=100, cost2=125, cost3=150)

class Bullet_Damage(Morpher):
    information_text = 'Increases Rifle and Shotgun damage'
    information_text2 = '(Rifle: (7 Damage) Shotgun (15 Damage).'

    def __init__(self, cost, cost2, cost3, x=1200, y=150, img=SI.bullet_icon,
                 selectedImg=SI.bullet_selected_icon, unselectedImg=SI.bullet_icon):
        Morpher.__init__(self, cost2, cost3, x, y, cost, img, selectedImg, unselectedImg)

    """Upgrades the Rifle and Shotgun bullet Damage upon purchase
    (Starting values: (Rifle: (5 Damage) Shotgun: (10 Damage)"""
    def purchase(self):
        if self.current_upgrade_level == 0:
            HC.Rifle.damage = 7
            HC.Shotgun.damage = 15
            self.information_text2 = '(Rifle: (8 Damage), Shotgun: (20 Damage).'

        elif self.current_upgrade_level == 1:
            HC.Rifle.damage = 8
            HC.Shotgun.damage = 20
            self.information_text2 = '(Rifle: (10 Damage), Shotgun: (25 Damage).'

        elif self.current_upgrade_level == 2:
            HC.Rifle.damage = 10
            HC.Shotgun.damage = 25

        self.confirm_morpher_purchase()


bullet_damage_Morpher = Bullet_Damage(cost= 75, cost2=100, cost3=200)

"""Increases Piles battery heal amount."""
class Battery_Upgrade(Morpher):
    information_text = 'Increases Battery Heal to 30'
    information_text2 = '(When Piles the robot heals you; he heals you for more!)'

    def __init__(self, cost, cost2, cost3, x=1100, y=250, img=SI.battery_icon,
                 selectedImg=SI.battery_selected_icon, unselectedImg=SI.battery_icon):
        Morpher.__init__(self, cost2, cost3, x, y, cost, img, selectedImg, unselectedImg)

    def purchase(self):
        if self.current_upgrade_level == 0:
            HC.Piles.healAmount = 30
            self.information_text = 'Increases Battery Heal to 40'

        elif self.current_upgrade_level == 1:
            HC.Piles.healAmount = 40
            self.information_text = 'Increases Battery Heal to 50'

        elif self.current_upgrade_level == 2:
            HC.Piles.healAmount = 50

        self.confirm_morpher_purchase()


battery_upgrade_Morpher = Battery_Upgrade(cost=75, cost2=100, cost3=150)

"""Increases Player max_health amount.
(Limit is at 400 Health)"""
class Health_Upgrade(Morpher):
    information_text = 'Increases health to 300'
    information_text2 = '(Heart of a Champion)'

    def __init__(self, cost, cost2, cost3, x=1100, y=150, img=SI.health_icon,
                 selectedImg=SI.health_selected_icon, unselectedImg=SI.health_icon):
        Morpher.__init__(self, cost2, cost3, x, y, cost, img, selectedImg, unselectedImg)

    def purchase(self):
        if self.current_upgrade_level == 0:
            HC.player.maxHealth = 300
            self.information_text = 'Increases health to 350'

        elif self.current_upgrade_level == 1:
            HC.player.maxHealth = 350
            self.information_text = 'Increases health to 400'

        elif self.current_upgrade_level == 2:
            HC.player.maxHealth  = 400
            self.information_text = 'max health possible reached'
        print(f'this is the player maxHealth now: {player.maxHealth}')
        self.confirm_morpher_purchase()


health_upgrade_Morpher = Health_Upgrade(cost=100, cost2=120, cost3= 200)


class Shield_Upgrade(Morpher):
    information_text = 'Increases shield capacity to 150'
    information_text2 = '(Untouchable)'

    def __init__(self, cost, cost2, cost3, x=1100, y=350, img=SI.shield_upgrade_icon,
                 selectedImg=SI.shield_upgrade_selected_icon, unselectedImg=SI.shield_upgrade_icon):
        Morpher.__init__(self, cost2, cost3, x, y, cost, img, selectedImg, unselectedImg)

    def purchase(self):
        if self.current_upgrade_level == 0:
            HC.player.overshield_max_amount = 150
            self.information_text = 'Increases shield capacity to 200'

        elif self.current_upgrade_level == 1:
            HC.player.overshield_max_amount = 200
            self.information_text = 'Increases shield capacity to 250'

        elif self.current_upgrade_level == 2:
            HC.player.overshield_max_amount = 250
            self.information_text = 'max shield capacity possible reached'

        print(f'this is the player max_shields now: {HC.player.overshield_max_amount}')
        self.confirm_morpher_purchase()


shield_upgrade_Morpher = Shield_Upgrade(cost=75, cost2=100, cost3=150)

"""Unlocks the shotgun augment for the player weapon!"""
class Shotgun_Panel(Panel):
    information_text = 'This core empowers your weapon into a shotgun,'
    information_text2 = 'dealing high damage up-close with high reload time.'

    def __init__(self, x=60, y=470, cost = 100, img=SI.shotgun_icon,
                      selectedImg=SI.shotgun_selected_icon, unselectedImg=SI.shotgun_icon):
        Panel.__init__(self, x, y, cost, img, selectedImg, unselectedImg)

        self.animated = True
        self.iterationList = SI.redEyesShotgunShootRight
    """Does this when purchased(always makes bought True and changes to unavailable img
    while also doing the specific unlock or funciton for it's purchase"""
    def purchase(self):
        self.confirm_purchase()
        HC.player.shotgun_unlocked = True
        print('shotgun purchased')
        print(player.gems, shopping_cart.runningTotal)


shotgun_panel = Shotgun_Panel()

"""Unlocks the Rocket Launcher augment for the player!"""
class Rocket_Launcher_Panel(Panel):
    information_text = 'This core empowers your weapon into a rocket launcher,'
    information_text2 = 'dealing high explosive damage with a low fire rate.'

    def __init__(self, x=305, y=470, cost = 200, img=SI.rocket_icon,
                      selectedImg=SI.rocket_selected_icon, unselectedImg=SI.rocket_icon):
        Panel.__init__(self, x, y, cost, img, selectedImg, unselectedImg)

        self.animated = True
        self.iterationList = SI.redEyesRocketLauncherRight

    def purchase(self):
        self.confirm_purchase()
        HC.player.rocket_launcher_unlocked = True
        print('rocket_launcher_purchased')
        print(player.gems, shopping_cart.runningTotal)


rocket_launcher_panel = Rocket_Launcher_Panel()

"""Unlocks the roll ability for player when purchased!"""
class Roll_Panel(Panel):
    information_text = 'Unlocks the roll ability, making the player immune'
    information_text2 = 'to damage while rolling and adding mobility.'

    def __init__(self, x=210, y=700, cost = 150, img=SI.roll_icon,
                      selectedImg=SI.roll_selected_icon, unselectedImg=SI.roll_icon):
        Panel.__init__(self, x, y, cost, img, selectedImg, unselectedImg)

        self.animated = True
        self.iterationList = SI.redEyesRollRight

    def purchase(self):
        self.confirm_purchase()
        HC.player.roll_unlocked = True
        print('player roll ability unlocked!')
        print(player.gems, shopping_cart.runningTotal)

roll_panel = Roll_Panel()

"""Unlocks the Melee ability for the player when purchased!"""
class Melee_Panel(Panel):
    information_text = "When 'b' key is pressed you will perform a melee attack;"
    information_text2 = 'deals damage, stuns, and knocks enemy backwards!.'

    def __init__(self, x=50, y=700, cost = 125, img=SI.melee_icon,
                      selectedImg=SI.melee_selected_icon, unselectedImg=SI.melee_icon):
        Panel.__init__(self, x, y, cost, img, selectedImg, unselectedImg)

        self.animated = True
        self.iterationList = SI.redEyesKnockbackRight


    def purchase(self):
        self.confirm_purchase()
        HC.player.melee_unlocked = True
        print('player melee ability unlocked!')
        print(player.gems, shopping_cart.runningTotal)

melee_panel = Melee_Panel()

"""Unlocks Grenade consumables and throw Grenade ability for the player when purchased!"""
class Throw_Grenade_Panel(Panel):
    information_text = 'Unlocks the grenades as consumables that will drop,'
    information_text2 = 'player can pickup and throw them for explosive damage.'

    def __init__(self, x=395, y=700, cost = 125, img=SI.throw_grenade_icon,
                      selectedImg=SI.throw_grenade_selected_icon, unselectedImg=SI.throw_grenade_icon):
        Panel.__init__(self, x, y, cost, img, selectedImg, unselectedImg)

        self.animated = True
        self.iterationList = SI.redEyesThrowGrenadeRight

    def purchase(self):
        self.confirm_purchase()
        HC.player.grenades_unlocked = True
        print('player sprint ability unlocked!')
        print(player.gems, shopping_cart.runningTotal)


throw_grenade_panel = Throw_Grenade_Panel()

"""Unlocks the shield on use ability for the player when purchased!"""
class Shield_Generator_Panel(Panel):
    information_text = "Allows player to activate shields on Use with the 'z' key,"
    information_text2 = 'Use sparingly as it does incur long recovery time.'

    def __init__(self, x=645, y=710, cost = 125, img=SI.shield_generator_icon,
                      selectedImg=SI.shield_generator_selected_icon, unselectedImg=SI.shield_generator_icon):
        Panel.__init__(self, x, y, cost, img, selectedImg, unselectedImg)

        self.animated = True
        self.iterationList = SI.redEyesIdleRight

    def purchase(self):
        self.confirm_purchase()
        HC.player.shield_generator_unlocked = True
        HC.player.shield_generator_available = True
        print('player on use shield skill is unlocked!')
        print(player.gems, shopping_cart.runningTotal)

shield_generator = Shield_Generator_Panel()


panels_list = [shotgun_panel, rocket_launcher_panel, roll_panel, melee_panel, throw_grenade_panel, shield_generator,
               bullet_damage_Morpher, health_upgrade_Morpher, explosive_damage_Morpher, magazine_capacity_Morpher,
               battery_upgrade_Morpher, shield_upgrade_Morpher]

"""Draws the preview screen upon panel selection to showcase the abilities / upgrades!"""
class Preview_Screen():

    preview_img = None
    price_text = '200'

    information_text = ''
    current_panel = None # current attactched panel being previewed

    def __init__(self, name):
        self.name = name

    def reset_preview(self):
        if self.price_text != None:  # check if not reset
            self.price_text = ''
            self.information_text = ''
            #print('reset to defaults')

    def run_preview(self):
        if self.current_panel.animated:
            self.current_panel.animateMe()

            if self.current_panel is shotgun_panel:
                scaled_image = pygame.transform.scale(self.current_panel.iteration_img, (178, 185))
                win.blit(scaled_image, (335, 100))



            #elif self.current_panel is shield_generator:
               # win.blit(SI.redEyesIdleRight[0], (275, 100))
               # scaled_image = pygame.transform.scale(self.current_panel.iteration_img, (178, 185))
                #win.blit(scaled_image, (275, 100))

            else:
                scaled_image = pygame.transform.scale(self.current_panel.iteration_img, (300, 300))
                win.blit(scaled_image, (275, 60))

                #if sheild is active animate the shield
                if self.current_panel is shield_generator:
                    if self.current_panel.iterationCounter < 8:
                        shield_scaled_image = pygame.transform.scale(SI.redEyesShieldActive[self.current_panel.iterationCounter], (180, 195))
                        win.blit(shield_scaled_image, (304, 100))
        else:
            self.display_image = self.current_panel.selectedImg
            scaled_image = pygame.transform.scale(self.display_image, (200, 200))
            win.blit(scaled_image, (250, 100))

    def display_panel(self):
        if self.current_panel != None:
            if self.current_panel.tag == 'Panel':
                self.price_text = self.current_panel.cost
            elif self.current_panel.tag == 'Morpher':
                self.price_text = self.current_panel.current_cost
            self.information_text = self.current_panel.information_text
            self.information_text2 = self.current_panel.information_text2

            self.update_price_text()
            self.update_information_text()
            self.run_preview()
        else:
            self.reset_preview()

    def update_price_text(self):
        price_text = interfaceText.render(str(self.price_text), True, (255, 0, 0))
        win.blit(price_text, (735, 85))

    def update_information_text(self):
        information_text = informationText.render(str(self.information_text), True, (0, 255, 0))
        information_text2 = informationText.render(str(self.information_text2), True, (0, 255, 0))
        win.blit(information_text, (310, 320))
        win.blit(information_text2, (310, 340))
    #def update_preview_visuals(self):


preview_screen = Preview_Screen('preview_screen')

class Stats_Screen():

    def draw_stats_text(self):

        player_shields_text = interfaceText.render(str(HC.player.overshieldAmount) + ' / ' +\
                str(HC.player.overshield_max_amount), True, (0, 0, 255))
        win.blit(player_shields_text, (950, 512)) #-60 for adjustment

        player_max_health_text = interfaceText.render(str(HC.player.health) + ' / ' +\
                str(HC.player.maxHealth), True, (0, 255, 0))
        win.blit(player_max_health_text, (950, 570))

        player_healing_text = interfaceText.render('+' + str(HC.Piles.healAmount), True, (0, 255, 0))
        win.blit(player_healing_text, (950, 630))

        rifle_damage_text = informationText.render(str(HC.Rifle.damage), True, (255, 0, 0))
        win.blit(rifle_damage_text, (1300, 510))

        rifle_magazine_text = informationText.render(str(HC.Rifle.clipSize), True, (255, 0, 0))
        win.blit(rifle_magazine_text, (1310, 545))

        shotgun_damage_text = informationText.render(str(HC.Shotgun.damage), True, (255, 0, 0))
        win.blit(shotgun_damage_text, (1300, 611))

        shotgun_magazine_text = informationText.render(str(HC.Shotgun.clipSize), True, (255, 0, 0))
        win.blit(shotgun_magazine_text, (1310, 643))

        explosive_damage_text = informationText.render(str(HC.Rocket_Launcher.damage), True, (255, 0, 0))
        win.blit(explosive_damage_text, (1310, 710))


stats_screen = Stats_Screen()