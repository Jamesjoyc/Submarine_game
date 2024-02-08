import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

pygame.font.init()
sea_level = 350
width = 1400
height = 900
Window = pygame.display.set_mode((width, height))


pygame.display.set_caption("Mine Your Head")
BLUE = (15, 94, 156)
SKY = (135, 206, 235)

moving_sound = pygame.mixer.Sound(os.path.join('Assets', 'move_around.mp3'))
sonar_sound = pygame.mixer.Sound(os.path.join('Assets', 'sonar.mp3'))
bubbles_sound = pygame.mixer.Sound(os.path.join('Assets', 'bubbles.mp3'))
engine_sound = pygame.mixer.Sound(os.path.join('Assets', 'engine.mp3'))
sub_shoot = pygame.mixer.Sound(os.path.join('Assets', 'sub_shoot.mp3'))
engine_sound.set_volume(0.2)
engine_sound.play(-1)
bubbles_sound.set_volume(0)
bubbles_sound.play(-1)
horizontal_speed = 4
vertical_speed = 1
NukeSpeed = 5
nuke_list = []


sonar_sound.set_volume(0.5)
cloud = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'cloud.png')),(640,360))
enemy_ship = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'ship3.png')),(160,90))
nuke = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'nuke2.png')),(50,50))
submarine10 = pygame.image.load(os.path.join('assets', 'sub11.png'))


class Submarine:
    def __init__(self, x, y, width , height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 100


class boat:
    def __init__(self,x ,y, width, height):
        self.x = x
        self.y = y
        self.widthboat = width
        self.heightboat = height


def window(sub,boat):
    Window.fill(BLUE)

    pygame.draw.rect(Window, SKY, (0, 0, 1400, sea_level))
    # Window.blit(enemy_ship, (500, sea_level-75))

    Window.blit(cloud, (0, 0, ))
    Window.blit(cloud, (400, -56))
    Window.blit(cloud, (800, 60))


    submarine_image = pygame.transform.scale(submarine10,(sub.width, sub.height))
    Window.blit(submarine_image, (sub.x, sub.y))
    Window.blit(enemy_ship, (boat.x, boat.y))


def sub_sound():
    pygame.mixer.Sound(os.path.join('Assets',  'move_around.mp3'))

def health_bar(sub):
    GameFont = pygame.font.SysFont('Comic Sans MS', 20)

    Window.blit(GameFont.render('Health:', False, (000, 000, 000)), (20, 0))
    pygame.draw.rect(Window, (200, 000, 000),(20,30,sub.health * 3,50))



def submarine_handle_movement(keys_pressed, sub,boat):
    if keys_pressed[pygame.K_a] and sub.x - horizontal_speed > -25:
        sub.x -= horizontal_speed
        engine_sound.set_volume(0.7)

    if keys_pressed[pygame.K_d] and sub.x + horizontal_speed + sub.width < width + 25:
        sub.x += horizontal_speed
        engine_sound.set_volume(0.7)

    if keys_pressed[pygame.K_w] and sub.y - vertical_speed >= sea_level - 90:
        sub.y -= vertical_speed
        engine_sound.set_volume(0.7)

    if keys_pressed[pygame.K_s] and sub.y + vertical_speed + sub.height < height + 45:
        sub.y += vertical_speed
        bubbles_sound.set_volume(0.5)

    if not keys_pressed[pygame.K_s]:
        bubbles_sound.set_volume(0)

    if not keys_pressed[pygame.K_a] and not keys_pressed[pygame.K_d] and not keys_pressed[pygame.K_w]:
        engine_sound.set_volume(0.2)

    if keys_pressed[pygame.K_ESCAPE]:
        pygame.quit()

    boat.x += random.randint(1,2)

def handle_bullets(nuke_list, nuke, boat,sub):
    bullets_to_remove = []

    for bullet in nuke_list:
        bullet.x += NukeSpeed
        bullet.y -= 0



        torpedo = pygame.Rect( (bullet.x, bullet.y + 15, 50, 15))
        boatrect = pygame.Rect( (boat.x, boat.y, 155, 90))
        Window.blit(nuke, (bullet.x, bullet.y))

        if bullet.x > width:
            bullets_to_remove.append(bullet)

        if torpedo.colliderect(boatrect):
            bullets_to_remove.append(bullet)
            print("shot")
            sub.health -= random.randint(15,50)

    for bullet in bullets_to_remove:
        nuke_list.remove(bullet)


def handle_collisions(boat, sub):
    boatrect = pygame.Rect (boat.x, boat.y, 155, 90)
    subrect = pygame.Rect(sub.x + 20, sub.y + 55, 110, 50)

    if boatrect.colliderect(subrect):
        sub.health -= 5
        print(sub.health)





def main():
    sub = Submarine(359, 350, 150, 150 )
    boat = Submarine(400,sea_level-80, 300,200)
    sonar_sound.play()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(nuke_list) <= 2:
                    bullet = pygame.Rect(sub.x + sub.width, sub.y + sub.height// 2 -4,10,5)
                    nuke_list.append(bullet)
                    sub_shoot.play()

        keys_pressed = pygame.key.get_pressed()
        submarine_handle_movement(keys_pressed, sub,boat)

        handle_bullets(nuke_list, nuke, boat, sub)
        handle_collisions(boat,sub)
        pygame.display.update()
        window(sub, boat)
        health_bar(sub)
        if sub.health <= 0:
            pygame.quit()

    pygame.quit()
    #maybe itll comit


main()