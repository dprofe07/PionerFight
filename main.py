import random

import pygame
import time
import tkinter as tk
import tkinter.ttk as ttk
import sys
import pickle

# IMPORTS

from funcs import delete_extra, help_, check_number, can_create_unit, debug
from classes import (
    ALL_UNITS, Building, Spell,
    List, Castle, Tower,
    Collector, ShowError,
    Spawn, UnitInfo, SpellInfo, RandomUnit
)
from ai.ai_main import Ai, AI_MODULES
from unit import UNITS
from constants import (
    WIDTH, HEIGHT,
    RED, GREEN, BLACK, WHITE,
    BG,
    font, PAUSE_FONT,
    START_POINTS, PAUSE_ADD_POINTS, ADD_POINTS, MAX_POINTS,
    WAIT_BEFORE_START, LST_RED_KEYS, LST_GREEN_KEYS,
)


pygame.init()

used = {
    'red': {k.__name__.lower(): v for k, v in zip(
        ALL_UNITS,
        [UNITS[x.__name__.lower()]['wait'] + time.time() + WAIT_BEFORE_START for x in ALL_UNITS])},
    'green': {k.__name__.lower(): v for k, v in zip(ALL_UNITS, [
        UNITS[x.__name__.lower()]['wait'] + time.time() + WAIT_BEFORE_START for x in ALL_UNITS])},
}
GREEN_POINTS = START_POINTS
RED_POINTS = START_POINTS
TIME_ADD_RED = 0
TIME_ADD_GREEN = 0

GREEN_DECK = List()
RED_DECK = List()

AI_RED = False
AI_GREEN = False


def key_analyse(command, number, only_info=False):
    global used, GREEN_POINTS, RED_POINTS

    if command == RED:
        unit = RED_DECK[number]
        spawner = red_spawn
        command_name = 'red'
        points = RED_POINTS
        num_for_check_group = 1
    elif command == GREEN:
        unit = GREEN_DECK[number]
        spawner = green_spawn
        num_for_check_group = 0
        command_name = 'green'
        points = GREEN_POINTS
    else:
        raise ValueError('Command unknown')

    unit_name = unit.__name__.lower()
    unit_params = UNITS[unit_name]

    err = can_create_unit(group, unit, spawner, used, points)
    if not err:
        ShowError(spells, command, err.message)
        return err.message
    if not only_info:
        used[command_name][unit_name] = time.time() + unit_params.get('wait', 0)
        if command == GREEN:
            GREEN_POINTS -= unit_params.get('points', 0)
        else:
            RED_POINTS -= unit_params.get('points', 0)
    if issubclass(unit, Spell):
        # noinspection PyArgumentList
        un = SpellInfo(
            unit,
            screen,
            spells,
            group,
            command,
            spawner.reverse
        )
    else:
        un = UnitInfo(
            unit,
            screen,
            command,
            spawner.rect.center,
            group,
            spawner.reverse
        )
    if not only_info:
        un.create()
    return un


#@debug
def check_units_in_deck_count(vars_):
    return sum(1 for i in vars_ if i.get())


def update_interface_after_change(vars_, ok_button, window):
    if check_units_in_deck_count(vars_):
        ok_button['state'] = 'normal'
        for i in window.children['!frame2'].children.values():
            i['state'] = 'normal'
    else:
        ok_button['state'] = 'disabled'
        for i in window.children['!frame2'].children.values():
            i['state'] = 'disabled'


def save(deck, vars_):
    for x in vars_:
        if x.get():
            deck.append(ALL_UNITS[vars_.index(x)])


def save_deck(vars_, num, cmd):
    with open('decks/' + cmd + num + '.deck', 'wb') as file:
        pickle.dump([x.get() for x in vars_], file)


def use_deck(vars_, num, command, ok_button, window):
    num = str(num)
    try:
        with open('decks/' + command + num + '.deck', 'rb') as file:
            for num, x in enumerate(pickle.load(file)):
                try:
                    vars_[num].set(x)
                except IndexError:
                    print(f'Index Error! {num=}, {x=}!')
    except FileNotFoundError:
        for i in range(len(vars_)):
            vars_[i].set(False)

    update_interface_after_change(vars_, ok_button, window)


def resize_frames_in_units_selector(fr1, fr2, fr3):
    if fr3.winfo_width() % 2 == 0:
        fr1['width'] = fr3.winfo_width() // 2
        fr2['width'] = fr3.winfo_width() // 2
    else:
        fr1['width'] = fr3.winfo_width() // 2 + 1
        fr2['width'] = fr3.winfo_width() // 2


def select_units(command):
    if command == RED:
        command_text_en = 'red'
        command_text_ru = 'красных'
        deck = RED_DECK
    elif command == GREEN:
        command_text_en = 'green'
        command_text_ru = 'зелёных'
        deck = GREEN_DECK
    else:
        raise ValueError('Incorrect command!')

    window = tk.Tk()
    window.title(f'Выбор воинов для {command_text_ru}')
    window.protocol('WM_DELETE_WINDOW', lambda: [window.destroy(), sys.exit()])
    vars_ = []
    fr4 = tk.Frame(window)
    fr1 = tk.LabelFrame(fr4, bg=command_text_en)
    fr2 = tk.LabelFrame(fr4, bg=command_text_en)
    fr3 = tk.LabelFrame(fr4, bg=command_text_en)

    fr1.pack(side=tk.LEFT, fill=tk.BOTH)
    fr2.pack(side=tk.LEFT, fill=tk.BOTH)
    fr3.pack(side=tk.LEFT, fill=tk.BOTH)
    fr4.pack(side=tk.TOP, fill=tk.BOTH)
    for i in ALL_UNITS:
        vars_.append(tk.BooleanVar(window, False))

        if ALL_UNITS.index(i) < len(ALL_UNITS) // 3:
            cur_fr = fr1
        elif ALL_UNITS.index(i) < len(ALL_UNITS) // 3 * 2:
            cur_fr = fr2
        else:
            cur_fr = fr3
        tk.Checkbutton(
            cur_fr, bg=command_text_en, fg='white', selectcolor='black',
            text=UNITS[i.__name__.lower()].get('name', 'Штука'),
            variable=vars_[-1],
            command=lambda: update_interface_after_change(vars_, ok_button, window), anchor='w'
        ).pack()

    ttk.Label(window, text="Сохранить колоды:").pack()
    fr5 = tk.Frame(window)
    fr5.pack(fill=tk.X)
    for i in range(1, 8):
        a = tk.Button(
            fr5, text=str(i),
            command=lambda x=i: save_deck(vars_, str(x), command_text_en)
        )
        a['width'] = 7
        a.pack(fill=tk.X, side=tk.LEFT)
    fr5.pack()

    ttk.Label(window, text="Использовать колоды:").pack()
    fr6 = tk.Frame(window)

    fr6.pack(fill=tk.X)
    for i in range(1, 8):
        a = tk.Button(
            fr6, text=str(i),
            command=lambda i_=i: use_deck(vars_, i_, command_text_en, ok_button, window)
        )
        a['width'] = 7
        a.pack(fill=tk.X, side=tk.LEFT)
    fr5.pack()

    ok_button = ttk.Button(window, text="OK", command=lambda: [save(deck, vars_), window.destroy()])
    ok_button.pack(side=tk.BOTTOM, fill='x')
    ttk.Button(window, text="HELP", command=help_).pack(side=tk.BOTTOM, fill=tk.X)

    fr1.update_idletasks()

    update_interface_after_change(vars_, ok_button, window)

    window.after(500, lambda: resize_frames_in_units_selector(fr1, fr2, fr3))
    window.mainloop()


if not AI_RED:
    select_units(RED)
if not AI_GREEN:
    select_units(GREEN)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Пионерское побоище')

group = pygame.sprite.Group()
spells = pygame.sprite.Group()

red_castle = Castle(screen, RED, [260, HEIGHT // 2, 70, 70], group, False)
green_castle = Castle(screen, GREEN, [WIDTH - 260, HEIGHT // 2, 70, 70], group, False)

red_spawn = Spawn(spells, RED, [260, HEIGHT // 2, 70, 70])
green_spawn = Spawn(spells, GREEN, [WIDTH - 260, HEIGHT // 2, 70, 70])

red_random = RandomUnit(screen, spells, group, RED, False)
green_random = RandomUnit(screen, spells, group, GREEN, False)

rt1 = Tower(screen, RED, [360, 325, 70, 70], group, False)
rt2 = Tower(screen, RED, [360, 75, 70, 70], group, False)

gt1 = Tower(screen, GREEN, [840, 325, 70, 70], group, False)
gt2 = Tower(screen, GREEN, [840, 75, 70, 70], group, False)

pause = False
pressed = [False, False]

quest_mark_font = pygame.font.Font(None, 30)

ais = []
if AI_RED:
    modules = [
        i() for i in AI_MODULES
    ]
    ais.append(Ai(red_castle, [rt1, rt2], key_analyse, red_spawn, modules))
    RED_DECK = ais[-1].make_deck(ALL_UNITS)
if AI_GREEN:
    modules = [
        i() for i in AI_MODULES
    ]
    ais.append(Ai(green_castle, [gt1, gt2], key_analyse, green_spawn, modules))
    GREEN_DECK = ais[-1].make_deck(ALL_UNITS)

while not (red_castle.died or green_castle.died):
    for ai in ais:
        ai.make_move(group, [RED_POINTS, GREEN_POINTS][ai.command == GREEN])
    screen.fill(WHITE)
    for y, e in enumerate(RED_DECK):
        text = font.render(
            f'{(y if y < 9 else -1) + 1} - {UNITS[e.__name__.lower()].get("name", "Штука")} '
            f'({UNITS[e.__name__.lower()]["points"]})',
            1,
            BLACK
        )
        rect = text.get_rect(topleft=[25, 25 * y])
        screen.blit(text, rect)

    text = font.render(
        f'z - {UNITS[red_random.unit.__name__.lower()].get("name", "Штука")} '
        f'({UNITS[red_random.unit.__name__.lower()]["points"]})',
        1,
        BLACK
    )
    rect = text.get_rect(topleft=[25, 275])
    screen.blit(text, rect)

    for y, e in enumerate(GREEN_DECK):
        text = font.render(
            f'{(y if y < 9 else -1) + 1} - {UNITS[e.__name__.lower()].get("name", "Штука")} '
            f'({UNITS[e.__name__.lower()]["points"]})',
            1,
            BLACK
        )
        rect = text.get_rect(topleft=[1025, 25 * y])
        screen.blit(text, rect)

    text = font.render(
        f'/ - {UNITS[green_random.unit.__name__.lower()].get("name", "Штука")} '
        f'({UNITS[green_random.unit.__name__.lower()]["points"]})',
        1,
        BLACK
    )
    rect = text.get_rect(topleft=[1025, 275])
    screen.blit(text, rect)

    text = font.render('Кол-во воинов: ' + str(check_number(group)[1]), 1, BLACK)
    rect = text.get_rect(topleft=[25, 300])
    screen.blit(text, rect)

    text = font.render('Кол-во воинов: ' + str(check_number(group)[0]), 1, BLACK)
    rect = text.get_rect(topleft=[1025, 300])
    screen.blit(text, rect)

    text = quest_mark_font.render(' ? ', True, [255, 255, 255], [0, 0, 0])
    rect = text.get_rect(topright=[WIDTH, 0])
    screen.blit(text, rect)
    # dynamic graphic
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            red_castle.health = 0
            green_castle.health = 0
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            breakpoint()
        if e.type == pygame.KEYDOWN and not pause:
            # Make points full
            if e.key == pygame.K_KP_PERIOD:
                pressed[1] = True
            if e.key == pygame.K_TAB:
                pressed[0] = True
            # RED Cards

            for i in range(len(LST_RED_KEYS)):
                if e.key == LST_RED_KEYS[i]:
                    key_analyse(RED, i)

            # GREEN Cards

            for i in range(len(LST_GREEN_KEYS)):
                if e.key == LST_GREEN_KEYS[i]:
                    key_analyse(GREEN, i)

            # GIVING UP
            if e.key == pygame.K_KP_MINUS:
                green_castle.health = 0
            if e.key == pygame.K_ESCAPE:
                red_castle.health = 0
            # *** Retreating ***

            if e.key == pygame.K_LALT:
                for y in group:
                    if y.command == RED and not isinstance(y, Building):
                        y.retreat = not y.retreat

            if e.key == pygame.K_RALT:
                for y in group:
                    if y.command == GREEN and not isinstance(y, Building):
                        y.retreat = not y.retreat

            # MOVING RED SPAWNER
            if e.key == pygame.K_w:
                red_spawn.up = True

            if e.key == pygame.K_s:
                red_spawn.down = True

            if e.key == pygame.K_a:
                red_spawn.left = True

            if e.key == pygame.K_d:
                red_spawn.right = True

            if e.key == pygame.K_z and not red_spawn.reverse:
                err = can_create_unit(group, red_random.unit, red_spawn, used, RED_POINTS)
                if err:
                    used['red'][red_random.unit.__name__.lower()] = time.time() + UNITS[red_random.unit.__name__.lower()].get('wait', 0)
                    red_random.unit(screen, RED, [red_spawn.rect.centerx, red_spawn.rect.centery], group, False)
                    red_random.time = 0

                    RED_POINTS -= UNITS[red_random.unit.__name__.lower()].get('points', 0)
                else:
                    ShowError(spells, RED, err.message)

            if e.key == pygame.K_LSHIFT:
                red_spawn.reverse = not red_spawn.reverse
            # MOVING GREEN SPAWNER
            if e.key == pygame.K_UP:
                green_spawn.up = True

            if e.key == pygame.K_DOWN:
                green_spawn.down = True

            if e.key == pygame.K_RIGHT:
                green_spawn.right = True

            if e.key == pygame.K_LEFT:
                green_spawn.left = True

            if e.key == pygame.K_RSHIFT:
                green_spawn.reverse = not green_spawn.reverse

            if e.key == pygame.K_SLASH and not green_spawn.reverse:
                err = can_create_unit(group, green_random.unit, green_spawn, used, GREEN_POINTS)
                if err:
                    used['green'][green_random.unit.__name__.lower()] = time.time() + UNITS[green_random.unit.__name__.lower()].get('wait', 0)

                    green_random.unit(screen, GREEN, [green_spawn.rect.centerx, green_spawn.rect.centery], group, False)
                    green_random.time = 0

                    GREEN_POINTS -= UNITS[green_random.unit.__name__.lower()].get('points', 0)
                else:
                    ShowError(spells, GREEN, err.message)

        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
            pause = not pause
        if e.type == pygame.KEYUP:
            # Making points full
            if e.key == pygame.K_TAB:
                pressed[0] = False
            if e.key == pygame.K_KP_PERIOD:
                pressed[1] = False

            # MOVING RED SPAWNER
            if e.key == pygame.K_w:
                red_spawn.up = False

            if e.key == pygame.K_s:
                red_spawn.down = False

            if e.key == pygame.K_a:
                red_spawn.left = False

            if e.key == pygame.K_d:
                red_spawn.right = False

            # MOVING GREEN SPAWNER
            if e.key == pygame.K_UP:
                green_spawn.up = False

            if e.key == pygame.K_DOWN:
                green_spawn.down = False

            if e.key == pygame.K_RIGHT:
                green_spawn.right = False

            if e.key == pygame.K_LEFT:
                green_spawn.left = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            # Help
            if pygame.Rect(rect).collidepoint(e.pos):
                help_()
    screen.blit(BG, [200, 0, 800, 400])
    if all(pressed):
        RED_POINTS = MAX_POINTS
        GREEN_POINTS = MAX_POINTS
        ShowError(spells, RED, 'Очки заполнены!!!')
        ShowError(spells, GREEN, 'Очки заполнены!!!')
    if not pause:
        group.update()
        group.draw(screen)
        spells.update()
        spells.draw(screen)

        delete_extra(group)

        for e in group:
            if type(e) == Collector:
                # noinspection PyUnresolvedReferences
                if e.command == RED:
                    RED_POINTS = e.add(RED_POINTS)
                elif e.command == GREEN:
                    GREEN_POINTS = e.add(GREEN_POINTS)
                else:
                    # noinspection PyUnresolvedReferences
                    raise ValueError(f"Incorrect command: {e.command}")
        if TIME_ADD_GREEN <= time.time() and GREEN_POINTS < MAX_POINTS:
            TIME_ADD_GREEN = time.time() + PAUSE_ADD_POINTS
            GREEN_POINTS += ADD_POINTS
        if TIME_ADD_RED <= time.time() and RED_POINTS < MAX_POINTS:
            TIME_ADD_RED = time.time() + PAUSE_ADD_POINTS
            RED_POINTS += ADD_POINTS
    else:
        a = PAUSE_FONT.render('Пауза', 1, [0, 0, 0])
        screen.blit(a, a.get_rect(center=[WIDTH // 2, HEIGHT // 2]))
    for e, y in enumerate([f'{RED_POINTS}', f'{GREEN_POINTS}']):
        t = font.render(y, 1, [abs(255 * (e - 1)), 255 * e, 0], [255, 255, 255])
        r = t.get_rect(center=[WIDTH // 2, (HEIGHT * e) + 6 * (-1 if e == 1 else 1)])
        screen.blit(t, r)

    for e in group:
        # noinspection PyUnresolvedReferences
        if e.died and type(e) not in [Castle, Tower]:
            group.remove(e)
        elif e.died and type(e) in [Castle, Tower]:
            # noinspection PyUnresolvedReferences
            e.destroyed()
    time.sleep(0.05)

    for e in group:
        if e.rect.colliderect([575, 100, 50, 200]):
            if e.rect.centery > 200:
                e.rect.top = 305
            else:
                e.rect.bottom = 95
    pygame.display.flip()
else:

    screen.fill(WHITE)
    screen.blit(BG, [200, 0, 800, 400])
    win = 'none'
    caron = pygame.image.load('images/winner.png')

    group.update()
    group.draw(screen)

    if red_castle.died:
        red_castle.destroyed()
        screen.blit(caron, caron.get_rect(center=[WIDTH - 100, HEIGHT // 2 - 30]))
        win = 'green'
    if green_castle.died:
        green_castle.destroyed()
        screen.blit(caron, caron.get_rect(center=[100, HEIGHT // 2 - 30]))
        win = 'red' if win == 'none' else 'none'
    font = pygame.font.Font(None, 50)
    if win == 'green':
        text = font.render("Победили зелёные", True, [0, 0, 0])
    elif win == 'red':
        text = font.render("Победили красные", True, [0, 0, 0])
    elif win == 'none':
        text = font.render("Ничья!", True, [0, 0, 0])
    else:
        raise ValueError(f'Incorrect winner: {win}')

    screen.blit(text, text.get_rect(center=[WIDTH // 2, HEIGHT // 2]))

    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
