import pygame
from sys import exit
from random import randint

class Game():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((700,700))
        self.clock = pygame.time.Clock()
        self.grid_size = 20
        self.snake_body = [(350,420),(350,400),(350,380)]
        self.font = 'graphics/Pixeltype.ttf'
        self.running = True
        self.move = [0,0]
        self.transparency = 260
        self.start_time = 0
        self.state = 0
        self.score = 0

        self.sprites = {
            'menu text1':Text(self.font,'Snake',200,(32,36,2),(350,350)),
            'menu text2':Text(self.font,'Press space to start',50,(67,74,5),(350,600)),
            'game text1':Text(self.font,'Score: 0',50,(32,36,2),(350,35)),
            'wall left':Wall([0,0]),'wall right':Wall([0,1]),'wall bot':Wall([1,0]),'wall top':Wall([1,1]),
            'fruit':Fruit()}

        self.menu_sprites = pygame.sprite.Group(self.sprites['menu text1'],self.sprites['menu text2'])
        self.game_sprites = pygame.sprite.Group(self.sprites['game text1'],self.sprites['wall left'],
                                                self.sprites['wall right'],self.sprites['wall bot'],
                                                self.sprites['wall top'],self.sprites['fruit'])
        
        for index,part in enumerate(self.snake_body):
            self.sprites[f'snake body{index}'] = SnakePart(part)
            self.game_sprites.add(self.sprites[f'snake body{index}'])

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.state == 0:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.state = 1
            
            if self.state == 1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.move = [0,-1]
                    if event.key == pygame.K_s:
                        self.move = [0,1]
                    if event.key == pygame.K_a:
                        self.move = [-1,0]
                    if event.key == pygame.K_d:
                        self.move = [1,0]

    def run(self):
        while self.running:
            if self.state == 0:
                self.menu()
            if self.state == 1:
                self.game()
            if self.state == 2:
                self.game_over()

            self.clock.tick(60)

    def menu(self):
        if self.transparency == 50:
            self.transparency = 260
        self.transparency -= 2.5

        self.input()
        self.screen.fill((218, 232, 88))
        self.sprites['menu text2'].image.set_alpha(self.transparency)
        self.menu_sprites.draw(self.screen)

        pygame.display.update()

    def game(self):
        time_elapsed = pygame.time.get_ticks() - self.start_time
        self.input()
        if time_elapsed >= 100:
            self.movement()
            self.start_time = pygame.time.get_ticks()

            for sprite in self.game_sprites:
                if hasattr(sprite,'name') and sprite.name == 'snake':
                    sprite.kill()

            for index,part in enumerate(self.snake_body):
                self.sprites[f'snake body{index}'] = SnakePart(part)
                self.game_sprites.add(self.sprites[f'snake body{index}'])

            self.sprites[f'snake body{len(self.snake_body)-1}'].collision_check(self)

        self.screen.fill((218, 232, 88))
        self.game_sprites.draw(self.screen)

        pygame.display.update()

    def movement(self):
        x,y = self.snake_body[-1]
        self.snake_body.append((x+20*(self.move[0]),y+20*(self.move[1])))
        
class SnakePart(pygame.sprite.Sprite):
    def __init__(self, location:tuple):
        super().__init__()
        self.name = 'snake'
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect(center=location)
        self.image.fill((32,36,2))

    def collision_check(self, game:Game):
        eat = False
        for sprite in game.game_sprites:
            if self.rect.colliderect(sprite.rect):
                if sprite.name == 'fruit':
                    eat = True
                    game.score += 1
                    sprite.kill()
                    game.game_sprites.add(Fruit())
                if sprite.name == 'wall':
                    game.state = 2
        if not eat:
            game.snake_body.pop(0)

class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = 'fruit'
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect(center=(randint(30,670),randint(90,670)))
        self.image.fill((250, 118, 10))

class Text(pygame.sprite.Sprite):
    def __init__(self, font_location:str, text:str, size:int, color:tuple, location:tuple ):
        super().__init__()
        self.name = 'text'
        self.font = pygame.font.Font(font_location,size)
        self.image = self.font.render(text,False,color)
        self.rect = self.image.get_rect(center=location)

    def render(self,new_size:int ,new_text:str ,new_color:tuple):
        pass

class Wall(pygame.sprite.Sprite):
    def __init__(self, index:list):
        super().__init__()
        self.name = 'wall'

        if index[0] == 0:
            self.image = pygame.Surface((10,620))
        
        elif index[0] == 1:
            self.image = pygame.Surface((680,10))

        if index[1] == 0:
            self.rect = self.image.get_rect(bottomleft=(10,690))

        elif index[1] == 1:
            self.rect = self.image.get_rect(topright=(690,70))

        self.image.fill((32,36,2))

if __name__ == '__main__':
    game = Game()
    game.run()
