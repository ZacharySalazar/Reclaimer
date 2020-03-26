import pygame
import HeroClassCode as HC
import Panels
import Shop_Images as SI
import Sounds

pygame.init()
win = pygame.display.set_mode((1400, 900))
priceText = pygame.font.SysFont('Comic SanaMs', 35)
gemText = pygame.font.SysFont('Comic SanaMs', 30)
"""Adjusts panel images and adds their cost to the shopping cart
(Only will detect click when the panel hasn't already been bought)"""
def click(given_panel):
    if not given_panel.bought:
        if not given_panel.selected:
            Sounds.select_panel_sound.play()
            if Panels.shopping_cart.cart_list != []:
                Panels.shopping_cart.cart_list[0].selected = False
                Panels.shopping_cart.cart_list[0].img = Panels.shopping_cart.cart_list[0].unselectedImg
                Panels.shopping_cart.cart_list = []
                Panels.shopping_cart.runningTotal = 0

                Panels.preview_screen.reset_preview()


            given_panel.img = given_panel.selectedImg
            given_panel.selected = True
            Panels.shopping_cart.add_item(given_panel)

            Panels.preview_screen.current_panel = given_panel


        elif given_panel.selected:
            Sounds.select_panel_sound.play()
            given_panel.img = given_panel.unselectedImg
            given_panel.selected = False
            Panels.shopping_cart.remove_item(given_panel)

            Panels.preview_screen.current_panel = None
        print(f'this is the cartList: {Panels.shopping_cart.cart_list}')

"""Maintains the preview screen redraws and updates"""
def operate_preview_screen():
    Panels.preview_screen.display_panel()
    #win.blit()

def show_player_gems():
    player_gems = gemText.render(str(HC.player.gems), True, (0, 255, 0))
    win.blit(player_gems, (40, 65))

def interface_controls():
    event = pygame.event.poll()
    mousePosition = pygame.mouse.get_pos()

    #check if closing shop
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_TAB:
            SI.shop.shop_screen = False

    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_ESCAPE]:
        print(pygame.quit())
        exit()

#checking and drawing panels

    show_player_gems()
    operate_preview_screen()
    Panels.shopping_cart.update_running_total()  # constantly updates the the running total based off the item in the cart
    Panels.stats_screen.draw_stats_text()

    #the buy button
    win.blit(Panels.buy_button.img, (Panels.buy_button.x, Panels.buy_button.y))
    if mousePosition[0] in Panels.buy_button.x_width and mousePosition[1] in Panels.buy_button.y_height:
        if HC.player.gems >= Panels.shopping_cart.runningTotal:
            Panels.buy_button.img = SI.green_buy_button
            if event.type == pygame.MOUSEBUTTONDOWN:
                Panels.buy_button.purchase_cart()
                Sounds.upgrade_purchased_sound.play()
        else:
            Panels.buy_button.img = SI.red_buy_button
            if event.type == pygame.MOUSEBUTTONDOWN:
                Sounds.denied_purchased_sound.play()
            print('not enough gems')
    else:
        Panels.buy_button.img = SI.buy_button

    #icons panels checking
    for panels in Panels.panels_list:
        win.blit(panels.img, (panels.x, panels.y))
        #Morphers
        if panels.tag == 'Morpher':
            panels.display_upgrade_level()

            if panels.current_upgrade_level == 3:
                panels.update_max_reached()

        if panels.bought and panels.tag == 'Panel':
            win.blit(SI.purchased_image, (panels.x, panels.y))

        if mousePosition[0] in panels.x_width and mousePosition[1] in panels.y_height:
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(panels)






