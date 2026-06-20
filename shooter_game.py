#Create your own shooter
from pygame import *
from random import randint
from time import time as timer
win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('assets/space.jpg'), (win_width,win_height))
clock = time.Clock()
lost = 0
max_lost = 10
score = 0
goals = 100
life = 5



font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render("YOU WIN!", True,(0,255, 0))
lose = font2.render("YOU LOSE!", True,(255,0, 0))
mixer.init()
mixer.music.load('sound/space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()
fire_sound = mixer.Sound('sound/fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >10:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed  

   
    def fire(self):
        bullet = Bullet('assets/bullet.png', self.rect.centerx, self.rect.top, 15, 20, 10 )
        bullets.add(bullet)



class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


class Asteroid(GameSprite):
        def update(self):
          self.rect.y += self.speed

          if self.rect.y > win_height:
              self.rect.x = randint(80, win_width - 80)
              self.rect.y = 0

            

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player('assets/rocket.png', 80, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 8):
    monster = Enemy('assets/ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
    monsters.add(monster)

bullets = sprite.Group()

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroid('assets/asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1,4))
    asteroids.add(asteroid)
run = True
finish = False
reload_time = False
num_fire = 0


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
               if num_fire < 5 and reload_time == False:
                   num_fire + num_fire + 1
                   fire_sound.play()
                   ship.fire()
                
               if num_fire >= 5 and reload_time == False:
                   last_time = timer()
                   reload_time = True
    if not finish:

        window.blit(background, (0,0))

        ship.reset()
        ship.update()

        bullets.update()
        monsters.update()
        asteroids.update()

        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if reload_time == True:
            now_time = timer()
            
            if now_time - last_time < 3:
                reload = font1.render("RELOADING", True, (255,255,0))
                window.blit(reload, (260,460))
            else:
                num_fire = 0
                reload_time = False
        
        
        

        collides = sprite.groupcollide(monsters, bullets, True,True)
        for c in collides:
            score += 1
            monster = Enemy('assets/ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, True):
            life = life - 1
            monster = Enemy('assets/ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)

        if sprite.spritecollide(ship, asteroids, True):
            life = life - 1
            asteroid = Asteroid('assets/asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1,4))
            asteroids.add(asteroid)



        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if score >= goals:
            finish = True
            window.blit(win, (200,200))
        missed = font1.render('missed:  ' + str(lost), True, (225, 0, 0))
        window.blit(missed, (5,10))

        hit = font1.render('Score:  ' + str(score), True, (225, 0, 0))
        window.blit(hit, (5,50))

        if life >= 3:
            life_color = (255,255,255)
        if life >= 2:
            life_color = (255,255,0)
        if life >= 1:
            life_color = (255,0,0)
        text_life = font2.render(str(life), True, (255, 255, 255))
        window.blit(text_life, (650, 10))
        display.update()
    else:
        finish = False
        lost = 0
        max_lost = 10
        score = 0
        goals = 100
        life = 5
        num_fire = 0
        for b in bullets:
            b.kill()
        for n in monsters:
            n.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1, 8):
            monster = Enemy('assets/ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
            monsters.add(monster)
        for i in range(1, 3):
            asteroid = Asteroid('assets/asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1,4))
            asteroids.add(asteroid)
    clock.tick(40)




