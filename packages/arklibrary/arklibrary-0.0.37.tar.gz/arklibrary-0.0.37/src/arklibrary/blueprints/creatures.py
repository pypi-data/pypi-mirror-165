import re
from arklibrary.blueprints.saddles import Saddles
from arklibrary.blueprints.colors import Colorize


def set_creatures_admin(admin):
    _Creature._ADMIN = admin


class _Creature:
    _ADMIN = None
    __SADDLES = {k.replace('_SADDLE', ""): v for k, v in Saddles.__dict__.items() if '__' not in k}

    def __init__(self, blueprint_path, alpha=False, boss=None, event=None):
        self._tamed = False if alpha or boss is not None else True
        self._dino_blueprint_path = blueprint_path
        self._saddle_blueprint_path = ""
        self._saddle_quality = 0
        self._base_level = 0 if alpha or boss is not None else 150
        self._extra_levels = 0
        self._base_stats = "0,0,0,0,0,0,0,0"
        self._added_stats = "0,0,0,0,0,0,0,0"
        self._dino_name = ""
        self._cloned = 0
        self._neutered = 0
        self._tamed_on = ""
        self._uploaded_from = ""
        self._imprinter_name = ""
        self._imprinter_player_id = 0
        self._imprint_quality = 0
        self._colors = Colorize(self)
        self._dino_id = 0
        self._exp = 0
        self._spawn_distance = 0
        self._y_offset = 0
        self._z_offset = 0
        self._file_name = self.__get_file_name(blueprint_path)
        self.__special = False
        self.__alpha = alpha
        self.__boss = boss
        self.__event = event


    def __get_file_name(self, bp: str):
        found = re.findall(r'\..*', bp)
        if len(found) > 0:
            return found[0].replace(".", "").replace("'", "")
        else:
            return bp.split('/')[-1].replace("'", "")

    def color_regions(self):
        """Each dino has different color regions return the regions specific to that dino"""
        return {}

    def level(self, base_level: int):
        self._base_level = base_level
        return self

    def untamed(self):
        self._tamed = False
        return self

    def colored(self, region_1=0, region_2=0, region_3=0, region_4=0, region_5=0, region_6=0):
        if self.__boss is None and not self.__alpha:
            self.__special = True
            self._colors = "{},{},{},{},{},{}".format(region_1, region_2, region_3, region_4,
                                                     region_5, region_6)
        return self

    def neutered(self):
        if self.__boss is None and not self.__alpha:
            self.__special = True
            self._neutered = True
        return self

    def imprinted_by(self, player_id: int):
        if self.__boss is None and not self.__alpha:
            self.__special = True
            self._imprinter_player_id = player_id
        return self

    def saddled(self, quality: int=0):
        if self.__boss is None and not self.__alpha:
            self.__special = True
            self._saddle_quality = quality
            #TODO: find the saddle
        return self

    def cloned(self):
        if self.__boss is None and not self.__alpha:
            self.__special = True
            self._cloned = True
        return self

    def __spawn_exact_dino(self):
        format =  'cheat SpawnExactDino "{}" "{}" {} {} {} "{}" "{}" ' \
                  '"{}" {} {} "{}" "{}" "{}" {} {} "{}" {} {} {} {} {}'
        return format.format(self._dino_blueprint_path, self._saddle_blueprint_path, self._saddle_quality,
                                               self._base_level, self._extra_levels, self._base_stats, self._added_stats,
                                               self._dino_name, self._cloned, self._neutered, self._tamed_on,
                                               self._uploaded_from, self._imprinter_name, self._imprinter_player_id,
                                               self._imprint_quality, self._colors, self._dino_id, self._exp,
                                               self._spawn_distance, self._y_offset, self._z_offset)

    def __spawn_dino(self):
        return 'cheat SDF {} {} {}'.format(self._file_name, self._tamed, self._base_level)

    def spawn(self):
        if self.__special and not (self.__boss is not None or self.__alpha):
            command = self.__spawn_exact_dino()
        else:
            command = self.__spawn_dino()
        if _Creature._ADMIN is not None:
            _Creature._ADMIN.command(command)
        else:
            return command

    def __str__(self):
        if self.__boss is not None and '_Character' not in self._file_name:
            found = re.findall(r'_.*Char', self._file_name)
            if len(found) > 0:
                name = self._file_name.split(found[0])[0]
            else:
                name = self._file_name
        else:
            name = self._file_name.split("_Character")[0].replace('_', " ").replace('-', ' ')
        if self.__alpha:
            if 'mega' in name.lower():
                return f"Alpha {name[4:].strip()}"
            else:
                return name
        elif self.__boss is not None:
            return f"{name}" if self.__boss == '' else f"{self.__boss} {name}"
        return name

    def __repr__(self):
        return '_'.join([s.upper() for s in str(self).split()])


class Alphas:
    __ALPHA_BASILISK = "Blueprint'/Game/Aberration/Dinos/Basilisk/MegaBasilisk_Character_BP.MegaBasilisk_Character_BP'"
    __ALPHA_BLOOD_CRYSTAL_WYVERN = "Blueprint'/Game/PrimalEarth/Dinos/CrystalWyvern/CrystalWyvern_Character_BP_Mega.CrystalWyvern_Character_BP_Mega'"
    __ALPHA_CARNO = "Blueprint'/Game/PrimalEarth/Dinos/Carno/MegaCarno_Character_BP.MegaCarno_Character_BP'"
    __ALPHA_DEATHWORM = "Blueprint'/Game/ScorchedEarth/Dinos/Deathworm/MegaDeathworm_Character_BP.MegaDeathworm_Character_BP'"
    __ALPHA_FIRE_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/MegaWyvern_Character_BP_Fire.MegaWyvern_Character_BP_Fire'"
    __ALPHA_KARKINOS = "Blueprint'/Game/Aberration/Dinos/Crab/MegaCrab_Character_BP.MegaCrab_Character_BP'"
    __ALPHA_LEEDSICHTHYS = "Blueprint'/Game/PrimalEarth/Dinos/Leedsichthys/Alpha_Leedsichthys_Character_BP.Alpha_Leedsichthys_Character_BP'"
    __ALPHA_MEGALODON = "Blueprint'/Game/PrimalEarth/Dinos/Megalodon/MEgaMegalodon_Character_BP.MegaMegalodon_Character_BP'"
    __ALPHA_MOSASAUR = "Blueprint'/Game/PrimalEarth/Dinos/Mosasaurus/Mosa_Character_BP_Mega.Mosa_Character_BP_Mega'"
    __ALPHA_RAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Raptor/MegaRaptor_Character_BP.MegaRaptor_Character_BP'"
    __ALPHA_SURFACE_REAPER_KING = "Blueprint'/Game/Aberration/Dinos/Nameless/MegaXenomorph_Character_BP_Male_Surface.MegaXenomorph_Character_BP_Male_Surface'"
    __ALPHA_T_REX = "Blueprint'/Game/PrimalEarth/Dinos/Rex/MegaRex_Character_BP.MegaRex_Character_BP'"
    __ALPHA_TUSOTEUTHIS = "Blueprint'/Game/PrimalEarth/Dinos/Tusoteuthis/Mega_Tusoteuthis_Character_BP.Mega_Tusoteuthis_Character_BP'"
    __ALPHA_X_TRICERATOPS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Retrieve/Volcanic/Volcano_Trike_Character_BP_Retrieve_Alpha.Volcano_Trike_Character_BP_Retrieve_Alpha'"

    ALPHA_BASILISK = _Creature(__ALPHA_BASILISK, alpha=True)
    ALPHA_BLOOD_CRYSTAL_WYVERN = _Creature(__ALPHA_BLOOD_CRYSTAL_WYVERN, alpha=True)
    ALPHA_CARNO = _Creature(__ALPHA_CARNO, alpha=True)
    ALPHA_DEATHWORM = _Creature(__ALPHA_DEATHWORM, alpha=True)
    ALPHA_FIRE_WYVERN = _Creature(__ALPHA_FIRE_WYVERN, alpha=True)
    ALPHA_KARKINOS = _Creature(__ALPHA_KARKINOS, alpha=True)
    ALPHA_LEEDSICHTHYS = _Creature(__ALPHA_LEEDSICHTHYS, alpha=True)
    ALPHA_MEGALODON = _Creature(__ALPHA_MEGALODON, alpha=True)
    ALPHA_MOSASAUR = _Creature(__ALPHA_MOSASAUR, alpha=True)
    ALPHA_RAPTOR = _Creature(__ALPHA_RAPTOR, alpha=True)
    ALPHA_SURFACE_REAPER_KING = _Creature(__ALPHA_SURFACE_REAPER_KING, alpha=True)
    ALPHA_T_REX = _Creature(__ALPHA_T_REX, alpha=True)


class Bosses:
    __BROODMOTHER_LYSRIX = "Blueprint'/Game/PrimalEarth/Dinos/Spider-Large/SpiderL_Character_BP.SpiderL_Character_BP'"
    __CORRUPTED_MASTER_CONTROLLER_ALPHA = "Blueprint'/Game/Genesis/Dinos/VRMainBoss/VRMainBoss_Character_Hard.VRMainBoss_Character_Hard'"
    __CORRUPTED_MASTER_CONTROLLER_BETA = "Blueprint'/Game/Genesis/Dinos/VRMainBoss/VRMainBoss_Character_Medium.VRMainBoss_Character_Medium'"
    __CORRUPTED_MASTER_CONTROLLER_GAMMA = "Blueprint'/Game/Genesis/Dinos/VRMainBoss/VRMainBoss_Character_Easy.VRMainBoss_Character_Easy'"
    __CRYSTAL_WYVERN_QUEEN_ALPHA = "Blueprint'/Game/Mods/CrystalIsles/Assets/Dinos/CIBoss/CrystalWyvern_Character_BP_Boss_Hard.CrystalWyvern_Character_BP_Boss_Hard'"
    __CRYSTAL_WYVERN_QUEEN_BETA = "Blueprint'/Game/Mods/CrystalIsles/Assets/Dinos/CIBoss/CrystalWyvern_Character_BP_Boss_Medium.CrystalWyvern_Character_BP_Boss_Medium'"
    __CRYSTAL_WYVERN_QUEEN_GAMMA = "Blueprint'/Game/Mods/CrystalIsles/Assets/Dinos/CIBoss/CrystalWyvern_Character_BP_Boss_Easy.CrystalWyvern_Character_BP_Boss_Easy'"
    __DESERT_TITAN = "Blueprint'/Game/Extinction/Dinos/DesertKaiju/DesertKaiju_Character_BP.DesertKaiju_Character_BP'"
    __DESERT_TITAN_FLOCK = "Blueprint'/Game/Extinction/Dinos/DesertKaiju/DesertKaiju_FirstFlockChar_BP.DesertKaiju_FirstFlockChar_BP'"
    __DRAGON_ALPHA = "Blueprint'/Game/PrimalEarth/Dinos/Dragon/Dragon_Character_BP_Boss_Hard.Dragon_Character_BP_Boss_Hard'"
    __DRAGON_BETA = "Blueprint'/Game/PrimalEarth/Dinos/Dragon/Dragon_Character_BP_Boss_Medium.Dragon_Character_BP_Boss_Medium'"
    __DRAGON_GAMMA = "Blueprint'/Game/PrimalEarth/Dinos/Dragon/Dragon_Character_BP_Boss_Easy.Dragon_Character_BP_Boss_Easy'"
    __FOREST_TITAN = "Blueprint'/Game/Extinction/Dinos/ForestKaiju/ForestKaiju_Character_BP.ForestKaiju_Character_BP'"
    __ICE_TITAN = "Blueprint'/Game/Extinction/Dinos/IceKaiju/IceKaiju_Character_BP.IceKaiju_Character_BP'"
    __KING_TITAN_ALPHA = "Blueprint'/Game/Extinction/Dinos/KingKaiju/KingKaiju_Character_BP_Alpha.KingKaiju_Character_BP_Alpha'"
    __KING_TITAN_BETA = "Blueprint'/Game/Extinction/Dinos/KingKaiju/KingKaiju_Character_BP_Beta.KingKaiju_Character_BP_Beta'"
    __KING_TITAN_GAMMA = "Blueprint'/Game/Extinction/Dinos/KingKaiju/KingKaiju_Character_BP.KingKaiju_Character_BP'"
    __MANTICORE_ALPHA = "Blueprint'/Game/ScorchedEarth/Dinos/Manticore/Manticore_Character_BP_Hard.Manticore_Character_BP_Hard'"
    __MANTICORE_BETA = "Blueprint'/Game/ScorchedEarth/Dinos/Manticore/Manticore_Character_BP_Medium.Manticore_Character_BP_Medium'"
    __MANTICORE_GAMMA = "Blueprint'/Game/ScorchedEarth/Dinos/Manticore/Manticore_Character_BP_Easy.Manticore_Character_BP_Easy'"
    __MEGAPITHECUS = "Blueprint'/Game/PrimalEarth/Dinos/Gorilla/Gorilla_Character_BP.Gorilla_Character_BP'"
    __MOEDER_ALPHA = "Blueprint'/Game/Genesis/Dinos/EelBoss/EelBoss_Character_BP_Hard.EelBoss_Character_BP_Hard'"
    __MOEDER_BETA = "Blueprint'/Game/Genesis/Dinos/EelBoss/EelBoss_Character_BP_Medium.EelBoss_Character_BP_Medium'"
    __MOEDER_GAMMA = "Blueprint'/Game/Genesis/Dinos/EelBoss/EelBoss_Character_BP_Easy.EelBoss_Character_BP_Easy'"
    __ROCKWELL = "Blueprint'/Game/Aberration/Boss/Rockwell/Rockwell_Character_BP.Rockwell_Character_BP'"
    __ROCKWELL_ALPHA = "Blueprint'/Game/Aberration/Boss/Rockwell/Rockwell_Character_BP_Hard.Rockwell_Character_BP_Hard'"
    __ROCKWELL_BETA = "Blueprint'/Game/Aberration/Boss/Rockwell/Rockwell_Character_BP_Medium.Rockwell_Character_BP_Medium'"
    __ROCKWELL_GAMMA = "Blueprint'/Game/Aberration/Boss/Rockwell/Rockwell_Character_BP_Easy.Rockwell_Character_BP_Easy'"
    __ROCKWELL_NODE = "Blueprint'/Game/Genesis2/Missions/ModularMission/FinalBattleAlt/Dinos/RockwellNode_Character_BP_FinalFight.RockwellNode_Character_BP_FinalFight'"
    __ROCKWELL_NODE_ALPHA = "Blueprint'/Game/Genesis2/Missions/ModularMission/FinalBattleAlt/Difficulties/Alpha/RockwellNode_Character_BP_FinalFight_Alpha.RockwellNode_Character_BP_FinalFight_Alpha'"
    __ROCKWELL_NODE_BETA = "Blueprint'/Game/Genesis2/Missions/ModularMission/FinalBattleAlt/Difficulties/Beta/RockwellNode_Character_BP_FinalFight_Beta.RockwellNode_Character_BP_FinalFight_Beta'"
    __ROCKWELL_NODE_GAMMA = "Blueprint'/Game/Genesis2/Missions/ModularMission/FinalBattleAlt/Difficulties/Gamma/RockwellNode_Character_BP_FinalFight_Gamma.RockwellNode_Character_BP_FinalFight_Gamma'"
    __ROCKWELL_PRIME = "Blueprint'/Game/Genesis2/Missions/ModularMission/FinalBattleAlt/Dinos/RockwellNode_Character_BP_Boss.RockwellNode_Character_BP_Boss'"
    __ROCKWELL_PRIME_ALPHA = "Blueprint'/Game/Genesis2/Missions/ModularMission/FinalBattleAlt/Difficulties/Alpha/RockwellNode_Character_BP_Boss_Alpha.RockwellNode_Character_BP_Boss_Alpha'"
    __ROCKWELL_PRIME_BETA = "Blueprint'/Game/Genesis2/Missions/ModularMission/FinalBattleAlt/Difficulties/Beta/RockwellNode_Character_BP_Boss_Beta.RockwellNode_Character_BP_Boss_Beta'"
    __ROCKWELL_PRIME_GAMMA = "Blueprint'/Game/Genesis2/Missions/ModularMission/FinalBattleAlt/Difficulties/Gamma/RockwellNode_Character_BP_Boss_Gamma.RockwellNode_Character_BP_Boss_Gamma'"
    __ROCKWELL_TENTACLE = "Blueprint'/Game/Aberration/Boss/RockwellTentacle/RockwellTentacle_Character_BP.RockwellTentacle_Character_BP'"
    __ROCKWELL_TENTACLE_ALPHA = "Blueprint'/Game/Aberration/Boss/RockwellTentacle/RockwellTentacle_Character_BP_Alpha.RockwellTentacle_Character_BP_Alpha'"
    __ROCKWELL_TENTACLE_BETA = "Blueprint'/Game/Aberration/Boss/RockwellTentacle/RockwellTentacle_Character_BP_Beta.RockwellTentacle_Character_BP_Beta'"
    __ROCKWELL_TENTACLE_GAMMA = "Blueprint'/Game/Aberration/Boss/RockwellTentacle/RockwellTentacle_Character_BP_Gamma.RockwellTentacle_Character_BP_Gamma'"

    BROODMOTHER_LYSRIX = _Creature(__BROODMOTHER_LYSRIX, boss='')
    CORRUPTED_MASTER_CONTROLLER_ALPHA = _Creature(__CORRUPTED_MASTER_CONTROLLER_ALPHA, boss='Alpha')
    CORRUPTED_MASTER_CONTROLLER_BETA = _Creature(__CORRUPTED_MASTER_CONTROLLER_BETA, boss='Beta')
    CORRUPTED_MASTER_CONTROLLER_GAMMA = _Creature(__CORRUPTED_MASTER_CONTROLLER_GAMMA, boss='Gamma')
    CRYSTAL_WYVERN_QUEEN_ALPHA = _Creature(__CRYSTAL_WYVERN_QUEEN_ALPHA, boss='Alpha')
    CRYSTAL_WYVERN_QUEEN_BETA = _Creature(__CRYSTAL_WYVERN_QUEEN_BETA, boss='Beta')
    CRYSTAL_WYVERN_QUEEN_GAMMA = _Creature(__CRYSTAL_WYVERN_QUEEN_GAMMA, boss='Gamma')
    DESERT_TITAN = _Creature(__DESERT_TITAN, boss='')
    DESERT_TITAN_FLOCK = _Creature(__DESERT_TITAN_FLOCK, boss='')
    DRAGON_ALPHA = _Creature(__DRAGON_ALPHA, boss='Alpha')
    DRAGON_BETA = _Creature(__DRAGON_BETA, boss='Beta')
    DRAGON_GAMMA = _Creature(__DRAGON_GAMMA, boss='Gamma')
    FOREST_TITAN = _Creature(__FOREST_TITAN, boss='')
    ICE_TITAN = _Creature(__ICE_TITAN, boss='')
    KING_TITAN_ALPHA = _Creature(__KING_TITAN_ALPHA, boss='Alpha')
    KING_TITAN_BETA = _Creature(__KING_TITAN_BETA, boss='Beta')
    KING_TITAN_GAMMA = _Creature(__KING_TITAN_GAMMA, boss='Gamma')
    MANTICORE_ALPHA = _Creature(__MANTICORE_ALPHA, boss='Alpha')
    MANTICORE_BETA = _Creature(__MANTICORE_BETA, boss='Beta')
    MANTICORE_GAMMA = _Creature(__MANTICORE_GAMMA, boss='Gamma')
    MEGAPITHECUS = _Creature(__MEGAPITHECUS, boss='')
    MOEDER_ALPHA = _Creature(__MOEDER_ALPHA, boss='Alpha')
    MOEDER_BETA = _Creature(__MOEDER_BETA, boss='Beta')
    MOEDER_GAMMA = _Creature(__MOEDER_GAMMA, boss='Gamma')
    ROCKWELL = _Creature(__ROCKWELL, boss='')
    ROCKWELL_ALPHA = _Creature(__ROCKWELL_ALPHA, boss='Alpha')
    ROCKWELL_BETA = _Creature(__ROCKWELL_BETA, boss='Beta')
    ROCKWELL_GAMMA = _Creature(__ROCKWELL_GAMMA, boss='Gamma')
    ROCKWELL_NODE = _Creature(__ROCKWELL_NODE, boss='')
    ROCKWELL_NODE_ALPHA = _Creature(__ROCKWELL_NODE_ALPHA, boss='Alpha')
    ROCKWELL_NODE_BETA = _Creature(__ROCKWELL_NODE_BETA, boss='Beta')
    ROCKWELL_NODE_GAMMA = _Creature(__ROCKWELL_NODE_GAMMA, boss='Gamma')
    ROCKWELL_PRIME = _Creature(__ROCKWELL_PRIME, boss='')
    ROCKWELL_PRIME_ALPHA = _Creature(__ROCKWELL_PRIME_ALPHA, boss='Alpha')
    ROCKWELL_PRIME_BETA = _Creature(__ROCKWELL_PRIME_BETA, boss='Beta')
    ROCKWELL_PRIME_GAMMA = _Creature(__ROCKWELL_PRIME_GAMMA, boss='Gamma')
    ROCKWELL_TENTACLE = _Creature(__ROCKWELL_TENTACLE, boss='')
    ROCKWELL_TENTACLE_ALPHA = _Creature(__ROCKWELL_TENTACLE_ALPHA, boss='Alpha')
    ROCKWELL_TENTACLE_BETA = _Creature(__ROCKWELL_TENTACLE_BETA, boss='Beta')
    ROCKWELL_TENTACLE_GAMMA = _Creature(__ROCKWELL_TENTACLE_GAMMA, boss='Gamma')


class Dinos:
    __ABERRANT_DIPLOCAULUS = "Blueprint'/Game/PrimalEarth/Dinos/Diplocaulus/Diplocaulus_Character_BP_Aberrant.Diplocaulus_Character_BP_Aberrant'"
    __DIPLOCAULUS = "Blueprint'/Game/PrimalEarth/Dinos/Diplocaulus/Diplocaulus_Character_BP.Diplocaulus_Character_BP'"
    __ABERRANT_DODO = "Blueprint'/Game/PrimalEarth/Dinos/Dodo/Dodo_Character_BP_Aberrant.Dodo_Character_BP_Aberrant'"
    __ARCHAEOPTERYX = "Blueprint'/Game/PrimalEarth/Dinos/Archaeopteryx/Archa_Character_BP.Archa_Character_BP'"
    __ARGENTAVIS = "Blueprint'/Game/PrimalEarth/Dinos/Argentavis/Argent_Character_BP.Argent_Character_BP'"
    __DODO = "Blueprint'/Game/PrimalEarth/Dinos/Dodo/Dodo_Character_BP.Dodo_Character_BP'"
    __HESPERORNIS = "Blueprint'/Game/PrimalEarth/Dinos/Hesperornis/Hesperornis_Character_BP.Hesperornis_Character_BP'"
    __ICHTHYORNIS = "Blueprint'/Game/PrimalEarth/Dinos/Ichthyornis/Ichthyornis_Character_BP.Ichthyornis_Character_BP'"
    __KAIRUKU = "Blueprint'/Game/PrimalEarth/Dinos/Kairuku/Kairuku_Character_BP.Kairuku_Character_BP'"
    __PELAGORNIS = "Blueprint'/Game/PrimalEarth/Dinos/Pelagornis/Pela_Character_BP.Pela_Character_BP'"
    __SNOW_OWL = "Blueprint'/Game/Extinction/Dinos/Owl/Owl_Character_BP.Owl_Character_BP'"
    __TERROR_BIRD = "Blueprint'/Game/PrimalEarth/Dinos/TerrorBird/TerrorBird_Character_BP.TerrorBird_Character_BP'"
    __VULTURE = "Blueprint'/Game/ScorchedEarth/Dinos/Vulture/Vulture_Character_BP.Vulture_Character_BP'"
    __BRUTE_ARANEO = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Bog/SpiderS_Character_BP_Hunt.SpiderS_Character_BP_Hunt'"
    __BRUTE_ASTROCETUS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Lunar/SpaceWhale_Character_BP_Brute.SpaceWhale_Character_BP_Brute'"
    __BRUTE_BASILOSAURUS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Ocean/Basilosaurus_Character_BP_Hunt.Basilosaurus_Character_BP_Hunt'"
    __BRUTE_BLOODSTALKER = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Bog/BogSpider_Character_BP_Hunt.BogSpider_Character_BP_Hunt'"
    __BRUTE_FEROX = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Arctic/Shapeshifter_Large_Character_BP_Hunt.Shapeshifter_Large_Character_BP_Hunt'"
    __BRUTE_FIRE_WYVERN = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Gauntlet/Volcanic/Wyvern_Character_BP_Fire_GauntletBoss.Wyvern_Character_BP_Fire_GauntletBoss'"
    __BRUTE_LEEDSICHTHYS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Ocean/Leedsichthys_Character_BP_Hunt.Leedsichthys_Character_BP_Hunt'"
    __BRUTE_MAGMASAUR = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Volcanic/Cherufe_Character_BP_Hunt.Cherufe_Character_BP_Hunt'"
    __BRUTE_MALFUNCTIONED_TEK_GIGANOTOSAURUS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Lunar/BionicGigant_Character_BP_Malfunctioned_Hunt.BionicGigant_Character_BP_Malfunctioned_Hunt'"
    __BRUTE_MALFUNCTIONED_TEK_REX = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Lunar/BionicRex_Character_BP_Malfunctioned_Hunt.BionicRex_Character_BP_Malfunctioned_Hunt'"
    __BRUTE_MAMMOTH = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Arctic/Mammoth_Character_BP_Hunt.Mammoth_Character_BP_Hunt'"
    __BRUTE_MEGALOCEROS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Arctic/Stag_Character_BP_Hunt.Stag_Character_BP_Hunt'"
    __BRUTE_PLESIOSAUR = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Ocean/Plesiosaur_Character_BP_Hunt.Plesiosaur_Character_BP_Hunt'"
    __BRUTE_REAPER_KING = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Lunar/Xenomorph_Character_BP_Male_InitialBuryOnly_Hunt.Xenomorph_Character_BP_Male_InitialBuryOnly_Hunt'"
    __BRUTE_SARCO = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Bog/Sarco_Character_BP_Hunt.Sarco_Character_BP_Hunt'"
    __BRUTE_SEEKER = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Lunar/Pteroteuthis_Char_BP_HuntFollower.Pteroteuthis_Char_BP_HuntFollower'"
    __BRUTE_TUSOTEUTHIS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Ocean/Tusoteuthis_Character_BP_Hunt.Tusoteuthis_Character_BP_Hunt'"
    __BRUTE_X_ALLOSAURUS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Volcanic/Volcano_Allo_Character_BP_Hunt.Volcano_Allo_Character_BP_Hunt'"
    __BRUTE_X_MEGALODON = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Ocean/Ocean_Megalodon_Character_BP_Hunt.Ocean_Megalodon_Character_BP_Hunt'"
    __BRUTE_X_MOSASAURUS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Ocean/Ocean_Mosa_Character_BP_Hunt.Ocean_Mosa_Character_BP_Hunt'"
    __BRUTE_X_RAPTOR = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Bog/Bog_Raptor_Character_BP_Hunt.Bog_Raptor_Character_BP_Hunt'"
    __BRUTE_X_REX = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Volcanic/Volcano_Rex_Character_BP_Hunt.Volcano_Rex_Character_BP_Hunt'"
    __BRUTE_X_ROCK_ELEMENTAL = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Volcanic/Volcano_Golem_Character_BP_Hunt.Volcano_Golem_Character_BP_Hunt'"
    __BRUTE_X_SPINO = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Bog/Bog_Spino_Character_BP_Hunt.Bog_Spino_Character_BP_Hunt'"
    __BRUTE_X_YUTYRANNUS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Hunt/Arctic/Snow_Yutyrannus_Character_BP_Hunt.Snow_Yutyrannus_Character_BP_Hunt'"
    __GOLDEN_STRIPED_BRUTE_MEGALODON = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Retrieve/Ocean/Ocean_Megalodon_Character_BP_Retrieve_Brute.Ocean_Megalodon_Character_BP_Retrieve_Brute'"
    __INJURED_BRUTE_REAPER_KING = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Retrieve/Lunar/Xenomorph_Character_BP_Male_InitialBuryOnly_Brute_Retrieve.Xenomorph_Character_BP_Male_InitialBuryOnly_Brute_Retrieve'"
    __ABERRANT_ANKYLOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Ankylo/Ankylo_Character_BP_Aberrant.Ankylo_Character_BP_Aberrant'"
    __ABERRANT_BARYONYX = "Blueprint'/Game/PrimalEarth/Dinos/Baryonyx/Baryonyx_Character_BP_Aberrant.Baryonyx_Character_BP_Aberrant'"
    __ABERRANT_CARNOTAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Carno/Carno_Character_BP_Aberrant.Carno_Character_BP_Aberrant'"
    __ABERRANT_DIMETRODON = "Blueprint'/Game/PrimalEarth/Dinos/Dimetrodon/Dimetro_Character_BP_Aberrant.Dimetro_Character_BP_Aberrant'"
    __ABERRANT_DIMORPHODON = "Blueprint'/Game/PrimalEarth/Dinos/Dimorphodon/Dimorph_Character_BP_Aberrant.Dimorph_Character_BP_Aberrant'"
    __ABERRANT_DIPLODOCUS = "Blueprint'/Game/PrimalEarth/Dinos/Diplodocus/Diplodocus_Character_BP_Aberrant.Diplodocus_Character_BP_Aberrant'"
    __ABERRANT_DOEDICURUS = "Blueprint'/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP_Aberrant.Doed_Character_BP_Aberrant'"
    __ABERRANT_IGUANODON = "Blueprint'/Game/PrimalEarth/Dinos/Iguanodon/Iguanodon_Character_BP_Aberrant.Iguanodon_Character_BP_Aberrant'"
    __ABERRANT_LYSTROSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Lystrosaurus/Lystro_Character_BP_Aberrant.Lystro_Character_BP_Aberrant'"
    __ABERRANT_MEGALOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Megalosaurus/Megalosaurus_Character_BP_Aberrant.Megalosaurus_Character_BP_Aberrant'"
    __ABERRANT_PARASAUR = "Blueprint'/Game/PrimalEarth/Dinos/Para/Para_Character_BP_Aberrant.Para_Character_BP_Aberrant'"
    __ABERRANT_RAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Raptor/Raptor_Character_BP_Aberrant.Raptor_Character_BP_Aberrant'"
    __ABERRANT_SPINO = "Blueprint'/Game/PrimalEarth/Dinos/Spino/Spino_Character_BP_Aberrant.Spino_Character_BP_Aberrant'"
    __ABERRANT_STEGOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Stego/Stego_Character_BP_Aberrant.Stego_Character_BP_Aberrant'"
    __ABERRANT_TRICERATOPS = "Blueprint'/Game/PrimalEarth/Dinos/Trike/Trike_Character_BP_Aberrant.Trike_Character_BP_Aberrant'"
    __ALLOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Allosaurus/Allo_Character_BP.Allo_Character_BP'"
    __ANKYLOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Ankylo/Ankylo_Character_BP.Ankylo_Character_BP'"
    __BARYONYX = "Blueprint'/Game/PrimalEarth/Dinos/Baryonyx/Baryonyx_Character_BP.Baryonyx_Character_BP'"
    __BRONTOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Sauropod/Sauropod_Character_BP.Sauropod_Character_BP'"
    __CARNOTAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Carno/Carno_Character_BP.Carno_Character_BP'"
    __COMPY = "Blueprint'/Game/PrimalEarth/Dinos/Compy/Compy_Character_BP.Compy_Character_BP'"
    __CORRUPTED_CARNOTAURUS = "Blueprint'/Game/Extinction/Dinos/Corrupt/Carno/Carno_Character_BP_Corrupt.Carno_Character_BP_Corrupt'"
    __CORRUPTED_DILOPHOSAUR = "Blueprint'/Game/Extinction/Dinos/Corrupt/Dilo/Dilo_Character_BP_Corrupt.Dilo_Character_BP_Corrupt'"
    __CORRUPTED_DIMORPHODON = "Blueprint'/Game/Extinction/Dinos/Corrupt/Dimorphodon/Dimorph_Character_BP_Corrupt.Dimorph_Character_BP_Corrupt'"
    __CORRUPTED_GIGANOTOSAURUS = "Blueprint'/Game/Extinction/Dinos/Corrupt/Giganotosaurus/Gigant_Character_BP_Corrupt.Gigant_Character_BP_Corrupt'"
    __CORRUPTED_PTERANODON = "Blueprint'/Game/Extinction/Dinos/Corrupt/Ptero/Ptero_Character_BP_Corrupt.Ptero_Character_BP_Corrupt'"
    __CORRUPTED_RAPTOR = "Blueprint'/Game/Extinction/Dinos/Corrupt/Raptor/Raptor_Character_BP_Corrupt.Raptor_Character_BP_Corrupt'"
    __CORRUPTED_REX = "Blueprint'/Game/Extinction/Dinos/Corrupt/Rex/Rex_Character_BP_Corrupt.Rex_Character_BP_Corrupt'"
    __CORRUPTED_SPINO = "Blueprint'/Game/Extinction/Dinos/Corrupt/Spino/Spino_Character_BP_Corrupt.Spino_Character_BP_Corrupt'"
    __CORRUPTED_STEGOSAURUS = "Blueprint'/Game/Extinction/Dinos/Corrupt/Stego/Stego_Character_BP_Corrupt.Stego_Character_BP_Corrupt'"
    __CORRUPTED_TRICERATOPS = "Blueprint'/Game/Extinction/Dinos/Corrupt/Trike/Trike_Character_BP_Corrupt.Trike_Character_BP_Corrupt'"
    __DEINONYCHUS = "Blueprint'/Game/PrimalEarth/Dinos/Raptor/Uberraptor/Deinonychus_Character_BP.Deinonychus_Character_BP'"
    __DILOPHOSAUR = "Blueprint'/Game/PrimalEarth/Dinos/Dilo/Dilo_Character_BP.Dilo_Character_BP'"
    __DIMETRODON = "Blueprint'/Game/PrimalEarth/Dinos/Dimetrodon/Dimetro_Character_BP.Dimetro_Character_BP'"
    __DIMORPHODON = "Blueprint'/Game/PrimalEarth/Dinos/Dimorphodon/Dimorph_Character_BP.Dimorph_Character_BP'"
    __DIPLODOCUS = "Blueprint'/Game/PrimalEarth/Dinos/Diplodocus/Diplodocus_Character_BP.Diplodocus_Character_BP'"
    __ENRAGED_CORRUPTED_REX = "Blueprint'/Game/Extinction/Dinos/Corrupt/Rex/MegaRex_Character_BP_Corrupt.MegaRex_Character_BP_Corrupt'"
    __ENRAGED_TRICERATOPS = "Blueprint'/Game/Extinction/Dinos/Corrupt/Trike/MegaTrike_Character_BP_Corrupt.MegaTrike_Character_BP_Corrupt'"
    __GALLIMIMUS = "Blueprint'/Game/PrimalEarth/Dinos/Gallimimus/Galli_Character_BP.Galli_Character_BP'"
    __GIGANOTOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Giganotosaurus/Gigant_Character_BP.Gigant_Character_BP'"
    __IGUANODON = "Blueprint'/Game/PrimalEarth/Dinos/Iguanodon/Iguanodon_Character_BP.Iguanodon_Character_BP'"
    __KENTROSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Kentrosaurus/Kentro_Character_BP.Kentro_Character_BP'"
    __LYSTROSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Lystrosaurus/Lystro_Character_BP.Lystro_Character_BP'"
    __MEGALOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Megalosaurus/Megalosaurus_Character_BP.Megalosaurus_Character_BP'"
    __MICRORAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Microraptor/Microraptor_Character_BP.Microraptor_Character_BP'"
    __MORELLATOPS = "Blueprint'/Game/ScorchedEarth/Dinos/Camelsaurus/camelsaurus_Character_BP.camelsaurus_Character_BP'"
    __MOSCHOPS = "Blueprint'/Game/PrimalEarth/Dinos/Moschops/Moschops_Character_BP.Moschops_Character_BP'"
    __OVIRAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Oviraptor/Oviraptor_Character_BP.Oviraptor_Character_BP'"
    __PACHY = "Blueprint'/Game/PrimalEarth/Dinos/Pachy/Pachy_Character_BP.Pachy_Character_BP'"
    __PACHYRHINOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Pachyrhinosaurus/Pachyrhino_Character_BP.Pachyrhino_Character_BP'"
    __PARASAUROLOPHUS = "Blueprint'/Game/PrimalEarth/Dinos/Para/Para_Character_BP.Para_Character_BP'"
    __PEGOMASTAX = "Blueprint'/Game/PrimalEarth/Dinos/Pegomastax/Pegomastax_Character_BP.Pegomastax_Character_BP'"
    __PTERANODON = "Blueprint'/Game/PrimalEarth/Dinos/Ptero/Ptero_Character_BP.Ptero_Character_BP'"
    __RAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Raptor/Raptor_Character_BP.Raptor_Character_BP'"
    __REX = "Blueprint'/Game/PrimalEarth/Dinos/Rex/Rex_Character_BP.Rex_Character_BP'"
    __SPINO = "Blueprint'/Game/PrimalEarth/Dinos/Spino/Spino_Character_BP.Spino_Character_BP'"
    __STEGOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Stego/Stego_Character_BP.Stego_Character_BP'"
    __THERIZINOSAUR = "Blueprint'/Game/PrimalEarth/Dinos/Therizinosaurus/Therizino_Character_BP.Therizino_Character_BP'"
    __TITANOSAUR = "Blueprint'/Game/PrimalEarth/Dinos/titanosaur/Titanosaur_Character_BP.Titanosaur_Character_BP'"
    __TRICERATOPS = "Blueprint'/Game/PrimalEarth/Dinos/Trike/Trike_Character_BP.Trike_Character_BP'"
    __TROODON = "Blueprint'/Game/PrimalEarth/Dinos/Troodon/Troodon_Character_BP.Troodon_Character_BP'"
    __YUTYRANNUS = "Blueprint'/Game/PrimalEarth/Dinos/Yutyrannus/Yutyrannus_Character_BP.Yutyrannus_Character_BP'"
    __ASTROCETUS = "Blueprint'/Game/Genesis/Dinos/SpaceWhale/SpaceWhale_Character_BP.SpaceWhale_Character_BP'"
    __ASTRODELPHIS = "Blueprint'/Game/Genesis2/Dinos/SpaceDolphin/SpaceDolphin_Character_BP.SpaceDolphin_Character_BP'"
    __BASILISK = "Blueprint'/Game/Aberration/Dinos/Basilisk/Basilisk_Character_BP.Basilisk_Character_BP'"
    __BLOOD_CRYSTAL_WYVERN = "Blueprint'/Game/PrimalEarth/Dinos/CrystalWyvern/CrystalWyvern_Character_BP_Blood.CrystalWyvern_Character_BP_Blood'"
    __BLOODSTALKER = "Blueprint'/Game/Genesis/Dinos/BogSpider/BogSpider_Character_BP.BogSpider_Character_BP'"
    __BULBDOG = "Blueprint'/Game/Aberration/Dinos/LanternPug/LanternPug_Character_BP.LanternPug_Character_BP'"
    __CHALK_GOLEM = "Blueprint'/Game/Mods/Valguero/Assets/Dinos/RockGolem/ChalkGolem/ChalkGolem_Character_BP.ChalkGolem_Character_BP'"
    __CORRUPTED_REAPER_KING = "Blueprint'/Game/Extinction/Dinos/Corrupt/Nameless/Xenomorph_Character_BP_Male_Tamed_Corrupt.Xenomorph_Character_BP_Male_Tamed_Corrupt'"
    __CORRUPTED_ROCK_DRAKE = "Blueprint'/Game/Extinction/Dinos/Corrupt/RockDrake/RockDrake_Character_BP_Corrupt.RockDrake_Character_BP_Corrupt'"
    __CORRUPTED_WYVERN = "Blueprint'/Game/Extinction/Dinos/Corrupt/Wyvern/Wyvern_Character_BP_Fire_Corrupt.Wyvern_Character_BP_Fire_Corrupt'"
    __DEFENSE_UNIT = "Blueprint'/Game/Extinction/Dinos/Tank/Defender_Character_BP.Defender_Character_BP'"
    __EEL_MINION = "Blueprint'/Game/Genesis/Dinos/EelBoss/EelMinion_Character_BP_Easy.EelMinion_Character_BP_Easy'"
    __EMBER_CRYSTAL_WYVERN = "Blueprint'/Game/PrimalEarth/Dinos/CrystalWyvern/CrystalWyvern_Character_BP_Ember.CrystalWyvern_Character_BP_Ember'"
    __ENFORCER = "Blueprint'/Game/Extinction/Dinos/Enforcer/Enforcer_Character_BP.Enforcer_Character_BP'"
    __FEATHERLIGHT = "Blueprint'/Game/Aberration/Dinos/LanternBird/LanternBird_Character_BP.LanternBird_Character_BP'"
    __FEROX = "Blueprint'/Game/Genesis/Dinos/Shapeshifter/Shapeshifter_Small/Shapeshifter_Small_Character_BP.Shapeshifter_Small_Character_BP'"
    __FEROX_LARGE = "Blueprint'/Game/Genesis/Dinos/Shapeshifter/Shapeshifter_Large/Shapeshifter_Large_Character_BP.Shapeshifter_Large_Character_BP'"
    __FIRE_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_Fire.Wyvern_Character_BP_Fire'"
    __FOREST_WYVERN = "Blueprint'/Game/Extinction/Dinos/ForestKaiju/Minion/Wyvern_Character_BP_Fire_Minion.Wyvern_Character_BP_Fire_Minion'"
    __GACHA = "Blueprint'/Game/Extinction/Dinos/Gacha/Gacha_Character_BP.Gacha_Character_BP'"
    __GACHACLAUS = "Blueprint'/Game/Extinction/Dinos/Gacha/Gacha_Claus_Character_BP.Gacha_Claus_Character_BP'"
    __GASBAGS = "Blueprint'/Game/Extinction/Dinos/GasBag/GasBags_Character_BP.GasBags_Character_BP'"
    __GLOWBUG = "Blueprint'/Game/Aberration/Dinos/Lightbug/Lightbug_Character_BaseBP.Lightbug_Character_BaseBP'"
    __GLOWTAIL = "Blueprint'/Game/Aberration/Dinos/LanternLizard/LanternLizard_Character_BP.LanternLizard_Character_BP'"
    __GRIFFIN = "Blueprint'/Game/PrimalEarth/Dinos/Griffin/Griffin_Character_BP.Griffin_Character_BP'"
    __ICE_GOLEM = "Blueprint'/Game/PrimalEarth/Dinos/IceGolem/IceGolem_Character_BP.IceGolem_Character_BP'"
    __ICE_WYVERN = "Blueprint'/Game/Mods/Ragnarok/Custom_Assets/Dinos/Wyvern/Ice_Wyvern/Ragnarok_Wyvern_Override_Ice.Ragnarok_Wyvern_Override_Ice'"
    __INSECT_SWARM = "Blueprint'/Game/Genesis/Dinos/Swarms/InsectSwarmChar_BP.InsectSwarmChar_BP'"
    __KARKINOS = "Blueprint'/Game/Aberration/Dinos/Crab/Crab_Character_BP.Crab_Character_BP'"
    __LIGHTNING_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_Lightning.Wyvern_Character_BP_Lightning'"
    __MACROPHAGE = "Blueprint'/Game/Genesis2/Dinos/Macrophage/Macrophage_Swarm_Character.Macrophage_Swarm_Character'"
    __MAEWING = "Blueprint'/Game/Genesis2/Dinos/MilkGlider/MilkGlider_Character_BP.MilkGlider_Character_BP'"
    __MAGMASAUR = "Blueprint'/Game/Genesis/Dinos/Cherufe/Cherufe_Character_BP.Cherufe_Character_BP'"
    __MANAGARMR = "Blueprint'/Game/Extinction/Dinos/IceJumper/IceJumper_Character_BP.IceJumper_Character_BP'"
    __MEGA_MEK = "Blueprint'/Game/Extinction/Dinos/Mek/MegaMek_Character_BP.MegaMek_Character_BP'"
    __MEGACHELON = "Blueprint'/Game/Genesis/Dinos/GiantTurtle/GiantTurtle_Character_BP.GiantTurtle_Character_BP'"
    __MEK = "Blueprint'/Game/Extinction/Dinos/Mek/Mek_Character_BP.Mek_Character_BP'"
    __NAMELESS = "Blueprint'/Game/Aberration/Dinos/ChupaCabra/ChupaCabra_Character_BP.ChupaCabra_Character_BP'"
    __NOGLIN = "Blueprint'/Game/Genesis2/Dinos/BrainSlug/BrainSlug_Character_BP.BrainSlug_Character_BP'"
    __PARAKEET_FISH_SCHOOL = "Blueprint'/Game/Genesis/Dinos/Swarms/MicrobeSwarmChar_BP.MicrobeSwarmChar_BP'"
    __PHOENIX = "Blueprint'/Game/ScorchedEarth/Dinos/Phoenix/Phoenix_Character_BP.Phoenix_Character_BP'"
    __POISON_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_Poison.Wyvern_Character_BP_Poison'"
    __RAVAGER = "Blueprint'/Game/Aberration/Dinos/CaveWolf/CaveWolf_Character_BP.CaveWolf_Character_BP'"
    __REAPER_KING = "Blueprint'/Game/Aberration/Dinos/Nameless/Xenomorph_Character_BP_Male.Xenomorph_Character_BP_Male'"
    __REAPER_KING_TAMED = "Blueprint'/Game/Aberration/Dinos/Nameless/Xenomorph_Character_BP_Male_Tamed.Xenomorph_Character_BP_Male_Tamed'"
    __REAPER_PRINCE = "Blueprint'/Game/Aberration/Dinos/Nameless/Xenomorph_Character_BP_Male_InitialBuryOnly_Adolescent.Xenomorph_Character_BP_Male_InitialBuryOnly_Adolescent'"
    __REAPER_QUEEN = "Blueprint'/Game/Aberration/Dinos/Nameless/Xenomorph_Character_BP_Female.Xenomorph_Character_BP_Female'"
    __ROCK_DRAKE = "Blueprint'/Game/Aberration/Dinos/RockDrake/RockDrake_Character_BP.RockDrake_Character_BP'"
    __ROCK_ELEMENTAL = "Blueprint'/Game/ScorchedEarth/Dinos/RockGolem/RockGolem_Character_BP.RockGolem_Character_BP'"
    __ROLL_RAT = "Blueprint'/Game/Aberration/Dinos/MoleRat/MoleRat_Character_BP.MoleRat_Character_BP'"
    __RUBBLE_GOLEM = "Blueprint'/Game/ScorchedEarth/Dinos/RockGolem/RubbleGolem_Character_BP.RubbleGolem_Character_BP'"
    __SCOUT = "Blueprint'/Game/Extinction/Dinos/Scout/Scout_Character_BP.Scout_Character_BP'"
    __SEEKER = "Blueprint'/Game/Aberration/Dinos/Pteroteuthis/Pteroteuthis_Char_BP.Pteroteuthis_Char_BP'"
    __SHADOWMANE = "Blueprint'/Game/Genesis2/Dinos/LionfishLion/LionfishLion_Character_BP.LionfishLion_Character_BP'"
    __SHINEHORN = "Blueprint'/Game/Aberration/Dinos/LanternGoat/LanternGoat_Character_BP.LanternGoat_Character_BP'"
    __SUMMONER = "Blueprint'/Game/Genesis2/Dinos/Summoner/Summoner_Character_BP.Summoner_Character_BP'"
    __TROPICAL_CRYSTAL_WYVERN = "Blueprint'/Game/PrimalEarth/Dinos/CrystalWyvern/CrystalWyvern_Character_BP_WS.CrystalWyvern_Character_BP_WS'"
    __VELONASAUR = "Blueprint'/Game/Extinction/Dinos/Spindles/Spindles_Character_BP.Spindles_Character_BP'"
    __WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_Base.Wyvern_Character_BP_Base'"
    __ABERRANT_ANGLERFISH = "Blueprint'/Game/PrimalEarth/Dinos/Anglerfish/Angler_Character_BP_Aberrant.Angler_Character_BP_Aberrant'"
    __ABERRANT_COELACANTH = "Blueprint'/Game/PrimalEarth/Dinos/Coelacanth/Coel_Character_BP_Aberrant.Coel_Character_BP_Aberrant'"
    __ABERRANT_ELECTROPHORUS = "Blueprint'/Game/PrimalEarth/Dinos/Eel/Eel_Character_BP_Aberrant.Eel_Character_BP_Aberrant'"
    __ABERRANT_MANTA = "Blueprint'/Game/PrimalEarth/Dinos/Manta/Manta_Character_BP_Aberrant.Manta_Character_BP_Aberrant'"
    __ABERRANT_PIRANHA = "Blueprint'/Game/PrimalEarth/Dinos/Piranha/Piranha_Character_BP_Aberrant.Piranha_Character_BP_Aberrant'"
    __ABERRANT_SABERTOOTH_SALMON = "Blueprint'/Game/PrimalEarth/Dinos/Salmon/Salmon_Character_Aberrant.Salmon_Character_Aberrant'"
    __ANGLERFISH = "Blueprint'/Game/PrimalEarth/Dinos/Anglerfish/Angler_Character_BP.Angler_Character_BP'"
    __COELACANTH = "Blueprint'/Game/PrimalEarth/Dinos/Coelacanth/Coel_Character_BP.Coel_Character_BP'"
    __DUNKLEOSTEUS = "Blueprint'/Game/PrimalEarth/Dinos/Dunkleosteus/Dunkle_Character_BP.Dunkle_Character_BP'"
    __ELECTROPHORUS = "Blueprint'/Game/PrimalEarth/Dinos/Eel/Eel_Character_BP.Eel_Character_BP'"
    __LAMPREY = "Blueprint'/Game/Aberration/Dinos/Lamprey/Lamprey_Character.Lamprey_Character'"
    __LEEDSICHTHYS = "Blueprint'/Game/PrimalEarth/Dinos/Leedsichthys/Leedsichthys_Character_BP.Leedsichthys_Character_BP'"
    __MANTA = "Blueprint'/Game/PrimalEarth/Dinos/Manta/Manta_Character_BP.Manta_Character_BP'"
    __MEGALODON = "Blueprint'/Game/PrimalEarth/Dinos/Megalodon/Megalodon_Character_BP.Megalodon_Character_BP'"
    __PIRANHA = "Blueprint'/Game/PrimalEarth/Dinos/Piranha/Piranha_Character_BP.Piranha_Character_BP'"
    __SABERTOOTH_SALMON = "Blueprint'/Game/PrimalEarth/Dinos/Salmon/Salmon_Character_BP.Salmon_Character_BP'"
    __ABERRANT_ACHATINA = "Blueprint'/Game/PrimalEarth/Dinos/Achatina/Achatina_Character_BP_Aberrant.Achatina_Character_BP_Aberrant'"
    __ABERRANT_ARANEO = "Blueprint'/Game/PrimalEarth/Dinos/Spider-Small/SpiderS_Character_BP_Aberrant.SpiderS_Character_BP_Aberrant'"
    __ABERRANT_ARTHROPLUERA = "Blueprint'/Game/PrimalEarth/Dinos/Arthropluera/Arthro_Character_BP_Aberrant.Arthro_Character_BP_Aberrant'"
    __ABERRANT_CNIDARIA = "Blueprint'/Game/PrimalEarth/Dinos/Cnidaria/Cnidaria_Character_BP_Aberrant.Cnidaria_Character_BP_Aberrant'"
    __ABERRANT_DUNG_BEETLE = "Blueprint'/Game/PrimalEarth/Dinos/DungBeetle/DungBeetle_Character_BP_Aberrant.DungBeetle_Character_BP_Aberrant'"
    __ABERRANT_MEGANEURA = "Blueprint'/Game/PrimalEarth/Dinos/Dragonfly/Dragonfly_Character_BP_Aberrant.Dragonfly_Character_BP_Aberrant'"
    __ABERRANT_PULMONOSCORPIUS = "Blueprint'/Game/PrimalEarth/Dinos/Scorpion/Scorpion_Character_BP_Aberrant.Scorpion_Character_BP_Aberrant'"
    __ABERRANT_TRILOBITE = "Blueprint'/Game/PrimalEarth/Dinos/Trilobite/Trilobite_Character_Aberrant.Trilobite_Character_Aberrant'"
    __ACHATINA = "Blueprint'/Game/PrimalEarth/Dinos/Achatina/Achatina_Character_BP.Achatina_Character_BP'"
    __AMMONITE = "Blueprint'/Game/PrimalEarth/Dinos/Ammonite/Ammonite_Character.Ammonite_Character'"
    __ARANEO = "Blueprint'/Game/PrimalEarth/Dinos/Spider-Small/SpiderS_Character_BP.SpiderS_Character_BP'"
    __ARTHROPLUERA = "Blueprint'/Game/PrimalEarth/Dinos/Arthropluera/Arthro_Character_BP.Arthro_Character_BP'"
    __CNIDARIA = "Blueprint'/Game/PrimalEarth/Dinos/Cnidaria/Cnidaria_Character_BP.Cnidaria_Character_BP'"
    __CORRUPTED_ARTHROPLUERA = "Blueprint'/Game/Extinction/Dinos/Corrupt/Arthropluera/Arthro_Character_BP_Corrupt.Arthro_Character_BP_Corrupt'"
    __DEATHWORM = "Blueprint'/Game/ScorchedEarth/Dinos/DeathWorm/DeathWorm_Character_BP.DeathWorm_Character_BP'"
    __DISEASED_LEECH = "Blueprint'/Game/PrimalEarth/Dinos/Leech/Leech_Character_Diseased.Leech_Character_Diseased'"
    __DUNG_BEETLE = "Blueprint'/Game/PrimalEarth/Dinos/DungBeetle/DungBeetle_Character_BP.DungBeetle_Character_BP'"
    __EURYPTERID = "Blueprint'/Game/PrimalEarth/Dinos/Eurypterid/Euryp_Character.Euryp_Character'"
    __GIANT_BEE = "Blueprint'/Game/PrimalEarth/Dinos/Bee/Bee_Character_BP.Bee_Character_BP'"
    __GIANT_WORKER_BEE = "Blueprint'/Game/Mods/CrystalIsles/Assets/Dinos/HoneyBee/HoneyBee_Character_BP.HoneyBee_Character_BP'"
    __JUG_BUG = "Blueprint'/Game/ScorchedEarth/Dinos/Jugbug/JugBug_Character_BaseBP.JugBug_Character_BaseBP'"
    __LEECH = "Blueprint'/Game/PrimalEarth/Dinos/Leech/Leech_Character.Leech_Character'"
    __LYMANTRIA = "Blueprint'/Game/ScorchedEarth/Dinos/Moth/Moth_Character_BP.Moth_Character_BP'"
    __MANTIS = "Blueprint'/Game/ScorchedEarth/Dinos/Mantis/Mantis_Character_BP.Mantis_Character_BP'"
    __MEGANEURA = "Blueprint'/Game/PrimalEarth/Dinos/Dragonfly/Dragonfly_Character_BP.Dragonfly_Character_BP'"
    __OIL_JUG_BUG = "Blueprint'/Game/ScorchedEarth/Dinos/Jugbug/Jugbug_Oil_Character_BP.Jugbug_Oil_Character_BP'"
    __PULMONOSCORPIUS = "Blueprint'/Game/PrimalEarth/Dinos/Scorpion/Scorpion_Character_BP.Scorpion_Character_BP'"
    __TITANOMYRMA = "Blueprint'/Game/PrimalEarth/Dinos/Ant/Ant_Character_BP.Ant_Character_BP'"
    __TITANOMYRMA = "Blueprint'/Game/PrimalEarth/Dinos/Ant/FlyingAnt_Character_BP.FlyingAnt_Character_BP'"
    __TRILOBITE = "Blueprint'/Game/PrimalEarth/Dinos/Trilobite/Trilobite_Character.Trilobite_Character'"
    __TUSOTEUTHIS = "Blueprint'/Game/PrimalEarth/Dinos/Tusoteuthis/Tusoteuthis_Character_BP.Tusoteuthis_Character_BP'"
    __WATER_JUG_BUG = "Blueprint'/Game/ScorchedEarth/Dinos/Jugbug/Jugbug_Water_Character_BP.Jugbug_Water_Character_BP'"
    __MALFUNCTIONED_TEK_GIGANOTOSAURUS = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Gauntlet/Lunar/BionicGigant_Character_BP_Malfunctioned_Gauntlet.BionicGigant_Character_BP_Malfunctioned_Gauntlet'"
    __MALFUNCTIONED_TEK_GIGANOTOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Giganotosaurus/BionicGigant_Character_BP_Malfunctioned.BionicGigant_Character_BP_Malfunctioned'"
    __MALFUNCTIONED_TEK_PARASAUR = "Blueprint'/Game/PrimalEarth/Dinos/Para/BionicPara_Character_BP_Malfunctioned.BionicPara_Character_BP_Malfunctioned'"
    __MALFUNCTIONED_TEK_QUETZAL = "Blueprint'/Game/PrimalEarth/Dinos/Quetzalcoatlus/BionicQuetz_Character_BP_Malfunctioned.BionicQuetz_Character_BP_Malfunctioned'"
    __MALFUNCTIONED_TEK_RAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Raptor/BionicRaptor_Character_BP_Malfunctioned.BionicRaptor_Character_BP_Malfunctioned'"
    __MALFUNCTIONED_TEK_REX = "Blueprint'/Game/PrimalEarth/Dinos/Rex/BionicRex_Character_BP_Malfunctioned.BionicRex_Character_BP_Malfunctioned'"
    __MALFUNCTIONED_TEK_STEGOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Stego/BionicStego_Character_BP_Malfunctioned.BionicStego_Character_BP_Malfunctioned'"
    __MALFUNCTIONED_TEK_TRICERATOPS = "Blueprint'/Game/PrimalEarth/Dinos/Trike/BionicTrike_Character_BP_Malfunctioned.BionicTrike_Character_BP_Malfunctioned'"
    __MOEDER_ALPHA = "Blueprint'/Game/PrimalEarth/Dinos/Direbear/Direbear_Character_BP_Aberrant.Direbear_Character_BP_Aberrant'"
    __ABERRANT_EQUUS = "Blueprint'/Game/PrimalEarth/Dinos/Equus/Equus_Character_BP_Aberrant.Equus_Character_BP_Aberrant'"
    __ABERRANT_GIGANTOPITHECUS = "Blueprint'/Game/PrimalEarth/Dinos/Bigfoot/Bigfoot_Character_BP_Aberrant.Bigfoot_Character_BP_Aberrant'"
    __ABERRANT_OTTER = "Blueprint'/Game/PrimalEarth/Dinos/Otter/Otter_Character_BP_Aberrant.Otter_Character_BP_Aberrant'"
    __ABERRANT_OVIS = "Blueprint'/Game/PrimalEarth/Dinos/Sheep/Sheep_Character_BP_Aberrant.Sheep_Character_BP_Aberrant'"
    __ABERRANT_PARACERATHERIUM = "Blueprint'/Game/PrimalEarth/Dinos/Paraceratherium/Paracer_Character_BP_Aberrant.Paracer_Character_BP_Aberrant'"
    __BASILOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Basilosaurus/Basilosaurus_Character_BP.Basilosaurus_Character_BP'"
    __CASTOROIDES = "Blueprint'/Game/PrimalEarth/Dinos/Beaver/Beaver_Character_BP.Beaver_Character_BP'"
    __CHALICOTHERIUM = "Blueprint'/Game/PrimalEarth/Dinos/Chalicotherium/Chalico_Character_BP.Chalico_Character_BP'"
    __CORRUPTED_AVATAR = "Blueprint'/Game/Genesis/Dinos/Bots/Bot_Character_BP.Bot_Character_BP'"
    __CORRUPTED_CHALICOTHERIUM = "Blueprint'/Game/Extinction/Dinos/Corrupt/Chalicotherium/Chalico_Character_BP_Corrupt.Chalico_Character_BP_Corrupt'"
    __CORRUPTED_PARACERATHERIUM = "Blueprint'/Game/Extinction/Dinos/Corrupt/Paraceratherium/Paracer_Character_BP_Corrupt.Paracer_Character_BP_Corrupt'"
    __DAEODON = "Blueprint'/Game/PrimalEarth/Dinos/Daeodon/Daeodon_Character_BP.Daeodon_Character_BP'"
    __DIRE_BEAR = "Blueprint'/Game/PrimalEarth/Dinos/Direbear/Direbear_Character_BP.Direbear_Character_BP'"
    __DIREWOLF = "Blueprint'/Game/PrimalEarth/Dinos/Direwolf/Direwolf_Character_BP.Direwolf_Character_BP'"
    __DOEDICURUS = "Blueprint'/Game/PrimalEarth/Dinos/Doedicurus/Doed_Character_BP.Doed_Character_BP'"
    __EQUUS = "Blueprint'/Game/PrimalEarth/Dinos/Equus/Equus_Character_BP.Equus_Character_BP'"
    __GIGANTOPITHECUS = "Blueprint'/Game/PrimalEarth/Dinos/Bigfoot/Bigfoot_Character_BP.Bigfoot_Character_BP'"
    __HUMAN_FEMALE = "Blueprint'/Game/PrimalEarth/CoreBlueprints/PlayerPawnTest_Female.PlayerPawnTest_Female'"
    __HUMAN_MALE = "Blueprint'/Game/PrimalEarth/CoreBlueprints/PlayerPawnTest_Male.PlayerPawnTest_Male'"
    __HYAENODON = "Blueprint'/Game/PrimalEarth/Dinos/Hyaenodon/Hyaenodon_Character_BP.Hyaenodon_Character_BP'"
    __JERBOA = "Blueprint'/Game/ScorchedEarth/Dinos/Jerboa/Jerboa_Character_BP.Jerboa_Character_BP'"
    __MAMMOTH = "Blueprint'/Game/PrimalEarth/Dinos/Mammoth/Mammoth_Character_BP.Mammoth_Character_BP'"
    __MEGALOCEROS = "Blueprint'/Game/PrimalEarth/Dinos/Stag/Stag_Character_BP.Stag_Character_BP'"
    __MEGATHERIUM = "Blueprint'/Game/PrimalEarth/Dinos/Megatherium/Megatherium_Character_BP.Megatherium_Character_BP'"
    __MESOPITHECUS = "Blueprint'/Game/PrimalEarth/Dinos/Monkey/Monkey_Character_BP.Monkey_Character_BP'"
    __ONYCHONYCTERIS = "Blueprint'/Game/PrimalEarth/Dinos/Bat/Bat_Character_BP.Bat_Character_BP'"
    __OTTER = "Blueprint'/Game/PrimalEarth/Dinos/Otter/Otter_Character_BP.Otter_Character_BP'"
    __OVIS = "Blueprint'/Game/PrimalEarth/Dinos/Sheep/Sheep_Character_BP.Sheep_Character_BP'"
    __PARACERATHERIUM = "Blueprint'/Game/PrimalEarth/Dinos/Paraceratherium/Paracer_Character_BP.Paracer_Character_BP'"
    __PHIOMIA = "Blueprint'/Game/PrimalEarth/Dinos/Phiomia/Phiomia_Character_BP.Phiomia_Character_BP'"
    __PROCOPTODON = "Blueprint'/Game/PrimalEarth/Dinos/Procoptodon/Procoptodon_Character_BP.Procoptodon_Character_BP'"
    __SABERTOOTH = "Blueprint'/Game/PrimalEarth/Dinos/Saber/Saber_Character_BP.Saber_Character_BP'"
    __THYLACOLEO = "Blueprint'/Game/PrimalEarth/Dinos/Thylacoleo/Thylacoleo_Character_BP.Thylacoleo_Character_BP'"
    __UNICORN = "Blueprint'/Game/PrimalEarth/Dinos/Equus/Equus_Character_BP_Unicorn.Equus_Character_BP_Unicorn'"
    __WOOLLY_RHINO = "Blueprint'/Game/PrimalEarth/Dinos/WoollyRhino/Rhino_Character_BP.Rhino_Character_BP'"
    __YETI = "Blueprint'/Game/PrimalEarth/Dinos/Bigfoot/Yeti_Character_BP.Yeti_Character_BP'"
    __TEK_STRYDER = "Blueprint'/Game/Genesis2/Dinos/TekStrider/TekStrider_Character_BP.TekStrider_Character_BP'"
    __VOIDWYRM = "Blueprint'/Game/Genesis2/Dinos/TekWyvern/TekWyvern_Character_BP.TekWyvern_Character_BP'"
    __R_ALLOSAURUS = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Allo_Character_BP_Rockwell.Allo_Character_BP_Rockwell'"
    __R_BRONTOSAURUS = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Sauropod_Character_BP_Rockwell.Sauropod_Character_BP_Rockwell'"
    __R_CARBONEMYS = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Turtle_Character_BP_Rockwell.Turtle_Character_BP_Rockwell'"
    __R_CARNOTAURUS = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Carno_Character_BP_Rockwell.Carno_Character_BP_Rockwell'"
    __R_DAEODON = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Daeodon_Character_BP_Eden.Daeodon_Character_BP_Eden'"
    __R_DILOPHOSAUR = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Dilo_Character_BP_Rockwell.Dilo_Character_BP_Rockwell'"
    __R_DIRE_BEAR = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Direbear_Character_BP_Rockwell.Direbear_Character_BP_Rockwell'"
    __R_DIREWOLF = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Direwolf_Character_BP_Eden.Direwolf_Character_BP_Eden'"
    __R_EQUUS = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Equus_Character_BP_Eden.Equus_Character_BP_Eden'"
    __R_GASBAGS = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/GasBags_Character_BP_Eden.GasBags_Character_BP_Eden'"
    __R_GIGANOTOSAURUS = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Gigant_Character_BP_Rockwell.Gigant_Character_BP_Rockwell'"
    __R_MEGATHERIUM = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Megatherium_Character_BP_Eden.Megatherium_Character_BP_Eden'"
    __R_PARASAUR = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Para_Character_BP_Eden.Para_Character_BP_Eden'"
    __R_PROCOPTODON = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Procoptodon_Character_BP_Eden.Procoptodon_Character_BP_Eden'"
    __R_QUETZAL = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Quetz_Character_BP_Rockwell.Quetz_Character_BP_Rockwell'"
    __R_REAPER_KING = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Xenomorph_Character_BP_Male_Gen2.Xenomorph_Character_BP_Male_Gen2'"
    __R_REAPER_KING_TAMED = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Xenomorph_Character_BP_Male_Tamed_Gen2.Xenomorph_Character_BP_Male_Tamed_Gen2'"
    __R_REAPER_QUEEN = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Xenomorph_Character_BP_Female_Gen2.Xenomorph_Character_BP_Female_Gen2'"
    __R_SNOW_OWL = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Owl_Character_BP_Eden.Owl_Character_BP_Eden'"
    __R_THYLACOLEO = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Thylacoleo_Character_BP_Eden.Thylacoleo_Character_BP_Eden'"
    __R_VELONASAUR = "Blueprint'/Game/Genesis2/Dinos/BiomeVariants/Spindles_Character_BP_Rockwell.Spindles_Character_BP_Rockwell'"
    __ABERRANT_BEELZEBUFO = "Blueprint'/Game/PrimalEarth/Dinos/Toad/Toad_Character_BP_Aberrant.Toad_Character_BP_Aberrant'"
    __ABERRANT_CARBONEMYS = "Blueprint'/Game/PrimalEarth/Dinos/Turtle/Turtle_Character_BP_Aberrant.Turtle_Character_BP_Aberrant'"
    __ABERRANT_MEGALANIA = "Blueprint'/Game/PrimalEarth/Dinos/Megalania/Megalania_Character_BP_Aberrant.Megalania_Character_BP_Aberrant'"
    __ABERRANT_SARCO = "Blueprint'/Game/PrimalEarth/Dinos/Sarco/Sarco_Character_BP_Aberrant.Sarco_Character_BP_Aberrant'"
    __ABERRANT_TITANOBOA = "Blueprint'/Game/PrimalEarth/Dinos/BoaFrill/BoaFrill_Character_BP_Aberrant.BoaFrill_Character_BP_Aberrant'"
    __BEELZEBUFO = "Blueprint'/Game/PrimalEarth/Dinos/Toad/Toad_Character_BP.Toad_Character_BP'"
    __CARBONEMYS = "Blueprint'/Game/PrimalEarth/Dinos/Turtle/Turtle_Character_BP.Turtle_Character_BP'"
    __ICHTHYOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Dolphin/Dolphin_Character_BP.Dolphin_Character_BP'"
    __KAPROSUCHUS = "Blueprint'/Game/PrimalEarth/Dinos/Kaprosuchus/Kaprosuchus_Character_BP.Kaprosuchus_Character_BP'"
    __LIOPLEURODON = "Blueprint'/Game/PrimalEarth/Dinos/Liopleurodon/Liopleurodon_Character_BP.Liopleurodon_Character_BP'"
    __MEGALANIA = "Blueprint'/Game/PrimalEarth/Dinos/Megalania/Megalania_Character_BP.Megalania_Character_BP'"
    __MOSASAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Mosasaurus/Mosa_Character_BP.Mosa_Character_BP'"
    __PLESIOSAUR = "Blueprint'/Game/PrimalEarth/Dinos/Plesiosaur/Plesiosaur_Character_BP.Plesiosaur_Character_BP'"
    __QUETZALCOATLUS = "Blueprint'/Game/PrimalEarth/Dinos/Quetzalcoatlus/Quetz_Character_BP.Quetz_Character_BP'"
    __SARCO = "Blueprint'/Game/PrimalEarth/Dinos/Sarco/Sarco_Character_BP.Sarco_Character_BP'"
    __TAPEJARA = "Blueprint'/Game/PrimalEarth/Dinos/Tapejara/Tapejara_Character_BP.Tapejara_Character_BP'"
    __THORNY_DRAGON = "Blueprint'/Game/ScorchedEarth/Dinos/SpineyLizard/SpineyLizard_Character_BP.SpineyLizard_Character_BP'"
    __TITANOBOA = "Blueprint'/Game/PrimalEarth/Dinos/BoaFrill/BoaFrill_Character_BP.BoaFrill_Character_BP'"
    __TROPEOGNATHUS = "Blueprint'/Game/PrimalEarth/Dinos/Tropeognathus/Tropeognathus_Character_BP.Tropeognathus_Character_BP'"
    __ABERRANT_MOSCHOPS = "Blueprint'/Game/PrimalEarth/Dinos/Moschops/Moschops_Character_BP_Aberrant.Moschops_Character_BP_Aberrant'"
    __ABERRANT_PURLOVIA = "Blueprint'/Game/PrimalEarth/Dinos/Purlovia/Purlovia_Character_BP_Aberrant.Purlovia_Character_BP_Aberrant'"
    __PURLOVIA = "Blueprint'/Game/PrimalEarth/Dinos/Purlovia/Purlovia_Character_BP.Purlovia_Character_BP'"
    __TEK_PARASAUR = "Blueprint'/Game/PrimalEarth/Dinos/Para/BionicPara_Character_BP.BionicPara_Character_BP'"
    __TEK_QUETZAL = "Blueprint'/Game/PrimalEarth/Dinos/Quetzalcoatlus/BionicQuetz_Character_BP.BionicQuetz_Character_BP'"
    __TEK_RAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Raptor/BionicRaptor_Character_BP.BionicRaptor_Character_BP'"
    __TEK_REX = "Blueprint'/Game/PrimalEarth/Dinos/Rex/BionicRex_Character_BP.BionicRex_Character_BP'"
    __TEK_STEGOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Stego/BionicStego_Character_BP.BionicStego_Character_BP'"
    __TEK_TRICERATOPS = "Blueprint'/Game/PrimalEarth/Dinos/Trike/BionicTrike_Character_BP.BionicTrike_Character_BP'"
    __EXO_MEK = "Blueprint'/Game/Genesis2/Dinos/Exosuit/Exosuit_Character_BP.Exosuit_Character_BP'"
    __GOLDEN_STRIPED_MEGALODON = "Blueprint'/Game/Genesis/Dinos/MissionVariants/Retrieve/Ocean/Ocean_Megalodon_Character_BP_Retrieve.Ocean_Megalodon_Character_BP_Retrieve'"
    __X_ALLOSAURUS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Volcano_Allosaurus/Volcano_Allo_Character_BP.Volcano_Allo_Character_BP'"
    __X_ANKYLOSAURUS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Volcano_Ankylosaurus/Volcano_Ankylo_Character_BP.Volcano_Ankylo_Character_BP'"
    __X_ARGENTAVIS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Snow_Argentavis/Snow_Argent_Character_BP.Snow_Argent_Character_BP'"
    __X_BASILOSAURUS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Ocean_Basilosaurus/Ocean_Basilosaurus_Character_BP.Ocean_Basilosaurus_Character_BP'"
    __X_DUNKLEOSTEUS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Ocean_Dunkleosteus/Ocean_Dunkle_Character_BP.Ocean_Dunkle_Character_BP'"
    __X_ICHTHYOSAURUS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Ocean_Dolphin/Ocean_Dolphin_Character_BP.Ocean_Dolphin_Character_BP'"
    __X_MEGALODON = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Ocean_Megalodon/Ocean_Megalodon_Character_BP.Ocean_Megalodon_Character_BP'"
    __X_MOSASAURUS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Ocean_Mosasaurus/Ocean_Mosa_Character_BP.Ocean_Mosa_Character_BP'"
    __X_OTTER = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Snow_Otter/Snow_Otter_Character_BP.Snow_Otter_Character_BP'"
    __X_PARACERATHERIUM = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/BogParaceratherium/Bog_Paracer_Character_BP.Bog_Paracer_Character_BP'"
    __X_PARASAUR = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/BogPara/Bog_Para_Character_BP.Bog_Para_Character_BP'"
    __X_RAPTOR = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Bog_Raptor/Bog_Raptor_Character_BP.Bog_Raptor_Character_BP'"
    __X_REX = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Volcano_Rex/Volcano_Rex_Character_BP.Volcano_Rex_Character_BP'"
    __X_ROCK_ELEMENTAL = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Lava_Golem/Volcano_Golem_Character_BP.Volcano_Golem_Character_BP'"
    __X_SABERTOOTH = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Snow_Saber/Snow_Saber_Character_BP.Snow_Saber_Character_BP'"
    __X_SABERTOOTH_SALMON = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Lunar_Salmon/Lunar_Salmon_Character_BP.Lunar_Salmon_Character_BP'"
    __X_SPINO = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Bog_Spino/Bog_Spino_Character_BP.Bog_Spino_Character_BP'"
    __X_TAPEJARA = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Bog_Tapejara/Bog_Tapejara_Character_BP.Bog_Tapejara_Character_BP'"
    __X_TRICERATOPS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Volcano_Trike/Volcano_Trike_Character_BP.Volcano_Trike_Character_BP'"
    __X_WOOLLY_RHINO = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Snow_WoollyRhino/Snow_Rhino_Character_BP.Snow_Rhino_Character_BP'"
    __X_YUTYRANNUS = "Blueprint'/Game/Genesis/Dinos/BiomeVariants/Snow_Yutyrannus/Snow_Yutyrannus_Character_BP.Snow_Yutyrannus_Character_BP'"

    ABERRANT_DIPLOCAULUS = _Creature(__ABERRANT_DIPLOCAULUS)
    DIPLOCAULUS = _Creature(__DIPLOCAULUS)
    ABERRANT_DODO = _Creature(__ABERRANT_DODO)
    ARCHAEOPTERYX = _Creature(__ARCHAEOPTERYX)
    ARGENTAVIS = _Creature(__ARGENTAVIS)
    DODO = _Creature(__DODO)
    HESPERORNIS = _Creature(__HESPERORNIS)
    ICHTHYORNIS = _Creature(__ICHTHYORNIS)
    KAIRUKU = _Creature(__KAIRUKU)
    PELAGORNIS = _Creature(__PELAGORNIS)
    SNOW_OWL = _Creature(__SNOW_OWL)
    TERROR_BIRD = _Creature(__TERROR_BIRD)
    VULTURE = _Creature(__VULTURE)
    BRUTE_ARANEO = _Creature(__BRUTE_ARANEO)
    BRUTE_ASTROCETUS = _Creature(__BRUTE_ASTROCETUS)
    BRUTE_BASILOSAURUS = _Creature(__BRUTE_BASILOSAURUS)
    BRUTE_BLOODSTALKER = _Creature(__BRUTE_BLOODSTALKER)
    BRUTE_FEROX = _Creature(__BRUTE_FEROX)
    BRUTE_FIRE_WYVERN = _Creature(__BRUTE_FIRE_WYVERN)
    BRUTE_LEEDSICHTHYS = _Creature(__BRUTE_LEEDSICHTHYS)
    BRUTE_MAGMASAUR = _Creature(__BRUTE_MAGMASAUR)
    BRUTE_MALFUNCTIONED_TEK_GIGANOTOSAURUS = _Creature(__BRUTE_MALFUNCTIONED_TEK_GIGANOTOSAURUS)
    BRUTE_MALFUNCTIONED_TEK_REX = _Creature(__BRUTE_MALFUNCTIONED_TEK_REX)
    BRUTE_MAMMOTH = _Creature(__BRUTE_MAMMOTH)
    BRUTE_MEGALOCEROS = _Creature(__BRUTE_MEGALOCEROS)
    BRUTE_PLESIOSAUR = _Creature(__BRUTE_PLESIOSAUR)
    BRUTE_REAPER_KING = _Creature(__BRUTE_REAPER_KING)
    BRUTE_SARCO = _Creature(__BRUTE_SARCO)
    BRUTE_SEEKER = _Creature(__BRUTE_SEEKER)
    BRUTE_TUSOTEUTHIS = _Creature(__BRUTE_TUSOTEUTHIS)
    BRUTE_X_ALLOSAURUS = _Creature(__BRUTE_X_ALLOSAURUS)
    BRUTE_X_MEGALODON = _Creature(__BRUTE_X_MEGALODON)
    BRUTE_X_MOSASAURUS = _Creature(__BRUTE_X_MOSASAURUS)
    BRUTE_X_RAPTOR = _Creature(__BRUTE_X_RAPTOR)
    BRUTE_X_REX = _Creature(__BRUTE_X_REX)
    BRUTE_X_ROCK_ELEMENTAL = _Creature(__BRUTE_X_ROCK_ELEMENTAL)
    BRUTE_X_SPINO = _Creature(__BRUTE_X_SPINO)
    BRUTE_X_YUTYRANNUS = _Creature(__BRUTE_X_YUTYRANNUS)
    GOLDEN_STRIPED_BRUTE_MEGALODON = _Creature(__GOLDEN_STRIPED_BRUTE_MEGALODON)
    INJURED_BRUTE_REAPER_KING = _Creature(__INJURED_BRUTE_REAPER_KING)
    ABERRANT_ANKYLOSAURUS = _Creature(__ABERRANT_ANKYLOSAURUS)
    ABERRANT_BARYONYX = _Creature(__ABERRANT_BARYONYX)
    ABERRANT_CARNOTAURUS = _Creature(__ABERRANT_CARNOTAURUS)
    ABERRANT_DIMETRODON = _Creature(__ABERRANT_DIMETRODON)
    ABERRANT_DIMORPHODON = _Creature(__ABERRANT_DIMORPHODON)
    ABERRANT_DIPLODOCUS = _Creature(__ABERRANT_DIPLODOCUS)
    ABERRANT_DOEDICURUS = _Creature(__ABERRANT_DOEDICURUS)
    ABERRANT_IGUANODON = _Creature(__ABERRANT_IGUANODON)
    ABERRANT_LYSTROSAURUS = _Creature(__ABERRANT_LYSTROSAURUS)
    ABERRANT_MEGALOSAURUS = _Creature(__ABERRANT_MEGALOSAURUS)
    ABERRANT_PARASAUR = _Creature(__ABERRANT_PARASAUR)
    ABERRANT_RAPTOR = _Creature(__ABERRANT_RAPTOR)
    ABERRANT_SPINO = _Creature(__ABERRANT_SPINO)
    ABERRANT_STEGOSAURUS = _Creature(__ABERRANT_STEGOSAURUS)
    ABERRANT_TRICERATOPS = _Creature(__ABERRANT_TRICERATOPS)
    ALLOSAURUS = _Creature(__ALLOSAURUS)
    ANKYLOSAURUS = _Creature(__ANKYLOSAURUS)
    BARYONYX = _Creature(__BARYONYX)
    BRONTOSAURUS = _Creature(__BRONTOSAURUS)
    CARNOTAURUS = _Creature(__CARNOTAURUS)
    COMPY = _Creature(__COMPY)
    CORRUPTED_CARNOTAURUS = _Creature(__CORRUPTED_CARNOTAURUS)
    CORRUPTED_DILOPHOSAUR = _Creature(__CORRUPTED_DILOPHOSAUR)
    CORRUPTED_DIMORPHODON = _Creature(__CORRUPTED_DIMORPHODON)
    CORRUPTED_GIGANOTOSAURUS = _Creature(__CORRUPTED_GIGANOTOSAURUS)
    CORRUPTED_PTERANODON = _Creature(__CORRUPTED_PTERANODON)
    CORRUPTED_RAPTOR = _Creature(__CORRUPTED_RAPTOR)
    CORRUPTED_REX = _Creature(__CORRUPTED_REX)
    CORRUPTED_SPINO = _Creature(__CORRUPTED_SPINO)
    CORRUPTED_STEGOSAURUS = _Creature(__CORRUPTED_STEGOSAURUS)
    CORRUPTED_TRICERATOPS = _Creature(__CORRUPTED_TRICERATOPS)
    DEINONYCHUS = _Creature(__DEINONYCHUS)
    DILOPHOSAUR = _Creature(__DILOPHOSAUR)
    DIMETRODON = _Creature(__DIMETRODON)
    DIMORPHODON = _Creature(__DIMORPHODON)
    DIPLODOCUS = _Creature(__DIPLODOCUS)
    ENRAGED_CORRUPTED_REX = _Creature(__ENRAGED_CORRUPTED_REX)
    ENRAGED_TRICERATOPS = _Creature(__ENRAGED_TRICERATOPS)
    GALLIMIMUS = _Creature(__GALLIMIMUS)
    GIGANOTOSAURUS = _Creature(__GIGANOTOSAURUS)
    IGUANODON = _Creature(__IGUANODON)
    KENTROSAURUS = _Creature(__KENTROSAURUS)
    LYSTROSAURUS = _Creature(__LYSTROSAURUS)
    MEGALOSAURUS = _Creature(__MEGALOSAURUS)
    MICRORAPTOR = _Creature(__MICRORAPTOR)
    MORELLATOPS = _Creature(__MORELLATOPS)
    MOSCHOPS = _Creature(__MOSCHOPS)
    OVIRAPTOR = _Creature(__OVIRAPTOR)
    PACHY = _Creature(__PACHY)
    PACHYRHINOSAURUS = _Creature(__PACHYRHINOSAURUS)
    PARASAUROLOPHUS = _Creature(__PARASAUROLOPHUS)
    PEGOMASTAX = _Creature(__PEGOMASTAX)
    PTERANODON = _Creature(__PTERANODON)
    RAPTOR = _Creature(__RAPTOR)
    REX = _Creature(__REX)
    SPINO = _Creature(__SPINO)
    STEGOSAURUS = _Creature(__STEGOSAURUS)
    THERIZINOSAUR = _Creature(__THERIZINOSAUR)
    TITANOSAUR = _Creature(__TITANOSAUR)
    TRICERATOPS = _Creature(__TRICERATOPS)
    TROODON = _Creature(__TROODON)
    YUTYRANNUS = _Creature(__YUTYRANNUS)
    ASTROCETUS = _Creature(__ASTROCETUS)
    ASTRODELPHIS = _Creature(__ASTRODELPHIS)
    BASILISK = _Creature(__BASILISK)
    BLOOD_CRYSTAL_WYVERN = _Creature(__BLOOD_CRYSTAL_WYVERN)
    BLOODSTALKER = _Creature(__BLOODSTALKER)
    BULBDOG = _Creature(__BULBDOG)
    CHALK_GOLEM = _Creature(__CHALK_GOLEM)
    CORRUPTED_REAPER_KING = _Creature(__CORRUPTED_REAPER_KING)
    CORRUPTED_ROCK_DRAKE = _Creature(__CORRUPTED_ROCK_DRAKE)
    CORRUPTED_WYVERN = _Creature(__CORRUPTED_WYVERN)
    DEFENSE_UNIT = _Creature(__DEFENSE_UNIT)
    EEL_MINION = _Creature(__EEL_MINION)
    EMBER_CRYSTAL_WYVERN = _Creature(__EMBER_CRYSTAL_WYVERN)
    ENFORCER = _Creature(__ENFORCER)
    FEATHERLIGHT = _Creature(__FEATHERLIGHT)
    FEROX = _Creature(__FEROX)
    FEROX_LARGE = _Creature(__FEROX_LARGE)
    FIRE_WYVERN = _Creature(__FIRE_WYVERN)
    FOREST_WYVERN = _Creature(__FOREST_WYVERN)
    GACHA = _Creature(__GACHA)
    GACHACLAUS = _Creature(__GACHACLAUS)
    GASBAGS = _Creature(__GASBAGS)
    GLOWBUG = _Creature(__GLOWBUG)
    GLOWTAIL = _Creature(__GLOWTAIL)
    GRIFFIN = _Creature(__GRIFFIN)
    ICE_GOLEM = _Creature(__ICE_GOLEM)
    ICE_WYVERN = _Creature(__ICE_WYVERN)
    INSECT_SWARM = _Creature(__INSECT_SWARM)
    KARKINOS = _Creature(__KARKINOS)
    LIGHTNING_WYVERN = _Creature(__LIGHTNING_WYVERN)
    MACROPHAGE = _Creature(__MACROPHAGE)
    MAEWING = _Creature(__MAEWING)
    MAGMASAUR = _Creature(__MAGMASAUR)
    MANAGARMR = _Creature(__MANAGARMR)
    MEGA_MEK = _Creature(__MEGA_MEK)
    MEGACHELON = _Creature(__MEGACHELON)
    MEK = _Creature(__MEK)
    NAMELESS = _Creature(__NAMELESS)
    NOGLIN = _Creature(__NOGLIN)
    PARAKEET_FISH_SCHOOL = _Creature(__PARAKEET_FISH_SCHOOL)
    PHOENIX = _Creature(__PHOENIX)
    POISON_WYVERN = _Creature(__POISON_WYVERN)
    RAVAGER = _Creature(__RAVAGER)
    REAPER_KING = _Creature(__REAPER_KING)
    REAPER_KING_TAMED = _Creature(__REAPER_KING_TAMED)
    REAPER_PRINCE = _Creature(__REAPER_PRINCE)
    REAPER_QUEEN = _Creature(__REAPER_QUEEN)
    ROCK_DRAKE = _Creature(__ROCK_DRAKE)
    ROCK_ELEMENTAL = _Creature(__ROCK_ELEMENTAL)
    ROLL_RAT = _Creature(__ROLL_RAT)
    RUBBLE_GOLEM = _Creature(__RUBBLE_GOLEM)
    SCOUT = _Creature(__SCOUT)
    SEEKER = _Creature(__SEEKER)
    SHADOWMANE = _Creature(__SHADOWMANE)
    SHINEHORN = _Creature(__SHINEHORN)
    SUMMONER = _Creature(__SUMMONER)
    TROPICAL_CRYSTAL_WYVERN = _Creature(__TROPICAL_CRYSTAL_WYVERN)
    VELONASAUR = _Creature(__VELONASAUR)
    WYVERN = _Creature(__WYVERN)
    ABERRANT_ANGLERFISH = _Creature(__ABERRANT_ANGLERFISH)
    ABERRANT_COELACANTH = _Creature(__ABERRANT_COELACANTH)
    ABERRANT_ELECTROPHORUS = _Creature(__ABERRANT_ELECTROPHORUS)
    ABERRANT_MANTA = _Creature(__ABERRANT_MANTA)
    ABERRANT_PIRANHA = _Creature(__ABERRANT_PIRANHA)
    ABERRANT_SABERTOOTH_SALMON = _Creature(__ABERRANT_SABERTOOTH_SALMON)
    ANGLERFISH = _Creature(__ANGLERFISH)
    COELACANTH = _Creature(__COELACANTH)
    DUNKLEOSTEUS = _Creature(__DUNKLEOSTEUS)
    ELECTROPHORUS = _Creature(__ELECTROPHORUS)
    LAMPREY = _Creature(__LAMPREY)
    LEEDSICHTHYS = _Creature(__LEEDSICHTHYS)
    MANTA = _Creature(__MANTA)
    MEGALODON = _Creature(__MEGALODON)
    PIRANHA = _Creature(__PIRANHA)
    SABERTOOTH_SALMON = _Creature(__SABERTOOTH_SALMON)
    ABERRANT_ACHATINA = _Creature(__ABERRANT_ACHATINA)
    ABERRANT_ARANEO = _Creature(__ABERRANT_ARANEO)
    ABERRANT_ARTHROPLUERA = _Creature(__ABERRANT_ARTHROPLUERA)
    ABERRANT_CNIDARIA = _Creature(__ABERRANT_CNIDARIA)
    ABERRANT_DUNG_BEETLE = _Creature(__ABERRANT_DUNG_BEETLE)
    ABERRANT_MEGANEURA = _Creature(__ABERRANT_MEGANEURA)
    ABERRANT_PULMONOSCORPIUS = _Creature(__ABERRANT_PULMONOSCORPIUS)
    ABERRANT_TRILOBITE = _Creature(__ABERRANT_TRILOBITE)
    ACHATINA = _Creature(__ACHATINA)
    AMMONITE = _Creature(__AMMONITE)
    ARANEO = _Creature(__ARANEO)
    ARTHROPLUERA = _Creature(__ARTHROPLUERA)
    CNIDARIA = _Creature(__CNIDARIA)
    CORRUPTED_ARTHROPLUERA = _Creature(__CORRUPTED_ARTHROPLUERA)
    DEATHWORM = _Creature(__DEATHWORM)
    DISEASED_LEECH = _Creature(__DISEASED_LEECH)
    DUNG_BEETLE = _Creature(__DUNG_BEETLE)
    EURYPTERID = _Creature(__EURYPTERID)
    GIANT_BEE = _Creature(__GIANT_BEE)
    GIANT_WORKER_BEE = _Creature(__GIANT_WORKER_BEE)
    JUG_BUG = _Creature(__JUG_BUG)
    LEECH = _Creature(__LEECH)
    LYMANTRIA = _Creature(__LYMANTRIA)
    MANTIS = _Creature(__MANTIS)
    MEGANEURA = _Creature(__MEGANEURA)
    OIL_JUG_BUG = _Creature(__OIL_JUG_BUG)
    PULMONOSCORPIUS = _Creature(__PULMONOSCORPIUS)
    TITANOMYRMA = _Creature(__TITANOMYRMA)
    TRILOBITE = _Creature(__TRILOBITE)
    TUSOTEUTHIS = _Creature(__TUSOTEUTHIS)
    WATER_JUG_BUG = _Creature(__WATER_JUG_BUG)
    MALFUNCTIONED_TEK_GIGANOTOSAURUS = _Creature(__MALFUNCTIONED_TEK_GIGANOTOSAURUS)
    MALFUNCTIONED_TEK_PARASAUR = _Creature(__MALFUNCTIONED_TEK_PARASAUR)
    MALFUNCTIONED_TEK_QUETZAL = _Creature(__MALFUNCTIONED_TEK_QUETZAL)
    MALFUNCTIONED_TEK_RAPTOR = _Creature(__MALFUNCTIONED_TEK_RAPTOR)
    MALFUNCTIONED_TEK_REX = _Creature(__MALFUNCTIONED_TEK_REX)
    MALFUNCTIONED_TEK_STEGOSAURUS = _Creature(__MALFUNCTIONED_TEK_STEGOSAURUS)
    MALFUNCTIONED_TEK_TRICERATOPS = _Creature(__MALFUNCTIONED_TEK_TRICERATOPS)
    MOEDER_ALPHA = _Creature(__MOEDER_ALPHA)
    ABERRANT_EQUUS = _Creature(__ABERRANT_EQUUS)
    ABERRANT_GIGANTOPITHECUS = _Creature(__ABERRANT_GIGANTOPITHECUS)
    ABERRANT_OTTER = _Creature(__ABERRANT_OTTER)
    ABERRANT_OVIS = _Creature(__ABERRANT_OVIS)
    ABERRANT_PARACERATHERIUM = _Creature(__ABERRANT_PARACERATHERIUM)
    BASILOSAURUS = _Creature(__BASILOSAURUS)
    CASTOROIDES = _Creature(__CASTOROIDES)
    CHALICOTHERIUM = _Creature(__CHALICOTHERIUM)
    CORRUPTED_AVATAR = _Creature(__CORRUPTED_AVATAR)
    CORRUPTED_CHALICOTHERIUM = _Creature(__CORRUPTED_CHALICOTHERIUM)
    CORRUPTED_PARACERATHERIUM = _Creature(__CORRUPTED_PARACERATHERIUM)
    DAEODON = _Creature(__DAEODON)
    DIRE_BEAR = _Creature(__DIRE_BEAR)
    DIREWOLF = _Creature(__DIREWOLF)
    DOEDICURUS = _Creature(__DOEDICURUS)
    EQUUS = _Creature(__EQUUS)
    GIGANTOPITHECUS = _Creature(__GIGANTOPITHECUS)
    HUMAN_FEMALE = _Creature(__HUMAN_FEMALE)
    HUMAN_MALE = _Creature(__HUMAN_MALE)
    HYAENODON = _Creature(__HYAENODON)
    JERBOA = _Creature(__JERBOA)
    MAMMOTH = _Creature(__MAMMOTH)
    MEGALOCEROS = _Creature(__MEGALOCEROS)
    MEGATHERIUM = _Creature(__MEGATHERIUM)
    MESOPITHECUS = _Creature(__MESOPITHECUS)
    ONYCHONYCTERIS = _Creature(__ONYCHONYCTERIS)
    OTTER = _Creature(__OTTER)
    OVIS = _Creature(__OVIS)
    PARACERATHERIUM = _Creature(__PARACERATHERIUM)
    PHIOMIA = _Creature(__PHIOMIA)
    PROCOPTODON = _Creature(__PROCOPTODON)
    SABERTOOTH = _Creature(__SABERTOOTH)
    THYLACOLEO = _Creature(__THYLACOLEO)
    UNICORN = _Creature(__UNICORN)
    WOOLLY_RHINO = _Creature(__WOOLLY_RHINO)
    YETI = _Creature(__YETI)
    TEK_STRYDER = _Creature(__TEK_STRYDER)
    VOIDWYRM = _Creature(__VOIDWYRM)
    R_ALLOSAURUS = _Creature(__R_ALLOSAURUS)
    R_BRONTOSAURUS = _Creature(__R_BRONTOSAURUS)
    R_CARBONEMYS = _Creature(__R_CARBONEMYS)
    R_CARNOTAURUS = _Creature(__R_CARNOTAURUS)
    R_DAEODON = _Creature(__R_DAEODON)
    R_DILOPHOSAUR = _Creature(__R_DILOPHOSAUR)
    R_DIRE_BEAR = _Creature(__R_DIRE_BEAR)
    R_DIREWOLF = _Creature(__R_DIREWOLF)
    R_EQUUS = _Creature(__R_EQUUS)
    R_GASBAGS = _Creature(__R_GASBAGS)
    R_GIGANOTOSAURUS = _Creature(__R_GIGANOTOSAURUS)
    R_MEGATHERIUM = _Creature(__R_MEGATHERIUM)
    R_PARASAUR = _Creature(__R_PARASAUR)
    R_PROCOPTODON = _Creature(__R_PROCOPTODON)
    R_QUETZAL = _Creature(__R_QUETZAL)
    R_REAPER_KING = _Creature(__R_REAPER_KING)
    R_REAPER_KING_TAMED = _Creature(__R_REAPER_KING_TAMED)
    R_REAPER_QUEEN = _Creature(__R_REAPER_QUEEN)
    R_SNOW_OWL = _Creature(__R_SNOW_OWL)
    R_THYLACOLEO = _Creature(__R_THYLACOLEO)
    R_VELONASAUR = _Creature(__R_VELONASAUR)
    ABERRANT_BEELZEBUFO = _Creature(__ABERRANT_BEELZEBUFO)
    ABERRANT_CARBONEMYS = _Creature(__ABERRANT_CARBONEMYS)
    ABERRANT_MEGALANIA = _Creature(__ABERRANT_MEGALANIA)
    ABERRANT_SARCO = _Creature(__ABERRANT_SARCO)
    ABERRANT_TITANOBOA = _Creature(__ABERRANT_TITANOBOA)
    BEELZEBUFO = _Creature(__BEELZEBUFO)
    CARBONEMYS = _Creature(__CARBONEMYS)
    ICHTHYOSAURUS = _Creature(__ICHTHYOSAURUS)
    KAPROSUCHUS = _Creature(__KAPROSUCHUS)
    LIOPLEURODON = _Creature(__LIOPLEURODON)
    MEGALANIA = _Creature(__MEGALANIA)
    MOSASAURUS = _Creature(__MOSASAURUS)
    PLESIOSAUR = _Creature(__PLESIOSAUR)
    QUETZALCOATLUS = _Creature(__QUETZALCOATLUS)
    SARCO = _Creature(__SARCO)
    TAPEJARA = _Creature(__TAPEJARA)
    THORNY_DRAGON = _Creature(__THORNY_DRAGON)
    TITANOBOA = _Creature(__TITANOBOA)
    TROPEOGNATHUS = _Creature(__TROPEOGNATHUS)
    ABERRANT_MOSCHOPS = _Creature(__ABERRANT_MOSCHOPS)
    ABERRANT_PURLOVIA = _Creature(__ABERRANT_PURLOVIA)
    PURLOVIA = _Creature(__PURLOVIA)
    TEK_PARASAUR = _Creature(__TEK_PARASAUR)
    TEK_QUETZAL = _Creature(__TEK_QUETZAL)
    TEK_RAPTOR = _Creature(__TEK_RAPTOR)
    TEK_REX = _Creature(__TEK_REX)
    TEK_STEGOSAURUS = _Creature(__TEK_STEGOSAURUS)
    TEK_TRICERATOPS = _Creature(__TEK_TRICERATOPS)
    EXO_MEK = _Creature(__EXO_MEK)
    GOLDEN_STRIPED_MEGALODON = _Creature(__GOLDEN_STRIPED_MEGALODON)
    X_ALLOSAURUS = _Creature(__X_ALLOSAURUS)
    X_ANKYLOSAURUS = _Creature(__X_ANKYLOSAURUS)
    X_ARGENTAVIS = _Creature(__X_ARGENTAVIS)
    X_BASILOSAURUS = _Creature(__X_BASILOSAURUS)
    X_DUNKLEOSTEUS = _Creature(__X_DUNKLEOSTEUS)
    X_ICHTHYOSAURUS = _Creature(__X_ICHTHYOSAURUS)
    X_MEGALODON = _Creature(__X_MEGALODON)
    X_MOSASAURUS = _Creature(__X_MOSASAURUS)
    X_OTTER = _Creature(__X_OTTER)
    X_PARACERATHERIUM = _Creature(__X_PARACERATHERIUM)
    X_PARASAUR = _Creature(__X_PARASAUR)
    X_RAPTOR = _Creature(__X_RAPTOR)
    X_REX = _Creature(__X_REX)
    X_ROCK_ELEMENTAL = _Creature(__X_ROCK_ELEMENTAL)
    X_SABERTOOTH = _Creature(__X_SABERTOOTH)
    X_SABERTOOTH_SALMON = _Creature(__X_SABERTOOTH_SALMON)
    X_SPINO = _Creature(__X_SPINO)
    X_TAPEJARA = _Creature(__X_TAPEJARA)
    X_TRICERATOPS = _Creature(__X_TRICERATOPS)
    X_WOOLLY_RHINO = _Creature(__X_WOOLLY_RHINO)
    X_YUTYRANNUS = _Creature(__X_YUTYRANNUS)


class Event:
    __BASILISK_GHOST = "Blueprint'/Game/Aberration/Dinos/Basilisk/Ghost_Basilisk_Character_BP.Ghost_Basilisk_Character_BP'"
    __BONE_FIRE_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/Bone_MegaWyvern_Character_BP_Fire.Bone_MegaWyvern_Character_BP_Fire'"
    __BULBDOG_GHOST = "Blueprint'/Game/Aberration/Dinos/LanternPug/Ghost_LanternPug_Character_BP.Ghost_LanternPug_Character_BP'"
    __BUNNY_DODO = "Blueprint'/Game/PrimalEarth/Dinos/Dodo/Dodo_Character_BP_Bunny.Dodo_Character_BP_Bunny'"
    __BUNNY_OVIRAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Oviraptor/BunnyOviraptor_Character_BP.BunnyOviraptor_Character_BP'"
    __DIREWOLF_GHOST = "Blueprint'/Game/PrimalEarth/Dinos/Direwolf/Ghost_Direwolf_Character_BP.Ghost_Direwolf_Character_BP'"
    __DODO_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/DodoWyvern/DodoWyvern_Character_BP.DodoWyvern_Character_BP'"
    __DODOREX = "Blueprint'/Game/PrimalEarth/Dinos/DodoRex/DodoRex_Character_BP.DodoRex_Character_BP'"
    __MANTIS_GHOST = "Blueprint'/Game/ScorchedEarth/Dinos/Mantis/Ghost_Mantis_Character_BP.Ghost_Mantis_Character_BP'"
    __REX_GHOST = "Blueprint'/Game/PrimalEarth/Dinos/Rex/Ghost_Rex_Character_BP.Ghost_Rex_Character_BP'"
    __SKELETAL_BRONTO = "Blueprint'/Game/PrimalEarth/Dinos/Sauropod/Bone_Sauropod_Character_BP.Bone_Sauropod_Character_BP'"
    __SKELETAL_CARNOTAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Carno/Bone_MegaCarno_Character_BP.Bone_MegaCarno_Character_B'"
    __SKELETAL_GIGANOTOSAURUS = "Blueprint'/Game/PrimalEarth/Dinos/Giganotosaurus/Bone_Gigant_Character_BP.Bone_Gigant_Character_BP'"
    __SKELETAL_JERBOA = "Blueprint'/Game/ScorchedEarth/Dinos/Jerboa/Bone_Jerboa_Character_BP.Bone_Jerboa_Character_BP'"
    __SKELETAL_QUETZAL = "Blueprint'/Game/PrimalEarth/Dinos/Quetzalcoatlus/Bone_Quetz_Character_BP.Bone_Quetz_Character_BP'"
    __SKELETAL_RAPTOR = "Blueprint'/Game/PrimalEarth/Dinos/Raptor/Bone_MegaRaptor_Character_BP.Bone_MegaRaptor_Character_BP'"
    __SKELETAL_REX = "Blueprint'/Game/PrimalEarth/Dinos/Rex/Bone_MegaRex_Character_BP.Bone_MegaRex_Character_BP'"
    __SKELETAL_STEGO = "Blueprint'/Game/PrimalEarth/Dinos/Stego/Bone_Stego_Character_BP'"
    __SKELETAL_TRIKE = "Blueprint'/Game/PrimalEarth/Dinos/Trike/Bone_Trike_Character_BP'"
    __SNOW_OWL_GHOST = "Blueprint'/Game/Extinction/Dinos/Owl/Ghost_Owl_Character_BP.Ghost_Owl_Character_BP'"
    __SUPER_TURKEY = "Blueprint'/Game/PrimalEarth/Dinos/Dodo/Turkey_Character_BP.Turkey_Character_BP'"
    __SURFACE_REAPER_KING_GHOST = "Blueprint'/Game/Aberration/Dinos/Nameless/Ghost_Xenomorph_Character_BP_Male_Surface.Ghost_Xenomorph_Character_BP_Male_Surface'"
    __TURKEY = "Blueprint'/Game/PrimalEarth/Dinos/Dodo/TurkeyBase_Character_BP.TurkeyBase_Character_BP'"
    __ZOMBIE_FIRE_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_ZombieFire.Wyvern_Character_BP_ZombieFire'"
    __ZOMBIE_LIGHTNING_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_ZombieLightning.Wyvern_Character_BP_ZombieLightning'"
    __ZOMBIE_POISON_WYVERN = "Blueprint'/Game/ScorchedEarth/Dinos/Wyvern/Wyvern_Character_BP_ZombiePoison.Wyvern_Character_BP_ZombiePoison'"
    __ZOMDODO = "Blueprint'/Game/PrimalEarth/Dinos/Dodo/ZombieDodo_Character_BP.ZombieDodo_Character_BP'"

    GHOST_BASILISK = _Creature(__BASILISK_GHOST, event='Ghost')
    SKELETAL_FIRE_WYVERN = _Creature(__BONE_FIRE_WYVERN, event='Bone')
    GHOST_BULBDOG = _Creature(__BULBDOG_GHOST, event='Ghost')
    BUNNY_DODO = _Creature(__BUNNY_DODO, event='Bunny')
    BUNNY_OVIRAPTOR = _Creature(__BUNNY_OVIRAPTOR, event='Bunny')
    GHOST_DIREWOLF = _Creature(__DIREWOLF_GHOST, event='Ghost')
    DODO_WYVERN = _Creature(__DODO_WYVERN, event='Dodo')
    DODO_REX = _Creature(__DODOREX, event='Dodo')
    GHOST_MANTIS = _Creature(__MANTIS_GHOST, event='Ghost')
    GHOST_REX = _Creature(__REX_GHOST, event='Ghost')
    SKELETAL_BRONTO = _Creature(__SKELETAL_BRONTO, event='Skeletal')
    SKELETAL_CARNOTAURUS = _Creature(__SKELETAL_CARNOTAURUS, event='Skeletal')
    SKELETAL_GIGANOTOSAURUS = _Creature(__SKELETAL_GIGANOTOSAURUS, event='Skeletal')
    SKELETAL_JERBOA = _Creature(__SKELETAL_JERBOA, event='Skeletal')
    SKELETAL_QUETZAL = _Creature(__SKELETAL_QUETZAL, event='Skeletal')
    SKELETAL_RAPTOR = _Creature(__SKELETAL_RAPTOR, event='Skeletal')
    SKELETAL_REX = _Creature(__SKELETAL_REX, event='Skeletal')
    SKELETAL_STEGO = _Creature(__SKELETAL_STEGO, event='Skeletal')
    SKELETAL_TRIKE = _Creature(__SKELETAL_TRIKE, event='Skeletal')
    GHOST_SNOW_OWL = _Creature(__SNOW_OWL_GHOST, event='Ghost')
    SUPER_TURKEY = _Creature(__SUPER_TURKEY, event='')
    GHOST_SURFACE_REAPER_KING = _Creature(__SURFACE_REAPER_KING_GHOST, event='Ghost')
    TURKEY = _Creature(__TURKEY, event='')
    ZOMBIE_FIRE_WYVERN = _Creature(__ZOMBIE_FIRE_WYVERN, event='Zombie')
    ZOMBIE_LIGHTNING_WYVERN = _Creature(__ZOMBIE_LIGHTNING_WYVERN, event='Zombie')
    ZOMBIE_POISON_WYVERN = _Creature(__ZOMBIE_POISON_WYVERN, event='Zombie')
    ZOMBIE_DODO = _Creature(__ZOMDODO, event='Zombie')


if __name__ == '__main__':
    griffin = Dinos.GRIFFIN
    print(griffin)
    print(griffin.spawn())
    print(repr(griffin))

    bone_trike = Event.SKELETAL_TRIKE
    print(bone_trike)
    print(bone_trike.spawn())
    print(repr(bone_trike))

    alpha_trex = Alphas.ALPHA_T_REX
    print(alpha_trex)
    print(alpha_trex.spawn())
    print(repr(alpha_trex))

    manticore = Bosses.MANTICORE_ALPHA
    print(manticore)
    print(manticore.spawn())
    print(repr(manticore))

    flock = Bosses.DESERT_TITAN_FLOCK
    print(flock)
    print(flock.spawn())
    print(repr(flock))


