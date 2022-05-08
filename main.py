from itemtypes import *


def cfg_parser(file):
    file = open(file, encoding='utf-8').read().split('\n')
    res = {}
    for x in file:
        if x.startswith('###'):
            continue
        if x in ['\n', '', ' ']:
            continue
        xx = x.split(': ')
        if len(xx) > 1:
            res[xx[0]] = xx[1]
    return res


print('Запуск программы...')
enchants = cfg_parser('config/enchants.cfg')
items = cfg_parser('config/items.cfg')
attributes = cfg_parser('config/attributes.cfg')
color_scheme = cfg_parser('config/color_scheme.cfg')
rarities = cfg_parser('config/rarity.cfg')
effects = cfg_parser('config/effects.cfg')
mobs = cfg_parser('config/mobs.cfg')
config = cfg_parser('config/config.cfg')
config = {x: bool(int(config[x])) for x in config}
print('Запуск успешен!')
print('='*30 + '\nCollections Studio v0.1a by SirGromov')
initial = {'enchants': enchants, 'attributes': attributes, 'color_scheme': color_scheme,
           'rarities': rarities, 'config': config, 'items': items, 'mobs': mobs, 'effects': effects}


def nice_item_input(stt):
    lst = stt.split('\n\n')
    meta = []
    item = lst[5].split('\n')[0]
    if len(lst) == 7:
        meta = lst[6].split('\n')
    if item.lower() == 'яйцо призыва':
        i = SpawnEgg(lst[0], lst[1], lst[2] + '\n\n' + lst[3], lst[4],
                     lst[5].split('\n')[1].lower(), item, 1, initial, meta)
    elif item.lower() in ['зелье', 'взрывное зелье', 'туманное зелье', 'стрела с эффектом']:
        i = Potion(lst[0], lst[1], lst[2] + '\n\n' + lst[3], lst[4],
                     lst[5].split('\n')[1].lower(), item, 1, initial, meta)
    else:
        i = Item(lst[0], lst[1], lst[2] + '\n\n' + lst[3], lst[4],
                 lst[5].split('\n')[1].lower(), item, 1, initial, meta)
    return i


inp = open('input.txt', encoding='utf-8').read().split('\n===\n')
c = Collection()

slot = 0
for i in inp:
    c.add(nice_item_input(i))
    slot += 1
c.save_collection()
