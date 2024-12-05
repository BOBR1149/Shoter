from pygame import *
from random import randint

clock = time.Clock()
FPS = 60
win_width = 700
win_heigh = 700
window = display.set_mode((win_width, win_heigh))
display.set_caption('shoter')
background = transform.scale(image.load('backgroundspace.jpg'),(win_width, win_heigh))
lost = 0
kill = 0
font.init()
font1 = font.Font(None, 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
   
class Player(GameSprite):
        
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
            
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    def update(self,):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_heigh:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > 700:
            self.kill()
            
bullets = sprite.Group()
enemys = sprite.Group()
player = Player('rocket.png', 350, 600, 10)
win = font1.render('YOU WIN', 1, (255, 255, 0))
lose = font1.render("YOU LOSE", 1, (255, 0, 0))

for i in range(6):
    enemy = Enemy('spaceship.png', randint(0, 600), 0, randint(1, 5))
    enemys.add(enemy)

finish = False
game = True
while game:
    if finish == False:
        window.blit(background,(0, 0))
        player.reset()
        player.update()
        enemys.draw(window)
        enemys.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_win = font1.render('Убито' + str(kill), 1, (255, 255, 255))
        sprites_list = sprite.spritecollide(player, enemys, False)
        collides = sprite.groupcollide(bullets, enemys, True, True)
        for i in collides:
            enemy = Enemy('spaceship.png', randint(0, 600), 0, randint(1, 5))
            enemys.add(enemy)
            kill += 1
        if kill >= 50:
            finish = True
            window.blit(win, (350, 350))
        if len(sprites_list) > 0 or lost >= 10:
            finish = True
            window.blit(lose, (350, 350))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    
    window.blit(text_lose, (0, 0))
    window.blit(text_win, (0, 30))
    display.update()
    clock.tick(FPS)
    