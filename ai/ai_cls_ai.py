import random
from unit import UNITS


class Ai:
    def __init__(self, castle, towers, key_analyse, spawner, modules):
        self.command = castle.command
        self.modules = modules
        self.castle = castle
        self.spawner = spawner
        self.screen = self.spawner.screen
        self.key_analyse = key_analyse
        self.towers = towers
        self.deck = []
        self.tmp_healths = self.healths
        self.atack_started = False
        self.atack_main_unit = None
        self.atack_unit_count = 0

    @property
    def healths(self):
        return self.castle.health, self.towers[0].health, self.towers[1].health

    def make_deck(self, units):
        units = units[:]
        random.shuffle(units)
        while len(self.deck) < 10:
            unit = units.pop()
            if 'ai_ignore' not in UNITS[unit.__name__.lower()]['roles']:
                self.deck.append(unit)

        return self.deck

    def analyse(self, group, points):
        res = []
        for i in self.modules:
            if i.triggered(self, group, points):
                res.append(i.make_move(self, group))
        try:
            return min(res, key=lambda x: sum(i.points for i in x))
        except ValueError:
            return None
        except TypeError:
            return None

    def make_move(self, group, points):
        best_move = self.analyse(group, points)
        if best_move is not None:
            for i in best_move:
                i.create()
        self.tmp_healths = self.healths
