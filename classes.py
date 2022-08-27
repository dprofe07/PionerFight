#!/usr/bin/python3

# ***classes.py***
import time
from math import sqrt
import random

import pygame

from funcs import distance_between, n_maxes
from unit import UNITS
from constants import (
    RED, GREEN,
    HEIGHT, WIDTH,
)
from base_units import Unit, Spell, Building

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


class Vampire(Unit):
    params_name = 'vampire'

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
            available = [
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
                    if x.rect.colliderect(available) and x is not self and type(x) != Castle and type(x) != Tower:
                        x.vampirism += self.vampirism
                        self.vampired.append(x)

    def on_death(self):
        for x in self.vampired:
            x.vampirism -= self.vampirism


class Wizard(Unit):
    params_name = 'wizard'


class Pekka(Unit):
    params_name = 'pekka'


class Bat(Unit):
    params_name = 'bat'


# noinspection PyMissingConstructor
class BatArmy(Unit):
    params_name = 'bat_army'

    def __init__(self, screen, command, coords, group, sp_reversed):
        m = None
        for x in range(-(self.param['number'] // 2), self.param['number'] // 2):
            c = list(coords)
            c[1] += x * 10
            m = Bat(screen, command, c, group, sp_reversed)

        self.last_obj = m

    def __getattr__(self, name):
        return getattr(self.last_obj, name)


# noinspection PyMissingConstructor
class BatMob(Unit):
    params_name = 'bat_mob'

    def __init__(self, screen, command, coords, group, sp_reversed):
        m = None
        for x in range(-self.param['number'] // 2, self.param['number'] // 2):
            c = list(coords)
            c[1] += x * 10
            m = Bat(screen, command, c, group, sp_reversed)

        self.last_obj = m

    def __getattr__(self, name):
        return getattr(self.last_obj, name)


class Car(Unit):
    params_name = 'car'

    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.time_go = time.time()
        self.get_radius = self.param['get_radius']
        self.inside = []
        available = [self.rect.centerx - self.get_radius, self.rect.centery - self.get_radius,
                   self.get_radius * 2, self.get_radius * 2]
        for x in self.group:
            if (
                    x.rect.colliderect(available) and
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

    def on_death(self):
        a = [20, -20, 10, -10, 0, -30, 30, -40, 40]
        for x in self.inside:
            x.rect.centerx = self.rect.centerx + random.choice(a)
            x.rect.centery = self.rect.centery + random.choice(a)
            x.group.add(x)


class Soldat(Unit):
    params_name = 'soldat'


class Elite(Soldat):
    params_name = 'elite'


class Witch(Unit):
    params_name = 'witch'

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
                    s = Bat(
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

    def on_death(self):
        for x in range(self.param['on_death_number']):
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


class Sauron(Unit):
    params_name = 'sauron'

    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.number = self.param['number']
        self.spawn_time = self.param['resurrect_time'] + time.time()

    def update(self):
        if super().update():
            if self.spawn_time <= time.time():
                for x in range(self.param['number']):
                    a = [5, -5, 0]
                    # noinspection PyUnusedLocal
                    s = Gigant(
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

    def on_death(self):
        for x in range(self.param['on_death_number']):
            # noinspection PyUnusedLocal
            s = Wizard(
                self.screen,
                self.command,
                [
                    self.rect.centerx,
                    self.rect.centery
                ],
                self.group,
                False
            )
            # s.health = 50


class Sparky(Unit):
    params_name = 'sparky'


class Archer(Unit):
    params_name = 'archer'


class Gigant(Unit):
    params_name = 'gigant'


class Golem(Unit):
    params_name = 'golem'

    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.boom_radius = self.param['boom_radius']
        self.boom_damage = self.param['boom_damage']

    def on_death(self):
        targets = [self.rect.centerx - self.boom_radius, self.rect.centery - self.boom_radius,
                      self.boom_radius * 2, self.boom_radius * 2]
        for x in self.group:
            if x.command != self.command and pygame.Rect(targets).colliderect(x):
                x.attacked(self.boom_damage)
        if type(self) != LiteGolem:
            LiteGolem(self.screen, self.command, (self.rect.centerx, self.rect.centery - 20),
                      self.group, False)
            LiteGolem(self.screen, self.command, (self.rect.centerx, self.rect.centery + 20),
                      self.group, False)


class LiteGolem(Unit):
    params_name = 'lite_golem'


class WallBreaker(Unit):
    params_name = 'wall_breaker'


class Wall(Unit):
    params_name = 'wall'

    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.hill_radius = self.param['hill_radius']
        self.hill = self.param['hill']

    def on_death(self):
        targets = [
            self.rect.centerx - self.hill_radius,
            self.rect.centery - self.hill_radius,
            self.hill_radius * 2,
            self.hill_radius * 2
        ]
        for x in self.group:
            if x.command == self.command and pygame.Rect(targets).colliderect(x) and x is not self:
                x.health += self.hill


class Digger(Unit):
    params_name = 'digger'

    def __init__(self, screen, command, coords, group, sp_reversed):
        self.self_spawn_time = time.time() + self.param['time_spawn']
        super().__init__(screen, command, coords, group, sp_reversed)

    def update(self):
        if super().update():
            self.damage = self.param['damage']
            # noinspection PyAttributeOutsideInit
            self.update = super().update
        spade_img = pygame.image.load(
            f"images/{'red' if RED == self.command else 'green'}_spade.png")
        spade_rect = spade_img.get_rect(
            center=[WIDTH // 2, HEIGHT // 2 - 100] if self.command == RED else [WIDTH // 2,
                                                                                HEIGHT // 2 + 100])
        self.screen.blit(spade_img, spade_rect)


# noinspection PyPep8Naming
class CannonWheels(Unit):  # ANC_CANNON_WHEELS #ANC_WHEELS
    params_name = 'cannon_wheels'
    def on_death(self):
        Cannon(self.screen, self.command, self.rect.center, self.group, False)


class Taran(Unit):  # ANC_TARAN
    params_name = 'taran'

    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.time_go = time.time()

    def on_death(self):
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
    params_name = 'snake'

    def __init__(self, screen, command, coords, group, sp_reversed=0):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.self_venom_time = self.param['venom_time']
        self.venom_damage = self.param['venom'] * UNITS['snake']['damage']

    def attack(self, x, need_update_attack_time=True):
        def n_upd():
            x.update_old()
            if x.venom_time <= time.time():
                x.attacked(self.venom_damage)
                x.venom_time = 1 + time.time()
            if x.venom_finish <= time.time():
                x.update = x.update_old

        if self.attack_time <= time.time():
            x.venom_time = time.time()
            x.venom_finish = self.self_venom_time + time.time()
        super().attack(x, need_update_attack_time)

        if not hasattr(x, 'update_old') or x.update_old == x.update:
            x.update_old = x.update
            x.update = n_upd
            x.venom_time = time.time()
            x.venom_finish = self.self_venom_time + time.time()


class Spirit(Unit):
    params_name = 'spirit'


class Cavalry(Unit):
    params_name = 'cavalry'


class Hiller(Unit):
    params_name = 'hiller'

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

                targets = [
                    self.rect.centerx - self.hill_radius,
                    self.rect.centery - self.hill_radius,
                    self.hill_radius * 2,
                    self.hill_radius * 2
                ]
                for x in self.group:
                    if (
                            x.command == self.command and
                            pygame.Rect(targets, center=targets[:2]).colliderect(x) and
                            not isinstance(x, Building)
                    ):
                        x.health += self.hill
                        if self.param['health'] < x.health:
                            x.health = self.param['health']


# noinspection PyMissingConstructor
class Army(Unit):
    params_name = 'army'

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


class ArmyGolem(Unit):
    params_name = 'army_golem'

    def __init__(self, screen, command, coords, group, sp_reversed):
        s = None
        for x in range(-self.param['number'] // 2, self.param['number'] // 2):
            c = list(coords)
            c[1] += x * 10
            s = Golem(
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
    params_name = 'elite_army'

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


# noinspection PyMissingConstructor
class ArmyArcher(Unit):
    params_name = 'army_archer'

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


class Musician(Unit):
    params_name = 'musician'

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
                x.reloading_time *= 1 + self.speeding
            self.sped = []
            surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
            pygame.draw.circle(surf, tuple(self.command + (75,)), self.rect.center,
                               self.speed_radius)
            self.screen.blit(surf, [0, 0])
            targets = [self.rect.centerx - self.speed_radius,
                          self.rect.centery - self.speed_radius, self.speed_radius * 2,
                          self.speed_radius * 2]
            for x in self.group:
                if (
                        x.command == self.command and
                        pygame.Rect(targets, center=targets[:2]).colliderect(x) and
                        not isinstance(x, Building)
                ):
                    self.sped.append(x)
            for x in self.sped:
                x.speed *= (1 + self.speeding)
                x.reloading_time //= (1 + self.speeding)

    def on_death(self):
        for x in self.sped:
            x.speed //= 1 + self.speeding
            x.reloading_time *= 1 + self.speeding


class HillBattery(Unit):
    params_name = 'hill_battery'

    def attack(self, x, need_update_attack_time=True):
        dmg = x.param['health'] - x.health
        x.health += dmg
        self.health += self.vampirism * dmg
        # plus because vampirism < 0


class AttackBattery(Unit):
    params_name = 'attack_battery'

    def attack(self, x, need_update_attack_time=True):
        self.damage = min(self.health, x.health)
        super().attack(x, need_update_attack_time)


#   ЫЫЫЫЫЫ   ЫЫЫЫЫ    ЫЫЫЫЫ  Ы      Ы       ЫЫЫЫЫЫ
#  Ы         Ы    Ы   Ы      Ы      Ы      Ы
#   ЫЫЫЫЫ    ЫЫЫЫЫ    ЫЫЫ    Ы      Ы       ЫЫЫЫЫ
#        Ы   Ы        Ы      Ы      Ы            Ы
#  ЫЫЫЫЫЫ    Ы        ЫЫЫЫЫ  ЫЫЫЫЫ  ЫЫЫЫЫ  ЫЫЫЫЫЫ


class Spawn(Spell):
    params_name = 'spawn'

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

    def move(self, move_x, move_y):
        self.rect.left += move_x
        self.rect.top += move_y
        if (self.command == RED and not self.reverse) or (self.command == GREEN and self.reverse):
            if self.rect.left < 200:
                self.rect.left = 200
                self.left = False
            if self.rect.right > WIDTH // 2:
                self.rect.right = WIDTH // 2
                self.reverse = not self.reverse
            if self.rect.top < 0:
                self.rect.top = 0
                self.up = False
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.down = False
        elif (self.command == GREEN and not self.reverse) or (self.command == RED and self.reverse):
            if self.rect.right > WIDTH - 200:
                self.rect.right = WIDTH - 200
                self.right = False
            if self.rect.left < WIDTH // 2:
                self.rect.left = WIDTH // 2
                self.reverse = not self.reverse
            if self.rect.top < 0:
                self.rect.top = 0
                self.up = False
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
                self.down = False

    @property
    def reverse(self):
        return self.__reverse

    @reverse.setter
    def reverse(self, new_val):
        self.rect.centerx = WIDTH - self.rect.centerx
        self.__reverse = new_val


class RandomUnit(Spell):
    params_name = 'random_unit'

    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        super().__init__(
            self_group,
            other_group,
            command,
            [0, 0],
            screen,
            sp_reversed
        )
        self.refresh_time = self.param['refresh_time']
        self.time = 0
        self.unit = None
        self.update()

    def update(self):
        if self.time < time.time():
            self.time = time.time() + self.refresh_time
            self.unit = Spell
            while issubclass(self.unit, Spell) or issubclass(self.unit, Building):
                self.unit = random.choice(ALL_UNITS)


class SoldatFlight(Spell):
    params_name = 'soldat_flight'

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
    params_name = 'cemetery'

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
    params_name = 'teleport'

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
    params_name = 'hill'

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
    params_name = 'freeze'

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
    params_name = 'fix'

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
    params_name = 'double_damage'

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
    params_name = 'meteor'

    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        self.attack_radius = self.param['attack_radius']
        rect = [0, 0, 0, 0]
        for x in self_group:
            if type(x) == Spawn and x.command == command:
                rect = [
                    x.rect.centerx - self.attack_radius,
                    x.rect.centery - self.attack_radius,
                    self.attack_radius * 2,
                    self.attack_radius * 2
                ]

        super().__init__(
            self_group,
            other_group,
            command,
            [rect[0] + self.attack_radius, rect[1] + self.attack_radius, rect[2], rect[3]],
            screen,
            sp_reversed
        )
        dmg = self.param['damage'] if not sp_reversed else self.param['reversed_damage']

        for x in self.other_group:
            if x.rect.colliderect(rect):
                if x.command == command:
                    x.attacked(dmg * self.param['self_damage'])
                else:
                    x.attacked(dmg)

        self.time = time.time() + self.param['display_time']

    def update(self):
        if self.time <= time.time():
            self.self_group.remove(self)


class Rocket(Meteor):
    params_name = 'rocket'


class ShieldBreaker(Spell):
    params_name = 'shield_breaker'

    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        self.attack_radius = self.param['attack_radius']
        rect = [0, 0, 0, 0]
        for x in self_group:
            if type(x) == Spawn and x.command == command:
                rect = [
                    x.rect.centerx - self.attack_radius,
                    x.rect.centery - self.attack_radius,
                    self.attack_radius * 2,
                    self.attack_radius * 2
                ]

        super().__init__(
            self_group,
            other_group,
            command,
            [rect[0] + self.attack_radius, rect[1] + self.attack_radius, rect[2], rect[3]],
            screen,
            sp_reversed
        )
        dmg = self.param['damage'] if not sp_reversed else self.param['reversed_damage']

        for x in self.other_group:
            if x.rect.colliderect(rect) and x.command != command:
                x.attacked(0, dmg * x.shield)

        self.time = time.time() + self.param['display_time']

    def update(self):
        if self.time <= time.time():
            self.self_group.remove(self)


class Lightning(Spell):
    params_name = 'lightning'

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
                best[i].attacked(dmg)
                img = pygame.image.load(self.param['attack_image'][command])
                self.images.append(img)

                rect = img.get_rect(
                    center=[
                        best[i].rect.centerx,
                        best[i].rect.centery - 50
                    ]
                )
                self.rects.append(rect)

                best[i].attack_time = time.time() + best[i].reloading_time
                best[i].time_go = time.time()

        self.time = time.time() + 1
        self.imaging_time = self.param['display_time'] + time.time()

    def update(self):
        for r, i in zip(self.rects, self.images):
            self.screen.blit(i, r)
        if time.time() >= self.imaging_time:
            self.self_group.remove(self)


class Push(Spell):
    params_name = 'push'

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


class CannonSpell(Spell):
    params_name = 'cannon_spell'

    def __init__(self, screen, self_group, other_group, command, sp_reversed):
        pygame.sprite.Sprite.__init__(self)
        rect = [0, 0]
        for x in self_group:
            if type(x) == Spawn and x.command == command:
                rect = x.rect.center
                self.start_x = x.rect.left if command == GREEN else x.rect.right

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
        self.attack_time = 0
        self.hill_time = 0
        self.attack_reloading_time = self.param['attack_reloading_time']
        self.hill_radius = self.attack_radius = self.param['action_radius']
        self.hill_reloading_time = self.param['hill_reloading_time']
        self.group = self.other_group
        self.moving = self.param['moving']

    def hill_func(self, other):
        if self.attack_time > time.time():
            return
        other.health += self.hill
        self.hill_time = time.time() + self.hill_reloading_time

    def attack_func(self, other):
        other.attacked(self.damage)

    def auto_attack(self):
        return self.make_action('attack')

    def auto_hill(self):
        self.make_action('hill')

    def make_action(self, action):
        if action == 'attack':
            f = self.attack_func
            rad = self.attack_radius
            time_ = self.attack_time
            rel_time = self.attack_reloading_time
            cmd_eq_neq = object.__ne__
        elif action == 'hill':
            f = self.hill_func
            rad = self.hill_radius
            time_ = self.hill_time
            rel_time = self.hill_reloading_time
            cmd_eq_neq = tuple.__eq__
        else:
            raise ValueError(f'Incorrect action: \"{action}\"')

        if time_ > time.time():
            return
        if action == 'attack':
            self.attack_time = time.time() + rel_time
        elif action == 'hill':
            self.hill_time = time.time() + rel_time

        targets = [
            self.rect.centerx - rad,
            self.rect.centery - rad,
            rad * 2,
            rad * 2
        ]
        can_be_best = []
        for x in self.group:
            if cmd_eq_neq(x.command, self.command) and pygame.Rect(targets).colliderect(x):
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
        self.auto_attack()
        self.auto_hill()

    def move(self, move_x):
        self.rect.centerx += move_x
        if self.command == RED:
            if (
                    self.rect.right >= self.start_x + self.moving or
                    self.command == GREEN and self.rect.left <= self.start_x - self.moving
            ):
                self.self_group.remove(self)


# ЫЫЫЫ   Ы   Ы  ЫЫЫЫЫ Ы      ЫЫЫЫ   ЫЫЫЫЫ  Ы     Ы   ЫЫЫЫ    ЫЫЫЫЫ
# Ы   Ы  Ы   Ы    Ы   Ы      Ы   Ы    Ы    Ы Ы   Ы  Ы       Ы    
# ЫЫЫЫЫ  Ы   Ы    Ы   Ы      Ы   Ы    Ы    Ы  Ы  ы  Ы  ЫЫЫ   ЫЫЫЫЫ  
# Ы   Ы  Ы   Ы    Ы   Ы      Ы   Ы    Ы    Ы   Ы Ы  Ы     Ы       Ы
# ЫЫЫЫ    ЫЫЫ   ЫЫЫЫЫ ЫЫЫЫЫ  ЫЫЫЫ   ЫЫЫЫЫ  Ы    ЫЫ   ЫЫЫЫ Ы  ЫЫЫЫЫ
#


class HealthByTime(Building):
    params_name = 'health_by_time'

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
        self.health = self.param['health']

    def attacked(self, damage, shield_damage=None):
        if shield_damage is None:
            shield_damage = damage

        if self.shield > 0:
            self.shield -= shield_damage
            self.show_damage_message(f'-{shield_damage}')
        else:
            self.show_damage_message(f'Неуязвимость')

    def update(self):
        if super().update():
            if self.minus <= time.time():
                self.minus = time.time() + 1
                self.health -= 1
            return True
        return False


class LifeGenerator(HealthByTime):
    params_name = 'life_generator'

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
        self.health -= self.param['health']

    def update(self):
        if super().update():
            # noinspection DuplicatedCode
            available = [
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
                                x.rect.colliderect(available) and
                                x is not self
                                and not isinstance(x, Building)
                        ):
                            x.health += 100
                            if x.health >= x.param['health'] * 2:
                                x.health = x.param['health'] * 2
                self.hill_time = time.time() + 1


class Column(Building):
    params_name = 'column'


class Xbow(Building):
    params_name = 'xbow'


class Transferer(Building):
    params_name = 'transferer'

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

                targets = [
                    self.rect.centerx - self.radius,
                    self.rect.centery - self.radius,
                    self.radius * 2,
                    self.radius * 2
                ]
                for x in self.group:
                    # noinspection PyArgumentList
                    if (
                            x.command == self.command and
                            pygame.Rect(targets, center=targets[:2]).colliderect(x) and
                            not isinstance(x, eval(self.param.get('dont_attack', 'Spell')))
                    ):
                        ch = [1] * round((1 / self.chance) - 1) + [-1]
                        s = random.choice(ch) * random.randint(self.s // 2, self.s)
                        x.rect.centerx += s
                        break


class Cannon(Building):
    params_name = 'cannon'


class MagicCannon(Building):
    params_name = 'magic_cannon'


class Spawner(Building):
    params_name = 'spawner'

    def __init__(self, screen, command, coords, group, unit_cls):
        super().__init__(
            screen,
            command,
            coords,
            group,
            False
        )
        self.spawn_time = self.reloading_time + time.time()
        self.unit_cls = unit_cls

    def update(self):
        if super().update():
            if self.spawn_time <= time.time():
                self.unit_cls(self.screen, self.command, self.rect.center, self.group, False)
                self.spawn_time = time.time() + self.reloading_time


class SoldatSpawner(Spawner):
    params_name = 'soldat_spawner'

    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, Soldat)


class ArcherSpawner(Spawner):
    params_name = 'archer_spawner'

    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, Archer)


class Collector(Building):
    params_name = 'collector'

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
                self.param['image_full'][self.command]
            )
        super().update()


class Inferno(Building):
    params_name = 'inferno'

    def __init__(self, screen, command, coords, group, sp_reversed):
        super().__init__(screen, command, coords, group, sp_reversed)
        self.fog_time = 0
        self.fog_image = pygame.image.load(self.param['fog_image'])
        self.fog_rect = [0, 0]
        self.kill_reloading_time = self.param['kill_reloading_time']
        self.damage_increment = self.param['damage_increment']

    def attack(self, other, need_update_attack_time=True):
        super().attack(other, need_update_attack_time)

        if other.died:
            self.attack_time = time.time() + self.kill_reloading_time
            self.damage = self.damage_
            self.fog_rect = self.fog_image.get_rect(center=other.rect.center)
            self.fog_time = time.time() + self.param['fog_display_time']
        else:
            self.damage += self.damage_increment


    def update(self):
        super().update()
        if self.fog_time >= time.time():
            self.screen.blit(self.fog_image, self.fog_rect)

    def auto_attack(self):
        return super().auto_attack()
        variants = []
        for x in self.group:
            if (
                    x.command == self.attack_command and
                    isinstance(x, eval(self.attack_only)) and
                    not isinstance(x, eval(self.dont_attack))
            ):
                variants.append(x)

        if len(variants) >= 3:
            self.attack(random.choice(variants))


class Castle(Building):
    params_name = 'castle'

    def destroyed(self):
        self.image = pygame.image.load('images/castle_destroy.png')
        self.damage = 0
        self.health = 0

    def update(self):
        Unit.update(self)


class Tower(Castle):
    params_name = 'tower'


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

        if hasattr(self, 'on_create'):
            self.on_create(self)

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

        if hasattr(self, 'on_create'):
            self.on_create(self)

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
    Rocket, Cannon, Sparky, SoldatSpawner, Collector, Lightning,
    Golem, Digger, Teleport, Spirit, Cavalry, Push, Fix, Army,
    Cemetery, Hiller, Freeze, CannonWheels, Elite,
    EliteArmy, Taran, Witch, ArmyArcher, Car, Vampire,
    Pekka, BatArmy, BatMob, Wall, WallBreaker,
    Snake, LifeGenerator, LiteGolem, HillBattery, AttackBattery,
    CannonSpell, SoldatFlight, Wizard,  ArcherSpawner,
    Transferer, MagicCannon, Xbow, Sauron, Inferno, ShieldBreaker
]
REMOVED_FROM_ALL_UNITS = [
    Musician
]
