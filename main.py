import random

import pygame as p
import pygame.freetype
import sprite
import os
from settings import *


# plimg = p.image.load('png.png/playership1.png')
# meteornamelist = os.listdir('png.png/meteor')
def drawgame():
    dp.blit(background, (0, 0))
    ship.draw(dp)
    lg.draw(dp)
    mg.draw(dp)
    power_ups.draw(dp)
    spacestation14.draw(dp)
    dp.blit(hpimage, (20, hi - 60))
    dp.blit(Ximage, (60, hi - 52))
    scorefont.render_to(dp, (85, hi - 60), str(ship.hp), (0, 0, 255))
    scorefont.render_to(dp, (wi - 180, 23), str(ship.score).zfill(5), (0, 0, 255))


def drivemenu():
    dp.fill(('#2F4F4F'))
    dp.blit(game_over_background, game_over_rect)
    button.draw(dp)

    dp.blit(hpimage, (20, hi - 60))
    dp.blit(Ximage, (60, hi - 52))
    scorefont.render_to(dp, (85, hi - 60), str(ship.hp), (0, 0, 255))
    scorefont.render_to(dp, (wi - 180, 23), str(ship.score).zfill(5), (0, 0, 255))


def update():
    ship.update()
    mg.update()
    lg.update()
    power_ups.update()

    checkship()
    checklaser()
def Stop_Game():
    p.mouse.set_visible(True)
    spacesound.fadeout(5000)
    mg.empty()
    lg.empty()
def restart_game():
    p.mouse.set_visible(False)
    spacesound.play(-1)
    ship.rebound()


def checklaser():
    for i in lg:
        if p.sprite.spritecollide(i, mg, True):
            meteorhitsound.play()
            i.kill()
            ship.score += 1


def checkship():
    if p.sprite.spritecollide(ship, mg, True):
        hitsound.play()
        ship.getdamage(1)


def laser():
    lg.add(sprite.Laserpiupiu(ship.rect.center, laser_imagen))


def meteor():
    mi = random.choice(mis)
    mete = sprite.mt((random.randint(0, wi), -20), mi)
    mg.add(mete)


def makepowup():
    rn = random.randint(0,4)
    pos = (random.randint(0,wi),-20)
    if rn % 2 == 0:
        powerup = sprite.Power_up(pos,power_ups['shield'],'shield')
        spacestation14.add(powerup)
    elif rn % 3 == 0:
        powerup = sprite.Power_up(pos, power_ups['bolt'], 'bolt')
        spacestation14.add(powerup)



p.init()

laser_imagen =[p.image.load(f'png.png/laser/laserBlue{i}.png') for i in range(12,18)]
mis = [p.image.load('png.png/meteor/' + name)
       for name in os.listdir('png.png/meteor')]
plimg = [p.image.load(f'png.png/Damage/playerShip1_damage{i}.png')
         for i in range(1, 4)]
plimg.insert(0, p.image.load('png.png/playership1.png'))
background = p.image.load('png.png/blue.png')
background = p.transform.scale(background, (wi, hi))
hpimage = p.image.load('png.png/playerLife1_blue.png')
power_ups = {'shield':p.image.load('png.png/bonusi/shield_silver.png'),
             'bolt':p.image.load('png.png/bonusi/bolt_silver.png')}
shield_images = [p.image.load(f'png.png/bonusi/shield{i}.png')
                 for i in range(1,4)]
Ximage = p.image.load('png.png/numeralX.png')
losesound = p.mixer.Sound('sound/sfx_lose.ogg')
lasersound = p.mixer.Sound('sound/sfx_laser1.ogg')
meteorhitsound = p.mixer.Sound('sound/meteor_hit.wav')
hitsound = p.mixer.Sound('sound/hit.wav')
spacesound = p.mixer.Sound('sound/space_ambiance.wav')
twotone = p.mixer.Sound('sound/sfx_twoTone.ogg')

clock = p.time.Clock()
dp = p.display.set_mode((wi, hi))
p.display.set_caption('spacestation14')
game_state = 'MAIN GAME'
ship = sprite.pl((wi / 2, hi / 2), plimg, shield_images)
scorefont = p.freetype.Font('res/kenvector_future.ttf', 39)
textfont = p.freetype.Font('res/kenvector_future.ttf', 50)
button = sprite.butter((wi / 2, hi / 2), 'Restart game?', textfont)
game_over_background, game_over_rect = textfont.render('Game over')
mg = p.sprite.Group()
lg = p.sprite.GroupSingle()
spacestation14 = p.sprite.Group()
METE = p.USEREVENT
p.time.set_timer(METE, 300)
SPAPOUP = p.USEREVENT + 2
p.time.set_timer(SPAPOUP,3000)

spacesound.play(-1)
p.mouse.set_visible(False)
running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT or (event.type == p.KEYDOWN and event.key == p.K_ESCAPE):
            running = False
        if game_state == 'MAIN GAME':

            if event.type == METE:
                meteor()
            elif event.type == p.MOUSEBUTTONDOWN:
                if len(lg) == 0:
                    laser()
            elif event.type == ship.DESTROYEVENT:
                game_state = 'MENU'
                Stop_Game()
            elif event.type == SPAPOUP:
                makepowup()
        else:
            if(event.type == p.MOUSEBUTTONDOWN and button.rect.collidepoint(event.pos)):
                game_state = "MAIN GAME"
                restart_game()
    if game_state == "MAIN GAME":
        drawgame()
        update()
    else:
        drivemenu()
    clock.tick(60)
    p.display.flip()
