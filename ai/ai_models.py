import random

from constants import RED, GREEN
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
        return ai.key_analyse(ai.command, number)

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
        ai.atack_started = False
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
        ai.atack_started = False
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
            (ai.atack_started) or
            (not any(i.triggered(ai, group_of_units, points) for i in ai.modules if i is not self))
        )

    def make_move(self, ai, group_of_units, time=0):
        if time > 10:
            return []

        ai.spawner.reversed = False
        if ai.atack_started:
            print('Atack had started DAVNO')
            if ai.atack_unit_count >= 5:
                print('Atack STOPED')
                ai.atack_main_unit = None
                ai.atack_started = False
                ai.atack_unit_count = 0
                self.wait_for_points(random.randint(5, 20) * 100)
                return []
            try:
                ai.spawner.rect.center = ai.atack_main_unit.rect.center
            except AttributeError:
                ai.atack_started = False
                return
            ai.spawner.rect.centerx += 30 * (int(ai.command == GREEN) * 2 - 1)

            unit = self.get_rnd_unit(ai, 'support')
            if unit is None:
                unit = self.get_rnd_unit(ai, 'atack')
                if unit is None:
                    return []
            unit.oncreated = lambda self: [
                setattr(ai, 'atack_unit_count', ai.atack_unit_count + 1)
            ]
            return [unit]
        else:
            ai.spawner.move(random.randint(-300, 300), random.randint(-300, 300))

            unit = self.get_rnd_unit(ai, 'atack')
            if unit is None:
                return []

            unit.oncreate = lambda self: [
                setattr(ai, 'atack_started', True),
                setattr(ai, 'atack_main_unit', self.created),
                setattr(ai, 'atack_unit_count', 1),
                setattr(unit, 'ondeath', lambda self: [
                    (self.ondeath if hasattr(self, 'ondeath') else lambda self: None)(self),
                    setattr(ai, 'atack_started', False)
                ]),
                print('Starting atack'),
            ]

            return [unit]


AI_MODULES = [
    CastleOrTowerInDanger,
    CastleOrTowerDamaged,
    Atack,
]
