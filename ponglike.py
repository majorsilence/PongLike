#!/usr/bin/python
import sys, pygame
import random
import time
pygame.init()

class GameData:
    def __init__(self):
        self.size = width, height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.image.load("background.jpg").convert()
        self.backrect = self.background.get_rect()
        
    def get_size(self):
        return self.size
        
    def get_window_width(self):
        return self.size[0]
        
    def get_window_height(self):
        return self.size[1]
        
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

class paddle:
    
    def __init__(self,x,y):
        self.width=45
        self.height=10
        self.xvelocity=0
        self.XPos = x
        self.YPos = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.paddlespeed = 5
        
    def get_paddle_height(self):
        return 10
    
    def get_paddle_width(self):    
        return 32
        
    def xvel(self,x):
        self.xvelocity=x
        return

    def updatePos(self):
        if ((self.XPos+self.xvelocity)>640-self.width):
            self.XPos=640-self.width
        elif ((self.XPos+self.xvelocity)<0):
            self.XPos=0
        else:
            self.XPos=self.XPos+self.xvelocity
        
        #change this to correctness
        #self.rect=pygame.Rect(self.Position[0], self.Position[1], self.width, self.height)
        self.rect=self.rect.move(self.XPos, self.YPos)
     

    def get_rect(self):
        return self.rect
    
    def draw(self, screen):
        self.updatePos()
        screen.blit(pygame.Surface(self.rect.size).convert_alpha(), (self.XPos, self.YPos) )

class cball:
    def __init__(self,x, y):
        self.x=x
        self.y=y
        self.XSpeed = 2.5
        self.YSpeed = 2.5
        
    def draw(self, surface):
        pygame.draw.circle(surface, (255,255,255), [int(self.x), int(self.y)], int(5), int(0))
    
 
 
class MainGame:
    def __init__(self):
        random.seed(time.time())
        self.gamedata = GameData()
        self.player = paddle(self.gamedata.get_window_width()/2, self.gamedata.get_window_height()-20)
        
        self.ball = cball(self.player.XPos, self.player.YPos)
        #back = background()
        self.ai = paddle(self.gamedata.get_window_width()/2, 20)
        
        self.paddlespeed = 5
 
    def __drawscreen(self):
        self.gamedata.screen.blit(self.gamedata.background, self.gamedata.backrect)
        self.player.draw(self.gamedata.screen)
        self.ai.draw(self.gamedata.screen)
        self.ball.draw(self.gamedata.screen)
        pygame.display.flip()
            
    def __moveassets(self, ball, player, ai, gamedata):
        rand = 0
        # if not in x alignment with ball.x then keep moving    
        if ball.YSpeed>0:
            if ai.XPos > (ball.x - rand):
                ai.xvel(-ai.paddlespeed)
            if ai.XPos < (ball.x + rand):
                ai.xvel(ai.paddlespeed)
        else:
            rand=int(100*random.random())%30
            ai.xvel(0)
                
        if ai.XPos < 0: ai.XPos=3 
        if ai.XPos >= gamedata.get_window_width(): ai.XPos = gamedata.get_window_width()-30  
            

        ball.x = ball.x + ball.XSpeed
        ball.y = ball.y + -ball.YSpeed
        #if ball.ballrect.left < 0 or ball.ballrect.right > width:
        if ball.x < 0 or ball.x > gamedata.get_window_width(): 
            ball.XSpeed = -ball.XSpeed
        #if ball.ballrect.top < 0 or ball.ballrect.bottom > height:
        if ball.y < 0 or ball.y > gamedata.get_window_height():
            ball.YSpeed = -ball.YSpeed

        # check to see if hit player paddle
        # and whether the ball is behind paddle or coming in front
        # left of paddle is beginning of position x
        # top of paddle is beginning of position y
        if ball.YSpeed < 0:
            if ball.y >= player.YPos and ball.y <= player.YPos + player.get_paddle_height():
                if ball.x >= player.XPos-2 and ball.x <= player.XPos + player.get_paddle_width():
                    ball.YSpeed=-ball.YSpeed
                    print "player Paddle Hit"

        #check to see if ai paddle hit
        if ball.YSpeed > 0:
            if ball.y >= ai.YPos and ball.y <= ai.YPos+player.get_paddle_height():
                if ball.x >= ai.XPos-2 and ball.x <= ai.XPos + player.get_paddle_width():
                    ball.YSpeed=-ball.YSpeed
                    print "ai paddle hit"

    def mainLoop(self):

        self.__drawscreen()
        
        framerate=60
        framems = 1000 / framerate #calculate the length of each frame
        
        while 1:
            #when the frame starts
            startms = pygame.time.get_ticks() 
            
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
                        self.player.xvel(self.player.paddlespeed)
                        print "K_RIGHT Event"
                    elif event.key == pygame.K_LEFT:
                        #velocity to left
                        self.player.xvel(-self.player.paddlespeed)
                        print "K_LEFT Event"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        self.player.xvel(0)

            self.__moveassets(self.ball, self.player, self.ai, self.gamedata)
            
            self.__drawscreen()
            
            # when the frame ends
            endms = pygame.time.get_ticks()
            # how long to delay 
            delayms = framems - (endms - startms)
            # delay processing
            pygame.time.delay(delayms)

if __name__ == "__main__":
    game = MainGame()
    game.mainLoop()
