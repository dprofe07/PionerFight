import pygame
import time
import sys
import random
pygame.init()

RED = [255,0,0]
GREEN = [0,255,0]
WHITE = [255,255,255]
BLACK = [0,0,0]

GREEN_POINTS = 1000
RED_POINTS = 1000
TIME_ADD_RED = 0
TIME_ADD_GREEN = 0


WIDTH = 1000
HEIGHT = 400
BG = pygame.image.load('images\\BG.jpg')
from unit import UNITS
from classes import Unit, Soldat,Archer, Gigant, Hill, DoubleDamage, Meteor, Cannon, Spell, Tower, Sparky, Rocket, SoldatSpawner, Collector
from classes import Castle, Lightning

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Пионерское побоище')

group = pygame.sprite.Group()
spells = pygame.sprite.Group()

red_castle = Castle(screen, group, RED, [160,HEIGHT//2, 70, 70])
green_castle = Castle(screen, group, GREEN, [WIDTH-160,HEIGHT//2, 70, 70])

font = pygame.font.Font(None, 20)


pause = 0

Tower(screen, group, RED, [260,325,70,70])
Tower(screen, group, RED, [260,75,70,70])

Tower(screen, group,GREEN, [740,325,70,70])
Tower(screen, group, GREEN, [740,75,70,70])

class Meta(type):
    @property
    def _1(self):
        return self.deck[0]
    @property
    def _2(self):
        return self.deck[1]
    @property
    def _3(self):
        return self.deck[2]
    @property
    def _4(self):
        return self.deck[3]

class DECK_RED(metaclass = Meta):
    deck = [
            Soldat, Archer, Gigant, Hill, DoubleDamage,
            Meteor, Cannon, Rocket, Sparky, SoldatSpawner,
            Collector,
            ]
    
class DECK_GREEN(metaclass = Meta):
    deck = [
            Soldat, Archer, Gigant, Hill, DoubleDamage,
            Meteor, Cannon, Rocket, Sparky, SoldatSpawner,
            Collector, 
            ]

random.shuffle(DECK_RED.deck)
random.shuffle(DECK_GREEN.deck)


names = {
         'soldat':'Солдат',
         'archer':'Лучник',
         'gigant':'Гигант',
         'hill':'Исцеление',
         'doubledamage':'x2 урон',
         'meteor':'Метеорит',
         'cannon':'Пушка',
         'sparky':'Электро',
         'rocket':'Ракета',
         'soldatspawner':'Казарма',
         'collector':'Сборщик',
         #'molniy':"Молния",
         }

while not (red_castle.died or green_castle.died):

    # Static graphic
    screen.fill(WHITE)
    for pos, x in enumerate(DECK_RED.deck[:4]):
        a = pygame.image.load(f'images\\red_{x.__name__.lower()}.png')
        screen.blit(a, a.get_rect(center=[50,40+40*(pos)*2]))

        b = font.render(f'{pos+1} - {names[x.__name__.lower()]}', 1, [0,0,0])
        screen.blit(b, b.get_rect(center=[50,80+40*(pos)*2]))
    for pos, x in enumerate(DECK_GREEN.deck[:4]):
        a = pygame.image.load(f'images\\green_{x.__name__.lower()}.png')
        screen.blit(a, a.get_rect(center=[950,40+40*(pos)*2]))

        b = font.render(f'{pos+1} - {names[x.__name__.lower()]}', 1, [0,0,0])
        screen.blit(b, b.get_rect(center=[950,80+40*(pos)*2]))
    
    #dynamic graphic
    for x in pygame.event.get():
        if x.type == pygame.QUIT:
            red_castle.health = 0
            green_castle.health = 0
        if x.type == pygame.KEYDOWN and not pause:
            if x.key == pygame.K_1:
                #RED
                if UNITS[DECK_RED._1.__name__.lower()]['points'] > RED_POINTS:
                    continue
                RED_POINTS -= UNITS[DECK_RED._1.__name__.lower()]['points']
                if issubclass(DECK_RED._1, Spell):
                    DECK_RED._1(spells, group, [255,0,0])
                else:
                    DECK_RED._1(screen,[255,0,0], red_castle.rect.center, group)
                DECK_RED.deck.append(DECK_RED.deck.pop(0))
                DECK_RED.deck.insert(0, DECK_RED.deck.pop(4))
                #/RED
                
            if x.key == pygame.K_KP1:
                #GREEN
                if UNITS[DECK_GREEN._1.__name__.lower()]['points'] > GREEN_POINTS:
                    continue
                GREEN_POINTS -= UNITS[DECK_GREEN._1.__name__.lower()]['points']
                if issubclass(DECK_GREEN._1, Spell):
                    DECK_GREEN._1(spells, group, [0,255,0])
                else:
                    DECK_GREEN._1(screen,[0,255,0], green_castle.rect.center, group)
                DECK_GREEN.deck.append(DECK_GREEN.deck.pop(0))
                DECK_GREEN.deck.insert(0, DECK_GREEN.deck.pop(4))
                #/GREEN
                
            if x.key == pygame.K_2:
                if UNITS[DECK_RED._2.__name__.lower()]['points'] > RED_POINTS:
                    continue
                RED_POINTS -= UNITS[DECK_RED._2.__name__.lower()]['points']
                if issubclass(DECK_RED._2, Spell):
                    DECK_RED._2(spells, group, [255,0,0])
                else:
                    DECK_RED._2(screen,[255,0,0], red_castle.rect.center, group)
                DECK_RED.deck.append(DECK_RED.deck.pop(1))
                DECK_RED.deck.insert(1, DECK_RED.deck.pop(4))
                
            if x.key == pygame.K_KP2:
                if UNITS[DECK_GREEN._2.__name__.lower()]['points'] > GREEN_POINTS:
                    continue
                GREEN_POINTS -= UNITS[DECK_GREEN._2.__name__.lower()]['points']
                if issubclass(DECK_GREEN._2, Spell):
                    DECK_GREEN._2(spells, group, [0,255,0])
                else:
                    DECK_GREEN._2(screen,[0,255,0], green_castle.rect.center, group)
                DECK_GREEN.deck.append(DECK_GREEN.deck.pop(1))
                DECK_GREEN.deck.insert(1, DECK_GREEN.deck.pop(4))
                
            if x.key == pygame.K_3:
                if UNITS[DECK_RED._3.__name__.lower()]['points'] > RED_POINTS:
                    continue
                RED_POINTS -= UNITS[DECK_RED._3.__name__.lower()]['points']
                if issubclass(DECK_RED._3, Spell):
                    DECK_RED._3(spells, group, [255,0,0])
                else:
                    DECK_RED._3(screen,[255,0,0], red_castle.rect.center, group)
                DECK_RED.deck.append(DECK_RED.deck.pop(2))
                DECK_RED.deck.insert(2, DECK_RED.deck.pop(4))
                
            if x.key == pygame.K_KP3:
                if UNITS[DECK_GREEN._3.__name__.lower()]['points'] > GREEN_POINTS:
                    continue
                GREEN_POINTS -= UNITS[DECK_GREEN._3.__name__.lower()]['points']
                if issubclass(DECK_GREEN._3, Spell):
                    DECK_GREEN._3(spells, group, [0,255,0])
                else:
                    DECK_GREEN._3(screen,[0,255,0], green_castle.rect.center, group)
                DECK_GREEN.deck.append(DECK_GREEN.deck.pop(2))
                DECK_GREEN.deck.insert(2, DECK_GREEN.deck.pop(4))
                
            if x.key == pygame.K_4:
                if UNITS[DECK_RED._4.__name__.lower()]['points'] > RED_POINTS:
                    continue
                RED_POINTS -= UNITS[DECK_RED._4.__name__.lower()]['points']
                if issubclass(DECK_RED._4, Spell):
                    DECK_RED._4(spells, group, [255,0,0])
                else:
                    DECK_RED._4(screen,[255,0,0], red_castle.rect.center, group)
                DECK_RED.deck.append(DECK_RED.deck.pop(3))
                DECK_RED.deck.insert(3, DECK_RED.deck.pop(4))
            if x.key == pygame.K_KP4:
                if UNITS[DECK_GREEN._4.__name__.lower()]['points'] > GREEN_POINTS:
                    continue
                GREEN_POINTS -= UNITS[DECK_GREEN._4.__name__.lower()]['points']
                if issubclass(DECK_GREEN._4, Spell):
                    DECK_GREEN._4(spells, group, [0,255,0])
                else:
                    DECK_GREEN._4(screen,[0,255,0], green_castle.rect.center, group)
                DECK_GREEN.deck.append(DECK_GREEN.deck.pop(3))
                DECK_GREEN.deck.insert(3, DECK_GREEN.deck.pop(4))
            if x.key == pygame.K_LSHIFT:
                red_castle.speed = int(not red_castle.speed)
            if x.key == pygame.K_RSHIFT:
                green_castle.speed = int(not green_castle.speed)
            # MOVING RED CASTLE
            if x.key == pygame.K_w:
                if 50 > RED_POINTS:
                    continue
                RED_POINTS -= 50
                red_castle.move(0,-5)
            if x.key == pygame.K_s:
                if 50 > RED_POINTS:
                    continue
                RED_POINTS -= 50
                red_castle.move(0,5)
            if x.key == pygame.K_a:
                if 50 > RED_POINTS:
                    continue
                RED_POINTS -= 50
                red_castle.move(-5,0)
            if x.key == pygame.K_d:
                if 50 > RED_POINTS:
                    continue
                RED_POINTS -= 50
                red_castle.move(5,0)
            #MOVING GREEN CASTLE
            if x.key == pygame.K_UP:
                if 50 > GREEN_POINTS:
                    continue
                GREEN_POINTS -= 50
                green_castle.move(0,-5)
            if x.key == pygame.K_DOWN:
                if 50 > GREEN_POINTS:
                    continue
                GREEN_POINTS -= 50
                green_castle.move(0,5)
            if x.key == pygame.K_RIGHT:
                if 50 > GREEN_POINTS:
                    continue
                GREEN_POINTS -= 50
                green_castle.move(5,0)
            if x.key == pygame.K_LEFT:
                if 50 > GREEN_POINTS:
                    continue
                GREEN_POINTS -= 50
                green_castle.move(-5,0)
        if x.type == pygame.KEYDOWN and x.key == pygame.K_p:
            pause = not pause
    screen.blit(BG, [100,0,800,400])
    if not pause:
        group.update()
        group.draw(screen)

        spells.update()
        spells.draw(screen)

        for x in group:
            if type(x) == Collector:
                if x.command == [255,0,0]:
                    RED_POINTS = x.add(RED_POINTS)
                else:
                    GREEN_POINTS = x.add(GREEN_POINTS)
        
        if TIME_ADD_GREEN <= time.time() and GREEN_POINTS < 3000:
            TIME_ADD_GREEN = time.time() + 1
            GREEN_POINTS += 100
        if TIME_ADD_RED <= time.time() and RED_POINTS < 3000:
            TIME_ADD_RED = time.time() + 1
            RED_POINTS += 100
    else:
        a = pygame.font.Font(None, 50).render('Пауза', 1, [0,0,0])
        screen.blit(a, a.get_rect(center=[WIDTH//2,HEIGHT//2]))
    screen.blit(font.render(f'{RED_POINTS}', 1, [255,0,0], [255,255,255]), [WIDTH//2,0])
    screen.blit(font.render(f'{GREEN_POINTS}', 1, [0,255,0], [255,255,255]), [WIDTH//2, HEIGHT-10])

    
        
    pygame.display.flip()
    for x in group:
        if x.died:
            if type(x) != Castle and type(x) != Tower:
                group.remove(x)
            else:
                x.destroyed()
    time.sleep(0.05)
else:
    
    screen.fill(WHITE)  
    screen.blit(BG, [100,0,800,400])
    win = 'blue'
    caron = pygame.image.load('images\\winner.png')
    
    
    group.update()
    group.draw(screen)

    if red_castle.died:
        red_castle.destroyed()
        screen.blit(caron, caron.get_rect(center=[50,HEIGHT//2-30]))
        win = 'green'
    if green_castle.died:
        green_castle.destroyed()
        screen.blit(caron, caron.get_rect(center=[WIDTH-50, HEIGHT//2-30]))
        win = 'red' if win == 'blue' else 'blue'
    font = pygame.font.Font(None, 50)
    if win == 'green':
        text = font.render("Победили зелёные", 1, [0,0,0])
    elif win == 'red':
        text = font.render("Победили красные", 1, [0,0,0])
    elif win == 'blue':
        text = font.render("Ничья!", 1, [0,0,0])

    screen.blit(text, text.get_rect(center=[WIDTH//2, HEIGHT//2]))
    
    pygame.display.flip()
    while True:
        for x in pygame.event.get():
            if x.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
