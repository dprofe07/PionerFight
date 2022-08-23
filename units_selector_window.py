import pickle
import sys
from functools import partial

from PyQt5.QtWidgets import QLabel,  QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QCheckBox, QMessageBox
from PyQt5.QtCore import Qt

from constants import RED
from unit import UNITS


class UnitsSelectorWindow(QWidget):
    def __init__(self, gamer, units_list):
        super().__init__()

        self.success = False
        self.gamer = gamer
        self.units_list = units_list

        self.command_ru = 'красных' if self.gamer.color == RED else 'зелёных'
        self.command_en = self.gamer.en_name

        self.setWindowTitle(f'Выбор воинов для {self.command_ru}')

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.hbox_units = QHBoxLayout()
        self.vboxes_for_units = []
        for i in range(round(len(self.units_list) / 10)):
            vbox = QVBoxLayout()
            self.vboxes_for_units.append(vbox)
            self.hbox_units.addLayout(vbox)

        self.check_boxes = []
        for i, unit in enumerate(units_list):
            chk_box = QCheckBox(UNITS[unit.params_name]['name'])
            chk_box.stateChanged.connect(self.update_interface_after_change)
            self.setStyleSheet("background-color: rgb(%d, %d, %d);" % self.gamer.color)
            self.check_boxes.append(chk_box)
            self.vboxes_for_units[i * len(self.vboxes_for_units) // len(units_list)].addWidget(chk_box)

        self.vbox.addLayout(self.hbox_units)

        self.lbl_save_decks = QLabel("Сохранить колоды:")
        self.lbl_save_decks.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.lbl_save_decks)

        self.hbox_save_decks = QHBoxLayout()
        self.btns_save = []
        for i in range(len(self.gamer.saved_decks)):
            btn = QPushButton(str(i + 1))
            btn.clicked.connect(partial(self.on_save_btn_click, i))
            self.btns_save.append(btn)
            self.hbox_save_decks.addWidget(btn)
        self.vbox.addLayout(self.hbox_save_decks)

        self.lbl_save_decks = QLabel("Использовать колоды:")
        self.lbl_save_decks.setAlignment(Qt.AlignCenter)
        self.vbox.addWidget(self.lbl_save_decks)

        self.hbox_load_decks = QHBoxLayout()
        self.btns_load = []
        for i in range(len(self.gamer.saved_decks)):
            btn = QPushButton(str(i + 1))
            btn.clicked.connect(partial(self.on_load_btn_click, i))
            self.btns_load.append(btn)
            self.hbox_load_decks.addWidget(btn)

        self.vbox.addLayout(self.hbox_load_decks)

        self.btn_help = QPushButton('HELP')
        self.vbox.addWidget(self.btn_help)

        self.btn_ok = QPushButton('OK')
        self.btn_ok.clicked.connect(self.on_ok_button_click)
        self.vbox.addWidget(self.btn_ok)

        self.units_names = [i.params_name for i in self.units_list]
        for i in self.check_boxes:
            i.setCheckState(0)
        for name in self.gamer.last_deck:
            try:
                self.check_boxes[self.units_names.index(name)].setCheckState(2)
            except ValueError:
                # print(f'Value Error! {name=}!')
                mb = QMessageBox(
                    QMessageBox.Warning,
                    "Предупреждение",
                    f"Не найден воин (заклинание) \"{UNITS.get(name, {'name': name}).get('name', 'Штука')}\"",
                    QMessageBox.Ok
                )
                mb.exec()

        self.update_interface_after_change()

        self.setFixedSize(0, 0)
        self.show()

    def closeEvent(self, a0):
        a0.accept()
        super().closeEvent(a0)
        if not self.success:
            sys.exit()

    def on_ok_button_click(self):
        for i, chk_box in enumerate(self.check_boxes):
            if chk_box.checkState() == 2:
                self.gamer.deck.append(self.units_list[i])
        self.success = True
        self.gamer.save_info()
        self.close()

    def on_load_btn_click(self, number):
        for i in self.check_boxes:
            i.setCheckState(0)
        for name in self.gamer.saved_decks[number
        
        ]:
            try:
                self.check_boxes[self.units_names.index(name)].setCheckState(2)
            except ValueError:
                # print(f'Value Error! {name=}!')
                mb = QMessageBox(
                    QMessageBox.Warning,
                    "Предупреждение",
                    f"Не найден воин (заклинание) \"{UNITS[name].get('name', 'Штука')}\"",
                    QMessageBox.Ok
                )
                mb.exec()

        self.update_interface_after_change()

    def on_save_btn_click(self, number):
        self.gamer.saved_decks[number] = [
            self.units_names[i]
            for i in range(len(self.check_boxes))
            if self.check_boxes[i].checkState() == 2
        ]
        self.gamer.save_info()

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
