#Bibliotecas Importadas
import pygame
import math
import random
pygame.init()

#Tamanho do Ecrã
Screen_Width = 1000
Screen_Height = 380

Screen = pygame.display.set_mode((Screen_Width, Screen_Height))
pygame.display.set_caption('Heavy Ordnance')

clock = pygame.time.Clock()
FPS = 60

Level = 1
Level_Difficulty = 0
Max_Enemies = 10
Enemy_Timer = 1000
Last_Enemy = pygame.time.get_ticks()
Enemies_Alive = 0

#Imagens do Jogo
bg = pygame.image.load('img/Background.png').convert_alpha()
Cannon3 = pygame.image.load('img/Cannon3.png').convert_alpha()
Cannon2 = pygame.image.load('img/Cannon2.png').convert_alpha()
Cannon1 = pygame.image.load('img/Cannon1.png').convert_alpha()
Bullet_img = pygame.image.load('img/Bullet.png').convert_alpha()


enemy_animations = []
enemy_types = ['BoatS', 'BoatM', 'BoatL', 'BoatXL']
enemy_Health = [1]


animation_types = ['Walk', 'Attack', 'Death']

for enemy in enemy_types:
    #Animação
    animation_list = []
    for animation in animation_types:
        temp_list = []
        number_of_frames = 3
        for i in range(number_of_frames):
            img = pygame.image.load(f'img/Enemies/{enemy}/{animation}/{i}.png').convert_alpha()
            temp_list.append(img)
        animation_list.append(temp_list)
    enemy_animations.append(animation_list)


#Cores
WHITE = (255, 255, 255 )

#Classes:

    #Classe Rato:
class Mouse_Pointer():
    def __init__(self, scale):
        image = pygame.image.load('img/Target.png').convert_alpha()
        self.rect = self.image.get_rect()

        #Esconder rato
        pygame.mouse.set_visible(False)

    def draw(self):
        mx, my, = pygame.mouse.get_pos()
        self.rect.center = (mx, my)
        screen.blit(self.image, self.rect)

    #Classe Enemies:
class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True 
        self.speed = speed
        self.health = health
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000
        self.animation_list = animation_list
        self.frame_index = 0

        self.action = 0 
        #0 é andar; 1 é atacar; 2 é morrer

        self.update_time = pygame.get_ticks()

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
    def update(self, surface, target, bullet_group):

        if self.alive:

            #Colisão com balas
            if pygame.sprite.spritecollide(self, bullet_group, True):
                #Baixar vida do inimigo
                self.health -= 1

            #Verificar se o enemy chegou ao canhão
            if self.rect.right > target.rect.left:
                self.update_action(1)

            #Movimento 
            if self.action ==0:
                #Update da posição de enemy
                self.rect.x += speed

            #Ataque
            if self.action == 1:
                #Verificar se tempo suficiente passou
                if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                    target.health -= 1
                    if target.health < 0:
                        target.health = 0
                    self.last_attack = pygame.time.get_ticks()

            #Verificação se a vida é 0
            if self.health <= 0:
                self.update_action(2)
                target.score += 5
                self.alive = False



            self.update_animations()

            Surface.blit(self.image, self.rect)

    def update_animation(self):

        #Atualiza Animação
        Animation_Cooldown = 50
        #Atualiza imagem consoante acção
        self.image = self.animation_list[self.action][self.frame_index]
        #Verificação de quanto tempo passou
        if pygame.time.get_ticks() - self.update_time > Animation_Cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #Reset da animação
        if self.frame_index >= len(self.animation_list[sef.action]):
            if self.action ==2:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                self.frame_index = 0

    def update_Action(self, new_action):
        #Verificar se a nova acção é igual à anterior
        if new_action != self.action:
            self.action = new_action
            self.frame_index =0
            self.update_date = pygame.time.get_ticks()


    #Classe Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get.rect()
        self.rect.x = x 
        self.rect.y = y 
        self.angle = math.radians(angle) #Conversao do angulo a radianos
        self.speed = 10
        #calculaçao da velocidade baseada no angulo
        self.dx = math.cos(self.angle) * self.speed
        self.dy = - (math.sin(self.angle) * self.speed)

    def update(self):

        #Out of Bounds Bullets
        if self.rect.right < 0 or self.rect.left > Screen_Widht or self.rect.bottom < 0 or self.rect.top > Screen_Height:
            self.kil()

        #Movimento da bala
        self.rect.x += self.dx
        self.rect.y += self.dy



    #Classe Canhao

class Cannon():
    def _init__(self, image3, image2, image1, x, y, scale):
        self.health = 3
        self.max_health = self.health
        self.fired = False
        self.score = 0

        widht = image3.get_widht()
        height = image3.get_height()

        self.image3 = pygame.transform.scale(image3,(int(widht * scale), int(height *scale)))
        self.image2 = pygame.transform.scale(image2,(int(widht * scale), int(height *scale)))
        self.image1 = pygame.transform.scale(image1,(int(widht * scale), int(height *scale)))
        self.rect = self.image3.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def Shoot(self):
        pos = pygame.mouse.get_pos()
        x_Dist = pos[0] - self.rect.midleft[0]
        y_Dist = - (pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_Dist, x_Dist))
        
        #Obter clicks
        if pygame.mouse.get_pressed()[0] and self.fired == False:
            self.fired = True
            Bulelt = Bullet(Bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            Bullet_Group.add(Bullet)

        #Reset dos Clicks
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False



    def draw(self):
        #Que imagem usar a base da vida
        if self.health <= 1:
            self.image = self.image1
        elif self.health <= 2:
            self.image = self.image2
        else:
            self.image = self.image3

        Screen.blit(self.image, self.rect)

#Cannon
Cannon = Cannon(Cannon3, Cannon2, Cannon1,  Screen_Widht - 250, Screen_Height - 300, 0)

#Grupo Bullets
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#Enemies
Enemy_1 = Enemy(enemy_health[0], enemy_animations[0], 200, Screen_Height - 100, 1)
enemy_animations.add(Enemy_1)

#Loop de Jogo
run = True
while run:       
    clock.tick(FPS)

    #Imagem de Fundo
    Screen.blit(bg, (0, 0)) 


    #Cannon
    Cannon.draw()
    Cannon.Shoot()

    #Bullets
    Bullet_Groups.update()
    Bullets_Group.draw(Screen)
    print(len(Bullet.Group))

    #draw Enemies
    enemy_group.update(Screen, Cannon, bullet_group)

    #Create Enemies
    if len(enemy_group) < Max_Enemies:
        if pygame.time.get_ticks() -Last_Enemy < EnemY_Timer:
            E = random.randit(0, len(enemy_types) -1)
            Enemy = Enemy(enemy_health[E], enemy_animations[E], -100, Screen_Height - 100, 1)
            enemy_animations.add(Enemy)
            #Reset do temporizador
            last_enemy = pygame.time.get_ticks()
            #Increase Level Difficulty
            Level_Difficulty -= Enemy_Timer

    #Draw Mouse
    Mouse_Pointer.draw()

    #Sistema de Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Atualização da janela
    pygame.display.update()

pygame.quit