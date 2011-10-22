#!/usr/bin/python
import sys, pygame
import random
import time
pygame.init()

class GameData:
    def __init__(self):
        self.size = width, height = 640, 480
        self.speed = [0.5, 0.5]
        self.black = 0, 0, 0
        self.white = 255,255,255
        self.PADDLE_HEIGHT = 10
        self.PADDLE_WIDTH = 32
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.image.load("background.jpg").convert()
        self.backrect = self.background.get_rect()
        
    def get_paddle_height(self):
        return self.PADDLE_HEIGHT
    
    def get_paddle_width(self):    
        return self.PADDLE_WIDTH
        
    def get_size(self):
        return self.size
        
    def get_window_width(self):
        return self.size[0]
        
    def get_window_height(self):
        return self.size[1]
        
    def get_speed(self):
        return self.speed
    
    def get_ball_speed_x(self):
        return self.speed[0]
        
    def set_ball_speed_x(self, x):
        self.speed[0] = x
        
    def get_ball_speed_y(self):
        return self.speed[1]
        
    def set_ball_speed_y(self, y):
        self.speed[1] = y
    
    def get_color(self):
        return (self.white, self.black)

    def get_screen(self):
        return self.screen
    
    def set_screen(self, x):
        self.screen=x
        
    def get_background(self):
        return self.background
        
    def set_background(self, x):
        self.background = x
        
    def get_backrect(self):
        return self.backrect
        
    def set_backrect(self, x):
        self.backrect = x
        

    screen = property(fget=get_screen, fset=set_screen)
    background = property(fget=get_background, fset=set_background)
    backrect = property(fget=get_backrect, fset=set_backrect)
    ball_speed_x = property(fget=get_ball_speed_x, fset=set_ball_speed_x)
    ball_speed_y = property(fget=get_ball_speed_y, fset=set_ball_speed_y)

class paddle:
    
    def __init__(self,x,y, surface):
        self.width=45
        self.height=10
        self.xvelocity=0
        self.Position = [x,y]
        self.rect = pygame.Rect(x, y, self.width, self.height)
        #(left, top), (width, height)

    def Pos(self): 
        return self.Position

    def xvel(self,x):
        self.xvelocity=x
        return

    def changeX(self, x):
        self.Position[0]=x

    def updatePos(self):
        if ((self.Position[0]+self.xvelocity)>640-self.width):
            self.Position[0]=640-self.width
        elif ((self.Position[0]+self.xvelocity)<0):
            self.Position[0]=0
        else:
            self.Position[0]=self.Position[0]+self.xvelocity
        
        #change this to correctness
        #self.rect=pygame.Rect(self.Position[0], self.Position[1], self.width, self.height)
        self.rect=self.rect.move(self.Position[0], self.Position[1])
        return self.Position        

    def get_rect(self):
        return self.rect
    

class cball:
    def __init__(self,pos):
        self.x=pos[0]
        self.y=pos[1]

 
def mainLoop():
    random.seed(time.time())
    gamedata = GameData()
    player = paddle(gamedata.get_window_width()/2, gamedata.get_window_height()-20, gamedata.get_screen())
    ball = cball(player.Pos())
    #back = background()
    ai = paddle(gamedata.get_window_width()/2, 20, gamedata.get_screen())
    
    
    gamedata.screen.blit(gamedata.background, gamedata.backrect)
    pygame.draw.rect(gamedata.screen, gamedata.get_color()[1], player.get_rect(), 0)
    pygame.draw.rect(gamedata.screen, gamedata.get_color()[1], ai.get_rect(), 0)
    pygame.draw.circle(gamedata.screen, gamedata.get_color()[0], (ball.x,ball.y), 5, 0)
    pygame.display.flip()
    rand=0
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "QUIT Event"
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print "K_ESCAPE Event"
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # velocity to right
                    player.xvel(2)
                    print "K_RIGHT Event"
                elif event.key == pygame.K_LEFT:
                    #velocity to left
                    player.xvel(-2)
                    print "K_LEFT Event"
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    player.xvel(0)

                    
        aiPos = ai.Pos()
        #print aiPos[0]
        
    
        # if not in x alignment with ball.x then keep moving    
        if gamedata.get_speed()[1]>0:
            if aiPos[0] > (ball.x - rand):
                ai.xvel(-2)
            if aiPos[0] < (ball.x + rand):
                ai.xvel(2)
        else:
            rand=int(100*random.random())%30
            ai.xvel(0)
                
        if aiPos[0] < 0: ai.changeX(3) 
        if aiPos[0] >= gamedata.get_window_width(): ai.changeX(gamedata.get_window_width()-30)  
            
    
        #ball.ballrect = ball.ballrect.move(speed)
        ball.x = ball.x + gamedata.get_speed()[0]
        ball.y = ball.y + -gamedata.get_speed()[1]
        #if ball.ballrect.left < 0 or ball.ballrect.right > width:
        if ball.x < 0 or ball.x > gamedata.get_window_width(): 
            gamedata.get_speed()[0] = -gamedata.get_speed()[0]
        #if ball.ballrect.top < 0 or ball.ballrect.bottom > height:
        if ball.y < 0 or ball.y > gamedata.get_window_height():
            gamedata.get_speed()[1] = -gamedata.get_speed()[1]

        # check to see if hit player paddle
        # and whether the ball is behind paddle or coming in front
        # left of paddle is beginning of position x
        # top of paddle is beginning of position y
        if gamedata.get_speed()[1] < 0:
            if ball.y >= player.Position[1] and ball.y <= player.Position[1]+gamedata.get_paddle_height():
                if ball.x >= player.Position[0]-2 and ball.x <= player.Position[0] + gamedata.get_paddle_width():
                    gamedata.get_speed()[1]=-gamedata.get_speed()[1]
                    print "player Paddle Hit"

        #check to see if ai paddle hit
        if gamedata.get_speed()[1] > 0:
            if ball.y >= ai.Position[1] and ball.y <= ai.Position[1]+gamedata.get_paddle_height():
                if ball.x >= ai.Position[0]-2 and ball.x <= ai.Position[0] + gamedata.get_paddle_width():
                    gamedata.get_speed()[1]=-gamedata.get_speed()[1]
                    print "ai paddle hit"

        #gamedata.screen.fill(white)
        gamedata.screen.blit(gamedata.background, gamedata.backrect)
        gamedata.screen.blit(pygame.Surface(ai.get_rect().size).convert_alpha(), ai.updatePos())
        gamedata.screen.blit(pygame.Surface(player.get_rect().size).convert_alpha(), player.updatePos())
        #gamedata.screen.blit(ball.ball, (ball.x,ball.y))
        
        print ball.x
        pygame.draw.circle(gamedata.screen, gamedata.get_color()[0], (int(ball.x), int(ball.y)), 5, 0)
        pygame.display.flip()

if __name__ == "__main__":
    mainLoop()
