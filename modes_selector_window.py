import random
import sys
from functools import partial

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox

from base_units import Spell
from classes import Soldat, Archer, Gigant, Meteor, DoubleDamage, Hill, Rocket, Cannon, Sparky, SoldatSpawner, Collector


class ModesSelectorWindow(QWidget):
    def __init__(self, all_units):
        super().__init__()

        self.need_ask_decks = True
        self.result_deck = []
        self.all_units = all_units
        self.default_all_units = all_units[:]
        self.use_random_unit = True
        self.success = False

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.hboxes = [
            QHBoxLayout(),
            QHBoxLayout()
        ]
        for hbox in self.hboxes:
            self.vbox.addLayout(hbox)

        self.modes = {}
        self.ticks = {}

        self.init_modes()

        for i, mode_name in enumerate(self.modes):
            btn = QPushButton(self.modes[mode_name]['name'])
            btn.clicked.connect(partial(self.on_mode_click, mode_name))
            self.hboxes[i * len(self.hboxes) // len(list(self.modes.keys()))].addWidget(btn)

        for tick_name in self.ticks:
            chk_box = QCheckBox(self.ticks[tick_name]['name'])
            self.ticks[tick_name]['check_box'] = chk_box
            chk_box.stateChanged.connect(partial(self.on_tick_click, tick_name))
            chk_box.setCheckState(self.ticks[tick_name]['default_value'])
            self.on_tick_click(tick_name)
            self.vbox.addWidget(chk_box)

        self.setFixedSize(0, 0)
        self.show()

    def get_result_deck(self):
        if self.result_deck == 'random':
            return [random.choice(self.all_units) for _ in range(10)]
        return self.result_deck[:]

    def init_modes(self):
        self.modes = {
            'classic': {
                'name': 'Классика',
                'need_ask_decks': False,
                'deck': [Soldat, Archer, Gigant, Meteor],
                'use_random_unit': False,
                'all_units': [],
            },
            'classic_big': {
                'name': 'Расширенная классика',
                'need_ask_decks': False,
                'deck': [
                    Soldat, Archer, Gigant,
                    Hill, DoubleDamage, Meteor,
                    Cannon, Sparky, SoldatSpawner,
                    Collector
                ],
                'use_random_unit': False,
                'all_units': []
            },
            'random': {
                'name': 'Только рандом',
                'need_ask_decks': False,
                'deck': [],
                'use_random_unit': True,
                'all_units': []
            },
            'random_deck': {
                'name': 'Случайные колоды',
                'need_ask_decks': False,
                'deck': 'random',
            },
            'standard': {
                'name': 'Обычный',
                'need_ask_decks': True,
                'deck': [],
            }
        }

        self.ticks = {
            'no_random': {
                'name': 'Использовать случайного воина',
                'check_box': None,
                'states': {
                    2: {
                        'use_random_unit': True
                    },
                    0: {
                        'use_random_unit': False,
                    }
                },
                'default_value': 2,
            },
            'no_spells': {
                'name': 'Без заклинаний',
                'check_box': None,
                'states': {
                    2: {
                        'all_units_filter': lambda units: list(filter(lambda i: not issubclass(i, Spell), units)),
                    },
                    0: {
                        'all_units_filter': lambda units: units
                    },
                },
                'default_value': 0,
            }
        }

    def closeEvent(self, a0):
        a0.accept()
        super().closeEvent(a0)
        if not self.success:
            sys.exit()

    def on_mode_click(self, mode_name):
        mode = self.modes[mode_name]
        self.result_deck = mode['deck']
        if 'all_units' in mode:
            self.all_units = mode['all_units']
        self.need_ask_decks = mode['need_ask_decks']
        if 'use_random_unit' in mode:
            self.use_random_unit = mode['use_random_unit']
        self.success = True
        self.close()

    def on_tick_click(self, tick_name):
        doings = self.ticks[tick_name]['states'][self.ticks[tick_name]['check_box'].checkState()]
        if 'use_random_unit' in doings:
            self.use_random_unit = doings['use_random_unit']
        if 'all_units_filter' in doings:
            self.all_units = self.default_all_units
            for tick_2_name in self.ticks:
                doings_2 = self.ticks[tick_2_name]['states'][self.ticks[tick_2_name]['check_box'].checkState()]
                if 'all_units_filter' in doings_2:
                    self.all_units = doings_2['all_units_filter'](self.all_units)