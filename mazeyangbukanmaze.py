from typing import Any
from pygame import*
win_width = 1000
win_height = 700
window = display.set_mode((win_width, win_height))
bg = transform.scale(image.load('space_2.jpg'),(win_width,win_height))


class GameSprite(sprite.Sprite):
    def __init__(self, picture, pict_x, pict_y, width,height ):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(picture),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = pict_x
        self.rect.y = pict_y
    def reset(self) :
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, pict_x, pict_y, width, height, speed_x, speed_y):
        super().__init__(picture, pict_x, pict_y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        if good.rect.x < win_width - 50 and good.speed_x > 0 or good.rect.x > 0 and good.speed_x < 0:
            self.rect.x += self.speed_x
        wall_touched = sprite.spritecollide(self, walls, False)
        if self.speed_x > 0:
            for p in wall_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speed_x < 0 :
            for p in wall_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if good.rect.y < win_height - 90 and good.speed_y > 0 or good.rect.y > 0 and good.speed_y < 0:
            self.rect.y += self.speed_y
        wall_touched = sprite.spritecollide(self,walls,False)
        if self.speed_y > 0:
            for p in wall_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.speed_y < 0:
            for p in wall_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire (self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 25,15,50,0)
        bullets.add(bullet)

class Enemy (GameSprite):
    direction_y = 'up'
    direction_x = 'right'
    def __init__(self, picture, pict_x, pict_y, width, height,speed_x,speed_y):
        super().__init__(picture, pict_x, pict_y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def updateV (self):
        if self.rect.y < 0:
            self.direction_y = 'down'
        elif self.rect.y > 250:
            self.direction_y = 'up'
        if self.direction_y == 'up':
            self.rect.y -= self.speed_y
        if self.direction_y == 'down':
            self.rect.y += self.speed_y
    def updateH (self):
        if self.rect.x < 0:
            self.direction_x = 'right'
        elif self.rect.x > 750:
            self.direction_x = 'left'
        if self.direction_x == 'left':
            self.rect.x -= self.speed_x
        if self.direction_x == 'right':
            self.rect.x += self.speed_x
       
class Bullet (GameSprite):
    def __init__(self, picture, pict_x, pict_y, width, height, speed_x, speed_y):
        super().__init__(picture, pict_x, pict_y, width, height)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x > win_width:
            self.kill()

wall = GameSprite('platform2.png', 400, 350, 400, 100)
wall2 = GameSprite('platform2.png', 50, 100, 400, 100)
wall3 = GameSprite('platform2.png', 350, 90, 100, 400)

walls = sprite.Group()
walls.add(wall)
walls.add(wall2)
walls.add(wall3)

good = Player('gut.png', 0,0,50,90,0,0 )
bad = Enemy('betboi.png',550, 250, 80, 90,0,10 )
bad2 = Enemy('stonmen.png',200, 550,80,90,15,0)
trophy = GameSprite('trophy.png', 850,500, 100,200)

enemies = sprite.Group()
enemies.add(bad)
enemies.add(bad2)

bullets = sprite.Group()

font.init()
# nama = input('Masukkan nama kamu:')
style = font.SysFont('Arial', 50)
wintext = style.render('audrey', True, (100,100,100))
finish = False
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                good.speed_x = -15
            elif e.key == K_RIGHT:
                good.speed_x = 15
            elif e.key == K_UP:
                good.speed_y = -15
            elif e.key == K_DOWN:
                good.speed_y = 15
            elif e.key == K_SPACE:
                good.fire()
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                good.speed_x = 0
            elif e.key == K_RIGHT:
                good.speed_x = 0
            elif e.key == K_UP:
                good.speed_y = 0
            elif e.key == K_DOWN:
                good.speed_y = 0
    if finish == False:
        window.blit(bg,(0,0))
        walls.draw(window)
        good.update()
        good.reset()
        enemies.draw(window)
        bad.updateV()
        bad2.updateH()
        trophy.reset()
        bullets.draw(window)
        bullets.update()
        if sprite.spritecollide(good,enemies,False):
            finish = True
            lose = transform.scale(image.load('gemover.jpg'), (win_width,win_height))
            window.blit(lose,(0,0))
        if sprite.collide_rect(good,trophy):
            finish = True
            win = transform.scale(image.load('winner_1.jpg'),(win_width,win_height))
            window.blit(win,(0,0))
            window.blit(wintext,(350,400))
        sprite.groupcollide(bullets, enemies,True, True)
        sprite.groupcollide(bullets,walls,True,False)
    display.update()


    
