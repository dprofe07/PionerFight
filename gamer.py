import pickle
import time

from base_units import Spell
from classes import ALL_UNITS, List, ShowError, UnitInfo, SpellInfo
from unit import UNITS
from constants import WAIT_BEFORE_START, START_POINTS, GREEN, RED
from funcs import can_create_unit


class Gamer:
    def __init__(self, color, ru_name, en_name):
        self.color = color
        self.ru_name = ru_name
        self.en_name = en_name
        self.last_deck = []
        self.login = ''

        self.saved_decks = []

        self.deck = List()
        self.used = {
            k.params_name: v
            for k, v in
            zip(ALL_UNITS, [UNITS[x.params_name]['wait'] + time.time() + WAIT_BEFORE_START for x in ALL_UNITS])

        }
        self.points = START_POINTS
        self.time_add_points = 0
        self.pressed_fill_button = False

        self.spawner = None
        self.castle = None
        self.tower1 = None
        self.tower2 = None
        self.random_unit = None

    def handle_spawner_move(self, pressed, key, key_down, key_up, key_right, key_left):
        if self.spawner is None:
            return
        if key == key_down:
            self.spawner.down = pressed
        elif key == key_up:
            self.spawner.up = pressed
        elif key == key_right:
            self.spawner.right = pressed
        elif key == key_left:
            self.spawner.left = pressed

    def handle_random_unit(self, screen, group, spells):
        r_unit = self.random_unit.unit
        err = can_create_unit(group, r_unit, self)
        if err:
            self.used[r_unit.params_name] = time.time() + UNITS[r_unit.params_name].get('wait', 0)
            r_unit(screen, self.color, self.spawner.rect.center, group, False)
            self.random_unit.time = 0

            self.points -= UNITS[r_unit.params_name].get('points', 0)
        else:
            ShowError(spells, self.color, err.message)

    def init_spawner(self, spawner):
        if self.spawner is None:
            self.spawner = spawner

    def init_castles(self, castle, tower1, tower2):
        if self.castle is None:
            self.castle = castle
        if self.tower1 is None:
            self.tower1 = tower1
        if self.tower2 is None:
            self.tower2 = tower2

    def init_random_unit(self, random_unit):
        if self.random_unit is None:
            self.random_unit = random_unit

    def key_analyse(self, number, screen, group, spells, only_info=False):
        try:
            unit = self.deck[number]
        except IndexError:
            return

        unit_params = UNITS[unit.params_name]

        err = can_create_unit(group, unit, self)
        if not err:
            ShowError(spells, self.color, err.message)
            return err.message
        if not only_info:
            self.used[unit.params_name] = time.time() + unit_params.get('wait', 0)
            self.points -= unit_params.get('points', 0)
        if issubclass(unit, Spell):
            # noinspection PyArgumentList
            un = SpellInfo(
                unit,
                screen,
                spells,
                group,
                self.color,
                self.spawner.reverse
            )
        else:
            un = UnitInfo(
                unit,
                screen,
                self.color,
                self.spawner.rect.center,
                group,
                self.spawner.reverse
            )
        if not only_info:
            un.create()
        return un

    def load_info(self, login):
        self.login = login
        try:
            with open('users/' + login + '.usr', 'rb') as f:
                dct = pickle.load(f)
                self.saved_decks = dct['decks']
                self.last_deck = dct['last_deck']

        except FileNotFoundError:
            with open('users/' + login + '.usr', 'wb') as f:
                dct = self.get_default_data()
                pickle.dump(dct, f)
            self.load_info(login)

    def save_info(self):
        with open('users/' + self.login + '.usr', 'wb') as f:
            pickle.dump(self.to_dict(), f)

    def to_dict(self):
        return {
            'decks': self.saved_decks,
            'last_deck': [i.params_name for i in self.deck],
        }

    @staticmethod
    def get_default_data():
        return {
            'decks': [
                [], [], [], [], [], [], []
            ],
            'last_deck': [],
        }


green_gamer = Gamer(GREEN, 'зелёные', 'green')
red_gamer = Gamer(RED, 'красные', 'red')
