# ¡Crea tu propio juego de disparos!

from pygame import *
mixer.init()
mixer.music.load('battle1.ogg')
mixer.music.play()
window = display.set_mode((700,500))
display.set_caption("Madokami en el espacio :3")

background = transform.scale(image.load("galaxy.jpg"),(700,500))

display.update()
# clase padre para otros objetos
class GameSprite(sprite.Sprite):
    # constructor de clase
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # llamamos al constructor de la clase (Sprite):
        sprite.Sprite.__init__(self)

        # cada objeto debe almacenar una propiedad image
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        # cada objeto debe almacenar la propiedad rect en la cual está inscrito
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # método que dibuja al personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# clase del jugador principal
class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
    def fire(self):
        a_arrow = bullet('arrow.png',self.rect.centerx,self.rect.top,15,29,19)
        arrow.add
class arrow(GameSprite):
    def update(self):
        self.rect.y -=self.speed
        if self.rect.y < 0:
            self.kill()


madokami = Player("madokami.png",100,100,100,100, 5)            
    #pass

run = True
while run:
    window.blit(background,(0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False
    madokami.update()
    madokami.reset()
    display.update()
    time.delay(100)



