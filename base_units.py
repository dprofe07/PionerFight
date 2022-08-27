import random

import pygame
import time

from funcs import primerno_ravno, distance_between
from unit import UNITS
from constants import RED, GREEN, HEIGHT, WIDTH, health_font, WHITE, GREY


class DamageText(pygame.sprite.Sprite):
    font = pygame.font.Font(None, 15)

    def __init__(self, text, unit):
        pygame.sprite.Sprite.__init__(self)
        self.screen = unit.screen
        self.color = RED if unit.command == GREEN else GREEN
        self.unit = unit

        self.start_time = time.time()
        self.display_time = 1
        self.iter_count = 0
        self.speed = 5

        self.image = DamageText.font.render(
            text,
            True,
            self.color
        )
        self.rect = self.image.get_rect(center=[unit.rect.left, unit.rect.top])

    def update(self):
        if self.start_time + self.display_time <= time.time():
            self.unit.damage_texts.remove(self)

        self.iter_count += 1
        self.rect.center = self.unit.rect.topleft
        self.rect.centery -= self.speed * self.iter_count

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Unit(pygame.sprite.Sprite):
    params_name = 'DEFAULT'

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
        self.image = pygame.image.load(u.get('image', {command: 'images/no.png'})[command])
        self.speed_ = u.get('speed', 0)
        self.speed = 0
        self.group = group
        self.rect = self.image.get_rect(center=coords[:2])
        self.command = command
        self.attack_radius = u.get('attack_radius', 0)
        self.shield = u.get('shield', 0)
        self.shield_damage = u.get('shield_damage', None)
        self.target_coords = self.rect
        self.sped = 0
        self.vampirism = u.get('vampirism', 0)
        self.self_spawn_time = 1 + time.time()
        self.retreat = False
        self.splash_radius = u.get('splash_radius', 0)
        self.attack_only = u.get('attack_only', 'Unit')
        self.attack_command = u.get('attack_command', 'other')
        self.dont_attack = u.get('do_not_attack', 'Spell')
        self.on_death_worked = False
        self.max_count = u.get('max_count', 51)
        if self.attack_command == 'other':
            if self.command == GREEN:
                self.attack_command = RED
            else:
                self.attack_command = GREEN
        else:
            if self.command == GREEN:
                self.attack_command = GREEN
            else:
                self.attack_command = RED
        self.stun = u.get('stun', 0)
        self.stunned = False
        self.attack_time = time.time() + u.get('first_reload', self.reloading_time)
        self.die_on_attack = u.get('die_on_attack', False)
        self.run_effect = u.get('run_effect', False)
        if self.run_effect:
            self.time_go = time.time()
        self.need_update_properties = True

        self.miss_chance = u.get('miss_chance', 0)
        self.miss_list_length = 1
        self.miss_count = 1
        while self.miss_chance % 1 != 0:
            self.miss_list_length *= 10
            self.miss_chance *= 10
        self.miss_count = self.miss_chance
        self.damage_texts = []
        # aura
        self.aura = u.get('aura', False)
        self.aura_radius = u.get('aura_radius', 0)
        self.aura_reloading_time = u.get('aura_rt', 0)
        self.aura_damage = u.get('aura_damage', 0)
        self.aura_time = time.time() + u.get('first_reload', self.aura_reloading_time)

        group.add(self)

    @property
    def param(self):
        return UNITS[self.__class__.params_name]

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
        if self.health <= 0 and not self.on_death_worked:
            self.on_death()
            self.on_death_worked = True
        return self.health <= 0

    def on_death(self):
        pass

    def missed(self):
        lst = [i < self.miss_count for i in range(self.miss_list_length)]
        return random.choice(lst)

    def show_damage_message(self, text):
        dmg = DamageText(text, self)
        self.damage_texts.append(dmg)

    def attack(self, other, need_update_attack_time=True):
        if self.attack_time > time.time():
            return

        if self.missed():
            other.show_damage_message('Промах')
            if need_update_attack_time:
                self.attack_time = time.time() + self.reloading_time
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

            targets = [
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
                        pygame.Rect(targets).colliderect(x) and
                        x is not other
                ):
                    self.attack(x, False)
            self.splash_radius = s

        other.attacked(self.damage, self.shield_damage)
        self.health += self.vampirism * abs(self.damage)
        if self.health > self.param['health']:
            self.health = self.param['health']
        if need_update_attack_time:
            self.attack_time = time.time() + self.reloading_time
        if self.die_on_attack:
            self.health = 0
        if self.run_effect:
            self.time_go = time.time()
        if self.stun:
            other.stunned = time.time() + self.stun
        #   "SMT -attack-> SMT"
        # print(self.__class__.__name__+' -attack-> '+other.__class__.__name__)

    def attacked(self, damage, shield_damage=None):
        if shield_damage is None:
            shield_damage = damage

        if self.shield > 0:
            self.shield -= shield_damage
            dmg = shield_damage
        else:
            self.health -= damage
            dmg = damage
        if dmg > 0:
            self.show_damage_message(f'-{dmg}')

    def update(self):
        self.update_()
        if self.self_spawn_time <= time.time():
            if self.stunned >= time.time():
                self.need_update_properties = True
                self.damage = 0
                self.speed = 0
                self.attack_time = self.stunned + self.reloading_time
                self.time_go = self.stunned

                i = pygame.image.load('images/stunned.png')
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
            if self.aura and self.aura_time < time.time():
                self.aura_time = time.time() + self.aura_reloading_time

                surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)
                pygame.draw.circle(
                    surf,
                    tuple(self.command + (50,)),
                    self.rect.center,
                    self.aura_radius,
                    2
                )
                self.screen.blit(surf, [0, 0])

                targets = [
                    self.rect.centerx - self.aura_radius,
                    self.rect.centery - self.aura_radius,
                    self.aura_radius * 2,
                    self.aura_radius * 2
                ]
                for x in self.group:
                    if (
                            x.command != self.command and
                            pygame.Rect(targets).colliderect(x)
                    ):
                        x.health -= self.aura_damage
            self.choose_target()
            self.auto_go()
            return True
        return False

    def update_(self):
        text = health_font.render(
            str(round((self.health if self.health >= 0 else 0) if self.shield <= 0 else self.shield)),
            1,
            WHITE,
            self.command if self.shield <= 0 else GREY
        )
        text_rect = text.get_rect(center=[self.rect.centerx, self.rect.top - 8])
        self.screen.blit(text, text_rect)

        for dmg in self.damage_texts:
            dmg.update()
            dmg.draw(self.screen)



    def auto_go(self):
        targets = [
            self.rect.centerx - self.attack_radius,
            self.rect.centery - self.attack_radius,
            self.attack_radius * 2,
            self.attack_radius * 2
        ]
        if pygame.Rect(targets).colliderect(self.target_coords):
            return self.auto_attack()

        move_x = 0
        move_y = 0
        if not primerno_ravno(self.rect.centerx, self.target_coords.centerx, self.speed):
            if self.rect.centerx < self.target_coords.centerx:
                move_x = self.speed
            if self.rect.centerx > self.target_coords.centerx:
                move_x = - self.speed
        if not primerno_ravno(self.rect.centery, self.target_coords.centery, self.speed):
            if self.rect.centery < self.target_coords.centery:
                move_y = self.speed
            if self.rect.centery > self.target_coords.centery:
                move_y = - self.speed
        self.move(move_x, move_y)

    def auto_attack(self):
        best = None
        targets = [
            self.rect.centerx - self.attack_radius,
            self.rect.centery - self.attack_radius,
            self.attack_radius * 2,
            self.attack_radius * 2
        ]
        for x in self.group:
            if (
                    x.command == self.attack_command and
                    pygame.Rect(targets).colliderect(x) and
                    isinstance(x, eval(self.attack_only)) and
                    not isinstance(x, eval(self.dont_attack))
            ):
                if (
                        best is None or
                        distance_between(best, self) > distance_between(self, x)
                ):
                    best = x
        if best is not None:
            self.attack(best)

    def move(self, move_x, move_y):
        self.rect.centerx += move_x
        self.rect.centery += move_y

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
                if type(i).__name__ == 'Spawn' and i.command == self.command:
                    self.target_coords = i.rect
        else:
            best = None
            for x in self.group:
                if (
                        x.command == self.attack_command and
                        isinstance(x, eval(self.attack_only)) and
                        not isinstance(x, eval(self.dont_attack))
                ):
                    if not x.died and (
                            best is None or
                            distance_between(self, best) > distance_between(self, x)
                    ):
                        best = x
            if best is not None:
                self.target_coords = best.rect

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(health = {self.health}, damage = {self.damage}, "
            f"reloading_time = {self.reloading_time}, speed = {self.speed})"
        )


class Building(Unit):
    params_name = 'building'

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


class Spell(pygame.sprite.Sprite):
    params_name = 'spell'

    def __init__(self, self_group, other_group, command, coords, screen, sp_reversed):
        super().__init__()
        self.self_group = self_group
        self.other_group = other_group
        self.command = command
        if self.param.get('image') is not None:
            self.image = pygame.image.load(self.param['image'][command])
            self.rect = self.image.get_rect(center=coords[:2])
        self.self_group.add(self)
        self.screen = screen
        self.reversed = sp_reversed

    @property
    def param(self):
        return UNITS[type(self).params_name]

    def __repr__(self):
        return f'{self.__class__.__name__}(command = {self.command}, rect={self.rect})'
