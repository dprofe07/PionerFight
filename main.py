import pygame
import time
import sys
from PyQt5.QtWidgets import QApplication

# IMPORTS
from base_units import Unit
from funcs import delete_extra, help_, check_number, get_user_login
from classes import (
    ALL_UNITS, Building, Spell,
    Castle, Tower,
    Collector, ShowError,
    Spawn, UnitInfo, SpellInfo, RandomUnit
)
from ai.ai_main import Ai, AI_MODULES
from unit import UNITS
from constants import (
    WIDTH, HEIGHT,
    RED, GREEN, BLACK, WHITE, BG,
    font, PAUSE_FONT, PAUSE_ADD_POINTS, ADD_POINTS, MAX_POINTS,
    LST_RED_KEYS, LST_GREEN_KEYS,
)
from units_selector_window import UnitsSelectorWindow
from modes_selector_window import ModesSelectorWindow
from gamer import red_gamer, green_gamer


pygame.init()
q_app = QApplication(sys.argv)

AI_RED = False
AI_GREEN = False


def test_all(gamer):
    for unit in ALL_UNITS:

        if issubclass(unit, Spell):
            # noinspection PyArgumentList
            un = SpellInfo(
                unit,
                screen,
                spells,
                group,
                gamer.color,
                gamer.spawner.reverse
            )
        else:
            un = UnitInfo(
                unit,
                screen,
                gamer.color,
                gamer.spawner.rect.center,
                group,
                gamer.spawner.reverse
            )
        un.create()

modes_selector = ModesSelectorWindow(ALL_UNITS)
q_app.exec_()
ALL_UNITS = modes_selector.all_units
use_random_unit = modes_selector.use_random_unit

red_gamer.deck = modes_selector.get_result_deck()
green_gamer.deck = modes_selector.get_result_deck()

red_login = get_user_login(q_app, 'красного')
red_gamer.load_info(red_login)

if not AI_RED and modes_selector.need_ask_decks:
    UnitsSelectorWindow(red_gamer, ALL_UNITS)
    q_app.exec_()


green_login = get_user_login(q_app, 'зелёного')
green_gamer.load_info(green_login)

if not AI_GREEN and modes_selector.need_ask_decks:
    UnitsSelectorWindow(green_gamer, ALL_UNITS)
    q_app.exec_()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Пионерское побоище')

group = pygame.sprite.Group()
spells = pygame.sprite.Group()

red_gamer.init_spawner(
    Spawn(spells, RED, [260, HEIGHT // 2, 70, 70])
)
green_gamer.init_spawner(
    Spawn(spells, GREEN, [WIDTH - 260, HEIGHT // 2, 70, 70])
)

red_gamer.init_castles(
    Castle(screen, RED, [260, HEIGHT // 2, 70, 70], group, False),
    Tower(screen, RED, [360, 325, 70, 70], group, False),
    Tower(screen, RED, [360, 75, 70, 70], group, False)
)

green_gamer.init_castles(
    Castle(screen, GREEN, [WIDTH - 260, HEIGHT // 2, 70, 70], group, False),
    Tower(screen, GREEN, [840, 325, 70, 70], group, False),
    Tower(screen, GREEN, [840, 75, 70, 70], group, False)
)
if use_random_unit:
    red_gamer.init_random_unit(
        RandomUnit(screen, spells, group, RED, False)
    )

    green_gamer.init_random_unit(
        RandomUnit(screen, spells, group, GREEN, False)
    )

pause = False

quest_mark_font = pygame.font.Font(None, 30)
quest_mark_text = quest_mark_font.render(' ? ', True, [255, 255, 255], [0, 0, 0])
quest_mark_rect = quest_mark_text.get_rect(topright=[WIDTH, 0])

ais = []
if AI_RED:
    modules = [
        i() for i in AI_MODULES
    ]
    ais.append(Ai(red_gamer, modules))
    RED_DECK = ais[-1].make_deck(ALL_UNITS)
if AI_GREEN:
    modules = [
        i() for i in AI_MODULES
    ]
    ais.append(Ai(green_gamer, modules))
    GREEN_DECK = ais[-1].make_deck(ALL_UNITS)

while not (red_gamer.castle.died or green_gamer.castle.died):
    for ai in ais:
        ai.make_move(group)
    screen.fill(WHITE)

    for y, e in enumerate(red_gamer.deck):
        text = font.render(
            f'{(y if y < 9 else -1) + 1} - {UNITS[e.params_name].get("name", "Штука")} '
            f'({UNITS[e.params_name]["points"]})',
            1,
            BLACK
        )
        rect = text.get_rect(topleft=[25, 25 * y])
        screen.blit(text, rect)
    if use_random_unit:
        text = font.render(
            f'z - {UNITS[red_gamer.random_unit.unit.params_name].get("name", "Штука")} '
            f'({UNITS[red_gamer.random_unit.unit.params_name]["points"]})',
            1,
            BLACK
        )
        rect = text.get_rect(topleft=[25, 275])
        screen.blit(text, rect)

    for y, e in enumerate(green_gamer.deck):
        text = font.render(
            f'{(y if y < 9 else -1) + 1} - {UNITS[e.params_name].get("name", "Штука")} '
            f'({UNITS[e.params_name]["points"]})',
            1,
            BLACK
        )
        rect = text.get_rect(topleft=[1025, 25 * y])
        screen.blit(text, rect)

    if use_random_unit:
        text = font.render(
            f'/ - {UNITS[green_gamer.random_unit.unit.params_name].get("name", "Штука")} '
            f'({UNITS[green_gamer.random_unit.unit.params_name]["points"]})',
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

    screen.blit(quest_mark_text, quest_mark_rect)

    # dynamic graphic
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            red_gamer.castle.health = 0
            green_gamer.castle.health = 0
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            breakpoint()
        if e.type == pygame.KEYDOWN and not pause:
            # Make points full
            if e.key == pygame.K_KP_PERIOD:
                green_gamer.pressed_fill_button = True
            if e.key == pygame.K_TAB:
                red_gamer.pressed_fill_button = True
            # RED Cards

            for i in range(len(LST_RED_KEYS)):
                if e.key == LST_RED_KEYS[i]:
                    red_gamer.key_analyse(i, screen, group, spells)

            # GREEN Cards

            for i in range(len(LST_GREEN_KEYS)):
                if e.key == LST_GREEN_KEYS[i]:
                    green_gamer.key_analyse(i, screen, group, spells)

            # GIVING UP
            if e.key == pygame.K_KP_MINUS:
                green_gamer.castle.health = 0
            if e.key == pygame.K_ESCAPE:
                red_gamer.castle.health = 0
            # *** Retreating ***

            if e.key == pygame.K_LALT:
                for y in group:
                    if isinstance(y, Unit):
                        if y.command == RED and not isinstance(y, Building):
                            y.retreat = not y.retreat

            if e.key == pygame.K_RALT:
                for y in group:
                    if isinstance(y, Unit):
                        if y.command == GREEN and not isinstance(y, Building):
                            y.retreat = not y.retreat

            red_gamer.handle_spawner_move(True, e.key, pygame.K_s, pygame.K_w, pygame.K_d, pygame.K_a)

            green_gamer.handle_spawner_move(
                True, e.key,
                pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT
            )

            if e.key == pygame.K_z and not red_gamer.spawner.reverse and use_random_unit:
                red_gamer.handle_random_unit(screen, group, spells)

            if e.key == pygame.K_LSHIFT:
                red_gamer.spawner.reverse = not red_gamer.spawner.reverse

            if e.key == pygame.K_RSHIFT:
                green_gamer.spawner.reverse = not green_gamer.spawner.reverse

            if e.key == pygame.K_SLASH and not green_gamer.spawner.reverse and use_random_unit:
                green_gamer.handle_random_unit(screen, group, spells)

        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
            pause = not pause
        if e.type == pygame.KEYUP:
            # Making points full
            if e.key == pygame.K_TAB:
                red_gamer.pressed_fill_button = False
            if e.key == pygame.K_KP_PERIOD:
                green_gamer.pressed_fill_button = False

            red_gamer.handle_spawner_move(False, e.key, pygame.K_s, pygame.K_w, pygame.K_d, pygame.K_a)

            green_gamer.handle_spawner_move(False, e.key, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT)

        if e.type == pygame.MOUSEBUTTONDOWN:
            # Help
            if pygame.Rect(quest_mark_rect).collidepoint(e.pos):
                pause = True
                help_()
    screen.blit(BG, [200, 0, 800, 400])
    if red_gamer.pressed_fill_button and green_gamer.pressed_fill_button:
        red_gamer.points = green_gamer.points = MAX_POINTS

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
                    red_gamer.points = e.add(red_gamer.points)
                elif e.command == GREEN:
                    green_gamer.points = e.add(green_gamer.points)
                else:
                    # noinspection PyUnresolvedReferences
                    raise ValueError(f"Incorrect command: {e.command}")
        if green_gamer.time_add_points <= time.time() and green_gamer.points < MAX_POINTS:
            green_gamer.time_add_points = time.time() + PAUSE_ADD_POINTS
            green_gamer.points += ADD_POINTS
        if red_gamer.time_add_points <= time.time() and red_gamer.points < MAX_POINTS:
            red_gamer.time_add_points = time.time() + PAUSE_ADD_POINTS
            red_gamer.points += ADD_POINTS
    else:
        a = PAUSE_FONT.render('Пауза', 1, [0, 0, 0])
        screen.blit(a, a.get_rect(center=[WIDTH // 2, HEIGHT // 2]))
    for e, y in enumerate([f'{red_gamer.points}', f'{green_gamer.points}']):
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

    if red_gamer.castle.died:
        red_gamer.castle.destroyed()
        screen.blit(caron, caron.get_rect(center=[WIDTH - 100, HEIGHT // 2 - 30]))
        win = 'green'
    if green_gamer.castle.died:
        green_gamer.castle.destroyed()
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
