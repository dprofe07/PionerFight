# ***funcs.py***

import math
import time
from tkinter import *
import tkinter as tk
from tkinter import tix

from unit import UNITS, HELP
from constants import RED, GREEN


def check_number(group):
    g = r = 0
    for x in group:
        if x.command == GREEN:
            g += 1
        elif x.command == RED:
            r += 1
    return g - 3, r - 3


def primerno_ravno(one, two, eps=5):
    if hasattr(one, '__iter__') and hasattr(two, '__iter__'):
        return all(primerno_ravno(o, t, eps) for o, t in zip(one, two))
    elif isinstance(one, int) and isinstance(two, int):
        return (one - eps < two < one + eps) and (two - eps < one < two + eps)


def delete_extra(group):

    while check_number(group)[0] > 50:
        for x in reversed(group.sprites()):
            if x.command == GREEN:
                group.remove(x)
                break

    while check_number(group)[1] > 50:
        for x in reversed(group.sprites()):
            if x.command == RED:
                group.remove(x)
                break


def help_():
    def else_(name, f, p):
        a = UNITS[name]
        b = {
            'atack_radius': 'Радиус атаки',
            'boom_damage': "Урон от взрыва",
            'boom_radius': "Радиус взрыва",
            'damage': "Урон",
            'effect_time': "Длительность эффекта(с)",
            'force': "Сила толчка",
            'get_radius': "Радиус сбора воинов",
            'health': "Здоровье",
            'hill': "Исцеление",
            'hill_radius': "Радиус исцеления",
            'hill_reloading_time': "Пауза между исцелениями(с)",
            'max_number': "Максимальное кол-во воинов",
            'number': "Количество воинов",
            'reloading_time': "Перезарядка(с)",
            'resurrect_time': "Пауза между воскрешениями воинов(с)",
            'run_damage': "Урон при разгоне",
            'run_speed': "Скорость при разгоне",
            'run_time': "Время разгона(с)",
            'self_damage': "Урон по своим усилен в (раз)",
            'spawn_time': "Время создания(с)",
            'speed': "Скорость",
            'speed_radius': "Радиус ускорения",
            'speeding': "Ускорение(р)",
            'time_spawn': "Время появления(с)",
            'vampire_radius': "Радиус раздачи вампиризма",
            'vampirism': "Вампиризм",
            'venom': "Отравление(часть от своего урона)",
            'venom_time': "Время отравления(с)",
            'splash_radius': 'Радиус сплеш-атаки',
            'reversed': 'Возможно использовать на чужой половине(True = да, False = нет)',
            'reversed_damage': 'Урон на чужой половине',
        }
        
        if len(f.children) == 0:
            fr = Frame(f, borderwidth=3, relief="solid")
            fr.pack(anchor=W)
            for x in a:
                if x in b:
                    Label(fr, text=f'{b[x]}: {a[x]}').pack(anchor=W)
            p['text'] = 'Скрыть подробности'
        else:
            f.children[list(f.children.keys())[0]].destroy()
            f.config(height="1")
            p['text'] = 'Показать подробности'

    hw = tk.Tk()
    hw.title('Help')
    # noinspection PyDeprecation
    qw = tix.ScrolledWindow(hw, height="500")
    qw.pack()
    Label(qw.window, text="Описание воинов", font=('Arial', 20)).pack()

    for k, v in HELP.items():
        Label(qw.window, text='-' * 212).pack(anchor=W)

        fr = Frame(qw.window)
        fr.pack(anchor=W, fill=X)

        Label(fr, text=' ' + v, justify=LEFT).pack(side=LEFT)
        a = Label(fr, text='Показать подробности', fg="blue", cursor="hand2",
                  font=('Arial', 10, 'underline'))
        a.pack(side=RIGHT, anchor=E)

        fr2 = Frame(qw.window)
        fr2.pack(anchor=W)

        a.bind('<Button-1>', lambda x, k=k, f=fr2, p=a: else_(k, f, p))
    Label(qw.window, text='=' * 132).pack(anchor=W)
    Label(qw.window, text='Пояснения:', font=('Arial', 18)).pack()
    Label(qw.window, text=' Вампиризм - воин восстанавливает себе '
                          'здоровье нанося урон противникам').pack(anchor=W)
    Label(qw.window, text=' Разгон - эффект, при наличии которого воин '
                          'при непрерывном движении  некоторое кол-во времени, 1 раз увеличивает '
                          'себе скорость и урон.\nПри атаке разгон сбрасывается').pack(anchor=W)
    Label(qw.window, text=' Сплеш-урон - урон наносится не 1 определённой цели, '
                          'а всем целям в области.').pack(anchor=W)
    Label(qw.window, text=' Эффект отравления - эффект, при наличии которого у цели, '
                          'ей постоянно наносится небольшой урон. '
                          'ВНИМАНИЕ: Этот эффект постоянно активен у зданий.').pack(anchor=W)
    hw.mainloop()


def distance_between(obj1, obj2):
    x1, y1 = obj1.rect.center
    x2, y2 = obj2.rect.center
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def count_units(group, cls, command):
    res = 0
    for i in group:
        if type(i) == cls and i.command == command:
            res += 1
    return res


def n_maxes(n, lst: list, key=None):
    if n > len(lst):
        return lst
    lst = lst[:]
    res = [min(lst, key=key) for _ in range(n)]

    for i in range(len(res)):
        try:
            res[i] = max(lst, key=key)
        except ValueError:
            break
        lst.remove(res[i])

    return res


def can_create_unit(group, unit, spawner, used, points):
    unit_name = unit.__name__.lower()
    unit_params = UNITS[unit_name]
    command = spawner.command
    command_name = 'red' if command == RED else 'green'
    if check_number(group)[0 if command == GREEN else 1] >= 50:
        return Error('Макс. кол-во воинов достигнуто')
    if not unit_params.get('reversed', 0) and spawner.reverse:
        return Error('Сначала выйдите из реверсированного режима')
    if unit_params.get('max_count', 51) <= count_units(group, unit, command):
        return Error('Максимальное количество таких воинов достигнуто')
    if unit_params.get('points', 0) > points:
        return Error('Не хватает очков')
    if used[command_name][unit_name] > time.time():
        return Error('Подождите немного')
    return True


class Error:
    def __init__(self, message=''):
        self.message = message

    def __bool__(self):
        return False


def debug(fn):
    def wrapper(*a, **kw):
        print(f'runned function {fn.__name__} with {a=}, {kw=}')
        res = fn(*a, **kw)
        print(f'returned: {res}')
        return res
    return wrapper
