#!/usr/bin/python3

# ***classes.py***
import time
from math import sqrt
import random

import pygame

from funcs import primerno_ravno, distance_between, n_maxes
from unit import UNITS
from constants import (
    RED, GREEN,
    health_font,
    HEIGHT, WIDTH, WHITE,
)

pygame.init()


class List(list):
    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except IndexError:
            return Soldat


class SomeThing:
    health = 0


class ShowError(pygame.sprite.Sprite):
    def __init__(self, group, command, text='Не хватает очков'):
        super().__init__()
        self.command = command
        self.group = group

        pygame.font.init()
        font = pygame.font.Font(None, 30)
        self.image = font.render(text, True, command)
        if command == RED:
            self.rect = self.image.get_rect(center=(WIDTH // 4 + 100, HEIGHT // 2))
        elif command == GREEN:
            self.rect = self.image.get_rect(center=(WIDTH // 4 + 500, HEIGHT // 2))

        self.group.add(self)
        self.time = time.time() + 0.6

    def update(self):
        if self.time <= time.time():
            self.group.remove(self)


class Unit(pygame.sprite.Sprite):
    def __init__(self, screen, command, coords, group, sp_reversed):
        pygame.sprite.Sprite.__init__(self)
        u = self.param
        self.screen = screen
        self.reversed = sp_reversed
        if sp_reversed:
            self.damage_ = u.get('reversed_damage', u.get('damage', 0))
        else:
            self.damage_ = u.get('damage', 0)
        self.damage = 0
        self.health = u.get('health', 0)
        self.reloading_time = u.get('reloading_time', 0)
        self.image = pygame.image.load(u.get('image', {command: 'images\\no.png'})[command])
        self.speed_ = u.get('speed', 0)
        self.speed = 0
        self.group = group
        self.rect = self.image.get_rect(center=coords[:2])
        self.command = command
        self.atack_radius = u.get('atack_radius', 0)
        self.target_coords = self.rect
        self.sped = 0
        self.vampirism = u.get('vampirism', 0)
        self.self_spawn_time = 1 + time.time()
        self.retreat = False
        self.splash_radius = u.get('splash_radius', 0)
        self.atack_only = u.get('atack_only', 'Unit')
        self.atack_command = u.get('atack_command', 'other')
        self.dont_atack = u.get('dont_atack', 'Spell')
        self.max_cout = u.get('max_count', 51)
        if self.atack_command == 'other':
            if self.command == GREEN:
                self.atack_command = RED
            else:
                self.atack_command = GREEN
        else:
            if self.command == GREEN:
                self.atack_command = GREEN
            else:
                self.atack_command = RED
        self.stun = u.get('stun', 0)
        self.stunned = False
        self.atack_time = time.time() + u.get('first_reload', self.reloading_time)
        self.flag = None
        self.goto_flag = False
        self.ignore_flags = []
        self.died_on_atack = u.get('died_on_atack', False)
        self.run_effect = u.get('run_effect', False)
        if self.run_effect:
            self.time_go = time.time()
        self.need_update_properties = True
        group.add(self)

    def correct_flag(self, flag):
        return type(flag) == Flag and flag not in self.ignore_flags

    @property
    def param(self):
        return UNITS[self.__class__.__name__.lower()]

    @property
    def vampirism(self):
        return self.__vampirism

    @vampirism.setter
    def vampirism(self, v):
        # if v > 1.5:
        #  v = 1.5
        self.__vampirism = v

    @property
    def died(self):
        if self.health <= 0 and hasattr(self, 'ondeath'):
            self.ondeath()
        return self.health <= 0

    def atack(self, other, need_update_atack_time=True):
        if type(other) == Flag:
            self.ignore_flags.append(other)
            return
        if self.atack_time > time.time():
            return

        if self.splash_radius != 0:
            surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                tuple(self.command + (50,)),
                self.target_coords.center,
                self.splash_radius,
                2
            )
            self.screen.blit(surf, [0, 0])

            targetable = [
                other.rect.centerx - self.splash_radius,
                other.rect.centery - self.splash_radius,
                self.splash_radius * 2,
                self.splash_radius * 2
            ]
            s = self.splash_radius
            self.splash_radius = 0
            for x in self.group:
                if (
                        x.command != self.command and
                        pygame.Rect(targetable).colliderect(x) and
                        x is not other
                ):
                    self.atack(x, False)
            self.splash_radius = s

        other.health -= self.damage
        self.health += self.vampirism * abs(self.damage)
        if self.health > self.param['health']:
            self.health = self.param['health']
        if need_update_atack_time:
            self.atack_time = time.time() + self.reloading_time
        if self.died_on_atack:
            self.health = 0
        if self.run_effect:
            self.time_go = time.time()
        if self.stun:
            other.stunned = time.time() + self.stun
        #   "SMT -atack-> SMT"
        # print(self.__class__.__name__+' -atack-> '+other.__class__.__name__)

    def update(self):
        self.update_()
        if self.self_spawn_time <= time.time():
            if self.stunned >= time.time():
                self.need_update_properties = True
                self.damage = 0
                self.speed = 0
                self.atack_time = self.stunned + self.reloading_time
                self.time_go = self.stunned

                i = pygame.image.load('images\\stunned.png')
                r = i.get_rect(center=[self.rect.centerx, self.rect.top - 20])
                self.screen.blit(i, r)
                return False
            if self.need_update_properties:
                self.damage = self.damage_
                self.speed = self.speed_
                self.need_update_properties = False
            if self.run_effect:
                if time.time() - self.time_go >= self.param['run_time']:
                    self.speed = self.param['run_speed']
                    self.damage = self.param['run_damage']
                else:
                    self.speed = self.param['speed']
                    self.damage = self.param['damage']
            self.choose_target()
            self.auto_go()
            return True
        return False

    def update_(self):
        text = health_font.render(
            str(round(self.health if self.health >= 0 else 0)),
            1,
            WHITE,
            self.command
        )
        text_rect = text.get_rect(center=[self.rect.centerx, self.rect.top - 8])
        self.screen.blit(text, text_rect)

    def auto_go(self):
        atackable = [
            self.rect.centerx - self.atack_radius,
            self.rect.centery - self.atack_radius,
            self.atack_radius * 2,
            self.atack_radius * 2
        ]
        if pygame.Rect(atackable).colliderect(self.target_coords):
            return self.auto_atack()

        movex = 0
        movey = 0
        if not primerno_ravno(self.rect.centerx, self.target_coords.centerx, self.speed):
            if self.rect.centerx < self.target_coords.centerx:
                movex = self.speed
            if self.rect.centerx > self.target_coords.centerx:
                movex = - self.speed
        if not primerno_ravno(self.rect.centery, self.target_coords.centery, self.speed):
            if self.rect.centery < self.target_coords.centery:
                movey = self.speed
            if self.rect.centery > self.target_coords.centery:
                movey = - self.speed
        self.move(movex, movey)

    def auto_atack(self):
        best = ''
        targetable = [
            self.rect.centerx - self.atack_radius,
            self.rect.centery - self.atack_radius,
            self.atack_radius * 2,
            self.atack_radius * 2
        ]
        for x in self.group:
            if (
                    (self.correct_flag(x) or x.command == self.atack_command) and
                    pygame.Rect(targetable).colliderect(x) and
                    isinstance(x, eval(self.atack_only)) and
                    not isinstance(x, eval(self.dont_atack))
            ):
                if (
                        best == '' or
                        distance_between(best, self) > distance_between(self, x)
                ):
                    best = x
        if best != '':
            self.atack(best)

    def move(self, movex, movey):
        self.rect.centerx += movex
        self.rect.centery += movey

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left <= 200:
            self.rect.left = 200
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right >= WIDTH - 200:
            self.rect.right = WIDTH - 200

    def choose_target(self):
        if self.retreat:
            for i in self.group:
                if type(i) == Spawn and i.command == self.command:
                    self.target_coords = i.rect
        else:
            aviable = [self.rect.centerx - 200, self.rect.centery - 200, 400, 400]
            best = ''
            for x in self.group:
                if (
                            (self.correct_flag(x) or x.command == self.atack_command) and
                            pygame.Rect(aviable).colliderect(x) and
                            isinstance(x, eval(self.atack_only)) and
                            not isinstance(x, eval(self.dont_atack))
                ):
                    if (
                            type(x) == Flag and
                            (
                                    type(best) != Flag or
                                    best == '' or
                                    distance_between(self, best) > distance_between(self, x)
                            )
                    ):
                        best = x
                    elif (
                            not x.died and
                            (
                                    best == '' or
                                    distance_between(self, best) > distance_between(self, x)
                            )
                    ):
                        best = x

            if best != '':
                self.target_coords = best.rect
            else:
                for x in self.group:
                    if not x.died and x.command != self.command and type(x) == Tower:
                        self.target_coords = x.rect
                        break
                else:
                    for x in self.group:
                        if not x.died and x.command != self.command and type(x) == Castle:
                            self.target_coords = x.rect
                            break

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(health = {self.health}, damage = {self.damage}, "
            f"reloading_time = {self.reloading_time}, speed = {self.speed})"
        )


class Vampire(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.vampired = []
        self.vampire_radius = self.param['vampire_radius']

    def update(self):
        if super().update():
            for x in self.vampired:
                x.vampirism -= self.vampirism
            self.vampired = []
            # noinspection DuplicatedCode
            aviable = [
                self.rect.centerx - self.vampire_radius,
                self.rect.centery - self.vampire_radius,
                self.vampire_radius * 2,
                self.vampire_radius * 2
            ]
            surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
            pygame.draw.circle(surf, tuple(self.command + (75,)), self.rect.center,
                               self.vampire_radius)
            self.screen.blit(surf, [0, 0])

            for x in self.group:
                if x.command == self.command:
                    if x.rect.colliderect(aviable) and x is not self and type(x) != Castle and type(
                            x) != Tower:
                        x.vampirism += self.vampirism
                        self.vampired.append(x)

    def ondied(self):
        for x in self.vampired:
            x.vampirism -= self.vampirism


class Wizard(Unit):
    pass


class Spider(Unit):
    pass


class Mouse(Unit):
    pass


# noinspection PyMissingConstructor
class MouseArmy(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        m = None
        for x in range(-UNITS['mousearmy']['number'] // 2, UNITS['mousearmy']['number'] // 2):
            c = list(coords)
            c[1] += x * 10
            m = Mouse(screen, command, c, group, sp_reversed)

        self.last_obj = m

    def __getattr__(self, name):
        return getattr(self.last_obj, name)


# noinspection PyMissingConstructor
class MouseMob(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):

        m = None
        for x in range(-UNITS['mousemob']['number'] // 2, UNITS['mousemob']['number'] // 2):
            c = list(coords)
            c[1] += x * 10
            m = Mouse(screen, command, c, group, sp_reversed)

        self.last_obj = m

    def __getattr__(self, name):
        return getattr(self.last_obj, name)


class Car(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.time_go = time.time()
        self.get_radius = self.param['get_radius']
        self.inside = []
        aviable = [self.rect.centerx - self.get_radius, self.rect.centery - self.get_radius,
                   self.get_radius * 2, self.get_radius * 2]
        for x in self.group:
            if (
                    x.rect.colliderect(aviable) and
                    not isinstance(x, Building) and
                    x is not self and
                    x.command == self.command
            ):
                if len(self.inside) >= self.param['max_number']:
                    break
                self.inside.append(x)
                x.group.remove(x)
        minus = round(sum(x.health for x in self.inside) / 1000)
        if minus > self.speed - 1:
            minus = self.speed - 1
        self.param['speed'] -= minus
        self.param['run_speed'] -= minus

    def ondied(self):
        a = [20, -20, 10, -10, 0, -30, 30, -40, 40]
        for x in self.inside:
            x.rect.centerx = self.rect.centerx + random.choice(a)
            x.rect.centery = self.rect.centery + random.choice(a)
            x.group.add(x)


class Soldat(Unit):
    pass


class Elite(Soldat):  # ANC_ELITE
    pass


class Witch(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.number = self.param['number']
        self.spawn_time = self.param['resurrect_time'] + time.time()

    def update(self):
        if super().update():
            if self.spawn_time <= time.time():
                for x in range(self.param['number']):
                    a = [20, -20]
                    # noinspection PyUnusedLocal
                    s = Soldat(
                        self.screen,
                        self.command,
                        [
                            self.rect.centerx + random.choice(a),
                            self.rect.centery + random.choice(a)
                        ],
                        self.group,
                        False
                    )
                    # s.health //= 2

                self.spawn_time = time.time() + self.param['resurrect_time']

    def ondied(self):
        for x in range(self.param['number']):
            a = [20, -20]
            # noinspection PyUnusedLocal
            s = Soldat(
                self.screen,
                self.command,
                [
                    self.rect.centerx + random.choice(a),
                    self.rect.centery + random.choice(a)
                ],
                self.group,
                False
            )
            # s.health = 50


class Sparky(Unit):  # ANC_SPARKY #ANC_ELECTRO
    pass


class Archer(Unit):
    pass


class Gigant(Unit):
    pass


class Golem(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.boom_radius = self.param['boom_radius']
        self.boom_damage = self.param['boom_damage']

    def ondeath(self):
        targetable = [self.rect.centerx - self.boom_radius, self.rect.centery - self.boom_radius,
                      self.boom_radius * 2, self.boom_radius * 2]
        for x in self.group:
            if x.command != self.command and pygame.Rect(targetable).colliderect(x):
                x.health -= self.boom_damage
        if type(self) != GolemLite:
            GolemLite(self.screen, self.command, (self.rect.centerx, self.rect.centery - 20),
                      self.group, False)
            GolemLite(self.screen, self.command, (self.rect.centerx, self.rect.centery + 20),
                      self.group, False)


class GolemLite(Golem):
    def ondeath(self):
        pass


class WallBreaker(Unit):
    def choose_target(self):
        aviable = [self.rect.centerx - 200, self.rect.centery - 200, 400, 400]
        best = ''
        for x in self.group:
            if pygame.Rect(aviable).colliderect(
                    x.rect) and x.command != self.command and isinstance(x, Building):
                if not x.died and (best == '' or sqrt(
                        pow(best.rect.centerx - self.rect.centerx, 2) + pow(
                            best.rect.centery - self.rect.centery, 2)) > sqrt(
                    pow(self.rect.centerx - x.rect.centerx, 2) + pow(
                        self.rect.centery - x.rect.centery, 2))):
                    best = x
        if best != '':
            self.target_coords = best.rect
        else:
            for x in self.group:
                if not x.died and x.command != self.command and type(x) == Tower:
                    self.target_coords = x.rect
                    break
            else:
                for x in self.group:
                    if not x.died and x.command != self.command and type(x) == Castle:
                        self.target_coords = x.rect


class Wall(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.hill_radius = self.param['hill_radius']
        self.hill = self.param['hill']

    def ondied(self):
        targetable = [self.rect.centerx - self.hill_radius, self.rect.centery - self.hill_radius,
                      self.hill_radius * 2, self.hill_radius * 2]
        for x in self.group:
            if x.command == self.command and pygame.Rect(targetable).colliderect(
                    x) and x is not self:
                x.health += self.hill


class Digger(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        self.self_spawn_time = time.time() + self.param['time_spawn']
        super().__init__(screen, command, coords, group, sp_reversed)

    def update(self):
        if super().update():
            self.damage = self.param['damage']
            # noinspection PyAttributeOutsideInit
            self.update = super().update
        spade_img = pygame.image.load(
            f"images\\{'red' if RED == self.command else 'green'}_spade.png")
        spade_rect = spade_img.get_rect(
            center=[WIDTH // 2, HEIGHT // 2 - 100] if self.command == RED else [WIDTH // 2,
                                                                                HEIGHT // 2 + 100])
        self.screen.blit(spade_img, spade_rect)


# noinspection PyPep8Naming
class Cannon_wheels(Unit):  # ANC_CANNON_WHEELS #ANC_WHEELS
    def ondied(self):
        Cannon(self.screen, self.command, self.rect.center, self.group, False)


class Taran(Unit):  # ANC_TARAN
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.time_go = time.time()

    def ondied(self):
        for x in range(self.param['number']):
            Elite(
                self.screen,
                self.command,
                [
                    self.rect.centerx,
                    self.rect.centery + 20 * x
                ],
                self.group,
                False
            )


class Snake(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed=0):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.self_venom_time = self.param['venom_time']
        self.venom_damage = self.param['venom'] * UNITS['snake']['damage']

    def atack(self, x, need_update_atack_time=True):
        def n_upd():
            x.update_old()
            if x.venom_time <= time.time():
                x.health -= self.venom_damage
                x.venom_time = 1 + time.time()
            if x.venom_finish <= time.time():
                x.update = x.update_old

        if self.atack_time <= time.time():
            x.venom_time = time.time()
            x.venom_finish = self.self_venom_time + time.time()
        super().atack(x, need_update_atack_time)

        if not hasattr(x, 'update_old') or x.update_old == x.update:
            x.update_old = x.update
            x.update = n_upd
            x.venom_time = time.time()
            x.venom_finish = self.self_venom_time + time.time()


class Spirit(Unit):
    pass


class Cavalry(Unit):
    pass


class Hiller(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.hill = self.param['hill']
        self.time_hill = time.time() + self.param['hill_reloading_time']
        self.hill_radius = self.param['hill_radius']

    def update(self):
        if super().update():
            surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                tuple(self.command + (75,)),
                self.rect.center,
                self.hill_radius
            )
            self.screen.blit(surf, [0, 0])
            if self.time_hill <= time.time():
                self.time_hill = time.time() + self.param['hill_reloading_time']

                targetable = [
                    self.rect.centerx - self.hill_radius,
                    self.rect.centery - self.hill_radius,
                    self.hill_radius * 2,
                    self.hill_radius * 2
                ]
                for x in self.group:
                    if (
                            x.command == self.command and
                            pygame.Rect(targetable, center=targetable[:2]).colliderect(x) and
                            not isinstance(x, Building)
                    ):
                        x.health += self.hill
                        if self.param['health'] < x.health:
                            x.health = self.param['health']


# noinspection PyMissingConstructor
class Army(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        s = None
        for x in range(-self.param['number'] // 2, self.param['number'] // 2):
            c = list(coords)
            c[1] += x * 10
            s = Soldat(
                screen,
                command,
                c,
                group,
                sp_reversed
            )

        self.last_obj = s

    def __getattr__(self, name):
        return getattr(self.last_obj, name)


# noinspection PyMissingConstructor
class EliteArmy(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        e = None
        for x in range(-self.param['number'] // 2, self.param['number'] // 2):
            c = list(coords)
            c[1] += x * 10
            e = Elite(
                screen,
                command,
                c,
                group,
                sp_reversed
            )
        self.last_obj = e

    def __getattr__(self, name):
        return getattr(self.last_obj, name)


# noinspection PyMissingConstructor,PyPep8Naming
class Army_Archer(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        a = None
        for x in range(-self.param['number'] // 2, self.param['number'] // 2):
            c = list(coords)
            c[1] += x * 10
            a = Archer(
                screen,
                command,
                c,
                group,
                sp_reversed
            )
        self.last_obj = a

    def __getattr__(self, name):
        return getattr(self.last_obj, name)


class Musicant(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(
            screen,
            command,
            coords,
            group,
            sp_reversed
        )

        self.speeding = self.param['speeding']
        self.speed_radius = self.param['speed_radius']
        self.sped = []

    def update(self):
        if super().update():
            for x in self.sped:
                x.speed //= 1 + self.speeding
                x.reloading_time *= 1 + self.speeding  # ANCHOR
            self.sped = []
            surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
            pygame.draw.circle(surf, tuple(self.command + (75,)), self.rect.center,
                               self.speed_radius)
            self.screen.blit(surf, [0, 0])
            targetable = [self.rect.centerx - self.speed_radius,
                          self.rect.centery - self.speed_radius, self.speed_radius * 2,
                          self.speed_radius * 2]
            for x in self.group:
                if (
                        x.command == self.command and
                        pygame.Rect(targetable, center=targetable[:2]).colliderect(x) and
                        not isinstance(x, Building)
                ):
                    self.sped.append(x)
            for x in self.sped:
                x.speed *= (1 + self.speeding)
                x.reloading_time //= (1 + self.speeding)


class HillBattery(Unit):
    def atack(self, x, need_update_atack_time=True):
        dmg = x.param['health'] - x.health
        x.health += dmg
        self.health += self.vampirism * dmg
        # plus because vampirism < 0


class AtackBattery(Unit):
    def atack(self, x, need_update_atack_time=True):
        self.damage = min(self.health, x.health)
        super().atack(x, need_update_atack_time)


#  ЫЫЫЫЫЫЫ   ЫЫЫЫЫЫ   ЫЫЫЫЫ  Ы      Ы       ЫЫЫЫЫЫ
#  Ы         Ы    Ы   Ы      Ы      Ы      Ы
#  ЫЫЫЫЫЫЫ   ЫЫЫЫЫЫ   ЫЫЫ    Ы      Ы       ЫЫЫЫЫ
#        Ы   Ы        Ы      Ы      Ы            Ы
#  ЫЫЫЫЫЫЫ   Ы        ЫЫЫЫЫ  ЫЫЫЫЫ  ЫЫЫЫЫ  ЫЫЫЫЫЫ

class Spell(pygame.sprite.Sprite):
    def __init__(self, self_group, other_group, command, coords, screen, sp_reversed):
        super().__init__()
        self.self_group = self_group
        self.other_group = other_group
        self.command = command
        self.image = pygame.image.load(self.param['image'][command])
        self.rect = self.image.get_rect(center=coords[:2])
        self.self_group.add(self)
        self.screen = screen
        self.reversed = sp_reversed

    @property
    def param(self):
        return UNITS[type(self).__name__.lower()]

    def __repr__(self):
        return f'{self.__class__.__name__}(command = {self.command}, rect={self.rect})'


class Spawn(Spell):
    def __init__(self, group, command, rect):
        super().__init__(
            group,
            {},
            command,
            rect,
            None,
            False
        )
        self.speed = self.param['speed']
        self.left = self.right = self.up = self.down = False
        self.__reverse = 0

    def update(self):
        self.move((self.right - self.left) * self.speed, (self.down - self.up) * self.speed)

    def move(self, movex, movey):
        self.rect.left += movex
        self.rect.top += movey
        if (self.command == RED and not self.reverse) or (self.command == GREEN and self.reverse):
            if self.rect.left < 200:
                self.rect.left = 200
                self.left = 0
            if self.rect.right > WIDTH // 2:
                self.rect.right = WIDTH // 2
                self.right = 0
            if self.rect.top < 0:
                self.rect.top = 0
                self.up = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.down = 0
        elif (self.command == GREEN and not self.reverse) or (self.command == RED and self.reverse):
            if self.rect.right > WIDTH - 200:
                self.rect.right = WIDTH - 200
                self.right = 0
            if self.rect.left < WIDTH // 2:
                self.rect.left = WIDTH // 2
                self.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
                self.up = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.down = 0

    @property
    def reverse(self):
        return self.__reverse

    @reverse.setter
    def reverse(self, nval):
        self.rect.centerx = WIDTH - self.rect.centerx
        self.__reverse = nval


class ThrowSoldat(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        super().__init__(
            self_group,
            other_group,
            command,
            [WIDTH // 2, HEIGHT // 2 - 100] if command == RED else [WIDTH // 2, HEIGHT // 2 + 100],
            screen,
            sp_reversed
        )
        coords = [0, 0]
        for i in self_group:
            if type(i) == Spawn and i.command == command:
                coords = [i.rect.centerx, i.rect.centery + self.image.get_height() // 2]
        self.self_spawn_time = time.time() + self.param['time_spawn']

        for y in range(-self.param['number'] // 2, self.param['number'] // 2):
            c = coords
            c[1] += y * 10
            Soldat(
                screen,
                command,
                c,
                other_group,
                sp_reversed
            )
        self.time = time.time() + 1

    def update(self):
        if self.time < time.time():
            self.self_group.remove(self)


class Cemetery(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        coords = []
        for x in self_group:
            if isinstance(x, Spawn) and x.command == command:
                coords = x.rect.copy()
                coords.left += 35
                coords.top += 35
        super().__init__(
            self_group,
            other_group,
            command,
            coords,
            screen,
            sp_reversed
        )
        self.spawn_time = time.time() + self.param['spawn_time']
        self.start_time = time.time()

    def update(self):
        if self.spawn_time <= time.time():
            Soldat(
                self.screen,
                self.command,
                random.choice(
                    [
                        self.rect.topleft,
                        self.rect.topright,
                        self.rect.bottomleft,
                        self.rect.bottomright
                    ]
                ),
                self.other_group,
                False
            )
            self.spawn_time = time.time() + self.param['spawn_time']
            if self.start_time + self.param['effect_time'] <= time.time():
                self.self_group.remove(self)


class Teleport(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        super().__init__(
            self_group,
            other_group,
            command,
            [WIDTH // 2, HEIGHT // 2 - 25] if command == RED else [WIDTH // 2, HEIGHT // 2 + 25],
            screen,
            sp_reversed
        )
        for x in other_group:
            if x.command == command and not isinstance(x, Building):
                x.rect.centerx = WIDTH - x.rect.centerx
        self.time = time.time() + 0.5

    def update(self):
        if self.time < time.time():
            self.self_group.remove(self)


class Hill(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        super().__init__(
            self_group,
            other_group,
            command,
            [WIDTH // 2, HEIGHT // 2 - 50] if command == RED else [WIDTH // 2, HEIGHT // 2 + 50],
            screen,
            sp_reversed
        )
        self.time = time.time() + 1
        for x in self.other_group:
            if x.command == self.command and not isinstance(x, Building):
                type_ = x.__class__.__name__.lower()
                x.health += self.param['hill']
                if x.param['health'] < x.health:
                    x.health = UNITS.get(type_, {'health': 1})['health']

    def update(self):
        if self.time < time.time():
            self.self_group.remove(self)


class Freeze(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        super().__init__(
            self_group,
            other_group,
            command,
            [WIDTH // 2, HEIGHT // 2 - 50] if command == RED else [WIDTH // 2, HEIGHT // 2 + 50],
            screen,
            sp_reversed
        )
        self.time_end = time.time() + self.param['effect_time']
        for x in other_group:
            if x.command != self.command:
                x.speed *= 1 - self.param['effect']
                x.damage *= 1 - self.param['effect']

    def update(self):
        if self.time_end <= time.time():
            self.self_group.remove(self)
            for x in self.other_group:
                if x.command != self.command:
                    x.speed = x.param.get('speed', 0)
                    x.damage = x.param.get('damage', 0)


class Fix(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        super().__init__(
            self_group,
            other_group,
            command,
            [WIDTH // 2, HEIGHT // 2 - 50] if command == RED else [WIDTH // 2, HEIGHT // 2 + 50],
            screen,
            sp_reversed
        )
        self.time = time.time() + 1
        for x in self.other_group:
            if x.command == self.command and isinstance(x, Building):
                x.health += self.param['hill']
                if x.param['health'] < x.health:
                    x.health = x.param['health']

    def update(self):
        if self.time < time.time():
            self.self_group.remove(self)


class DoubleDamage(Spell):
    data = {
        RED: {
            'time': 0,
            'active': False
        },
        GREEN: {
            'time': 0,
            'active': False
        }
    }
    damage = 0
    died = 0
    health = 1

    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        if DoubleDamage.data[command]['active']:
            return
        DoubleDamage.data[command]['time'] = time.time() + self.param['effect_time']
        DoubleDamage.data[command]['active'] = True

        for x in other_group:
            if x.command == command:
                x.damage *= self.param['effect']

        super().__init__(
            self_group,
            other_group,
            command,
            [WIDTH // 2, HEIGHT // 2 - 150] if command == RED else [WIDTH // 2, HEIGHT // 2 + 150],
            screen,
            sp_reversed
        )

    def update(self):
        for command in DoubleDamage.data.keys():
            if (
                    DoubleDamage.data[command]['active'] and
                    DoubleDamage.data[command]['time'] < time.time()
            ):
                for x in self.other_group:
                    if x.command == command:
                        x.damage //= 2
                self.self_group.remove(self)
                DoubleDamage.data[command]['active'] = False


class Meteor(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        self.atack_radius = self.param['atack_radius']
        rect = [0, 0, 0, 0]
        for x in self_group:
            if type(x) == Spawn and x.command == command:
                rect = [
                    x.rect.centerx - self.atack_radius,
                    x.rect.centery - self.atack_radius,
                    self.atack_radius * 2,
                    self.atack_radius * 2
                ]

        super().__init__(
            self_group,
            other_group,
            command,
            [rect[0] + self.atack_radius, rect[1] + self.atack_radius, rect[2], rect[3]],
            screen,
            sp_reversed
        )
        dmg = self.param['damage'] if not sp_reversed else self.param['reversed_damage']

        for x in self.other_group:
            if x.rect.colliderect(rect):
                if x.command == command:
                    x.health -= dmg * self.param['self_damage']
                else:
                    x.health -= dmg

        self.time = time.time() + self.param['display_time']

    def update(self):
        if self.time <= time.time():
            self.self_group.remove(self)


class Rocket(Meteor):
    pass


class Molniy(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        rect = [0, 0, 0, 0]
        for i in self_group:
            if type(i) == Spawn and i.command == command:
                rect = [
                    i.rect.centerx - self.param['radius'],
                    i.rect.centery - self.param['radius'],
                    self.param['radius'] * 2,
                    self.param['radius'] * 2
                ]
                break

        super().__init__(
            self_group,
            other_group,
            command,
            rect,
            screen,
            sp_reversed
        )

        dmg = self.param['damage'] if not sp_reversed else self.param['reversed_damage']

        self.images = []
        self.rects = []

        can_be_best = []
        for x in self.other_group:
            if x.rect.colliderect(rect) and x.command != self.command:
                can_be_best.append(x)

        best = n_maxes(
            self.param['count_targets'],
            can_be_best,
            key=lambda i: i.health
        )

        for i in range(len(best)):
            if best[i] is not None:
                best[i].health -= dmg
                img = pygame.image.load(self.param['atack_image'][command])
                self.images.append(img)

                rect = img.get_rect(
                    center=[
                        best[i].rect.centerx,
                        best[i].rect.centery - 50
                    ]
                )
                self.rects.append(rect)

                best[i].atack_time = time.time() + best[i].reloading_time
                best[i].time_go = time.time()

        self.time = time.time() + 1
        self.imaging_time = self.param['display_time'] + time.time()

    def update(self):
        for r, i in zip(self.rects, self.images):
            self.screen.blit(i, r)
        if time.time() >= self.imaging_time:
            self.self_group.remove(self)


class Push(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        rect = [400, 200, 400, 400] if command == RED else [800, 200, 400, 400]
        super().__init__(
            self_group,
            other_group,
            command,
            rect,
            screen,
            sp_reversed
        )
        self.time = time.time() + self.param['effect_time']

    def update(self):
        if self.time <= time.time():
            self.self_group.remove(self)
        for x in self.other_group:
            if not isinstance(x, Building) and x.command != self.command:
                if self.command == GREEN:
                    x.rect.centerx -= self.param['force']
                else:
                    x.rect.centerx += self.param['force']


# noinspection PyPep8Naming
class Cannon_Spell(Spell):
    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        pygame.sprite.Sprite.__init__(self)
        rect = [0, 0]
        for x in self_group:
            if type(x) == Spawn and x.command == command:
                rect = x.rect.center
                self.startx = x.rect.left if command == GREEN else x.rect.right

        super().__init__(
            self_group,
            other_group,
            command,
            rect,
            screen,
            sp_reversed
        )
        self.speed = self.param['speed']
        self.damage = self.param['damage']
        self.hill = self.param['hill']
        self.atack_time = 0
        self.hill_time = 0
        self.atack_reloading_time = self.param['atack_reloading_time']
        self.hill_radius = self.atack_radius = self.param['action_radius']
        self.hill_reloading_time = self.param['hill_reloading_time']
        self.group = self.other_group
        self.moving = self.param['moving']

    def hillf(self, other):
        if self.atack_time > time.time():
            return
        other.health += self.hill
        self.hill_time = time.time() + self.hill_reloading_time

    def atackf(self, other):
        other.health -= self.damage

    def auto_atack(self):
        return self.make_action('atack')

    def auto_hill(self):
        self.make_action('hill')

    def make_action(self, action):
        if action == 'atack':
            f = self.atackf
            rad = self.atack_radius
            time_ = self.atack_time
            rel_time = self.atack_reloading_time
            cmd_eq_neq = lambda a, b: a != b
        elif action == 'hill':
            f = self.hillf
            rad = self.hill_radius
            time_ = self.hill_time
            rel_time = self.hill_reloading_time
            cmd_eq_neq = lambda a, b: a == b
        else:
            raise ValueError(f'Incorrect action: {action}')

        if time_ > time.time():
            return
        if action == 'atack':
            self.atack_time = time.time() + rel_time
        elif action == 'hill':
            self.hill_time = time.time() + rel_time

        targetable = [
            self.rect.centerx - rad,
            self.rect.centery - rad,
            rad * 2,
            rad * 2
        ]
        can_be_best = []
        for x in self.group:
            if cmd_eq_neq(x.command, self.command) and pygame.Rect(targetable).colliderect(x):
                can_be_best.append(x)

        best = n_maxes(
            self.param[action + '_count'],
            can_be_best,
            lambda i: distance_between(i, self)
        )

        for i in best:
            f(i)

    def auto_go(self):
        self.move(self.speed * (int(self.command == RED) * 2 - 1))
        # x * 2 - 1 converts (0, 1) to (-1, 1)

    def update(self):
        self.auto_go()
        self.auto_atack()
        self.auto_hill()

    def move(self, movex):
        self.rect.centerx += movex
        if self.command == RED and self.rect.right >= self.startx + self.moving or self.command == GREEN and self.rect.left <= self.startx - self.moving:
            self.self_group.remove(self)


# ЫЫЫЫ   Ы   Ы  ЫЫЫЫЫ Ы      ЫЫЫЫ   ЫЫЫЫЫ  Ы     Ы   ЫЫЫЫ    ЫЫЫЫЫ
# Ы   Ы  Ы   Ы    Ы   Ы      Ы   Ы    Ы    Ы Ы   Ы  Ы       Ы    
# ЫЫЫЫЫ  Ы   Ы    Ы   Ы      Ы   Ы    Ы    Ы  Ы  ы  Ы  ЫЫЫ   ЫЫЫЫЫ  
# Ы   Ы  Ы   Ы    Ы   Ы      Ы   Ы    Ы    Ы   Ы Ы  Ы     Ы       Ы
# ЫЫЫЫ    ЫЫЫ   ЫЫЫЫЫ ЫЫЫЫЫ  ЫЫЫЫ   ЫЫЫЫЫ  Ы    ЫЫ   ЫЫЫЫ Ы  ЫЫЫЫЫ
#                                                                         


class Building(Unit):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(
            screen,
            command,
            coords,
            group,
            sp_reversed
        )
        self.time_del = time.time() + 0.5

    def update(self):
        if super().update():
            if self.time_del <= time.time():
                self.health -= 2
                self.time_del = time.time() + 0.5
            return True
        return False


class HealthByTime(Building):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(
            screen,
            command,
            coords,
            group,
            sp_reversed
        )
        self.effect_time = self.param['health'] + time.time()
        self.minus = 1 + time.time()
        self.set_health(self.param['health'], True)

    def update(self):
        if super().update():
            if self.minus <= time.time():
                self.minus = time.time() + 1
                self.set_health(self.health - 1, True)
            return True
        return False

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, v):
        self.set_health(v)

    def set_health(self, v, a=False):
        if a:
            self.__health = v


class Flag(HealthByTime):
    def update(self):
        if super().update():
            for i in self.group:
                if i.command == self.command:
                    i.flag = self
                    i.goto_flag = True


class LifeGenerator(HealthByTime):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(
            screen,
            command,
            coords,
            group,
            sp_reversed
        )
        self.hill = self.param['hill']
        self.hill_radius = self.param['hill_radius']
        self.effect_time = self.param['health'] + time.time()
        self.hill_time = 0
        self.set_health(self.param['health'], True)

    def update(self):
        if super().update():
            # noinspection DuplicatedCode
            aviable = [
                self.rect.centerx - self.hill_radius,
                self.rect.centery - self.hill_radius,
                self.hill_radius * 2,
                self.hill_radius * 2
            ]
            surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
            pygame.draw.circle(surf, tuple(self.command + (75,)), self.rect.center,
                               self.hill_radius)
            self.screen.blit(surf, [0, 0])
            if self.hill_time <= time.time():
                surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
                pygame.draw.circle(surf, tuple(self.command + (75,)), self.rect.center,
                                   self.hill_radius)
                self.screen.blit(surf, [0, 0])

                for x in self.group:
                    if x.command == self.command:
                        if (
                                x.rect.colliderect(aviable) and
                                x is not self
                                and not isinstance(x, Building)
                        ):
                            x.health += 100
                            if x.health >= x.param['health'] * 2:
                                x.health = x.param['health'] * 2
                self.hill_time = time.time() + 1


class Xbow(Building):
    pass


class Transferer(Building):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(
            screen,
            command,
            coords,
            group,
            sp_reversed
        )
        self.chance = self.param['chance']
        self.s = self.param['s']
        self.time_tp = time.time() + self.reloading_time
        self.radius = self.param['radius']

    def update(self):
        if super().update():
            surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
            pygame.draw.circle(surf, tuple(self.command + (75,)), self.rect.center, self.radius)
            p = pygame.image.load(self.param['cross_image'][self.command])
            r = p.get_rect(center=[self.rect.centerx + self.s, self.rect.centery])
            self.screen.blit(p, r)
            self.screen.blit(surf, [0, 0])
            if self.time_tp <= time.time():
                self.time_tp = time.time() + self.reloading_time

                targetable = [
                    self.rect.centerx - self.radius,
                    self.rect.centery - self.radius,
                    self.radius * 2,
                    self.radius * 2
                ]
                for x in self.group:
                    # noinspection PyArgumentList
                    if (
                            x.command == self.command and
                            pygame.Rect(targetable, center=targetable[:2]).colliderect(x) and
                            not isinstance(x, eval(self.param.get('dont_atack', 'Spell')))
                    ):
                        ch = [1] * round((1 / self.chance) - 1) + [-1]
                        s = random.choice(ch) * random.randint(self.s // 2, self.s)
                        x.rect.centerx += s
                        break


class Cannon(Building):
    pass


class MagicCannon(Building):
    pass


class Spawner(Building):
    def __init__(self, screen, command, coords, group, voin_cls):
        super().__init__(
            screen,
            command,
            coords,
            group,
            False
        )
        self.spawn_time = self.reloading_time + time.time()
        self.voin_cls = voin_cls

    def update(self):
        if super().update():
            if self.spawn_time <= time.time():
                self.voin_cls(self.screen, self.command, self.rect.center, self.group, False)
                self.spawn_time = time.time() + self.reloading_time


class SoldatSpawner(Spawner):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, Soldat)


class ArcherSpawner(Spawner):
    def __init__(self, screen, command, coords, group, reversed=0):
        super().__init__(screen, command, coords, group, Archer)


class Collector(Building):
    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.add_time = 0
        self.time_show = 0

    def add(self, points=0):
        if self.add_time <= time.time():
            points += self.param['add_points']
            self.add_time = time.time() + self.reloading_time
            self.time_show = time.time() + self.reloading_time
        if points > self.param['max_points']:
            return self.param['max_points']
        return points

    def update(self):
        if self.time_show <= time.time():
            self.image = pygame.image.load(
                self.param['image'][self.command]
            )
        else:
            self.image = pygame.image.load(
                self.param['image'][self.command].replace('.png', '_full.png')
            )
        super().update()


class Castle(Building):
    def destroyed(self):
        self.image = pygame.image.load('images\\castle_destroy.png')
        self.damage = 0
        self.health = 0

    def update(self):
        Unit.update(self)


class Tower(Castle):
    pass


class Info:
    def __init__(self, class_, **kw):
        self.class_ = class_
        for k, v in kw.items():
            setattr(self, k, v)

    def create(self):
        raise NotImplementedError()

    @staticmethod
    def from_object(obj):
        if isinstance(obj, Spell):
            return SpellInfo.from_object(obj)
        elif isinstance(obj, Unit):
            return UnitInfo.from_object(obj)

    @property
    def param(self):
        return UNITS[self.class_.__name__.lower()]

    @property
    def points(self):
        return self.param['points']


class UnitInfo(Info):
    def __init__(self, class_, screen, command, coords, group, sp_reversed):
        super().__init__(
            class_,
            screen=screen,
            command=command,
            coords=coords,
            group=group,
            reversed=sp_reversed
        )
        self.created = None

    @staticmethod
    def from_object(obj):
        return UnitInfo(
            type(obj),
            obj.screen,
            obj.command,
            obj.rect,
            obj.group,
            obj.reversed
        )

    # noinspection PyUnresolvedReferences
    def create(self):
        self.created = self.class_(
            self.screen,
            self.command,
            self.coords,
            self.group,
            self.reversed
        )

        if hasattr(self, 'oncreate'):
            self.oncreate(self)

        return self.created

    # noinspection PyUnresolvedReferences
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return all([
            self.class_ == other.class_,
            self.screen == other.screen,
            self.group == other.group,
            self.command == other.command,
            self.coords == other.coords,
            self.reversed == other.reversed
        ])

class SpellInfo(Info):
    # noinspection PyMissingConstructor
    def __init__(self, class_, screen, self_group, other_group, command, sp_reversed):
        super().__init__(
            class_,
            screen=screen,
            self_group=self_group,
            other_group=other_group,
            command=command,
            reversed=sp_reversed
        )
        self.created = None

    # noinspection PyUnresolvedReferences
    def create(self):
        self.created = self.class_(
            self.screen,
            self.self_group,
            self.other_group,
            self.command,
            self.reversed
        )

        if hasattr(self, 'oncreate'):
            self.oncreate(self)

        return self.created

    @staticmethod
    def from_object(obj):
        return SpellInfo(
            type(obj),
            obj.screen,
            obj.self_group,
            obj.other_group,
            obj.command,
            obj.reversed
        )

    # noinspection PyUnresolvedReferences
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return all([
            self.class_ == other.class_,
            self.screen == other.screen,
            self.self_group == other.self_group,
            self.other_group == other.other_group,
            self.command == other.command,
            self.reversed == other.reversed
        ])



ALL_UNITS = [
    Soldat, Archer, Gigant, Hill, DoubleDamage, Meteor,
    Rocket, Cannon, Sparky, SoldatSpawner, Collector, Molniy,
    Golem, Digger, Teleport, Spirit, Cavalry, Push, Fix, Army,
    Cemetery, Hiller, Musicant, Freeze, Cannon_wheels, Elite,
    EliteArmy, Taran, Witch, Army_Archer, Car, Vampire,
    Spider, MouseArmy, MouseMob, Wall, WallBreaker,
    Snake, LifeGenerator, GolemLite, HillBattery, AtackBattery,
    Cannon_Spell, ThrowSoldat, Wizard, Flag, ArcherSpawner,
    Transferer, MagicCannon, Xbow
]
