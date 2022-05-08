from random import randint


_SLOTS = {'mainhand': 'В главной руке: ', 'offhand': 'Во второй руке: ',
          'head': 'На голове: ', 'chest': 'На теле: ', 'legs': 'На ногах: ', 'feet': 'Обуто: '}


def to_rome_numeric(num):
    meta = {1: 'I', 5: 'V', 10: 'X', 50: 'L', 100: 'C', 500: 'D', 1000: 'M'}
    res = ''
    res += meta[1000] * (num // 1000)
    num = num % 1000
    if num // 900 == 1:
        res += meta[100] + meta[1000]
    elif num // 500 == 1:
        res += meta[500] + ((num - 500) // 100) * meta[100]
    elif num // 100 > 0:
        res += meta[100] * (num // 100)
    num = num - (num // 100 * 100)
    if num // 90 == 1:
        res += meta[10] + meta[100]
    elif num // 50 == 1:
        res += meta[50] + ((num - 50) // 10) * meta[10]
    elif num // 10 > 0:
        res += meta[10] * (num // 10)
    num = num - (num // 10 * 10)
    if num // 9 == 1:
        res += meta[1] + meta[10]
    elif num // 5 == 1:
        res += meta[5] + ((num - 5) // 1) * meta[1]
    elif num // 1 > 0:
        res += meta[1] * (num // 1)
    return res


def from_rome_numeric(num):
    meta = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    res = 0
    last = ''
    for x in num:
        if x in meta:
            res += meta[x]
            if x == 'X' and last == 'I':
                res -= 2
            if x == 'C' and last == 'X':
                res -= 20
            if x == 'M' and last == 'C':
                res -= 200
            last = x
        else:
            return 0
    return res


class ItemException(Exception):

    def __init__(self, text):
        self.text = text


class Potion:

    def __init__(self, name, ench, lore, atts, rarity, itype, amount, initial, meta=None):
        global enchants, attributes, color_scheme, rarities, config, items, mobs, effects
        enchants = initial['enchants']
        attributes = initial['attributes']
        color_scheme = initial['color_scheme']
        rarities = initial['rarities']
        config = initial['config']
        items = initial['items']
        mobs = initial['mobs']
        effects = initial['effects']
        if config['allow_color_codes']:
            self.name = color_scheme[rarities[rarity]] + name
        else:
            self.name = name
        self.name = self.name.replace('"', r'\"')
        self.ench = ench
        self.enchant_parser()
        self.lore = lore
        self.atts = atts
        self.attribute_parser()
        self.lore_parser()
        self.rarity = rarities[rarity]
        if rarity in ['epic', 'exotic', 'legendary', 'forbidden'] and atts == '':
            raise ItemException('Ахуел? Где атрибуты? Лови ошибку, сука')
        self.itype = items[itype.lower()]
        if len(self.itype.split()) == 2:
            self.var = self.itype.split()[1]
            self.itype = self.itype.split()[0]
        else:
            self.var = '0'
        self.pattern = 'Generic'
        self.amount = amount
        self.meta = [i.lower() for i in meta]
        self.effect_parser()
        self.hidden = 0
        if self.attribute_cosmetic or 'спрятать атрибуты' in self.meta or config['auto_lore_attributes'] or config['attributes_icons']:
            self.hidden += 2
        if 'спрятать чары' in self.meta or config['auto_lore_enchants']:
            self.hidden += 1
        self.nbt = '{display:{Name:"' + self.name + '",Lore:[' + self.lore_array + ']},ench:' + self.ench_list_nbt + \
                   ',AttributeModifiers:['+self.attribute_nbt_list+']'+',HideFlags:'+str(self.hidden)+self.effect_list_nbt+'}'
        print(self.nbt)
        self.give_command = f'/give @p minecraft:{self.itype} {self.amount} {self.var} ' + self.nbt

    def attribute_parser(self):
        res = {}
        nbt = []
        self.attribute_cosmetic = []
        lst = self.atts.split('\n')
        for x in lst:
            if x.endswith(':'):
                if x[:-1].lower() in attributes:
                    res[attributes[x[:-1].lower()]] = []
                    ###
                    slot = attributes[x[:-1].lower()]
                else:
                    self.attribute_cosmetic.append(x)
                    slot = 'custom'
            else:
                xx = x.split()
                if len(xx) > 1:
                    if xx[0][0] == '+' and (config['mainhand_damage_pluses'] and slot == 'mainhand'):
                        amount = xx[0][1:]
                    else:
                        amount = xx[0]
                    operation = '0'
                    if amount.endswith('%'):
                        operation = '1'
                        amount = str(int(amount[:-1]) / 100)
                    name = ' '.join(xx[1:])
                    if name.lower() in attributes:
                        if attributes[name.lower()] == 'generic.attackSpeed' and config['attack_speed_autocount'] and slot == 'mainhand':
                            amount = str(- 4 + float(amount))
                        s = '{AttributeName:'+attributes[name.lower()]+',Name:'+attributes[name.lower()]+',Slot:'+slot+',Amount:'+amount+',Operation:'+operation+',UUIDMost:'+str(randint(0, 2**17))+',UUIDLeast:'+str(randint(0, 2**17))+'}'
                        if slot != 'custom':  res[slot].append({'name': attributes[name.lower()], 'operation': operation, 'amount': amount})
                        nbt.append(s)
                    else:
                        self.attribute_cosmetic.append(x)
        self.attribute_nbt_list = ','.join(nbt)
        self.attributes = res

    def lore_parser(self):
        lst = self.lore.split('\n')
        res = []
        if config['allow_color_codes']: cc = '§7'
        else: cc = ''
        if not config['auto_lore_enchants']:
            if self.cosmetic_ench:
                for x in self.cosmetic_ench:
                    res.append(f'"{cc}{x}"')
                res.append('""')
        else:
            for x in self.ench.split('\n'):
                res.append(f'"{cc}{x}"')
        if config['allow_color_codes']:  cc = '§6'
        else: cc = ''
        for x in lst:
            x = x.replace('&', '§')
            x = x.replace('"', r'\"')
            res.append(f'"{cc}{x}"')
        if not config['attributes_icons']:
            if self.attribute_cosmetic:
                res.append('""')
                for x in self.atts.split('\n'):
                    if x.endswith(':'):
                        if config['allow_color_codes']: cc = '§1'
                        else: cc = ''
                        res.append(f'"{cc}{x}"')
                    else:
                        if config['allow_color_codes']: cc = '§8'
                        else: cc = ''
                        res.append(f'"{cc}{x}"')
        else:
            res.append('""')
            if self.attribute_cosmetic:
                for x in self.atts.split('\n'):
                    if x.endswith(':'):
                        if config['allow_color_codes']: cc = '§1'
                        else: cc = ''
                        res.append(f'"{cc}{x}"')
                    else:
                        if config['allow_color_codes']: cc = '§8'
                        else: cc = ''
                        res.append(f'"{cc}{x}"')
            else:
                for slot in self.attributes:
                    ss = ''
                    ss += _SLOTS[slot]
                    for i in self.attributes[slot]:
                        amo = float(i["amount"])
                        am = i["amount"]
                        if i["operation"] == '1':
                            am = f'{amo * 100}%'
                        if amo > 0:
                            if config['allow_color_codes']: cc = '§f'
                            else: cc = ''
                            am = f'+{amo}'
                        else:
                            if config['allow_color_codes']: cc = '§c'
                            else: cc = ''
                        if config['attack_speed_autocount'] and slot == 'mainhand' and i['name'] == 'generic.attackSpeed':
                            am = f'{-(-4-amo)}'
                        if am.endswith('.0'): am = am[:-2]
                        if am.endswith('.0%'): am = am[:-3] + '%'
                        if i['name'] == 'generic.luck':
                            if config['allow_color_codes']: ca = '§a'
                            else: ca = ''
                            ss += f'{ca}☘{cc}{am} '
                        elif i['name'] == 'generic.movementSpeed':
                            if config['allow_color_codes']: ca = '§8'
                            else: ca = ''
                            ss += f'{ca}➣{cc}{am} '
                        elif i['name'] == 'generic.maxHealth':
                            if config['allow_color_codes']: ca = '§8'
                            else: ca = ''
                            ss += f'{ca}❤{cc}{am} '
                        elif i['name'] == 'generic.attackSpeed':
                            if config['allow_color_codes']: ca = '§d'
                            else: ca = ''
                            ss += f'{ca}⚔{cc}{am} '
                        elif i['name'] == 'generic.attackDamage':
                            if config['allow_color_codes']: ca = '§e'
                            else: ca = ''
                            ss += f'{ca}➚{cc}{am} '
                        elif i['name'] == 'generic.armor':
                            if config['allow_color_codes']: ca = '§f'
                            else: ca = ''
                            ss += f'{ca}☗{cc}{am}'
                        elif i['name'] == 'generic.armorToughnes':
                            if config['allow_color_codes']: ca = '§b'
                            else: ca = ''
                            ss += f'{ca}☗{cc}{am} '
                    res.append(f'"{ss}"')
        self.lore_array = ','.join(res)

    def enchant_parser(self):
        cosmetic = []
        true = {}
        lst = self.ench.split('\n')
        for x in lst:
            xx = x.split()
            if len(xx) > 0:
                if from_rome_numeric(xx[-1]) == 0:
                    num = 1
                    name = ' '.join(xx[::])
                else:
                    num = from_rome_numeric(xx[-1])
                    xx.remove(xx[-1])
                    name = ' '.join(xx)
                if name.lower() in enchants:
                    true[enchants[name.lower()]] = num
                else:
                    cosmetic.append(x)
            else: pass
        self.true_ench = true
        self.cosmetic_ench = cosmetic
        self.ench_list_nbt = '['
        ench_list = []
        for ench in self.true_ench:
            ench_list.append('{id:' + ench + ',lvl:' + str(self.true_ench[ench]) + '}')
        self.ench_list_nbt += ','.join(ench_list)
        self.ench_list_nbt += ']'

    def effect_parser(self):
        effect_arr = []
        for x in self.meta:
            x = x.split('|')
            if len(x) >= 3: lvl = str(int(x[2]) - 1)
            else: lvl = '0'
            if len(x) >= 2:
                time = [int(i) for i in x[1].split(':')]
                duration = str((time[0] * 60 + time[1]) * 160)
            else: duration = '9600'
            if len(x) >= 1:
                if x[0] in effects:
                    effect_id = effects[x[0]]
                    effect_arr.append('{Id:'+effect_id+',Amplifier:'+lvl+',Duration:'+duration+'}')
        self.effect_list_nbt = ',Potion:"minecraft:water",CustomPotionEffects:[' + ','.join(effect_arr) + ']'
