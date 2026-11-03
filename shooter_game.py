# ¡Crea tu propio juego de disparos con Oleadas Infinitas!
from pygame import *
from random import randint, choice

# Inicializar Pygame y Mixer
init()
mixer.init()

# Configuración de audio
mixer.music.load('battle1.ogg')
mixer.music.set_volume(0.6)
fire_sound = mixer.Sound('fire.ogg')

# Configuración de pantalla
window = display.set_mode((700, 500))
display.set_caption("Madokami en el espacio :3")

# Imágenes de fondos y menús
menu_background = transform.scale(image.load("madokamistart.png"), (700, 500))
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

# --- LISTA DE ENEMIGOS DIFERENTES ---
enemigos_imagenes = ["kriemchild.png", "walpurgis.png", "bruja_sombra.png"]

# --- CLASES DEL JUEGO ---

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed

    def fire(self):
        flecha1 = bullet('arrow.png', self.rect.centerx, self.rect.top, 15, 20, 30)
        bullets.add(flecha1)

class bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class enemy(GameSprite):
    def update(self, jugador):
        desviacion_x = choice([-2, -1, 0, 1, 2])
        desviacion_y = choice([-2, -1, 0, 1, 2])

        if self.rect.x < jugador.rect.x:
            self.rect.x += self.speed + desviacion_x
        elif self.rect.x > jugador.rect.x:
            self.rect.x -= self.speed + desviacion_x

        if self.rect.y < jugador.rect.y:
            self.rect.y += self.speed + desviacion_y
        elif self.rect.y > jugador.rect.y:
            self.rect.y -= self.speed + desviacion_y

# --- CREACIÓN DE OBJETOS Y GRUPOS ---

bullets = sprite.Group()
enemigos = sprite.Group()

# Función para generar oleadas de enemigos
def crear_oleada(cantidad):
    for i in range(cantidad):
        imagen_aleatoria = choice(enemigos_imagenes)
        nuevo_enemigo = enemy(imagen_aleatoria, randint(10, 650), -randint(50, 400), 100, 100, 3)
        enemigos.add(nuevo_enemigo)

# Creamos la primera oleada inicial
crear_oleada(5)

madokami = Player("madokami.png", 100, 400, 100, 100, 8)
btn_play = GameSprite("PLAY.png", 250, 300, 200, 70, 0)

# Variables de control
run = True
en_menu = True

# ==========================================
# 1. MENÚ DE INICIO
# ==========================================
while en_menu and run:
    window.blit(menu_background, (0, 0))
    btn_play.reset()
    display.update()

    for e in event.get():
        if e.type == QUIT:
            run = False
            en_menu = False
        
        if e.type = MOUSEBUTTONDOWN if hasattr(e, 'pos') else False: # Mantener compatibilidad simple
        if e.type == MOUSEBUTTONDOWN:
            if btn_play.rect.collidepoint(e.pos):
                en_menu = False
                mixer.music.play()

# ==========================================
# 2. BUCLE PRINCIPAL DEL JUEGO
# ==========================================
gameover = False

while run:
    window.blit(background, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_SPACE:
            if not gameover:
                fire_sound.play()
                madokami.fire()

    # Colisiones balas y enemigos (True, True elimina bala y enemigo al chocar)
    sprite.groupcollide(enemigos, bullets, True, False)

    # REAPARICIÓN AUTOMÁTICA: Si no quedan enemigos, aparece una nueva oleada
    if len(enemigos) == 0 and not gameover:
        crear_oleada(5) # Genera 5 nuevos enemigos aleatorios

    if not gameover:
        madokami.update()
        enemigos.update(madokami)
        enemigos.draw(window)
        bullets.update()
        bullets.draw(window)

        if sprite.spritecollide(madokami, enemigos, False):
            gameover = True
            madokami.image = transform.scale(image.load("explosion.png"), (100, 100))
            mixer.music.stop()

    madokami.reset()
    display.update()
    time.delay(100)