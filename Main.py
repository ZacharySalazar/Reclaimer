import HeroClassCode
import Controls
import pygame
import Images
import Stages
import Spells
import CutScenes
import Tools
import Consumables


pygame.init()

update = pygame.display.update

win = pygame.display.set_mode((1400, 800))
surfaceCreation = pygame.font.SysFont('Comic Sans MS', 15)
stageCompletionFont = pygame.font.SysFont('castellar', 30)
interfaceText = pygame.font.SysFont('Comic SanaMs', 35)
pygame.display.set_caption("Fiends Realms")
white = (255, 255, 255)
blue = (0, 0, 255)
yellow = (255, 255, 0)
mousePosition = pygame.mouse.get_pos()

#redefine moduels
CS = CutScenes


'''Detects the ability of the character type and procs it'''
def getAbility(character):
#Aggressive actions / abilities
    if character.aggression:
        character.useAbility()

        #if character.name == 'regularSkeleton':
            #character.raiseShield()

        #if character.name == 'captainSkeleton':
            #character.rally()

        #if character.name == 'red_skeleton':
            #pass
            #character.summon_skeletons()

        #if character.name == 'ghost':
            #print(character.haunting)
            #character.hasunt(HeroClassCode.player)

#Passive actions / abilities
    if not character.aggression:
        if character.name == 'ghost':
            if not character.risen:
                character.await_rise(HeroClassCode.player)

#Game Main Loop
def getEnemyEdge(findEdge, enemy):
    mousePosition = pygame.mouse.get_pos()
    #print(f'this is mouse X: {mousePosition[0]}, this is mouse Y: {mousePosition[1]}')
    if findEdge == 'top':
        print(enemy.currrentY)
    elif findEdge == 'bottom':
        pass

def getEnemyHover():

    #special hover used by Grave_Keepers
    #they only summon adds and do not patrol with anchors
    if enemy.ranged == 'non combative':
        if enemy.name == 'grave_keeper':
            enemy.hover_keeper()
        elif enemy.name == 'fade_walker':
            enemy.port_first()

    elif enemy.ranged:
        #print('detecting a ranged unit')
        enemy.hover(rangedObject=enemy)

    elif not enemy.ranged:
        enemy.hover()



while True:
   # print(HeroClassCode.player.dead, ' is the player dead?')
    #print(HeroClassCode.death_screen.enabled,' is the death screen enabled?')
    #if Stages.stageHandler.currentStage.boss != None:
        #print(Stages.stageHandler.currentStage.boss.name)
    #print(mousePosition)
    #for enemy in Stages.stageHandler.currentStage.enemiesList:
        #print(f'enemy currentX: {enemy.currentX}')
    #print(f'this is the mouse position: {mousePosition}')
    # if HeroClassCode.player.currentWeapon.name == 'Shotgun':
    #     print('this is the shotgun right range: ', HeroClassCode.player.currentWeapon.right_x_range)
    # for matter in Stages.stageHandler.currentStage.matterList:
    #     print('this is the matter midLine: ', matter.midLine)
    #print(f'player yBubble: {HeroClassCode.player.Ybubble}')
    #print(f'shotgun yBubble: {HeroClassCode.Shotgun.full_y_range}')

    #print(f'player midLine: {HeroClassCode.player.midLine}')
    #print(f'shotgun full_x_range: {HeroClassCode.Shotgun.full_x_range}')
    #print(f'this is the player stun status: {HeroClassCode.player.stunned}')
    #print(f'this is the hero total currency: {HeroClassCode.player.total_credits}')
    #print(f' this is the player ybubble {HeroClassCode.player.Ybubble}')
    #print('this is player midline: ', HeroClassCode.player.midLine)
    #print('this is player Y: ', HeroClassCode.player.currentY)
    #print(f'this is the player topEdge: {HeroClassCode.player.topEdge}')
    #print(f'this is the player bottomEdge: {HeroClassCode.player.bottomEdge}')
    mousePosition = pygame.mouse.get_pos()
    #if Stages.stageHandler.currentStage.boss!= None:
    #print(f'this is the boss x: {Stages.stageHandler.currentStage.boss.currentX}')
    #print(f'this is the boss y: {Stages.stageHandler.currentStage.boss.currentY}')
    #print(f'this is the mousepoistion: {mousePosition}')
    #getEnemyEdge('top', HeroClassCode.blackMage1)
    #win.blit(Stages.stageHandler.currentStage.img, (0, 0))
    Stages.stageHandler.currentStage.drawStageBackground(HeroClassCode.player)
    #Tools.measureEnemy('midline')
    #print(f'this is mouse X: {mousePosition[0]}, this is mouse Y: {mousePosition[1]}')

    #print(f'player leftEdge: {HeroClassCode.player.leftEdge} rightEdge: {HeroClassCode.player.rightEdge}')


    #healthbars
    HeroClassCode.draw_player_healthbar_Icon()

    Stages.stageHandler.currentStage.checkBoundaries(HeroClassCode.player)
    #print(Stages.stageHandler.currentStage.nextStageUnlocked)

    for i in HeroClassCode.combatTextList:                           #iterates through the combatText List and has all active texts drawn until they disapate\
        i.drawText()                                                  #from floating to far from their anchors

    HeroClassCode.drawProjectiles()
    Stages.stageHandler.drawMatter()
    #print(f'this is the player midline: {HeroClassCode.player.midLine}')
    for enemy in Stages.stageHandler.currentStage.enemiesList:
        #print(f'is he leaping?: {enemy.leaping}')
        #print(f'enemy currentY: {enemy.currentY}')
        #print(f'enemy topedge: {enemy.topEdge}')s
        #print(f'enemy LeftEdge {enemy.leftEdge}')
        #print(f'enemy rightEdge {enemy.rightEdge}')
        #print(f'this is enemy currentY: {enemys.currentY}')
        #print(f'this is the mouse position: {mousePosition}')
        #print(f'lets you know if showing damage is ready or not: {enemy.showDamage}')
        #print(f'this is the skeleton"s midLine: {enemy.midLine}')
        Stages.stageHandler.currentStage.checkBoundaries(enemy)
        getEnemyHover()
        #print(f'this is the enemy midline: {enemy.midLine}')
        #print(f'topEdge {enemy.topEdge} bottom edge ; {enemy.bottomEdge}')
        if not enemy.stunned:
            getAbility(enemy)

        enemy.drawMe()

    #print(f'this is the wanderers list : {Stages.stageHandler.wanderers_list}')
    for enemy in Stages.stageHandler.wanderers_list:
        #print(f'enemy midLine: {enemy.midLine}', f'player midLine: {HeroClassCode.player.midLine}')
        #Stages.stageHandler.currentStage.checkBoundaries(enemy)
        getEnemyHover()
        if not enemy.stunned:
            getAbility(enemy)

        if Stages.stageHandler.currentStage.scrolling:
            enemy.currentX -= Stages.stageHandler.currentStage.scrollSpeed
            enemy.outlineSelf()
            enemy.startingX -= Stages.stageHandler.currentStage.scrollSpeed
            enemy.leftAnchor = enemy.startingX
            enemy.rightAnchor = enemy.startingX + 300 #accounts enemies always moving onward as not to impose on previously completed stage

        enemy.drawMe()

    #print(f'this is the matter lis: {Stages.stageHandler.currentStage.matterList}')
    #print(f'stage one boss {Stages.stage_one.boss}')
    #print(f'current Stage: {Stages.stageHandler.currentStage.name}')
    #print(f'current Stage enemies List: {Stages.stageHandler.currentStage.enemiesList}')
    Stages.stageHandler.drawConsumables()
    Stages.stageHandler.drawEffects()
    Stages.stageHandler.drawExplosives()
    #drawingSpells to screen
    Spells.showSpells()

    #drawEnemyDisplay()

    if Stages.stageHandler.currentStage.scrolling:
        HeroClassCode.player.currentX -= Stages.stageHandler.currentStage.scrollSpeed
        #print(HeroClassCode.Piles.humanoidName)
    HeroClassCode.Piles.followPlayer()
    HeroClassCode.player.checkPickup()
    HeroClassCode.report_player_health()
    HeroClassCode.player.draw_player()
    HeroClassCode.draw_player_interface()

    Controls.playerControls()

    #draw death screen if player is dead
    if HeroClassCode.death_screen.enabled:
        print('drawing death screen')
        HeroClassCode.death_screen.draw_screen()

    update()

    #drawing Hero
    #win.blit(HeroClassCode.player.img, (HeroClassCode.player.currentX, HeroClassCode.player.currentY))
