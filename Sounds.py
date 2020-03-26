

import pygame
pygame.mixer.init()


#Boss WHO sound effects
fine_sound = pygame.mixer.Sound('sounds/WhoSounds/fineHaveItMyWay.wav')
fine_sound.set_volume(.05)

minions_rise_sound = pygame.mixer.Sound('sounds/WhoSounds/minionsRise.wav')
minions_rise_sound.set_volume(.05)

stop_wasting_time = pygame.mixer.Sound('sounds/WhoSounds/stopWastingTime.wav')
stop_wasting_time.set_volume(.05)

noStop = pygame.mixer.Sound('sounds/WhoSounds/noStop.wav')
stopIt = pygame.mixer.Sound('sounds/WhoSounds/stopIt.wav')

my_marium_no = pygame.mixer.Sound('sounds/WhoSounds/myMeriumNoooo.wav')

who_damage_taken_1 = pygame.mixer.Sound('sounds/WhoSounds/takeDamage1.wav')
who_damage_taken_1.set_volume(.05)
who_damage_taken_2 = pygame.mixer.Sound('sounds/WhoSounds/takeDamage2.wav')
who_damage_taken_2.set_volume(.05)
who_damage_taken_3 = pygame.mixer.Sound('sounds/WhoSounds/takeDamage3.wav')
who_damage_taken_3.set_volume(.05)

whoLaugh = pygame.mixer.Sound('sounds/WhoSounds/whoLaugh.wav')
whoLaugh.set_volume(.09)
no_place_for_living = pygame.mixer.Sound('sounds/WhoSounds/noPlaceForLiving.wav')
no_place_for_living.set_volume(.08)

stun_sound = pygame.mixer.Sound('sounds/unitSounds/fade_walker_stun.wav')
flame_sound = pygame.mixer.Sound('sounds/WhoSounds/burning_sound.wav')
flame_sound.set_volume(1)
vortex_sound = pygame.mixer.Sound('sounds/WhoSounds/vortex_sound.wav')
vortex_sound.set_volume(6)



#Boss HOLLOW sound effects
dead_shall_serve = pygame.mixer.Sound('sounds/hollowSounds/dead_shall_serve.wav')
dead_shall_serve.set_volume(4)
death_devours_all = pygame.mixer.Sound('sounds/hollowSounds/death_devours_all.wav')
fear_wrath_of_dead = pygame.mixer.Sound('sounds/hollowSounds/fear_wrath_of_dead.wav')
feast_on_flesh = pygame.mixer.Sound('sounds/hollowSounds/feast_on_flesh.wav')
hatred_devours_all = pygame.mixer.Sound('sounds/hollowSounds/hatred_devours_all.wav')
i_cant_stand_the_living = pygame.mixer.Sound('sounds/hollowSounds/i_cant_stand_the_living.wav')
i_hunger = pygame.mixer.Sound('sounds/hollowSounds/i_hunger.wav')
my_fate_is_sealed = pygame.mixer.Sound('sounds/hollowSounds/my_fate_is_sealed.wav')
bite_sound = pygame.mixer.Sound('sounds/hollowSounds/bite_sound.wav')
your_fate_is_sealed = pygame.mixer.Sound('sounds/hollowSounds/your_fate_is_sealed.wav')
death_bell_tolls = pygame.mixer.Sound('sounds/hollowSounds/death_bell_tolls.wav')
hollow_rising = pygame.mixer.Sound('sounds/hollowSounds/hollow_rising.wav')
hollow_rising.set_volume(.08)
slam_sound = pygame.mixer.Sound('sounds/hollowSounds/slam_sound.wav')
slam_sound.set_volume(3)

#Store Sounds
upgrade_purchased_sound = pygame.mixer.Sound('sounds/Store_Sounds/upgrade_purchased_sound.wav')
denied_purchased_sound = pygame.mixer.Sound('sounds/Store_Sounds/denied_purchased_sound.wav')
select_panel_sound = pygame.mixer.Sound('sounds/Store_Sounds/select_panel_sound.wav')
select_panel_sound.set_volume(.2)

#Player Sounds
melee_sound = pygame.mixer.Sound('sounds/player_sounds/melee_sound.wav')
roll_sound = pygame.mixer.Sound('sounds/player_sounds/roll_sound.wav')
roll_sound.set_volume(20)
shield_sound = pygame.mixer.Sound('sounds/player_sounds/shield_sound.wav')
shield_sound.set_volume(7)
collect_gem_sound = pygame.mixer.Sound('sounds/player_sounds/collect_gem_sound.wav')
healing_sound = pygame.mixer.Sound('sounds/player_sounds/healing_sound.wav')
player_damaged_sound = pygame.mixer.Sound('sounds/player_sounds/player_damaged_sound.wav')
player_damaged_sound.set_volume(.09)


#Weapon Sounds
rifle_fire = pygame.mixer.Sound('sounds/weapon_sounds/rifle_sounds/rifle_fire.wav')
rifle_reload = pygame.mixer.Sound('sounds/weapon_sounds/rifle_sounds/rifle_reload.wav')

shotgun_fire = pygame.mixer.Sound('sounds/weapon_sounds/shotgun_sounds/shotgun_fire.wav')
shotgun_fire.set_volume(.3)
shotgun_reload = pygame.mixer.Sound('sounds/weapon_sounds/shotgun_sounds/shotgun_reload.wav')

RL_fire = pygame.mixer.Sound('sounds/weapon_sounds/RL/RL_fire.wav')
RL_fire.set_volume(10)
explosion_sound = pygame.mixer.Sound('sounds/explosion_sound.wav')

scythe_sound = pygame.mixer.Sound('sounds/unitSounds/scythe_sound.wav')
scythe_sound.set_volume(1)

#unit Sounds
#leaper
leaper_s1 = pygame.mixer.Sound('sounds/unitSounds/leaper_sound.wav')
plaguebolt_hit = pygame.mixer.Sound('sounds/unitSounds/plaguebolt_hit.wav')