import pygame
import HeroClassCode
import Images

win = pygame.display.set_mode((1400, 800))


def progressStage(stage):
    if stage.name == 'stage_zero':
        stage.CS2 = True
    if stage.name == 'stage_one':
        stage.CS1 = True

def play_cutscene(stage):
    if stage.name == 'stage_zero':

        if not HeroClassCode.Piles.placed:
            HeroClassCode.Piles.setPlacement(-200, 520)
            HeroClassCode.Piles.placed = True
            HeroClassCode.Piles.inPlay = True

        # get Piles to 400 X axis
        if HeroClassCode.Piles.currentX < 70:
            HeroClassCode.Piles.speakText('S0F1', 'text/PilesStageZeroTextBox.txt', specifiedDimensions=(10, 150))
            #HeroClassCode.Piles.animateMe()


        else:
            if HeroClassCode.Piles.batteryActive and not stage.CS1:  # These are markers for the CS (cutscene)
                HeroClassCode.Piles.speakText('S0F1', 'text/PilesStageZeroTextBox.txt', specifiedDimensions=(10, 150))

            elif not stage.CS2:
                stage.CS1 = True
                HeroClassCode.Piles.speakText('SOF2', 'text/PilesStageZeroTextBox2.txt', progressStage, [stage], specifiedDimensions=(10, 150))
                print(stage.CS2)

            else:
                stage.cutsceneAvailable = 'completed'
                stage.finalize()
                HeroClassCode.Piles.inPlay = True

                #print('ending stage')

    elif stage.name == 'stage_one':
        stage.boss.introduce()


        '''
        if not stage.CS1:
            HeroClassCode.Piles.speakText('S1F1', 'text/PilesStageOneTextBox.txt', progressStage, [stage])
        else:
            stage.cutsceneAvailable = 'completed'
        '''
    #elif stage.name == 'stage_one':


        #win.blit(HeroClassCode.Piles.img, (HeroClassCode.Piles.currentX, HeroClassCode.Piles.currentY))