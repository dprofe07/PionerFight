import random

from constants import GREEN
from funcs import debug


class Module:
    def __init__(self):
        self.wait_points = False
        self.wait_points_target = -1
        self.prev_unit = None

    def triggered(self, ai, group_of_units, points):
        raise NotImplementedError

    def make_move(self, ai, group_of_units, time=0):
        raise NotImplementedError

    # noinspection PyMethodMayBeStatic
    def select_unit(self, ai, number):
        return ai.key_analyse(ai.gamer, number)

    def get_rnd_unit(self, ai, role=None, time=0):
        if time > 10:
            return None
        unit = self.select_unit(ai, random.randint(0, 9))
        if isinstance(unit, str) or unit == self.prev_unit:
            return self.get_rnd_unit(ai, role, time + 1)
        if role is None or role in unit.param['roles']:
            print(f'For role {role} found unit class {unit.class_}; unit roles = {unit.param["roles"]}')
            self.prev_unit = unit
            return unit
        return self.get_rnd_unit(ai, role, time + 1)

    def wait_for_points(self, pnts):
        self.wait_points = True
        self.wait_points_target = pnts


class CastleOrTowerInDanger(Module):
    def triggered(self, ai, group_of_units, points):
        if self.wait_points and points < self.wait_points_target:
            return False

        for tower_or_castle in [ai.castle, ai.towers[0], ai.towers[1]]:
            castle_region = [
                tower_or_castle.rect.centerx - 150,
                tower_or_castle.rect.centery - 150,
                300,
                300
            ]

            for i in group_of_units:
                if i.command != ai.command and i.rect.colliderect(castle_region):
                    return True
        return False

    def make_move(self, ai, group_of_units, time=0):
        if time > 25:
            return []
        self.wait_for_points(random.randint(5, 10) * 100)
        ai.attack_started = False
        res = []
        for tower_or_castle in [ai.castle, ai.towers[0], ai.towers[1]]:
            castle_region = [
                tower_or_castle.rect.centerx - 150,
                tower_or_castle.rect.centery - 150,
                300,
                300
            ]

            for i in group_of_units:
                if i.command != ai.command and i.rect.colliderect(castle_region):
                    ai.spawner.reversed = False
                    ai.spawner.rect.center = tower_or_castle.rect.center
            unit = self.get_rnd_unit(ai, 'deaf')
            if unit is None:
                continue
            res.append(unit)
        return res


class CastleOrTowerDamaged(Module):
    def triggered(self, ai, group_of_units, points):
        if self.wait_points and points < self.wait_points_target:
            return False
        return ai.tmp_healths != ai.healths

    def make_move(self, ai, group_of_units, time=0):
        if time > 25:
            return []
        self.wait_for_points(random.randint(5, 10) * 100)
        ai.attack_started = False
        res = []
        for tower_or_castle, h_tmp, h_now in zip([ai.castle, ai.towers[0], ai.towers[1]], ai.tmp_healths, ai.healths):
            if h_tmp == h_now:
                continue
            ai.spawner.reversed = False
            ai.spawner.rect.center = tower_or_castle.rect.center
            unit = self.get_rnd_unit(ai, 'deaf')
            if unit is None:
                continue
            res.append(unit)
        return res


class Atack(Module):
    @debug
    def triggered(self, ai, group_of_units, points):
        if self.wait_points and points < self.wait_points_target:
            return False
        # noinspection PyRedundantParentheses
        return (
                (ai.attack_started) or
                (not any(i.triggered(ai, group_of_units, points) for i in ai.modules if i is not self))
        )

    def make_move(self, ai, group_of_units, time=0):
        if time > 10:
            return []

        ai.spawner.reversed = False
        if ai.attack_started:
            print('Atack had started DAVNO')
            if ai.attack_unit_count >= 5:
                print('Atack STOPED')
                ai.attack_main_unit = None
                ai.attack_started = False
                ai.attack_unit_count = 0
                self.wait_for_points(random.randint(5, 20) * 100)
                return []
            try:
                ai.spawner.rect.center = ai.attack_main_unit.rect.center
            except AttributeError:
                ai.attack_started = False
                return []
            ai.spawner.rect.centerx += 30 * (int(ai.command == GREEN) * 2 - 1)

            unit = self.get_rnd_unit(ai, 'support')
            if unit is None:
                unit = self.get_rnd_unit(ai, 'atack')
                if unit is None:
                    return []
            unit.on_create = lambda self: [
                setattr(ai, 'atack_unit_count', ai.attack_unit_count + 1)
            ]
            return [unit]
        else:
            ai.spawner.move(random.randint(-300, 300), random.randint(-300, 300))

            unit = self.get_rnd_unit(ai, 'atack')
            if unit is None:
                return []

            def unit_on_create(a):
                def on_death(b):
                    b.on_death(b)
                    ai.attack_started = False

                ai.attack_started = True
                ai.attack_main_unit = a.created
                ai.attack_unit_count = 1
                print('Starting atack')

            unit.on_create = unit_on_create

            return [unit]


AI_MODULES = [
    CastleOrTowerInDanger,
    CastleOrTowerDamaged,
    Atack,
]
