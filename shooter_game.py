#Создай собственный Шутер!
from random import *
from pygame import *  
mixer.init()
window = display.set_mode((700, 500))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def shoot(self):
            bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -5)
            bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(65, 635)
            self.speed = randint(1, 2)
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(65, 635)
            self.speed = randint(1, 2)
            
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

sprite1 = Player("rocket.png", 315, 410, 65, 65, 5)
monsters = sprite.Group()
asteroids = sprite.Group()
monster1 = Enemy("ufo.png", randint(0, 635), 0, 70, 60, randint(1,2))
monster2 = Enemy("ufo.png", randint(0, 635), 0, 70, 60, randint(1,2))
monster3 = Enemy("ufo.png", randint(0, 635), 0, 70, 60, randint(1,2))
monster4 = Enemy("ufo.png", randint(0, 635), 0, 70, 60, randint(1,2))
monster5 = Enemy("ufo.png", randint(0, 635), 0, 70, 60, randint(1,2))
asteroid1 = Asteroid("asteroid.png", randint(0, 635), 0, 70, 60, randint(1,2))
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
asteroids.add(asteroid1)
bullets = sprite.Group()
lost = 0
score = 0
goal = 10
max_lost = 999
font.init()
font = font.SysFont('Arial', 50)
sbito = font.render("Сбито" + str(score), True, (255, 255, 255))
propusheno = font.render("Пропущено: " + str(lost), True, (255, 255, 255))
win = font.render("Победа", True, (255,255,255))
loose = font.render("Проигрыш", True, (255,255,255))
finish = False       
game = True
num_fire = 0
rel_time = False
reload = 0
clock = time.Clock()
FPS = 60
while game:
    window.blit(background, (0, 0))
   
    # Обработка событий всегда должна быть в начале цикла
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN and not finish:  # Стрельба только если игра не закончена
            if e.key == K_SPACE:
                fire_sound.play()
                sprite1.shoot()               
   
    # Обновление спрайтов только если игра не закончена
    if not finish:
        sprite1.reset()
        sprite1.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
       
        # Проверка столкновений
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster1 = Enemy("ufo.png", randint(0, 635), 0, 70, 60, randint(1,2))
            monsters.add(monster1)  
       
        # Проверка условий окончания игры
        if sprite.spritecollide(sprite1, monsters, False) or sprite.spritecollide(sprite1, asteroids, False) or lost >= max_lost:
            finish = True
            game = False  # Можно оставить или убрать, finish всё равно остановит движение
        if score >= goal:
            finish = True
            game = False
    else:
        # Если игра закончена, просто отображаем спрайты без обновления
        sprite1.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
   
    # Отображение счетчиков
    sbito = font.render("Сбито " + str(score), True, (255, 255, 255))
    window.blit(sbito,(10, 20))
    propusheno = font.render("Пропущено: " + str(lost), True, (255, 255, 255))
    window.blit(propusheno, (10, 50))
   
    # Отображение сообщения о победе/поражении
    if finish:
        if score >= goal:
            window.blit(win, (250, 200))
        else:
            window.blit(loose, (250, 200))
   
    display.update()
    clock.tick(FPS)


# Небольшая задержка перед закрытием, чтобы игрок увидел результат
time.wait(2000)

        

