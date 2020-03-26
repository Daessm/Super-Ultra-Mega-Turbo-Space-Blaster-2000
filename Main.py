import math
import random
import pygame
from pygame import mixer

# Initialize Pygame and Pygame font
pygame.init()
pygame.font.init()

# Create the window
screen = pygame.display.set_mode((800,600))

# Background
background = pygame.image.load('SI_Background.png')

# Background sound
mixer.music.load('SI_Music.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('SI_Icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('SI_PlayerShip.png')
playerX = 370
playerY = 480
playerX_change = 0

# Aliens
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 10

for i in range(num_of_aliens):
    alienImg.append(pygame.image.load('SI_AlienShip.png'))
    alienX.append(random.randint(0,735))
    alienY.append(-40)
    alienX_change.append(4)
    alienY_change.append(40)

# Laser
# Ready - You can't see the laser on the screen
# Fire - The laser is currently in motion
laserImg = pygame.image.load('SI_Laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 10
laser_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('Batman.ttf',32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

over_font = pygame.font.Font('Batman.ttf',100)
over_font2  = pygame.font.Font('Batman.ttf',55)

def game_over_text():
    screen.fill((0,0,0))
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    over_text2 = over_font2.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(over_text, (50, 250))
    screen.blit(over_text2, (250, 350))

def player(x, y):
    screen.blit(playerImg, (x, y))

def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))

def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg,(x+16,y+10))

def isCollision(alienX, alienY, laserX, laserY):
    distance = math.sqrt((math.pow(alienX - laserX,2)) + (math.pow(alienY - laserY,2)))
    if distance < 27:
        return True
    else:
        return False
# Game loop
running = True

while running:

    # RGB background color setup
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background,(0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it's right or left arrow
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if laser_state is "ready":
                    laser_sound = mixer.Sound('SI_LaserSFX.wav')
                    laser_sound.play()
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking the boundaries of the spaceship so it doesn't move out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Alien movement
    for i in range(num_of_aliens):

        # Game over
        if alienY[i] > 440:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]

        if alienX[i] <= 0:
            alienX_change[i] = 4
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -4
            alienY[i] += alienY_change[i]
            

        # Collision
        collision = isCollision(alienX[i], alienY[i], laserX, laserY)
        if collision:
            laserY = 480
            laser_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0,735)
            alienY[i] = -40

        
        alien(alienX[i], alienY[i], i)

    # Laser movement
    if laserY <= -50:
        laserY = 480
        laser_state = "ready"

    if laser_state is "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()