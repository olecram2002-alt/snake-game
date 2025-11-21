import pygame
from sys import exit

class game():
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((700,700))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.state = 0
    #sprite groups
        self.menu_text_group = pygame.sprite.Group()
        self.game_group = pygame.sprite.Group()
    #sprites
        #menu
        self.menu_text1 = text(100,'Snake',(32,36,2),(350,350))
        self.menu_text2 = text(20,'Press space to start',(67,74,5),(350,600))
        self.menu_text_group.add(self.menu_text1,self.menu_text2)
        #game
        self.score_text = text(50,f'Score : {self.score}',(32,36,2),(350,60))
        self.game_group.add(self.score_text)

    def run(self):
        while self.running:
            if self.state == 0:
                self.menu()
            
            if self.state == 1:
                self.game()

            if self.state == 2:
                self.game_over()

            self.clock.tick(60)

    def input(self):
        for event in pygame.event.get():
        #closing game
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #menu inputs
            if self.state == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #starts game
                        self.state = 1

    def menu(self):
        self.input()
        self.screen.fill((218, 232, 88))
        self.menu_text_group.draw(self.screen)

        pygame.display.update()

    def game(self):
        self.input()
        self.screen.fill((218, 232, 88))
        self.game_group.draw(self.screen) 

        pygame.display.update()

class text(pygame.sprite.Sprite):
    def __init__(self,font_size: int,text: str,color: tuple,position: tuple):
        super().__init__()

        self.font = pygame.font.Font('graphics/Pixeltype.ttf',font_size)
        self.image = self.font.render(text, False, color)
        self.rect = self.image.get_rect(center=position)

if __name__ == '__main__':
    snake = game()
    snake.run()