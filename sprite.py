import pygame as p
import random
from settings import *


class pl:
    def __init__(self, pos, image,shield_images):
        self.shieldpower = 0
        self.shieldimags = shield_images
        self.shi_rect = shield_images[0].get_rect()
        self.image = image[0]
        self.images = image
        self.hp = 4
        self.score = 0
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.startpos = pos
        self.DESTROYEVENT = p.USEREVENT + 1

    def draw(self, spawn):
        if self.hp > 0:
            spawn.blit(self.image, self.rect)
            if self.hp < 4:
                spawn.blit(self.images[-self.hp], self.rect)
        self.draw_shift(spawn)

    def update(self):
        self.move()
        self.restrein()

    def rebound(self):
        self.hp = 4
        self.score = 0
        self.islive = True
        self.rect.center = self.startpos

    def move(self):
        keys = p.key.get_pressed()
        if keys[p.K_a]:
            self.rect.x -= 7
        if keys[p.K_d]:
            self.rect.x += 7
        if keys[p.K_w]:
            self.rect.y -= 7
        if keys[p.K_s]:
            self.rect.y += 7

    def restrein(self):
        if self.rect.x >= wi:
            self.rect.x = wi
        elif self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.y >= hi:
            self.rect.y = hi
        elif self.rect.y <= 0:
            self.rect.y = 0

    def getdamage(self, damage):
        if self.hp > 0:
            self.hp -= damage
            if self.hp <= 0:
                p.event.post(p.event.Event(self.DESTROYEVENT))
    def draw_shift(self,targetsurf):
        if self.shieldpower > 0:
            self.shi_rect.center = self.rect.center
            if self.shieldpower != 1:
                self.shi_rect.move_ip((-5,-5))
            targetsurf.blit(self.shieldimags[self.shieldpower - 1], self.shi_rect)


class mt(p.sprite.Sprite):
    def __init__(self, pose, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pose
        self.sx = random.randint(-3, 3)
        self.sy = random.randint(3, 9)
        self.origimag = image
        self.angle = 0
        self.rotationspeed = random.randint(-3,3)
    def rotate(self):
        self.angle += self.rotationspeed
        self.image = p.transform.rotate(self.origimag,self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)


    def update(self):
        self.rotate()
        self.rect.x += self.sx
        self.rect.y += self.sy
        if self.rect.y > hi:
            self.kill()


class Laserpiupiu(p.sprite.Sprite):
    def __init__(self, pos, imag):
        super().__init__()
        self.images = imag
        self.image = self.images[0]
        self.animlen = len(self.images)
        self.frame = 0
        self.rect = self.image.get_rect(center = pos)
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
        self.frame = 0.25
        if int(self.frame) == self.animlen:
            self.frame = 0
        self.image = self.images[int(self.frame)]

class butter():
    def __init__(self,pos,text,font):
        super().__init__()
        self.image = p.Surface((451,81))
        self.image.fill('#7FFFD4')
        self.rect = self.image.get_rect(center = pos)
        self.text_surf,self.text_rect = font.render(text,size = 24)
        self.text_rect.center = self.rect.center
    def draw(self,target_surf):
       target_surf.blit(self.image,self.rect)
       target_surf.blit(self.text_surf, self.text_rect)
class Power_up(p.sprite.Sprite):
    def __init__(self,pos,image,_type):
        super().__init__()
        self.image = image
        self.type = _type
        self.rect = self.image.get_rect(center = pos)
        self.speedy = random.randint(1,7)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()




