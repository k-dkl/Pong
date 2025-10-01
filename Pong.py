import pygame
import random
from Physics import *

## Redo the classes velocity and position attributes so they are stored using a pygame.Vector2
## wil also have to rewrite some functions in Physics.py
## so replace self.v, slef.v_y and seld.v_x with v = pygame.Vector(0, 0)
## and replace seld.x and self.y with self.s/self.pos = pygame.Vecot(0, 300)

pygame.init()

global dimensions
dimensions = pygame.Vector2(800, 600)

global turn
turn = 1

screen = pygame.display.set_mode(dimensions)
clock = pygame.time.Clock()
framerate = 60
padding = 20 # how many pixels of space to leave on the top and bottom of the page

class Paddle:
    def __init__(self, x=0, y=None, width=20, height=125):
        if y == None:
            y = (dimensions.y - height) /2
        self.v = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(x, y)
        self.size = pygame.Vector2(width, height)
        self.rect = pygame.Rect(*self.pos, *self.size)

class Ball:
    def __init__(self,):
        self.v = pygame.Vector2(0, 0)
        self.size = pygame.Vector2(20, 20)
        self.pos = pygame.Vector2(
            (dimensions.x - self.size.x) / 2, # centres the ball
            (dimensions.y - self.size.y) / 2 
        )
        self.rect = pygame.Rect(*self.pos, *self.size)

def updatePaddle(paddle):
    speedLimit(paddle)

    if not withinYBounds(paddle, dimensions, padding):
        paddle.v.y = 0
        if paddle.pos.y < padding:
            paddle.pos.y = padding
        else:
            paddle.pos.y = dimensions.y - paddle.size.y - padding

    paddle.rect = pygame.Rect(*paddle.pos, *paddle.size)    
    paddle.pos.y += paddle.v.y

def updateBall(ball):
    ball.pos += ball.v
    ball.rect = pygame.Rect(*ball.pos, *ball.size)

    if not withinYBounds(ball, dimensions, padding): # wall collision check
        ball.v.y *= -1

def makeRect(obj):
    return pygame.Rect(obj.pos.x, obj.pos.y, obj.size.x, obj.size.y)

class Game:
    global turn
    
    def __init__(self):
        self.reset()

    def reset(self):
        self.playerL = Paddle()
        self.playerL.pos.x = self.playerL.size.x * 2
        self.playerR = Paddle()
        self.playerR.pos.x = dimensions.x - self.playerR.size.x * 3
        self.ball = Ball()
        self.ball.v = pygame.Vector2(5 if turn == 1 else -5, 2) # 3 if self.turn == 1 else -3

    def inputHandler(self, keys):
        if keys[pygame.K_UP]:
            accelY(self.playerR, -1)
        elif keys[pygame.K_DOWN]:
            accelY(self.playerR)
        else:
            applyFriction(self.playerR)

        if keys[pygame.K_w]:
            accelY(self.playerL, -1)
        elif keys[pygame.K_s]:
            accelY(self.playerL)
        else:
            applyFriction(self.playerL)

    def update(self):
        updatePaddle(self.playerR)
        updatePaddle(self.playerL)
        updateBall(self.ball)
        # add in an update func for the ball here as well
    
    def draw(self):
        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (255, 255, 255), self.playerL.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.playerR.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.ball.rect)

        pygame.display.update()

    def winCheck(self, ball, dimensions):
        global turn

        if not withinXBounds(ball, dimensions):
            if ball.pos.x < 30:
                print('Right player wins')
                turn = 0
            elif ball.pos.x > dimensions.x - 30:
                print('Left player wins')
                turn = 1
            self.reset()

run = True

game = Game()

while run: # Game loop
    
    for event in pygame.event.get(): # Event checks

        if event.type == pygame.QUIT: # Exit condition
            run = False

    keys = pygame.key.get_pressed() # Key press checks

    game.inputHandler(keys)
    game.update()
    collisionCheck(game.ball, game.playerL)
    collisionCheck(game.ball, game.playerR)
    game.draw()
    game.winCheck(game.ball, dimensions)

    clock.tick(framerate)

pygame.quit()