import pygame
import random
import math
from pygame import mixer

pygame.init()
screen1 = pygame.display.set_mode((800, 555))  # 2 brackets are necessary

running = False
out = True


def gameloop():
    # from threading import Timer
    global running
    # initialize the pygame
    mixer.init()
    clock = pygame.time.Clock()
    mixer.music.load(r'material\background_music.mp3')
    mixer.music.play(-1)
    screen = pygame.display.set_mode((799, 600))  # 2 brackets are necessary
    pygame.display.set_caption('space invaders')
    icon = pygame.image.load(r'material\monster.png')
    pygame.display.set_icon(icon)
    # score

    score_values = 0
    high = pygame.font.Font('freesansbold.ttf', 18)
    font = pygame.font.Font('freesansbold.ttf', 32)
    textx = 10
    texty = 10
    font_over = pygame.font.Font('freesansbold.ttf', 64)
    a = ""

    def show_score(x, y):
        score = font.render('your score: ' + str(score_values) + a, True, (255, 255, 255))
        screen.blit(score, (x, y))

    # background
    background = pygame.image.load(r'material\space2.png')

    # game over
    def game_over():
        global running
        global a
        over = font_over.render('GAME OVER', True, (255, 255, 255))
        screen.blit(over, (200, 250))
        fh = open(r'high_score.txt', 'r')
        se = fh.readline()
        s = se.split()
        s = s[0]
        s = int(s)
        dis = high.render(f'HIGH SCORE: {s}', True, (255, 255, 0))
        screen.blit(dis, (500, 90))
        mixer.music.stop()
        dist = high.render('press r to replay', True, (0, 0, 0))
        screen.blit(dist, (430, 330))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                gameloop()
        if s < score_values:
            fh.close()
            fh = open(r'high_score.txt', 'w')
            fh.write(f'{score_values}')
            a = " is the new HIGH SCORE"

    # player

    playerimage = pygame.image.load(r'material\player.png')
    playerX = 369
    playerY = 479
    playerY_change = 0
    playerX_change = 0

    # enemy

    enemyimg = []
    enemyX = []
    enemyy = []
    enemyY_change = []
    enemyX_change = []

    for i in range(6):
        enemyimg.append(pygame.image.load(r'material\monster.png'))
        enemyX.append(random.randint(0, 735))
        enemyy.append(random.randint(50, 150))
        enemyY_change.append(40)
        enemyX_change.append(3)

    # bullet
    bullet = pygame.image.load(r'material\bullet.png')
    bulletX = 369
    bulletY = 479
    bulletY_change = 8
    bulletX_change = 0
    bullet_state = "ready"

    def player(x, y):
        screen.blit(playerimage, (x, y))

    def enemy(x, y, i):
        # global i
        screen.blit(enemyimg[i], (x, y))

    def fire(x, y):
        global bullet_state
        bullet_state = 'fire'
        screen.blit(bullet, (x + 16, y + 10))

    def iscollison(enemyx, enemyy, bulletx, bulletY):
        distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

    def iscolliso(enemyx, enemyy, playerX, playerY):
        distance1 = math.sqrt((math.pow(enemyx - playerX, 2)) + (math.pow(enemyy - playerY, 2)))
        if distance1 < 27:
            return True
        else:
            return False

    while running:
        # red blue green        screen.fill((22, 2, 1))
        # background image
        screen.blit(background, (0, 0))
        # playerY-=0.02
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    playerX_change = -5.5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = 5.5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    playerY_change = 5
                    playerY += playerY_change
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    playerY_change = -5

                if event.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        bulletX = playerX
                        bulletY = playerY
                        fire(bulletX, bulletY)
                        bullet_state = 'fire'
                        bullet_sound = mixer.Sound(r'material\gunshot.WAV')
                        bullet_sound.play()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = 0

                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    playerY_change = 0
        playerY += playerY_change
        playerX += playerX_change
        # bulletX = playerX
        if playerX <= 0:
            playerX = 0
        if playerX >= 736:
            playerX = 736
        if playerY <= 300:
            playerY = 300
        if playerY > 536:
            playerY = 536

        for i in range(6):
            if enemyy[i] > 440:
                for j in range(6):
                    enemyy[j] = 2000
                game_over()
                bullet_state = 'stopped'

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4.0
                enemyy[i] += enemyY_change[i]

            if enemyX[i] >= 736:
                enemyX_change[i] = -4.0
                enemyy[i] += enemyY_change[i]
            collision = iscollison(enemyX[i], enemyy[i], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = 'ready'
                score_values += 1
                enemyX[i] = random.randint(0, 735)
                enemyy[i] = random.randint(50, 150)
                explosion = mixer.Sound(r'material\invaderkilled.wav')
                explosion.play()
            enemy(enemyX[i], enemyy[i], i)
            collisio = iscolliso(enemyX[i], enemyy[i], playerX, playerY)
            if collisio:
                game_over()
                for j in range(6):
                    enemyy[j] = 2000
                explosion = mixer.Sound(r'material\explosion.wav')
                explosion.play()
                game_over()
                bullet_state = 'stopped'
                playerX = 12223
                playerY = 5456525

        if bulletY <= 0:
            bulletY = 480
            bullet_state = 'ready'

        if bullet_state == 'fire':
            fire(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        # speed_increase()
        show_score(textx, texty)
        pygame.display.update()


while out:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            out = False
    screen1.fill((255, 255, 255))

    high = pygame.font.Font('freesansbold.ttf', 18)
    message = high.render(" welcome to space invaders game", True, (0, 0, 0))
    message2 = high.render(
        " in this game there will be 6 enemies moving around and they slides down after touching the",
        True, (0, 0, 0))
    message3 = high.render(" corner and as soon as the enemies touches the line", True, (0, 0, 0))
    message4 = high.render(" --game over--", True, (0, 0, 0))
    message5 = high.render('controls**_', True, (0, 0, 0))
    message6 = high.render('<space> - shoot', True, (0, 0, 0))

    message7 = high.render('<arrow keys>- to control the player', True, (0, 0, 0))
    message8 = high.render("don not let the enemy touch you", True, (0, 0, 0))
    message9 = high.render("**press 'a' to continue:-", True, (0, 0, 0))
    message10 = high.render("you have to shoot them before they reach to the line ", True, (0, 0, 0))
    screen1.blit(message, (280, 10))
    screen1.blit(message2, (0, 30))
    screen1.blit(message3, (0, 50))
    screen1.blit(message4, (300, 70))
    screen1.blit(message10, (0, 90))
    screen1.blit(message5, (300, 110))
    screen1.blit(message6, (300, 130))
    screen1.blit(message7, (300, 150))
    screen1.blit(message8, (0, 170))
    screen1.blit(message9, (300, 190))

    for events in pygame.event.get():
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_a:
                out = False
                running = True
                gameloop()
    pygame.display.flip()
