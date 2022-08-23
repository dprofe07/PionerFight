# ***unit.py***
RED = (255, 0, 0)
GREEN = (0, 255, 0)

UNITS = {
    'spawn': {
        'image': {RED: 'images/red_spawn.png', GREEN: 'images/green_spawn.png'},
        'speed': 10,
    },
    'random_unit': {
        'refresh_time': 2,
        'image': {RED: 'images/no.png', GREEN: 'images/no.png'},
    },
    'soldat': {
        'name': 'Солдат',
        'damage': 10,
        'shield': 1,
        'health': 100,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_soldat.png', GREEN: 'images/green_soldat.png'},
        'speed': 5,
        'attack_radius': 20,
        'points': 100,
        'wait': 0.5,
        'roles': ['attack', 'deaf'],
    },
    'castle': {
        'name': 'Замок',
        'damage': 75,
        'health': 5000,
        'reloading_time': 1,
        'image': {RED: 'images/red_castle.png', GREEN: 'images/green_castle.png'},
        'attack_radius': 100,
    },
    'tower': {
        'name': 'Башня',
        'damage': 50,
        'health': 2000,
        'reloading_time': 0.8,
        'image': {RED: 'images/red_castle.png', GREEN: 'images/green_castle.png'},
        'attack_radius': 200,
    },
    'xbow': {
        'name': 'Арбалет',
        'points': 1000,
        'damage': 4,
        'health': 425,
        'reloading_time': 0.1,
        'image': {RED: 'images/red_xbow.png', GREEN: 'images/green_xbow.png'},
        'attack_radius': 350,
        'wait': 2,
        'max_count': 2,
        'roles': ['deaf']
    },
    'archer': {
        'name': 'Лучник',
        'damage': 15,
        'health': 50,
        'shield': 1,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_archer.png', GREEN: 'images/green_archer.png'},
        'speed': 4,
        'attack_radius': 100,
        'points': 100,
        'wait': 0.5,
        'roles': ['attack', 'deaf'],
    },
    'gigant': {
        'name': 'Гигант',
        'damage': 60,
        'health': 500,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_gigant.png', GREEN: 'images/green_gigant.png'},
        'speed': 3,
        'attack_radius': 30,
        'points': 500,
        'wait': 0.5,
        'roles': ['attack', 'deaf'],
    },
    'golem': {
        'name': 'Голем',
        'damage': 200,
        'health': 3000,
        'reloading_time': 3,
        'image': {RED: 'images/red_golem.png', GREEN: 'images/green_golem.png'},
        'speed': 1,
        'attack_radius': 30,
        'points': 2500,
        'boom_radius': 50,
        'boom_damage': 200,
        'attack_only': 'Building',
        'wait': 0.5,
        'roles': ['attack'],
    },
    'cannon_wheels': {
        'name': 'Пушка GO',
        'damage': 15,
        'health': 400,
        'reloading_time': 2,
        'image': {RED: 'images/red_cannon_wheels.png', GREEN: 'images/green_cannon_wheels.png'},
        'speed': 2,
        'attack_radius': 75,
        'points': 700,
        'wait': 0.5,
        'roles': ['attack'],
    },
    'hill': {
        'name': 'Исцеление',
        'hill': 70,
        'points': 400,
        'image': {RED: 'images/red_hill.png', GREEN: 'images/green_hill.png'},
        'wait': 2,
        'reversed': True,
        'roles': ['support'],
    },
    'fix': {
        'name': 'Починка',
        'hill': 50,
        'points': 1000,
        'image': {RED: 'images/red_fix.png', GREEN: 'images/green_fix.png'},
        'wait': 2,
        'reversed': True,
        'roles': ['support'],
    },
    'double_damage': {
        'name': 'Двойной урон',
        'effect_time': 5,
        'points': 300,
        'image': {RED: 'images/red_double_damage.png', GREEN: 'images/green_double_damage.png'},
        'wait': 2,
        'effect': 2,
        'reversed': True,
        'roles': ['support'],
    },

    'meteor': {
        'name': 'Метеор',
        'damage': 200,
        'points': 300,
        'image': {RED: 'images/red_meteor.png', GREEN: 'images/green_meteor.png'},
        'self_damage': 1.2,
        'wait': 6,
        'attack_radius': 70,
        'reversed': True,
        'reversed_damage': 100,
        'display_time': 1,
        'roles': ['deaf'],
    },
    'shield_breaker': {
        'name': 'Разрушитель щитов',
        'points': 1000,
        'wait': 1,
        'damage': 1.00,
        'image': {RED: 'images/red_meteor.png', GREEN: 'images/green_meteor.png'},
        'attack_radius': 70,
        'reversed': True,
        'reversed_damage': 0.50,
        'display_time': 1,
        'roles': ['deaf'],
    },
    'rocket': {
        'name': 'Ракета',
        'damage': 200,
        'points': 700,
        'image': {RED: 'images/red_meteor.png', GREEN: 'images/green_meteor.png'},
        'self_damage': 1.2,
        'wait': 6,
        'attack_radius': 70,
        'reversed': True,
        'display_time': 1,
        'reversed_damage': 500,
        'roles': ['attack'],
    },
    'cannon': {
        'name': 'Пушка',
        'damage': 50,
        'health': 500,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_cannon.png', GREEN: 'images/green_cannon.png'},
        'attack_radius': 100,
        'points': 500,
        'wait': 0.5,
        'roles': ['deaf'],
    },
    'inferno': {
        'name': 'Инферно',
        'damage': 1_000_000_000,
        'health': 700,
        'reloading_time': 10,
        'image': {RED: 'images/red_inferno.png', GREEN: 'images/green_inferno.png'},
        'fog_image': 'images/fog.png',
        'fog_display_time': 1,
        'attack_radius': 1_000_000_000,
        'points': 1600,
        'wait': 0.5,
        'max_count': 1,
        'do_not_attack': 'Building',
        'aura': True,
        'aura_rt': 0.5,
        'aura_damage': 40,
        'aura_radius': 80,
        'roles': ['deaf'],
    },
    'magic_cannon': {
        'name': 'Магическая пушка',
        'damage': 50,
        'health': 500,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_magic_cannon.png', GREEN: 'images/green_magic_cannon.png'},
        'attack_radius': 100,
        'points': 1000,
        'splash_radius': 30,
        'wait': 2,
        'roles': ['deaf'],
    },

    'sparky': {
        'name': 'Электро',
        'damage': 700,
        'health': 250,
        'reloading_time': 12,
        'image': {RED: 'images/red_sparky.png', GREEN: 'images/green_sparky.png'},
        'speed': 1,
        'attack_radius': 170,
        'points': 1500,
        'splash_radius': 50,
        'aura': True,
        'aura_rt': 0.5,
        'aura_damage': 30,
        'aura_radius': 100,
        'wait': 0.5,
        'first_reload': 4,
        'roles': ['deaf', 'attack']
    },
    'soldat_spawner': {
        'name': 'Казарма',
        'health': 500,
        'reloading_time': 5,
        'image': {RED: 'images/red_soldat_spawner.png', GREEN: 'images/green_soldat_spawner.png'},
        'points': 500,
        'wait': 0.5,
        'roles': ['deaf', 'support'],
    },
    'archer_spawner': {
        'name': 'Стрельбище',
        'health': 400,
        'reloading_time': 5,
        'image': {RED: 'images/red_archer_spawner.png', GREEN: 'images/green_archer_spawner.png'},
        'points': 800,
        'wait': 4,
        'roles': ['deaf', 'support'],
    },
    'transferer': {
        'name': 'Устройство переноса',
        'health': 150,
        'reloading_time': 0.5,
        'image': {RED: 'images/red_transferer.png', GREEN: 'images/green_transferer.png'},
        'points': 1000,
        'wait': 2,
        'cross_image': {RED: 'images/red_cross.png', GREEN: 'images/green_cross.png'},
        's': 200,
        'chance': 0.33,
        'radius': 50,
        'do_not_attack': 'Building',
        'roles': ['support'],
    },
    'collector': {  # ANC_COLLECTOR
        'name': 'Сборщик',
        'health': 500,
        'reloading_time': 7,
        'image': {RED: 'images/red_collector.png', GREEN: 'images/green_collector.png'},
        'image_full': {RED: 'images/red_full_collector.png', GREEN: 'images/green_full_collector.png'},
        'points': 600,
        'max_points': 3000,
        'add_points': 100,
        'wait': 3,
        'roles': ['support'],
    },
    'lightning': {
        'name': 'Молния',
        'damage': 200,
        'image': {RED: 'images/red_lightning.png', GREEN: 'images/green_lightning.png'},
        'attack_image': {
            RED: 'images/red_lightning_attack.png',
            GREEN: 'images/green_lightning_attack.png'
        },
        'points': 400,
        'display_time': 0.5,
        'wait': 4,
        'count_targets': 3,
        'reversed': True,
        'reversed_damage': 100,
        'radius': 200,
        'roles': ['deaf'],
    },
    'digger': {
        'name': 'Шахтёр',
        'damage': 0,
        'health': 400,
        'reloading_time': 1,
        'image': {RED: 'images/red_digger.png', GREEN: 'images/green_digger.png'},
        'speed': 3,
        'attack_radius': 15,
        'points': 500,
        'time_spawn': 1,
        'wait': 1,
        'reversed': True,
        'aura': True,
        'aura_damage': 40,
        'aura_radius': 40,
        'aura_rt': 1,
        'roles': ['attack'],
    },
    'teleport': {
        'name': 'Телепорт',
        'image': {RED: 'images/red_teleport.png', GREEN: 'images/green_teleport.png'},
        'points': 2000,
        'wait': 0.5,
        'reversed': True,
        'roles': ['support', 'attack'],
    },
    'spirit': {
        'name': 'Дух',
        'health': 300,
        'damage': 200,
        'speed': 8,
        'attack_radius': 30,
        'points': 300,
        'image': {RED: 'images/red_spirit.png', GREEN: 'images/green_spirit.png'},
        'wait': 3,
        'die_on_attack': True,
        'roles': ['attack', 'deaf'],
    },
    'cavalry': {
        'name': 'Конница',
        'health': 600,
        'damage': 100,
        'speed': 3,
        'attack_radius': 30,
        'reloading_time': 1.5,
        'points': 800,
        'image': {RED: 'images/red_cavalry.png', GREEN: 'images/green_cavalry.png'},
        'run_time': 3,
        'run_speed': 6,
        'run_damage': 500,
        'wait': 1.5,
        'run_effect': True,
        'shield': 500,
        'roles': ['attack', 'deaf'],
    },
    'push': {
        'name': 'Толчок',
        'force': 8,
        'points': 300,
        'effect_time': 0.5,
        'image': {RED: 'images/no.png', GREEN: 'images/no.png'},
        'wait': 3,
        'reversed': True,
        'roles': ['deaf', 'support', 'ai_ignore'],
    },
    'army': {  # ANC_ARMY
        'name': 'Армия',
        'number': 10,
        'points': 800,
        'wait': 0.5,
        'roles': ['deaf', 'support'],
    },
    'cemetery': {
        'name': "Зомби",
        'effect_time': 10,
        'spawn_time': 1,
        'image': {RED: 'images/red_cemetery.png', GREEN: 'images/green_cemetery.png'},
        'points': 1500,
        'wait': 0.5,
        'reversed': True,
        'roles': ['attack', 'deaf'],
    },
    'hiller': {
        'name': 'Целитель',
        'health': 400,
        'damage': 20,
        'speed': 2,
        'attack_radius': 50,
        'reloading_time': 2,
        'hill_reloading_time': 2,
        'hill': 30,
        'hill_radius': 75,
        'image': {RED: 'images/red_hiller.png', GREEN: 'images/green_hiller.png'},
        'points': 600,
        'wait': 0.5,
        'roles': ['attack', 'support', 'deaf'],
    },
    'musician': {  # ANC_MUSICIAN
        'name': 'Музыкант',
        'health': 300,
        'damage': 30,
        'speed': 2,
        'attack_radius': 30,
        'reloading_time': 2,
        'speeding': 1,
        'image': {RED: 'images/red_musician.png', GREEN: 'images/green_musician.png'},
        'points': 500,
        'speed_radius': 100,
        'wait': 0.5,
        'roles': ['support'],
    },
    'freeze': {
        'name': 'Заморозка',
        'points': 1000,
        'effect_time': 3,
        'effect': 1,
        'image': {RED: 'images/red_freeze.png', GREEN: 'images/green_freeze.png'},
        'wait': 10,
        'reversed': True,
        'roles': ['support', 'deaf'],
    },
    'elite': {
        'name': 'Элита',
        'damage': 100,
        'health': 250,
        'reloading_time': 0.8,
        'image': {RED: 'images/red_elite.png', GREEN: 'images/green_elite.png'},
        'speed': 6,
        'attack_radius': 20,
        'points': 500,
        'wait': 3,
        'roles': ['attack', 'deaf'],
    },
    'elite_army': {  # ANC_EL_ARMY
        'name': 'Элитная армия',
        'points': 2500,
        'number': 5,
        'wait': 0.5,
        'roles': ['attack', 'deaf'],
    },
    'taran': {  # ANC_TARAN
        'name': 'Таран',
        'points': 800,
        'health': 420,
        'damage': 200,
        'attack_radius': 30,
        'speed': 2,
        'image': {RED: 'images/red_taran.png', GREEN: 'images/green_taran.png'},
        'number': 1,
        'run_speed': 4,
        'run_damage': 400,
        'run_time': 4,
        'attack_only': 'Building',
        'wait': 5,
        'die_on_attack': True,
        'run_effect': True,
        'roles': ['attack', 'deaf'],
    },
    'witch': {  # ANC_WITCH
        'name': 'Ведьма',
        'points': 1000,
        'health': 400,
        'damage': 20,
        'attack_radius': 100,
        'number': 5,
        'reloading_time': 1,
        'resurrect_time': 6,
        'speed': 2,
        'image': {RED: 'images/red_witch.png', GREEN: 'images/green_witch.png'},
        'wait': 3,
        'splash_radius': 50,
        'on_death_number': 2,
        'roles': ['support', 'deaf'],
    },
    'sauron': {
        'name': 'Саурон',
        'points': 2000,
        'health': 250,
        'damage': 30,
        'attack_radius': 180,
        'number': 1,
        'reloading_time': 1,
        'resurrect_time': 12,
        'speed': 1,
        'image': {RED: 'images/red_sauron.png', GREEN: 'images/green_sauron.png'},
        'wait': 3,
        'splash_radius': 50,
        'on_death_number': 1,
        'roles': ['support', 'deaf'],
    },
    'army_archer': {
        'name': 'Взвод лучников',
        'number': 10,
        'points': 900,
        'wait': 0.5,
        'roles': ['support', 'deaf'],
    },
    'car': {
        'name': 'Машина',
        'points': 800,
        'image': {RED: 'images/red_car.png', GREEN: 'images/green_car.png'},
        'health': 500,
        'damage': 100,
        'reloading_time': 2,
        'attack_radius': 30,
        'speed': 3,
        'run_speed': 5,
        'run_damage': 200,
        'run_time': 4,
        'get_radius': 100,
        'max_number': 10,
        'attack_only': 'Building',
        'wait': 0.5,
        'die_on_attack': True,
        'run_effect': True,
        'roles': ['attack'],
    },
    'vampire': {  # ANC_VAMPIRE
        'name': 'Вампир',
        'points': 1000,
        'image': {RED: 'images/red_vampire.png', GREEN: 'images/green_vampire.png'},
        'health': 300,
        'damage': 15,
        'reloading_time': 1.5,
        'attack_radius': 75,
        'speed': 3,
        'vampirism': 1 + 7 / 100,
        'vampire_radius': 100,
        'wait': 0.5,
        'roles': ['attack', 'support'],
    },
    'wizard': {
        'name': 'Колдун',
        'points': 700,
        'image': {RED: 'images/red_wizard.png', GREEN: 'images/green_wizard.png'},
        'health': 250,
        'damage': 80,
        'attack_radius': 180,
        'speed': 3,
        'splash_radius': 50,
        'wait': 0.5,
        'reloading_time': 2,
        'roles': ['support', 'deaf'],
    },
    'pekka': {
        'name': 'Пекка',
        'points': 1500,
        'image': {RED: 'images/red_pekka.png', GREEN: 'images/green_pekka.png'},
        'health': 1000,
        'damage': 400,
        'shield': 50,
        'reloading_time': 2,
        'attack_radius': 60,
        'speed': 1,
        'wait': 0.5,
        'roles': ['attack', 'deaf'],
    },
    'bat': {
        'name': 'Летучая мышь',
        'points': 50,
        'health': 10,
        'damage': 5,
        'image': {RED: 'images/red_bat.png', GREEN: 'images/green_bat.png'},
        'reloading_time': 1.5,
        'attack_radius': 10,
        'speed': 6,
        'wait': 0.5,
        'roles': ['support', 'deaf'],
    },
    'bat_army': {
        'name': 'Армия мышей',
        'points': 500,
        'number': 20,
        'wait': 1,
        'roles': ['attack', 'deaf'],
    },
    'bat_mob': {
        'name': 'Орава мышей',
        'points': 1000,
        'number': 50,
        'wait': 0.5,
        'roles': ['attack', 'deaf'],
    },
    'soldat_flight': {
        'name': 'Полёт солдат',
        'points': 500,
        'number': 3,
        'time_spawn': 1,
        'wait': 6,
        'image': {RED: 'images/red_TS.png', GREEN: 'images/green_TS.png'},
        'reversed': True,
        'roles': ['attack', 'deaf'],
    },
    'wall': {
        'name': 'Стена',
        'points': 2000,
        'health': 4000,
        'damage': 0,
        'image': {RED: 'images/red_wall.png', GREEN: 'images/green_wall.png'},
        'reloading_time': 30,
        'attack_radius': 30,
        'speed': 1,
        'hill_radius': 75,
        'hill': 100,
        'attack_only': 'Building',
        'wait': 0.5,
        'roles': ['attack', 'deaf'],
    },
    'wall_breaker': {
        'name': 'Стенобой',
        'points': 500,
        'health': 300,
        'damage': 400,
        'image': {RED: 'images/red_wall_breaker.png', GREEN: 'images/green_wall_breaker.png'},
        'reloading_time': 0,
        'attack_radius': 30,
        'speed': 6,
        'attack_only': 'Building',
        'wait': 3,
        'die_on_attack': True,
        'splash_radius': 30,
        'roles': ['attack', 'support'],
    },
    'snake': {
        'name': 'Змея',
        'points': 500,
        'health': 150,
        'damage': 25,
        'image': {RED: 'images/red_snake.png', GREEN: 'images/green_snake.png'},
        'reloading_time': 3,
        'attack_radius': 30,
        'speed': 8,
        'venom': 1,
        'venom_time': 3,
        'wait': 3,
        'roles': ['attack', 'deaf'],
    },
    'life_generator': {
        'name': 'Генератор жизни',
        'points': 1000,
        'health': 30,
        'damage': 0,
        'image': {RED: 'images/red_generator.png', GREEN: 'images/green_generator.png'},
        'reloading_time': 2,
        'attack_radius': 0,
        'hill_radius': 75,
        'hill': 100,
        'do_not_attack': 'Building',
        # 'effect_time':30,
        'wait': 0.5,
        'roles': ['support'],
    },
    'flag': {
        'name': 'Флаг',
        'damage': 0,
        'health': 10,
        'points': 500,
        'image': {RED: 'images/red_flag.png', GREEN: 'images/green_flag.png'},
        'reloading_time': 11,
        'attack_radius': 0,
        'reversed': True,
        'wait': 10,
        'roles': ['support'],
    },
    'lite_golem': {
        'name': 'Мини-голем',
        'damage': 50,
        'health': 700,
        'reloading_time': 3,
        'image': {RED: 'images/red_lite_golem.png', GREEN: 'images/green_lite_golem.png'},
        'speed': 2,
        'attack_radius': 30,
        'points': 700,
        'boom_radius': 50,
        'boom_damage': 100,
        'attack_only': 'Building',
        'wait': 0.5,
        'roles': ['attack'],
    },
    'hill_battery': {
        'name': "Исцеляющая батарейка",
        'damage': -30,
        'health': 1000,
        'reloading_time': 2,
        'image': {RED: 'images/red_hill_battery.png', GREEN: 'images/green_hill_battery.png'},
        'speed': 3,
        'attack_radius': 75,
        'points': 1000,
        'vampirism': -5,
        'wait': 0.5,
        'attack_command': 'self',
        'do_not_attack': 'Building',
        'roles': ['support'],
    },
    'attack_battery': {
        'name': 'Атакующая батарейка',
        'damage': 0,
        'health': 1000,
        'reloading_time': 2,
        'image': {RED: 'images/red_attack_battery.png', GREEN: 'images/green_attack_battery.png'},
        'speed': 3,
        'attack_radius': 75,
        'points': 1200,
        'vampirism': -1,
        'wait': 0.5,
        'roles': ['attack', 'support', 'deaf'],
    },
    'cannon_spell': {
        'name': 'Ядро',
        'points': 500,
        'wait': 3,
        'moving': 300,
        'image': {RED: 'images/red_cannon_spell.png', GREEN: 'images/green_cannon_spell.png'},
        'speed': 8,

        'action_radius': 100,

        'damage': 100,
        'attack_reloading_time': 1,
        'attack_count': 5,

        'hill': 50,
        'hill_count': 5,
        'hill_reloading_time': 1,
        'roles': ['deaf', 'attack'],
    },

}

HELP = {
    'soldat': f'Солдат({UNITS["soldat"]["points"]} очков): Лёгкий воин ближнего боя',
    'archer': f'Лучник({UNITS["archer"]["points"]} очков): Лёгкий воин средней дальности',
    'gigant': f'Гигант({UNITS["gigant"]["points"]} очков): Средний воин ближнего боя',
    'hill': f'Исцеление({UNITS["hill"]["points"]} очков): Заклинание, которое восстанавливает '
            f'союзникам {UNITS["hill"]["hill"]} ед. здоровья',
    'double_damage': f'Двойной урон({UNITS["double_damage"]["points"]} очков): Заклинание, '
                     f'которое удваивает урон, наносимый союзниками, '
                     f'в течении {UNITS["double_damage"]["effect_time"]} сек.',
    'meteor': f'Метеорит({UNITS["meteor"]["points"]} очков): Заклинание, атакующее '
              f'все(включая ваши) войска в области. Урон своим уменьшен в '
              f'{UNITS["meteor"]["self_damage"]} раз(а). Наносит больше урона на своей половине',
    'rocket': f'Ракета({UNITS["rocket"]["points"]} очков): Заклинание, атакующее '
              f'все(включая ваши) войска в области. Урон своим уменьшен в '
              f'{UNITS["rocket"]["self_damage"]} раз(а). Наносит больше урона на чужой половине',
    'cannon': f'Пушка({UNITS["cannon"]["points"]} очков): Здание, '
              f'атакующее чужих воинов одиночными выстрелами',
    'sparky': f'Электро({UNITS["sparky"]["points"]} очков): Тяжёлый воин'
              f' средней дальности. Имеет сплеш-урон',
    'soldat_spawner': f'Казарма({UNITS["soldat_spawner"]["points"]} очков): Здание, '
                     f'каждые {UNITS["soldat_spawner"]["reloading_time"]} '
                     f'сек. выпускающее 1 солдата',
    'collector': f'Сборщик({UNITS["collector"]["points"]} очков): Здание, '
                 f'каждые {UNITS["collector"]["reloading_time"]} сек.'
                 f' добавляющее вам 100 очков. Максимум - 3000',
    'lightning': f'Молния({UNITS["lightning"]["points"]} очков): Заклинание, '
              f'атакующее 3 вражеские цели с наибольшим здоровьем. Останавливает'
              f' атакованных воинов',
    'golem': f'Голем({UNITS["golem"]["points"]} очков): Тяжёлый воин ближнего боя,'
             f' атакующий только здания. Наносит урон воинам возле него при уничтожении.'
             f'Создаёт маленьких големчиков',
    'digger': f'Шахтёр({UNITS["digger"]["points"]} очков): Средний воин ближнего боя. ',
    'teleport': f'Телепорт({UNITS["teleport"]["points"]} очков): Заклинание, перемещающее '
                f'все союзные войска зеркально относительно реки.',
    'spirit': f'Дух({UNITS["spirit"]["points"]} очков): Лёгкий воин ближнего боя. '
              f'Имеет сплеш-урон. Умирает при атаке',
    'cavalry': f'Конница({UNITS["cavalry"]["points"]} очков): средний воин'
               f' ближнего боя. Имеет эффект разгона.',
    'push': f'Толчок({UNITS["push"]["points"]} очков): Заклинание, в течении'
            f' {UNITS["push"]["effect_time"]} сек. непрерывно перемещающее'
            f' вражеских воинов в направлении от своей половины.',
    'fix': f'Починка({UNITS["fix"]["points"]} очков): Заклинание, которое восстанавливает '
           f'союзным зданиям {UNITS["fix"]["hill"]} ед. здоровья',
    'army': f'Армия({UNITS["army"]["points"]} очков): Армия солдат, состоящая '
            f'из {UNITS["army"]["number"]}',
    'cemetery': f'Зомби({UNITS["cemetery"]["points"]} очков): Заклинание, в течении'
                f' {UNITS["cemetery"]["effect_time"]} сек, каждые '
                f'{UNITS["cemetery"]["spawn_time"]} сек. создающее '
                f'1 солдата вокруг замка противника',
    'hiller': f'Целитель({UNITS["hiller"]["points"]} очков): Средний воин средний дальности.'
              f' Непрерывно исцеляет союзников, находящихся в области действия',
    'musician': f'Музыкант({UNITS["musician"]["points"]} очков): Средний воин средней дальности.'
                f' Постоянно ускоряет перемещение и перезарядку союзников в зоне действия',
    'freeze': f'Заморозка({UNITS["freeze"]["points"]} очков): Заклинание, останавливающее врагов '
              f'на {UNITS["freeze"]["effect_time"]} сек.',
    'cannon_wheels': f'Пушка GO({UNITS["cannon_wheels"]["points"]} очков): Средний воин средней'
                     f' дальности. Превращается в обычную пушку при уничтожении',
    'elite': f'Элита({UNITS["elite"]["points"]} очков): Улучшенные солдаты',
    'elite_army': f'Армия элит({UNITS["elite_army"]["points"]} очков): Армия элитных солдат, '
                 f'состоящая из {UNITS["elite_army"]["number"]} человек',
    'taran': f'Таран({UNITS["taran"]["points"]} очков): Средний воин ближнего боя.'
             f' Атакует только здания. Создаёт 2-х элит на месте себя при уничтожении '
             f'или при атаке. \n Имеет эффект разгона',
    'witch': f'Ведьма({UNITS["witch"]["points"]} очков): Средний воин средней дальности. '
             f'Имеет сплеш-урон. Каждые {UNITS["witch"]["resurrect_time"]} сек.'
             f' вызывает {UNITS["witch"]["number"]} солдатов.',
    'army_archer': f'Взвод лучников({UNITS["army_archer"]["points"]} очков): '
                   f'{UNITS["army_archer"]["number"]} лучников',
    'car': f'Машина({UNITS["car"]["points"]} очков): Средний воин ближнего боя.'
           f' Атакует только здания. При появлении в неё перемещаются все воины в зоне'
           f' действия.\nПри уничтожении или атаке выпускает всё своё содержимое. '
           f'Присутствует эффект разгона.',
    'vampire': f'Вампир({UNITS["vampire"]["points"]} очков): Средний воин средней'
               f' дальности. Даёт вампиризм воинам в зоне действия',
    'pekka': f'Паук({UNITS["pekka"]["points"]} очков): Тяжёлый воин ближнего боя',
    'bat': f'Мышь({UNITS["bat"]["points"]} очков): Очень лёгкий воин ближнего боя',
    'bat_army': f'Мышиная армия({UNITS["bat_army"]["points"]} очков): Армия, состоящая из'
                 f' {UNITS["bat_army"]["number"]} мышей',
    'bat_mob': f'Орава мышей({UNITS["bat_mob"]["points"]} очков): Орава, состоящая '
                f'из {UNITS["bat_mob"]["number"]} мышей',
    'wall': f'Стена({UNITS["wall"]["points"]} очков): Очень тяжёлый воин. Не имеет урона. '
            f'При смерти исцеляет {UNITS["wall"]["hill"]} ед. здоровья всем стоящим рядом войскам',
    'wall_breaker': f'Стенобой({UNITS["wall_breaker"]["points"]} очков): Средний воин ближнего боя.'
                   f' Атакует только здания',
    'snake': f'Змея({UNITS["snake"]["points"]} очков): Средний воин средней дальности. '
             f'При атаке отравляет атакуемого на {UNITS["snake"]["venom_time"]} сек.',
    'life_generator': f'Генератор жизни({UNITS["life_generator"]["points"]} очков): Неуязвимое '
                     f'строение. Исцеляет всем союзным воинам возле себя по'
                     f' {UNITS["life_generator"]["hill"]} ед. здоровья. '
                     f'Самоуничтожается через {UNITS["life_generator"]["health"]} сек.',
    'lite_golem': f'Мини-голем({UNITS["lite_golem"]["points"]} очков): Ослабленный голем',
    'attack_battery': f'Атакующая батарейка({UNITS["attack_battery"]["points"]} очков): Воин средней'
                    f' дальности. На атаку на 1 ед. урона тратит 1 ед. здоровья',
    'hill_battery': f'Исцеляющая батарейка({UNITS["hill_battery"]["points"]} очков): Воин средней '
                   f'дальности. На исцеление 1 ед. здоровья тратит 5 ед. здоровью',
    'cannon_spell': f'Ядро({UNITS["cannon_spell"]["points"]} очков): Неубиваемое заклинание-воин.'
                    f' Движется В сторону противника.\nНаносит урон противникам и '
                    f'исцеляет союзников поблизости.',
    'soldat_flight': f'Полёт солдат({UNITS["soldat_flight"]["points"]} очков): Бросок нескольких'
                   f'({UNITS["soldat_flight"]["number"]}) солдат в указанную точку.',
    'transferer': f'Устройство переноса({UNITS["transferer"]["points"]} очков): Здание,'
                  f' перемещающее 1 воина, находящегося в зоне его действия, на'
                  f' некоторое расстояние вправо(S ꞓ [{UNITS["transferer"]["s"] // 2},'
                  f' {UNITS["transferer"]["s"]}] или с'
                  f' шансом {UNITS["transferer"]["chance"] * 100}%'
                  f' S ꞓ [{-UNITS["transferer"]["s"]}, {-UNITS["transferer"]["s"] // 2}])',
    'wizard': f'Маг({UNITS["wizard"]["points"]} очков): Средний воин дальнего боя.'
              f' Имеет сплеш-урон.',
    'flag': f'Флаг({UNITS["flag"]["points"]} очков): Здание, заставляющее всех союзных'
            f' воинов перемещатся к нему',
    'xbow': f'Арбалет({UNITS["xbow"]["points"]} очков): Здание. Имеет очень большой '
            f'({UNITS["xbow"]["attack_radius"]}) радиус атаки.',
}
