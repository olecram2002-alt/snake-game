import pygame
from sys import exit
from random import randint

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake-Game')
        
        self.screen = pygame.display.set_mode((700,700))
        self.clock = pygame.time.Clock()
        self.player = Snake(self)
        self.running = True
        self.score = 0
        self.state = 0

        self.body_gen = pygame.USEREVENT + 1
        self.body_gen_event = pygame.event.Event(self.body_gen)
    #sprite groups
        self.menu_text_group = pygame.sprite.Group()
        self.game_over_group = pygame.sprite.Group()

        self.game_ui_group = pygame.sprite.Group()
        self.game_obstacle_group = pygame.sprite.Group()
        self.game_collectable_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
    #sprites
        self.sprites= {'snake_0': self.player,
                       'left wall':Wall([0,0]),'right wall':Wall([0,1]),'bottom wall':Wall([1,0]),'top wall':Wall([1,1]),
                       'fruit':Fruit(randint(25,675),randint(95,675)),
                       'menu text1':Text(100,'Snake',(32,36,2),(350,350)),
                        'menu text2':Text(20,'Press space to start',(67,74,5),(350,600)),
                        'score text':Text(50,f'Score : {self.score}',(32,36,2),(350,60)),
                        'game over':Text(100,'Game over',(32,36,2),(350,350))}

        self.menu_text_group.add(self.sprites['menu text1'],self.sprites['menu text2'])
        self.game_over_group.add(self.sprites['game over'])

        self.game_ui_group.add(self.sprites['score text'])
        self.game_obstacle_group.add(self.sprites['left wall'],self.sprites['right wall'],self.sprites['bottom wall'],self.sprites['top wall'])
        self.game_collectable_group.add(self.sprites['fruit'])
        self.player_group.add(self.sprites['snake_0'])

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
        #game inputs
            if self.state == 1:
                if event.type == pygame.KEYDOWN:
            #movement
                    if event.key == pygame.K_w:
                        self.player.direction = [0,-1]
                    if event.key == pygame.K_s:
                        self.player.direction = [0,1]
                    if event.key == pygame.K_a:
                        self.player.direction = [-1,0]
                    if event.key == pygame.K_d:
                        self.player.direction = [1,0]
                if event.type == self.body_gen:
                    self.sprites[f'snake_{self.score}'] = Body(self)
                    self.game_obstacle_group.add(self.sprites[f'snake_{self.score}'])

    def menu(self):
        self.input()
        self.screen.fill((218, 232, 88))
        self.menu_text_group.draw(self.screen)

        pygame.display.update()

    def game(self):
        self.input()
        self.screen.fill((218, 232, 88))

        self.game_ui_group.draw(self.screen)
        self.game_obstacle_group.draw(self.screen)
        self.game_collectable_group.draw(self.screen)
        self.player_group.draw(self.screen)

        self.player.update()

        pygame.display.update()
    
    def game_over(self):
        self.input()
        self.screen.fill((218, 232, 88))
        self.game_over_group.draw(self.screen)

        pygame.display.update()

class Snake(pygame.sprite.Sprite):
    def __init__(self,game:Game):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill((32,36,2))
        self.rect = self.image.get_rect(center=(350,350))

        self.game = game
        self.velocity = [5,5]
        self.direction = [0,0]

    def movement(self):
        self.rect.centerx += self.velocity[0]*self.direction[0]

        self.rect.centery +=self.velocity[1]*self.direction[1]

    def collision_detect(self):
        for sprite in self.game.game_obstacle_group:

        #check for collision
            if self.rect.colliderect(sprite.rect) and not sprite.recently_created:
                self.game.state = 2

        #activate collision with new body part
            if hasattr(sprite,'recently_created') and not self.rect.colliderect(sprite.rect):
                sprite.recently_created = False

        for sprite in self.game.game_collectable_group:

        #check for eating fruit
            if self.rect.colliderect(sprite.rect):
                self.game.score += 1
                self.game.sprites['score text'].update(f'Score : {self.game.score}',(32,36,2))
                sprite.kill()

                self.game.sprites['fruit'] = Fruit(randint(25,675),randint(95,675))
                self.game.game_collectable_group.add(self.game.sprites['fruit'])

                pygame.event.post(self.game.body_gen_event)

    def update(self):
        self.movement()
        self.collision_detect()

class Body(pygame.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((30,30))
        self.image.fill((32,36,2))
        self.rect = self.image.get_rect(center=(self.game.sprites[f'snake_{self.game.score - 1}'].rect.center))

        self.recently_created = True
        self.velocity = [5,5]
        self.direction = [0,0]
        
class Fruit(pygame.sprite.Sprite):
    def __init__(self,x:int,y:int):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.image.fill((67,74,5))
    
class Wall(pygame.sprite.Sprite):
    def __init__(self,index:list):
        super().__init__()
        if index[0] == 0:
            self.image = pygame.Surface((5,605))
        
        elif index[0] == 1:
            self.image = pygame.Surface((680,5))

        if index[1] == 0:
            self.rect = self.image.get_rect(bottomleft=(10,690))

        elif index[1] == 1:
            self.rect = self.image.get_rect(topright=(690,85))

        self.image.fill((32,36,2))

class Text(pygame.sprite.Sprite):
    def __init__(self,font_size: int,text: str,color: tuple,position: tuple):
        super().__init__()
        self.font = pygame.font.Font('graphics/Pixeltype.ttf',font_size)
        self.image = self.font.render(text, False, color)
        self.rect = self.image.get_rect(center=position)
    
    def update(self,text:str,color:tuple):
        self.image = self.font.render(text, False, color)

if __name__ == '__main__':
    snake = Game()
    snake.run()
