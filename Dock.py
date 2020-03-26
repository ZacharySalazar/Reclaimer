import HeroClassCode
import Bosses as B
import Consumables as C
import Stages
import random


#randomConsumables =
"""Loads Consumables into enemies and enemies into Stages"""
HC = HeroClassCode

#Stage Zero Setup
Stages.stage_zero.enemiesList = []#HC.Fade_Walker(700, 400, droppedConsumable=C.Battery)]#HC.Fade_Walker(700, 900, droppedConsumable=C.Battery)]#HC.Grave_Keeper(startingX= 600, startingY= 600, droppedConsumable=C.spawnRandomConsumables())]#HC.Skeleton('leaper', 1000, 550, droppedConsumable=C.spawnRandomConsumables())]
                                 #HC.Marksman(1000, 550, droppedConsumable=C.spawnRandomConsumables()
                                 #HC.Skeleton('regularSkeleton', 1200, 600, droppedConsumable=C.spawnRandomConsumables())]
                                 #HC.Skeleton('captainSkeleton', 1000, 600, droppedConsumable=C.spawnRandomConsumables())] #HC.Skeleton('captainSkeleton', 1000, 600, droppedConsumable=C.spawnRandomConsumables()
                                 #HC.Skeleton('regularSkeleton', 1250, 500, droppedConsumable=C.spawnRandomConsumables())]

Stages.stage_zero.matterList = [C.Chest(x=1100, y=600, containmentList=C.spawnRandomGems(for_chest=True)),
                                C.Chest(x=1200, y=600, containmentList=C.spawnRandomGems(for_chest=True)),
                                C.Chest(x=1300, y=600, containmentList=C.spawnRandomGems(for_chest=True))]
                                #C.Care_Package(x=1000, y=-60, containmentList=C.spawnRandomGems(for_chest=True), speed=1)]
                                #C.Chest(x=900, y=600, amount_of_gems=random.randint(3, 5))]s

#Loaded enemies after the stage is completed
Stages.stage_zero.wanderers = []#HC.Skeleton('regularSkeleton', startingX=Stages.stage_one.imgX + 200, startingY=600, droppedConsumable=C.spawnRandomConsumables())]#HC.Skeleton('regularSkeleton', startingX=Stages.stage_one.imgX + 200, startingY=600, droppedConsumable=C.spawnRandomConsumables())]

#Stage One Setup
Stages.stage_one.enemiesList = [HC.Fade_Walker(50, 650, droppedConsumable=C.spawnRandomGems()),
                                HC.Grave_Keeper(1250, 680, droppedConsumable=C.spawnRandomGems())]
                                #HC.Skeleton('regularSkeleton', 1100, 545, droppedConsumable=C.spawnRandomGems())]#HC.Skeleton('captainSkeleton', 1000, 600, droppedConsumable=C.spawnRandomConsumables())]
                                #HC.Skeleton('regularSkeleton', 1000, 550, droppedConsumable=C.spawnRandomConsumables())]
                                #HC.Skeleton('regularSkeleton', 1250, 500, droppedConsumable=C.spawnRandomConsumables())]
Stages.stage_one.reinforcementsList = []

Stages.stage_one.wanderers = [HC.Skeleton('leaper', startingX=Stages.stage_two.imgX + 200, startingY=600, droppedConsumable=C.spawnRandomConsumables()),
                              HC.Skeleton('leaper', startingX=Stages.stage_two.imgX + 300, startingY=650,
                                          droppedConsumable=C.spawnRandomConsumables())]

#Stage Two Setup
Stages.stage_two.matterList = [C.Chest(x=1300, y=600, containmentList=C.spawnRandomGems(for_chest=True))]

Stages.stage_two.enemiesList = [HC.Skeleton('leaper', 1200, 550, droppedConsumable=C.Battery),
                                HC.Skeleton('leaper', 1100, 600, droppedConsumable=C.spawnRandomGems()),
                                HC.Skeleton('leaper', 1000, 650, droppedConsumable=C.spawnRandomGems())]#HC.Skeleton('captainSkeleton', 1000, 600, droppedConsumable=C.spawnRandomConsumables())]


#Note for bosses: (Cutscene is completed upon end of boss intro then it can't continue scrolling until boss == None and thus does the boss.cycle())
#Stages.stage_one.boss = B.HOLLOW
#Stages.stage_one.bossList = [B.HOLLOW]
#Creating a boss to a specific stage
#Stages.stage_one.boss = B.HOLLOW
#Stages.stage_one.bossList = [B.HOLLOW]


#Stages.stage_two.enemiesList = []
#Stages.stage_one.matterList = [C.Chest(x=1100, y=600)]
#Stages.stage_two.matterList = [C.Chest(1100, 600)]
# HC.Canyon_Skeleton('trooper', 1250, 500, True)] #Canyon_Skeleton('peon', 700, 500), Canyon_Skeleton('trooper', 800, 550), Canyon_Skeleton('barbarian', 800, 600)] #Marksman(800, 600)]#Canyon_Skeleton('trooper', 800, 600)] #Canyon_Skeleton('barbarian', 800, 600)]  Canyon_Skeleton('peon', 700, 500), Canyon_Skeleton('trooper', 800, 600)
#Stages.stage_one.enemiesList =  [HC.Canyon_Skeleton('trooper', 1250, 500, True), HC.Canyon_Skeleton('peon', 1250, 600, True)]#[Skeleton('regularSkeleton', 800, 540), Skeleton('regularSkeleton', 1000, 500), Skeleton('captainSkeleton', 1000, 600), Red_Skeleton(1000, 600)]
#Stages.stage_two.enemiesList = [HC.Canyon_Skeleton('trooper', 1250, 500, True), HC.Canyon_Skeleton('peon', 1250, 700, True)]


