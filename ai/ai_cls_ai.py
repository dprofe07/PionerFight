import random
from unit import UNITS


class Ai:
    def __init__(self, gamer, modules):
        self.gamer = gamer
        self.command = gamer.command
        self.modules = modules
        self.screen = self.gamer.spawner.screen
        self.deck = []
        self.tmp_healths = self.healths
        self.attack_started = False
        self.attack_main_unit = None
        self.attack_unit_count = 0

    @property
    def healths(self):
        return self.gamer.castle.health, self.gamer.tower1.health, self.gamer.tower2.health

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

    def make_move(self, group):
        best_move = self.analyse(group, self.gamer.points)
        if best_move is not None:
            for i in best_move:
                i.create()
        self.tmp_healths = self.healths
