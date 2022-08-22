import pickle
import sys
from functools import partial

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QFrame, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QCheckBox
from PyQt5.QtCore import Qt

from constants import RED, GREEN
from unit import UNITS


class UnitsSelectorWindow(QWidget):
    def __init__(self, command, units_list, deck):
        super().__init__()

        self.success = False
        self.deck = deck
        self.units_list = units_list

        self.command = command
        self.command_ru = 'красных' if command == RED else 'зелёных'
        self.command_en = 'red' if command == RED else 'green'

        self.setWindowTitle(f'Выбор воинов для {self.command_ru}')

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.hbox_units = QHBoxLayout()
        self.frames = [
            QVBoxLayout(),
            QVBoxLayout(),
            QVBoxLayout(),
            QVBoxLayout()
        ]
        self.check_boxes = []
        for i, unit in enumerate(units_list):
            chk_box = QCheckBox(UNITS[unit.params_name]['name'])
            chk_box.stateChanged.connect(self.update_interface_after_change)
            self.check_boxes.append(chk_box)
            self.frames[i * len(self.frames) // len(units_list)].addWidget(chk_box)

        for i in self.frames:
            self.hbox_units.addLayout(i)
        self.vbox.addLayout(self.hbox_units)

        self.lbl_save_decks = QLabel("Сохранить колоды:")
        self.lbl_save_decks.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.lbl_save_decks)

        self.hbox_save_decks = QHBoxLayout()
        self.btns_save = []
        for i in range(7):
            btn = QPushButton(str(i + 1))
            btn.clicked.connect(partial(self.on_save_btn_click, i + 1))
            self.btns_save.append(btn)
            self.hbox_save_decks.addWidget(btn)
        self.vbox.addLayout(self.hbox_save_decks)

        self.lbl_save_decks = QLabel("Использовать колоды:")
        self.lbl_save_decks.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.lbl_save_decks)

        self.hbox_load_decks = QHBoxLayout()
        self.btns_load = []
        for i in range(7):
            btn = QPushButton(str(i + 1))
            btn.clicked.connect(partial(self.on_load_btn_click, i + 1))
            self.btns_load.append(btn)
            self.hbox_load_decks.addWidget(btn)

        self.vbox.addLayout(self.hbox_load_decks)

        self.btn_help = QPushButton('HELP')
        self.vbox.addWidget(self.btn_help)

        self.btn_ok = QPushButton('OK')
        self.btn_ok.clicked.connect(self.on_ok_button_click)
        self.vbox.addWidget(self.btn_ok)

        self.update_interface_after_change()

        self.setFixedSize(self.size())
        self.show()

    def closeEvent(self, a0):
        a0.accept()
        super().closeEvent(a0)
        if not self.success:
            sys.exit()

    def on_ok_button_click(self):
        for i, chk_box in enumerate(self.check_boxes):
            if chk_box.checkState() == 2:
                self.deck.append(self.units_list[i])
        self.success = True
        self.close()

    def on_load_btn_click(self, number):
        num = str(number)
        try:
            with open('decks/' + self.command_en + num + '.deck', 'rb') as file:
                for num, x in enumerate(pickle.load(file)):
                    try:
                        self.check_boxes[num].setCheckState(int(x) * 2)
                    except IndexError:
                        print(f'Index Error! {num=}, {x=}!')
        except FileNotFoundError:
            for i in self.check_boxes:
                i.setCheckState(0)

        self.update_interface_after_change()

    def on_save_btn_click(self, number):
        with open('decks/' + self.command_en + str(number) + '.deck', 'wb') as file:
            pickle.dump([x.checkState() == 2 for x in self.check_boxes], file)

    def update_interface_after_change(self):
        if self.check_units_in_deck_count():
            self.btn_ok.setEnabled(True)
            for btn_save in self.btns_save:
                btn_save.setEnabled(True)
        else:
            self.btn_ok.setEnabled(False)
            for btn_save in self.btns_save:
                btn_save.setEnabled(False)

    def check_units_in_deck_count(self):
        return sum(1 for i in self.check_boxes if i.checkState() == 2) == 10
