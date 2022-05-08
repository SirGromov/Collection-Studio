from .Item import Item


class Collection:

    def __init__(self):
        self.items_list = []

    def add(self, item: Item):
        print(item.name, item.pattern)
        self.items_list.append(item)

    def get_chest_nbt(self):
        common_items, common_s = [], 0
        uncommon_items, uncommon_s = [], 0
        epic_items, epic_s = [], 0
        exotic_items, exotic_s = [], 0
        legendary_items, legendary_s = [], 0
        forbidden_items, forbidden_s = [], 0
        for item in self.items_list:
            if item.rarity == 'common':
                common_items.append('{Slot:'+str(common_s)+',id:'+item.itype+',Damage:'+item.var+',Count:'+str(item.amount)+',tag:'+item.nbt+'}')
                common_s += 1
            elif item.rarity == 'uncommon':
                uncommon_items.append('{Slot:'+str(uncommon_s)+',id:'+item.itype+',Damage:'+item.var+',Count:'+str(item.amount)+',tag:'+item.nbt+'}')
                uncommon_s += 1
            elif item.rarity == 'epic':
                epic_items.append('{Slot:'+str(epic_s)+',id:'+item.itype+',Damage:'+item.var+',Count:'+str(item.amount)+',tag:'+item.nbt+'}')
                epic_s += 1
            elif item.rarity == 'exotic':
                exotic_items.append('{Slot:'+str(exotic_s)+',id:'+item.itype+',Damage:'+item.var+',Count:'+str(item.amount)+',tag:'+item.nbt+'}')
                exotic_s += 1
            elif item.rarity == 'legendary':
                legendary_items.append('{Slot:'+str(legendary_s)+',id:'+item.itype+',Damage:'+item.var+',Count:'+str(item.amount)+',tag:'+item.nbt+'}')
                legendary_s += 1
            elif item.rarity == 'forbidden':
                forbidden_items.append('{Slot:'+str(forbidden_s)+',id:'+item.itype+',Damage:'+item.var+',Count:'+str(item.amount)+',tag:'+item.nbt+'}')
                forbidden_s += 1
        res = '/give @p purple_shulker_box 1 0 {BlockEntityTag:{Items:[{Slot:0,id:lime_shulker_box,Count:1,tag:{display:{Name:"Обычная"},BlockEntityTag:{Items:['+\
              ','.join(common_items)+']}}},{Slot:1,id:cyan_shulker_box,Count:1,tag:{display:{Name:"Редкая"},BlockEntityTag:{Items:['+\
              ','.join(uncommon_items)+']}}},{Slot:2,id:magenta_shulker_box,Count:1,tag:{display:{Name:"Эпическая"},BlockEntityTag:{Items:['+\
              ','.join(epic_items)+']}}},{Slot:3,id:orange_shulker_box,Count:1,tag:{display:{Name:"Мифическая"},BlockEntityTag:{Items:['+\
              ','.join(exotic_items)+']}}},{Slot:4,id:yellow_shulker_box,Count:1,tag:{display:{Name:"Легендарная"},BlockEntityTag:{Items:['+\
              ','.join(legendary_items)+']}}},{Slot:5,id:red_shulker_box,Count:1,tag:{display:{Name:"Запрещенная"},BlockEntityTag:{Items:['+\
              ','.join(forbidden_items)+']}}}]}}'
        self.give_common = '/give @p lime_shulker_box 1 0 {display:{Name:"Обычная"},BlockEntityTag:{Items:[' + ','.join(common_items) + ']}}'
        self.give_uncommon = '/give @p cyan_shulker_box 1 0 {display:{Name:"Редкая"},BlockEntityTag:{Items:[' + ','.join(uncommon_items) + ']}}'
        self.give_epic = '/give @p magenta_shulker_box 1 0 {display:{Name:"Эпическая"},BlockEntityTag:{Items:[' + ','.join(epic_items) + ']}}'
        self.give_exotic = '/give @p orange_shulker_box 1 0 {display:{Name:"Мифическая"},BlockEntityTag:{Items:[' + ','.join(exotic_items) + ']}}'
        self.give_legendary = '/give @p yellow_shulker_box 1 0 {display:{Name:"Легендарная"},BlockEntityTag:{Items:[' + ','.join(legendary_items) + ']}}'
        self.give_forbidden = '/give @p red_shulker_box 1 0 {display:{Name:"Запрещенная"},BlockEntityTag:{Items:[' + ','.join(forbidden_items) + ']}}'
        self.give_command = res

    def save_collection(self):
        self.get_chest_nbt()
        print(self.give_common)
        print(self.give_uncommon)
        print(self.give_epic)
        print(self.give_exotic)
        print(self.give_legendary)
        print(self.give_forbidden)
        print(self.give_command)
        with open('output/master.txt', 'w', encoding='utf-8') as f:
            f.write(self.give_command)
            f.close()
        with open('output/common.txt', 'w', encoding='utf-8') as f:
            f.write(self.give_common)
            f.close()
        with open('output/uncommon.txt', 'w', encoding='utf-8') as f:
            f.write(self.give_uncommon)
            f.close()
        with open('output/epic.txt', 'w', encoding='utf-8') as f:
            f.write(self.give_epic)
            f.close()
        with open('output/exotic.txt', 'w', encoding='utf-8') as f:
            f.write(self.give_exotic)
            f.close()
        with open('output/legendary.txt', 'w', encoding='utf-8') as f:
            f.write(self.give_legendary)
            f.close()
        with open('output/forbidden.txt', 'w', encoding='utf-8') as f:
            f.write(self.give_forbidden)
            f.close()
