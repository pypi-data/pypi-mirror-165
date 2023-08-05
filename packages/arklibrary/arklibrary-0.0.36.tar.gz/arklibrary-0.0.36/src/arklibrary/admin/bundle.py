from arklibrary.admin.commands import Commands
from arklibrary.blueprints import *
import math


class Bundle(Commands):
    def execute(self):
        self.execute()

    def flak_armour(self, player_id, quality=0):
        boots = Armour.FLAK_BOOTS
        leggings = Armour.FLAK_LEGGINGS
        chest = Armour.FLAK_CHESTPIECE
        gauntlets = Armour.FLAK_GAUNTLETS
        helmet = Armour.FLAK_HELMET
        wings = Armour.GLIDER_SUIT
        self.give_items_to_player(player_id, [boots, leggings, chest, gauntlets, helmet, wings], quality=quality)

    def hazard_armour(self, player_id, quality=0):
        boots = Armour.HAZARD_SUIT_BOOTS
        leggings = Armour.HAZARD_SUIT_PANTS
        chest = Armour.HAZARD_SUIT_SHIRT
        gauntlets = Armour.HAZARD_SUIT_GLOVES
        helmet = Armour.HAZARD_SUIT_HAT
        wings = Armour.GLIDER_SUIT
        self.give_items_to_player(player_id, [boots, leggings, chest, gauntlets, helmet, wings], quality=quality)

    def desert_armour(self, player_id, quality=0):
        boots = Armour.DESERT_CLOTH_BOOTS
        leggings = Armour.DESERT_CLOTH_PANTS
        chest = Armour.DESERT_CLOTH_SHIRT
        gauntlets = Armour.DESERT_CLOTH_GLOVES
        helmet = Armour.DESERT_GOGGLES_AND_HAT
        wings = Armour.GLIDER_SUIT
        self.give_items_to_player(player_id, [boots, leggings, chest, gauntlets, helmet, wings], quality=quality)

    def fur_armour(self, player_id, quality=0):
        boots = Armour.FUR_BOOTS
        leggings = Armour.FUR_LEGGINGS
        chest = Armour.FUR_CHESTPIECE
        gauntlets = Armour.FUR_GAUNTLETS
        helmet = Armour.FUR_CAP
        wings = Armour.GLIDER_SUIT
        self.give_items_to_player(player_id, [boots, leggings, chest, gauntlets, helmet, wings], quality=quality)

    def tek_armour(self, player_id, quality=0):
        boots = Armour.TEK_BOOTS
        leggings = Armour.TEK_LEGGINGS
        chest = Armour.TEK_CHESTPIECE
        gauntlets = Armour.TEK_GAUNTLETS
        helmet = Armour.TEK_HELMET
        self.give_items_to_player(player_id, [boots, leggings, chest, gauntlets, helmet], quality=quality)

    def dino_starter(self, player_id, level=150):
        self.teleport_to_playerid(player_id)
        self.spawn_exact_dino(Dinos.PTERANODON, base_level=level)
        self.give_items_to_player(player_id, Saddles.PTERANODON_SADDLE)

    def rocket_set(self, player_id):
        rockets = Ammunition.ROCKET_PROPELLED_GRENADE
        launcher = Weapons.ROCKET_LAUNCHER
        self.give_items_to_player(player_id, [rockets], quantity=10)
        self.give_items_to_player(player_id, [launcher])

    def shotgun_set(self, player_id, quality=0):
        shotgun = Weapons.PUMP_ACTION_SHOTGUN
        ammo = Ammunition.SIMPLE_SHOTGUN_AMMO
        self.give_items_to_player(player_id, [ammo], quantity=100)
        self.give_items_to_player(player_id, [shotgun], quality=quality)

    def soaker_set(self, player_id, level=150, quality=0):
        self.teleport_to_playerid(player_id)
        self.spawn_exact_dino(Dinos.TEK_STEGOSAURUS, base_level=level)
        self.give_items_to_player(player_id, Saddles.STEGO_SADDLE, quality=quality)

    def sniper_set(self, player_id, quality=0):
        sniper = Weapons.FABRICATED_SNIPER_RIFLE
        ammo = Ammunition.ADVANCED_SNIPER_BULLET
        self.give_items_to_player(player_id, [ammo], quantity=100)
        self.give_items_to_player(player_id, [sniper], quality=quality)

    def compound_set(self, player_id, quality=0):
        bow = Weapons.COMPOUND_BOW
        ammo = Ammunition.METAL_ARROW
        flame = Ammunition.FLAME_ARROW
        self.give_items_to_player(player_id, [ammo, flame], quantity=100)
        self.give_items_to_player(player_id, [bow], quality=quality)

    def rifle_set(self, player_id, quality=0):
        rifle = Weapons.LONGNECK_RIFLE
        ammo = Ammunition.SIMPLE_RIFLE_AMMO
        tranq = Ammunition.SHOCKING_TRANQUILIZER_DART
        self.give_items_to_player(player_id, [ammo, tranq], quantity=100)
        self.give_items_to_player(player_id, [rifle], quality=quality)

    def hiking_set(self, player_id, quality=0):
        bow = Weapons.CROSSBOW
        grap = Ammunition.GRAPPLING_HOOK
        pick = Weapons.CLIMBING_PICK
        para = Armour.PARACHUTE
        glow = Weapons.GLOW_STICK
        self.give_items_to_player(player_id, [pick], quantity=3)
        self.give_items_to_player(player_id, [glow], quantity=5)
        self.give_items_to_player(player_id, [grap, para], quantity=50)
        self.give_items_to_player(player_id, [bow], quality=quality)

    def trap_set(self, player_id, quality=0):
        bow = Weapons.HARPOON_LAUNCHER
        net = Ammunition.NET_PROJECTILE
        trap = Weapons.BEAR_TRAP
        bear = Weapons.LARGE_BEAR_TRAP
        narc = Weapons.TRIPWIRE_NARCOTIC_TRAP
        bomb = Weapons.IMPROVISED_EXPLOSIVE_DEVICE
        self.give_items_to_player(player_id, [trap, bear, narc, bomb], quantity=3)
        self.give_items_to_player(player_id, [net], quantity=10)
        self.give_items_to_player(player_id, [bow], quality=quality)

    def c4_set(self, player_id):
        detonator = Weapons.C4_REMOTE_DETONATOR
        ammo = Ammunition.C4_CHARGE
        self.give_items_to_player(player_id, [ammo], quantity=20)
        self.give_items_to_player(player_id, [detonator])

    def flame_arrow_set(self, player_id, quality=0):
        crossbow = Weapons.CROSSBOW
        ammo = Ammunition.FLAME_ARROW
        self.give_items_to_player(player_id, [ammo], quantity=100)
        self.give_items_to_player(player_id, [crossbow], quality=quality)

    def electrical_set(self, player_id, quantity=1):
        generator = Structures.ELECTRICAL_GENERATOR
        outlet = Structures.ELECTRICAL_OUTLET
        wires = [Structures.STRAIGHT_ELECTRICAL_CABLE,
                 Structures.VERTICAL_ELECTRICAL_CABLE,
                 Structures.ELECTRICAL_CABLE_INTERSECTION,
                 Structures.INCLINED_ELECTRICAL_CABLE]
        gas = Resources.GASOLINE
        self.give_items_to_player(player_id, [gas] * quantity, quantity=50)
        self.give_items_to_player(player_id, [generator], quantity=quantity)
        self.give_items_to_player(player_id, wires + [outlet], quantity=quantity * 5)

    def crafting_set(self, player_id, quality=4, tek=False):
        smithy = Structures.SMITHY
        fabricator = Structures.FABRICATOR
        indiforge = Structures.INDUSTRIAL_FORGE
        chembench = Structures.CHEMISTRY_BENCH
        replicator = Structures.TEK_REPLICATOR
        gas = Resources.GASOLINE
        self.give_items_to_player(player_id, [smithy, fabricator, indiforge, chembench][:quality])
        self.give_item_to_player(player_id, gas, quantity=50)
        if tek:
            self.give_items_to_player(player_id, replicator)

    def storage_set(self, player_id, quantity=1):
        wood = Structures.STORAGE_BOX
        vault = Structures.VAULT
        fridge = Structures.REFRIGERATOR
        cryofridge = Structures.CRYOFRIDGE
        self.give_items_to_player(player_id, [wood, vault, fridge, cryofridge], quantity=quantity)

    def defense_set(self, player_id, quantity, quality=1):
        auto = Structures.AUTO_TURRET
        heavy = Structures.HEAVY_AUTO_TURRET
        ammo = Ammunition.ADVANCED_RIFLE_BULLET
        battery = Tools.BATTERY
        if quality == 1:
            self.give_items_to_player(player_id, [heavy, battery], quantity=quantity)
        else:
            self.give_items_to_player(player_id, [auto, battery], quantity=quantity)
        self.give_items_to_player(player_id, [ammo], quantity=200)

    def base_set(self, player_id, quantity=10):
        foundation = Structures.METAL_FOUNDATION
        wall = Structures.METAL_WALL
        ceiling = Structures.METAL_CEILING
        pillar = Structures.METAL_PILLAR
        doors = [Structures.METAL_DOUBLE_DOORFRAME, Structures.METAL_DOUBLE_DOOR]
        self.give_items_to_player(player_id, doors, quantity=math.ceil(quantity / 10))
        self.give_items_to_player(player_id, [pillar, foundation, wall, ceiling], quantity=quantity)

    def fob_set(self, player_id, quantity=1):
        self.base_set(player_id, quantity=10 * quantity)
        self.electrical_set(player_id, quantity=quantity)
        self.defense_set(player_id, quantity=quantity * 3)
        self.give_items_to_player(player_id, [Structures.GIANT_METAL_HATCHFRAME], quantity=quantity * 2)
        self.give_items_to_player(player_id, [Structures.SIMPLE_BED], quantity=quantity * 4)
        self.give_items_to_player(player_id, [Structures.VAULT], quantity=quantity)

    def resource_set(self, player_id, stacks=1, omit=[]):
        resources = [(Resources.METAL, 500),
                     (Resources.OBSIDIAN, 50),
                     (Resources.POLYMER, 50),
                     (Resources.HIDE, 300),
                     (Resources.OIL, 50),
                     (Resources.SILICA_PEARLS, 50),
                     (Resources.CHITIN, 100),
                     (Resources.STONE, 1000),
                     (Resources.FIBER, 1000),
                     (Resources.THATCH, 500),
                     (Resources.WOOD, 500),
                     (Resources.CRYSTAL, 50),
                     (Resources.FERTILIZER, 5),
                     (Resources.THATCH, 1000),
                     (Resources.FLINT, 1000),
                     (Resources.CHARCOAL, 500)]
        for resc in resources:
            blueprint, count = resc
            if blueprint not in omit:
                for i in range(stacks):
                    self.give_item_to_player(player_id, blueprint, quantity=count)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        items = []
        for k, v in self.__dict__.items():
            if k and k[0] != "_":
                items.append(f"\033[34m{k}\033[90m=\033[0m{repr(v)}\033[0m")
        args = ', '.join(items)
        return f'<\033[96m{type(self).__name__}\033[0m({args})>\033[0m'