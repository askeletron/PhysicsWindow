import pygame
from threading import Thread

class Game:
    def __init__(self,width:int=800,height:int=800):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True

        #контроль мышкой
        self.holding = False

        #мышка
        self.mouseInert = [0,0]
        self.savedmousePos = [0,0]

        #экран
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption("physics Container")

        #логика
        self.gravity = -10
        
        #визуал
        self.rect = pygame.Rect((0,0), (200, 200)); self.rect.center = (400,400)
        self.rectInert = [2,4]

        Thread(target=self.__gameYield__(),daemon=True).start()
    def __gameYield__(self):
        while self.running:
            #логика
            if self.holding:
                self.rectInert = [0,0]
                self.rect.center = pygame.mouse.get_pos()
                self.mouseInert = [(self.savedmousePos[0] - pygame.mouse.get_pos()[0]),(self.savedmousePos[1] - pygame.mouse.get_pos()[1])]
                self.savedmousePos = pygame.mouse.get_pos()

            if self.rect.right >= self.width:
                self.rect.right = self.width
                self.rectInert[0] = -self.rectInert[0]/1.1
            elif self.rect.left <= 0:
                self.rect.left = 0
                self.rectInert[0] = -self.rectInert[0]/1.1
            
            if self.rect.bottom >= self.height:
                self.rect.bottom = self.height
                self.rectInert[1] = -self.rectInert[1]/1.1
            elif self.rect.top <= 0:
                self.rect.top = 0
                self.rectInert[1] = -self.rectInert[1]/1.1

            if self.rect.bottom >= self.height and self.rect.top <= 0:
                self.rectInert[1] = -self.rectInert[1]/1.1
                
            # self.rectInert[0] = self.rectInert[0] if self.rect.right < 800 and self.rect.left > 0 else -self.rectInert[0]/1.1
            # self.rectInert[1] = self.rectInert[1] if self.rect.bottom < 800 and self.rect.top > 0 else -self.rectInert[1]/1.1

            self.rectInert[0]=self.rectInert[0]/1.001

            self.rect.x -= self.rectInert[0]
            self.rect.y -= self.rectInert[1]

            if self.gravity < 0:
                if self.rectInert[1] > self.gravity:
                    self.rectInert[1] -= abs(self.gravity)/50

            print(self.rectInert)
            #обновление
            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen,(255,255,0),self.rect)

            pygame.display.flip()
            self.clock.tick(60)
            for ev in pygame.event.get():
                match ev.type:
                    case pygame.QUIT:
                        self.running = False
                    case pygame.MOUSEBUTTONDOWN:
                        self.holding = True
                    case pygame.MOUSEBUTTONUP:
                        self.rectInert = self.mouseInert
                        self.holding = False
                        
        pygame.quit()
    
if __name__ == "__main__":
    example = Game(800,800)


