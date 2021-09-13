import pygame
import os


pygame.init()
LARGURA = 1000
ALTURA = 600
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Gundam shooter")
ROSA = (255, 51, 153)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VEL = 7
VEL_BALA = 7
MAX_BALAS = 5
FPS = 60
tempo = 0
zaku1_hit = pygame.USEREVENT + 1
BARREIRA = pygame.Rect(LARGURA//2 - 5, 0, 10, ALTURA)
GUNDAM_LARGURA, GUNDAM_ALTURA = 100, 100
ZAKU_LARGURA, ZAKU_ALTURA = 100, 100
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('ASSETS', 'background.png')), (LARGURA, ALTURA))
GUNDAM_IMAGEM = pygame.image.load(os.path.join('ASSETS', 'gundam.png'))
GUNDAM = (pygame.transform.scale(GUNDAM_IMAGEM, (GUNDAM_LARGURA, GUNDAM_ALTURA)))
ZAKU_CHAR_IMAGEM = pygame.image.load(os.path.join('ASSETS', 'zaku_char.png'))
ZAKU1 = (pygame.transform.scale(ZAKU_CHAR_IMAGEM, (ZAKU_LARGURA, ZAKU_ALTURA)))
DISPARO_SOM = pygame.mixer.Sound('ASSETS/TIRO_LASER.mp3')
EXPLOSAO_SOM = pygame.mixer.Sound('ASSETS/EXPLOSÃO.mp3')


def desenhar_janela(gundam, zaku1, balas):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, PRETO, BARREIRA)
    WIN.blit(GUNDAM, (gundam.x, gundam.y))
    WIN.blit(ZAKU1, (zaku1.x, zaku1.y))
    for bullet in balas:
        pygame.draw.rect(WIN, ROSA, bullet)
    pygame.display.update()


def gundam_handle_movement(keys_pressed, gundam):
    if keys_pressed[pygame.K_LEFT] and gundam.x - VEL > 0:  # LEFT
        gundam.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and gundam.x + VEL + gundam.width < BARREIRA.x:  # RIGHT
        gundam.x += VEL
    if keys_pressed[pygame.K_UP] and gundam.y - VEL > 0:  # UP
        gundam.y -= VEL
    if keys_pressed[pygame.K_DOWN] and gundam.y + VEL + gundam.height < ALTURA - 15:  # DOWN
        gundam.y += VEL


def zaku1_handle_movement(zaku1):
    if zaku1.y + 5 + zaku1.height < ALTURA:
        zaku1.y += 5
    if zaku1.y + 5 + zaku1.height >= ALTURA:
        while zaku1.y > 0:
            zaku1.y -= 3
    if zaku1.x + 2 + zaku1.width > LARGURA//2 + 180:
        zaku1.x -= 2
    if zaku1.x + 2 + zaku1.width <= LARGURA//2 + 180:
        while zaku1.x < LARGURA - 200:
            zaku1.x += 2


def handle_bullets(balas, zaku1):
    for bullet in balas:
        bullet.x += VEL_BALA
        if zaku1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(zaku1_hit))
            balas.remove(bullet)
        elif bullet.x > LARGURA:
            balas.remove(bullet)


def main():
    gundam = pygame.Rect(100, 300, GUNDAM_LARGURA, GUNDAM_ALTURA)
    zaku1 = pygame.Rect(1000, 100, ZAKU_LARGURA, ZAKU_ALTURA)
    balas = []
    zaku_hp = 30
    print('Movimentação: SETAS/ Tiro: BARRA DE ESPAÇO/ Munição: 3')
    print('zaku_hp:', zaku_hp)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(balas) < MAX_BALAS:
                    bullet = pygame.Rect(
                        gundam.x + gundam.width, gundam.y + gundam.height // 2 - 2, 10, 5)
                    balas.append(bullet)
                    DISPARO_SOM.play()
            if event.type == zaku1_hit:
                zaku_hp -= 1
                print(zaku_hp)
                EXPLOSAO_SOM.play()

        if zaku_hp <= 0:
            print('Você ganhou!')
            break
        tempo = int(pygame.time.get_ticks())
        if tempo >= 60000:
            print('Zaku ganhou.')
            break

        keys_pressed = pygame.key.get_pressed()
        gundam_handle_movement(keys_pressed, gundam)
        zaku1_handle_movement(zaku1)
        handle_bullets(balas, zaku1)
        desenhar_janela(gundam, zaku1, balas)

    pygame.quit()


main()
