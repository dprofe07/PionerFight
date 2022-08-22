import sys
from functools import partial

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from base_units import Spell
from classes import Soldat, Archer, Gigant, Meteor, DoubleDamage, Hill, Rocket, Cannon, Sparky, SoldatSpawner, Collector


class ModesSelectorWindow(QWidget):
    def __init__(self, all_units):
        super().__init__()

        self.need_ask_decks = True
        self.result_deck = []
        self.all_units = all_units
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
        self.init_modes()

        for i, mode_name in enumerate(self.modes):
            btn = QPushButton(self.modes[mode_name]['name'])
            btn.clicked.connect(partial(self.on_mode_click, mode_name))
            self.hboxes[i * len(self.hboxes) // len(list(self.modes.keys()))].addWidget(btn)

        self.setFixedSize(0, 0)
        self.show()

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
            'no_spells': {
                'name': 'Без заклинаний',
                'need_ask_decks': True,
                'deck': [],
                'use_random_unit': True,
                'all_units': list(filter(lambda i: not issubclass(i, Spell), self.all_units))
            },
            'no_random': {
                'name': 'Без случайного воина',
                'need_ask_decks': True,
                'deck': [],
                'use_random_unit': False,
                'all_units': self.all_units
            },
            'no_spells_random': {
                'name': 'Без заклинаний и случайного воина',
                'need_ask_decks': True,
                'deck': [],
                'use_random_unit': False,
                'all_units': list(filter(lambda i: not issubclass(i, Spell), self.all_units))
            },
            'random': {
                'name': 'Только рандом',
                'need_ask_decks': False,
                'deck': [],
                'use_random_unit': True,
                'all_units': []
            },
            'standard': {
                'name': 'Обычный',
                'need_ask_decks': True,
                'deck': [],
                'use_random_unit': True,
                'all_units': self.all_units,
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
        self.all_units = mode['all_units']
        self.need_ask_decks = mode['need_ask_decks']
        self.use_random_unit = mode['use_random_unit']
        self.success = True
        self.close()