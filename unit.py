# ***unit.py***
RED = (255, 0, 0)
GREEN = (0, 255, 0)

UNITS = {
    'spawn': {
        'image': {RED: 'images/red_spawn.png', GREEN: 'images/green_spawn.png'},
        'speed': 10,
    },
    'randomunit': {
        'refresh_time': 2,
        'image': {RED: 'images/no.png', GREEN: 'images/no.png'},
    },
    'soldat': {
        'name': 'Солдат',
        'damage': 10,
        'health': 100,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_soldat.png', GREEN: 'images/green_soldat.png'},
        'speed': 5,
        'atack_radius': 20,
        'points': 100,
        'wait': 0.5,
        'roles': ['atack', 'deaf'],
    },
    'castle': {
        'name': 'Замок',
        'damage': 75,
        'health': 5000,
        'reloading_time': 1,
        'image': {RED: 'images/red_castle.png', GREEN: 'images/green_castle.png'},
        'atack_radius': 100,
    },
    'tower': {
        'name': 'Башня',
        'damage': 50,
        'health': 2000,
        'reloading_time': 0.8,
        'image': {RED: 'images/red_castle.png', GREEN: 'images/green_castle.png'},
        'atack_radius': 200,
    },
    'xbow': {
        'name': 'Арбалет',
        'points': 1000,
        'damage': 4,
        'health': 425,
        'reloading_time': 0.1,
        'image': {RED: 'images/red_xbow.png', GREEN: 'images/green_xbow.png'},
        'atack_radius': 350,
        'wait': 2,
        'max_count': 2,
        'roles': ['deaf']
    },
    'archer': {
        'name': 'Лучник',
        'damage': 15,
        'health': 50,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_archer.png', GREEN: 'images/green_archer.png'},
        'speed': 4,
        'atack_radius': 100,
        'points': 100,
        'wait': 0.5,
        'roles': ['atack', 'deaf'],
    },
    'gigant': {
        'name': 'Гигант',
        'damage': 60,
        'health': 500,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_gigant.png', GREEN: 'images/green_gigant.png'},
        'speed': 3,
        'atack_radius': 30,
        'points': 500,
        'wait': 0.5,
        'roles': ['atack', 'deaf'],
    },
    'golem': {
        'name': 'Голем',
        'damage': 200,
        'health': 3000,
        'reloading_time': 3,
        'image': {RED: 'images/red_golem.png', GREEN: 'images/green_golem.png'},
        'speed': 1,
        'atack_radius': 30,
        'points': 2500,
        'boom_radius': 50,
        'boom_damage': 200,
        'atack_only': 'Building',
        'wait': 0.5,
        'roles': ['atack'],
    },
    'cannon_wheels': {
        'name': 'Пушка GO',
        'damage': 15,
        'health': 400,
        'reloading_time': 2,
        'image': {RED: 'images/red_cannon_wheels.png', GREEN: 'images/green_cannon_wheels.png'},
        'speed': 2,
        'atack_radius': 75,
        'points': 700,
        'wait': 0.5,
        'roles': ['atack'],
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
    'doubledamage': {
        'name': 'Двойной урон',
        'effect_time': 5,
        'points': 300,
        'image': {RED: 'images/red_doubledamage.png', GREEN: 'images/green_doubledamage.png'},
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
        'atack_radius': 70,
        'reversed': True,
        'reversed_damage': 100,
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
        'atack_radius': 70,
        'reversed': True,
        'display_time': 1,
        'reversed_damage': 500,
        'roles': ['atack'],
    },
    'cannon': {
        'name': 'Пушка',
        'damage': 50,
        'health': 500,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_cannon.png', GREEN: 'images/green_cannon.png'},
        'atack_radius': 100,
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
        'atack_radius': 1_000_000_000,
        'points': 1600,
        'wait': 0.5,
        'max_count': 1,
        'dont_atack': 'Building',
        'aura': True,
        'aura_rt': 0.5,
        'aura_damage': 40,
        'aura_radius': 80,
        'roles': ['deaf'],
    },
    'magiccannon': {
        'name': 'Магическая пушка',
        'damage': 50,
        'health': 500,
        'reloading_time': 1.5,
        'image': {RED: 'images/red_magiccannon.png', GREEN: 'images/green_magiccannon.png'},
        'atack_radius': 100,
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
        'atack_radius': 170,
        'points': 1500,
        'splash_radius': 50,
        'aura': True,
        'aura_rt': 0.5,
        'aura_damage': 30,
        'aura_radius': 100,
        'wait': 0.5,
        'first_reload': 4,
        'roles': ['deaf', 'atack']
    },
    'soldatspawner': {  # ANC_SOLDAT_SPAWNER #ANC_SOLDATSPAWNER #ANC_KAZARMY
        'name': 'Казарма',
        'health': 500,
        'reloading_time': 5,
        'image': {RED: 'images/red_soldatspawner.png', GREEN: 'images/green_soldatspawner.png'},
        'points': 500,
        'wait': 0.5,
        'roles': ['deaf', 'support'],
    },
    'archerspawner': {
        'name': 'Стрельбище',
        'health': 400,
        'reloading_time': 5,
        'image': {RED: 'images/red_archerspawner.png', GREEN: 'images/green_archerspawner.png'},
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
        'dont_atack': 'Building',
        'roles': ['support'],
    },
    'collector': {  # ANC_COLLECTOR
        'name': 'Сборщик',
        'health': 500,
        'reloading_time': 7,
        'image': {RED: 'images/red_collector.png', GREEN: 'images/green_collector.png'},
        'points': 600,
        'max_points': 3000,
        'add_points': 100,
        'wait': 3,
        'roles': ['support'],
    },
    'molniy': {
        'name': 'Молния',
        'damage': 200,
        'image': {RED: 'images/no.png', GREEN: 'images/no.png'},
        'atack_image': {RED: 'images/red_molniy_atack.png',
                        GREEN: 'images/green_molniy_atack.png'},
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
        'atack_radius': 15,
        'points': 500,
        'time_spawn': 1,
        'wait': 1,
        'reversed': True,
        'aura': True,
        'aura_damage': 40,
        'aura_radius': 40,
        'aura_rt': 1,
        'roles': ['atack'],
    },
    'teleport': {
        'name': 'Телепорт',
        'image': {RED: 'images/red_teleport.png', GREEN: 'images/green_teleport.png'},
        'points': 2000,
        'wait': 0.5,
        'reversed': True,
        'roles': ['support', 'atack'],
    },
    'spirit': {
        'name': 'Дух',
        'health': 300,
        'damage': 200,
        'speed': 8,
        'atack_radius': 30,
        'points': 300,
        'image': {RED: 'images/red_spirit.png', GREEN: 'images/green_spirit.png'},
        'wait': 3,
        'died_on_atack': True,
        'roles': ['atack', 'deaf'],
    },
    'cavalry': {
        'name': 'Конница',
        'health': 600,
        'damage': 100,
        'speed': 5,
        'atack_radius': 30,
        'reloading_time': 1.5,
        'points': 800,
        'image': {RED: 'images/red_cavalry.png', GREEN: 'images/green_cavalry.png'},
        'run_time': 3,
        'run_speed': 7,
        'run_damage': 500,
        'wait': 1.5,
        'run_effect': True,
        'roles': ['atack', 'deaf'],
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
    'cemetery': {  # ANC_ZOMBI #ANC_CEMETERY #ANC_KLADBISHE
        'name': "Зомби",
        'effect_time': 10,
        'spawn_time': 1,
        'image': {RED: 'images/red_cemetery.png', GREEN: 'images/green_cemetery.png'},
        'points': 1500,
        'wait': 0.5,
        'reversed': True,
        'roles': ['atack', 'deaf'],
    },
    'hiller': {
        'name': 'Целитель',
        'health': 400,
        'damage': 20,
        'speed': 2,
        'atack_radius': 50,
        'reloading_time': 2,
        'hill_reloading_time': 2,
        'hill': 30,
        'hill_radius': 75,
        'image': {RED: 'images/red_hiller.png', GREEN: 'images/green_hiller.png'},
        'points': 600,
        'wait': 0.5,
        'roles': ['atack', 'support', 'deaf'],
    },
    'musicant': {  # ANC_MUSICANT
        'name': 'Музыкант',
        'health': 300,
        'damage': 30,
        'speed': 2,
        'atack_radius': 30,
        'reloading_time': 2,
        'speeding': 1,
        'image': {RED: 'images/red_musicant.png', GREEN: 'images/green_musicant.png'},
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
        'atack_radius': 20,
        'points': 500,
        'wait': 3,
        'roles': ['atack', 'deaf'],
    },
    'elitearmy': {  # ANC_EL_ARMY
        'name': 'Элитная армия',
        'points': 2500,
        'number': 5,
        'wait': 0.5,
        'roles': ['atack', 'deaf'],
    },
    'taran': {  # ANC_TARAN
        'name': 'Таран',
        'points': 800,
        'health': 420,
        'damage': 200,
        'atack_radius': 30,
        'speed': 2,
        'image': {RED: 'images/red_taran.png', GREEN: 'images/green_taran.png'},
        'number': 1,
        'run_speed': 4,
        'run_damage': 400,
        'run_time': 4,
        'atack_only': 'Building',
        'wait': 5,
        'died_on_atack': True,
        'run_effect': True,
        'roles': ['atack', 'deaf'],
    },
    'witch': {  # ANC_WITCH
        'name': 'Ведьма',
        'points': 1000,
        'health': 400,
        'damage': 20,
        'atack_radius': 100,
        'number': 5,
        'reloading_time': 1,
        'resurrect_time': 6,
        'speed': 2,
        'image': {RED: 'images/red_witch.png', GREEN: 'images/green_witch.png'},
        'wait': 3,
        'splash_radius': 50,
        'ondeath_number': 2,
        'roles': ['support', 'deaf'],
    },
    'sauron': {
        'name': 'Саурон',
        'points': 2000,
        'health': 250,
        'damage': 30,
        'atack_radius': 180,
        'number': 1,
        'reloading_time': 1,
        'resurrect_time': 12,
        'speed': 1,
        'image': {RED: 'images/red_sauron.png', GREEN: 'images/green_sauron.png'},
        'wait': 3,
        'splash_radius': 50,
        'ondeath_number': 1,
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
        'atack_radius': 30,
        'speed': 3,
        'run_speed': 5,
        'run_damage': 200,
        'run_time': 4,
        'get_radius': 100,
        'max_number': 10,
        'atack_only': 'Building',
        'wait': 0.5,
        'died_on_atack': True,
        'run_effect': True,
        'roles': ['atack'],
    },
    'vampire': {  # ANC_VAMPIRE
        'name': 'Вампир',
        'points': 1000,
        'image': {RED: 'images/red_vampire.png', GREEN: 'images/green_vampire.png'},
        'health': 300,
        'damage': 15,
        'reloading_time': 1.5,
        'atack_radius': 75,
        'speed': 3,
        'vampirism': 1 + 7 / 100,
        'vampire_radius': 100,
        'wait': 0.5,
        'roles': ['atack', 'support'],
    },
    'wizard': {
        'name': 'Колдун',
        'points': 700,
        'image': {RED: 'images/red_wizard.png', GREEN: 'images/green_wizard.png'},
        'health': 250,
        'damage': 80,
        'atack_radius': 180,
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
        'reloading_time': 2,
        'atack_radius': 60,
        'speed': 1,
        'wait': 0.5,
        'roles': ['atack', 'deaf'],
    },
    'bat': {
        'name': 'Летучая мышь',
        'points': 50,
        'health': 10,
        'damage': 5,
        'image': {RED: 'images/red_bat.png', GREEN: 'images/green_bat.png'},
        'reloading_time': 1.5,
        'atack_radius': 10,
        'speed': 6,
        'wait': 0.5,
        'roles': ['support', 'deaf'],
    },
    'batarmy': {
        'name': 'Армия мышей',
        'points': 500,
        'number': 20,
        'wait': 1,
        'roles': ['atack', 'deaf'],
    },
    'batmob': {
        'name': 'Орава мышей',
        'points': 1000,
        'number': 50,
        'wait': 0.5,
        'roles': ['atack', 'deaf'],
    },
    'throwsoldat': {
        'name': 'Полёт солдат',
        'points': 500,
        'number': 3,
        'time_spawn': 1,
        'wait': 6,
        'image': {RED: 'images/red_TS.png', GREEN: 'images/green_TS.png'},
        'reversed': True,
        'roles': ['atack', 'deaf'],
    },
    'wall': {
        'name': 'Стена',
        'points': 2000,
        'health': 4000,
        'damage': 0,
        'image': {RED: 'images/red_wall.png', GREEN: 'images/green_wall.png'},
        'reloading_time': 30,
        'atack_radius': 30,
        'speed': 1,
        'hill_radius': 75,
        'hill': 100,
        'atack_only': 'Building',
        'wait': 0.5,
        'roles': ['atack', 'deaf'],
    },
    'wallbreaker': {
        'name': 'Стенобой',
        'points': 500,
        'health': 300,
        'damage': 400,
        'image': {RED: 'images/red_wallbreaker.png', GREEN: 'images/green_wallbreaker.png'},
        'reloading_time': 0,
        'atack_radius': 30,
        'speed': 6,
        'atack_only': 'Building',
        'wait': 3,
        'died_on_atack': True,
        'splash_radius': 30,
        'roles': ['atack', 'support'],
    },
    'snake': {
        'name': 'Змея',
        'points': 500,
        'health': 150,
        'damage': 25,
        'image': {RED: 'images/red_snake.png', GREEN: 'images/green_snake.png'},
        'reloading_time': 3,
        'atack_radius': 30,
        'speed': 8,
        'venom': 1,
        'venom_time': 3,
        'wait': 3,
        'roles': ['atack', 'deaf'],
    },
    'lifegenerator': {
        'name': 'Генератор жизни',
        'points': 1000,
        'health': 30,
        'damage': 0,
        'image': {RED: 'images/red_generator.png', GREEN: 'images/green_generator.png'},
        'reloading_time': 2,
        'atack_radius': 0,
        'hill_radius': 75,
        'hill': 100,
        'dont_atack': 'Building',
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
        'atack_radius': 0,
        'reversed': True,
        'wait': 10,
        'roles': ['support'],
    },
    'golemlite': {
        'name': 'Мини-голем',
        'damage': 50,
        'health': 700,
        'reloading_time': 3,
        'image': {RED: 'images/red_golemlite.png', GREEN: 'images/green_golemlite.png'},
        'speed': 2,
        'atack_radius': 30,
        'points': 700,
        'boom_radius': 50,
        'boom_damage': 100,
        'atack_only': 'Building',
        'wait': 0.5,
        'roles': ['atack'],
    },
    'hillbattery': {
        'name': "Исцеляющая батарейка",
        'damage': -30,
        'health': 1000,
        'reloading_time': 2,
        'image': {RED: 'images/red_hillbattery.png', GREEN: 'images/green_hillbattery.png'},
        'speed': 3,
        'atack_radius': 75,
        'points': 1000,
        'vampirism': -5,
        'wait': 0.5,
        'atack_command': 'self',
        'dont_atack': 'Building',
        'roles': ['support'],
    },
    'atackbattery': {
        'name': 'Атакующая батарейка',
        'damage': 0,
        'health': 1000,
        'reloading_time': 2,
        'image': {RED: 'images/red_atackbattery.png', GREEN: 'images/green_atackbattery.png'},
        'speed': 3,
        'atack_radius': 75,
        'points': 1200,
        'vampirism': -1,
        'wait': 0.5,
        'roles': ['atack', 'support', 'deaf'],
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
        'atack_reloading_time': 1,
        'atack_count': 5,

        'hill': 50,
        'hill_count': 5,
        'hill_reloading_time': 1,
        'roles': ['deaf', 'atack'],
    },

}

HELP = {
    'soldat': f'Солдат({UNITS["soldat"]["points"]} очков): Лёгкий воин ближнего боя',
    'archer': f'Лучник({UNITS["archer"]["points"]} очков): Лёгкий воин средней дальности',
    'gigant': f'Гигант({UNITS["gigant"]["points"]} очков): Средний воин ближнего боя',
    'hill': f'Исцеление({UNITS["hill"]["points"]} очков): Заклинание, которое восстанавливает '
            f'союзникам {UNITS["hill"]["hill"]} ед. здоровья',
    'doubledamage': f'Двойной урон({UNITS["doubledamage"]["points"]} очков): Заклинание, '
                    f'которое удваивает урон, наносимый союзниками, '
                    f'в течении {UNITS["doubledamage"]["effect_time"]} сек.',
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
    'soldatspawner': f'Казарма({UNITS["soldatspawner"]["points"]} очков): Здание, '
                     f'каждые {UNITS["soldatspawner"]["reloading_time"]} '
                     f'сек. выпускающее 1 солдата',
    'collector': f'Сборщик({UNITS["collector"]["points"]} очков): Здание, '
                 f'каждые {UNITS["collector"]["reloading_time"]} сек.'
                 f' добавляющее вам 100 очков. Максимум - 3000',
    'molniy': f'Молния({UNITS["molniy"]["points"]} очков): Заклинание, '
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
    'musicant': f'Музыкант({UNITS["musicant"]["points"]} очков): Средний воин средней дальности.'
                f' Постоянно ускоряет перемещение и перезарядку союзников в зоне действия',
    'freeze': f'Заморозка({UNITS["freeze"]["points"]} очков): Заклинание, останавливающее врагов '
              f'на {UNITS["freeze"]["effect_time"]} сек.',
    'cannon_wheels': f'Пушка GO({UNITS["cannon_wheels"]["points"]} очков): Средний воин средней'
                     f' дальности. Превращается в обычную пушку при уничтожении',
    'elite': f'Элита({UNITS["elite"]["points"]} очков): Улучшенные солдаты',
    'elitearmy': f'Армия элит({UNITS["elitearmy"]["points"]} очков): Армия элитных солдат, '
                 f'состоящая из {UNITS["elitearmy"]["number"]} человек',
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
    'batarmy': f'Мышиная армия({UNITS["batarmy"]["points"]} очков): Армия, состоящая из'
                 f' {UNITS["batarmy"]["number"]} мышей',
    'batmob': f'Орава мышей({UNITS["batmob"]["points"]} очков): Орава, состоящая '
                f'из {UNITS["batmob"]["number"]} мышей',
    'wall': f'Стена({UNITS["wall"]["points"]} очков): Очень тяжёлый воин. Не имеет урона. '
            f'При смерти исцеляет {UNITS["wall"]["hill"]} ед. здоровья всем стоящим рядом войскам',
    'wallbreaker': f'Стенобой({UNITS["wallbreaker"]["points"]} очков): Средний воин ближнего боя.'
                   f' Атакует только здания',
    'snake': f'Змея({UNITS["snake"]["points"]} очков): Средний воин средней дальности. '
             f'При атаке отравляет атакуемого на {UNITS["snake"]["venom_time"]} сек.',
    'lifegenerator': f'Генератор жизни({UNITS["lifegenerator"]["points"]} очков): Неуязвимое '
                     f'строение. Исцеляет всем союзным воинам возле себя по'
                     f' {UNITS["lifegenerator"]["hill"]} ед. здоровья. '
                     f'Самоуничтожается через {UNITS["lifegenerator"]["health"]} сек.',
    'golemlite': f'Мини-голем({UNITS["golemlite"]["points"]} очков): Ослабленный голем',
    'atackbattery': f'Атакующая батарейка({UNITS["atackbattery"]["points"]} очков): Воин средней'
                    f' дальности. На атаку на 1 ед. урона тратит 1 ед. здоровья',
    'hillbattery': f'Исцеляющая батарейка({UNITS["hillbattery"]["points"]} очков): Воин средней '
                   f'дальности. На исцеление 1 ед. здоровья тратит 5 ед. здоровью',
    'cannon_spell': f'Ядро({UNITS["cannon_spell"]["points"]} очков): Неубиваемое заклинание-воин.'
                    f' Движется В сторону противника.\nНаносит урон противникам и '
                    f'исцеляет союзников поблизости.',
    'throwsoldat': f'Полёт солдат({UNITS["throwsoldat"]["points"]} очков): Бросок нескольких'
                   f'({UNITS["throwsoldat"]["number"]}) солдат в указанную точку.',
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
            f'({UNITS["xbow"]["atack_radius"]}) радиус атаки.',
}
