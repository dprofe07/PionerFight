import time

from classes import ALL_UNITS, List, ShowError
from unit import UNITS
from constants import WAIT_BEFORE_START, START_POINTS, GREEN, RED
from funcs import can_create_unit


class Gamer:
    def __init__(self, color, ru_name, en_name):
        self.color = color
        self.ru_name = ru_name
        self.en_name = en_name

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


green_gamer = Gamer(GREEN, 'зелёные', 'green')
red_gamer = Gamer(RED, 'красные', 'red')
