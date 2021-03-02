from collections import defaultdict
from enum import Enum

DATA_PATH = "C:/Program Files (x86)/GOG Galaxy/Games/Morrowind/Data Files/"

RECORDS_ALL = ["TES3", "GMST", "GLOB", "CLAS", "FACT", "RACE", "SOUN", "SKIL", "MGEF", "SCPT", "REGN", "BSGN", "LTEX", "STAT", "DOOR", "MISC", "WEAP", "CONT", "SPEL", "CREA", "BODY", "LIGH", "ENCH", "NPC_", "ARMO", "CLOT", "REPA", "ACTI", "APPA", "LOCK", "PROB", "INGR", "BOOK", "ALCH", "LEVI", "LEVC", "CELL", "LAND", "PGRD", "SNDG", "DIAL", "INFO", "SSCR"]

RECORDS_MOST = ["TES3", "GMST", "GLOB", "CLAS", "FACT", "RACE", "SOUN", "SKIL", "MGEF", "SCPT", "REGN", "BSGN", "LTEX", "STAT", "DOOR", "MISC", "WEAP", "CONT", "SPEL", "CREA", "BODY", "LIGH", "ENCH", "NPC_", "ARMO", "CLOT", "REPA", "ACTI", "APPA", "LOCK", "PROB", "INGR", "BOOK", "ALCH", "LEVI", "LEVC", "SNDG", "SSCR"]

RECORDS_MIN = ["TES3", "CLAS", "RACE", "SKIL", "MGEF"]

ATTRIBUTES = ["Strength", "Intelligence", "Willpower", "Agility", "Speed", "Endurance", "Personality", "Luck"]
SPECIALIZATIONS = ["Magic", "Stealth", "Combat"]
SKILLS = ["Block", "Armorer", "Medium Armor", "Heavy Armor", "Blunt Weapon", "Long Blade", "Axe", "Spear", "Athletics", "Enchant", "Destruction", "Alteration", "Illusion", "Conjuration", "Mysticism", "Restoration", "Alchemy", "Unarmored", "Security", "Sneak", "Acrobatics", "Light Armor", "Short Blade", "Marksman", "Mercantile", "Speechcraft", "Hand-to-hand"]

MAGIC_EFFECTS = ["WaterBreathing", "SwiftSwim", "WaterWalking", "Shield", "FireShield", "LightningShield",
"FrostShield", "Burden", "Feather", "Jump", "Levitate", "SlowFall", "Lock", "Open", "FireDamage", "ShockDamage", "FrostDamage", "DrainAttribute", "DrainHealth", "DrainSpellpoints", "DrainFatigue", "DrainSkill", "DamageAttribute", "DamageHealth", "DamageMagicka", "DamageFatigue", "DamageSkill", "Poison", "WeaknessToFire", "WeaknessToFrost", "WeaknessToShock", "WeaknessToMagicka", "WeaknessToCommonDisease", "WeaknessToBlightDisease", "WeaknessToCorprusDisease", "WeaknessToPoison", "WeaknessToNormalWeapons", "DisintegrateWeapon", "DisintegrateArmor", "Invisibility", "Chameleon", "Light", "Sanctuary", "NightEye", "Charm", "Paralyze", "Silence", "Blind", "Sound", "CalmHumanoid", "CalmCreature", "FrenzyHumanoid", "FrenzyCreature", "DemoralizeHumanoid", "DemoralizeCreature", "RallyHumanoid", "RallyCreature", "Dispel", "Soultrap", "Telekinesis", "Mark", "Recall", "DivineIntervention", "AlmsiviIntervention", "DetectAnimal", "DetectEnchantment", "DetectKey", "SpellAbsorption", "Reflect", "CureCommonDisease", "CureBlightDisease", "CureCorprusDisease", "CurePoison", "CureParalyzation", "RestoreAttribute", "RestoreHealth", "RestoreSpellPoints", "RestoreFatigue", "RestoreSkill", "FortifyAttribute", "FortifyHealth", "FortifySpellpoints", "FortifyFatigue", "FortifySkill", "FortifyMagickaMultiplier", "AbsorbAttribute", "AbsorbHealth", "AbsorbSpellPoints", "AbsorbFatigue", "AbsorbSkill", "ResistFire", "ResistFrost", "ResistShock", "ResistMagicka", "ResistCommonDisease", "ResistBlightDisease", "ResistCorprusDisease", "ResistPoison", "ResistNormalWeapons", "ResistParalysis", "RemoveCurse", "TurnUndead", "SummonScamp", "SummonClannfear", "SummonDaedroth", "SummonDremora", "SummonAncestralGhost", "SummonSkeletalMinion", "SummonLeastBonewalker", "SummonGreaterBonewalker", "SummonBonelord", "SummonWingedTwilight", "SummonHunger", "SummonGoldensaint", "SummonFlameAtronach", "SummonFrostAtronach", "SummonStormAtronach", "FortifyAttackBonus", "CommandCreatures", "CommandHumanoids", "BoundDagger", "BoundLongsword", "BoundMace", "BoundBattleAxe", "BoundSpear", "BoundLongbow", "ExtraSpell", "BoundCuirass", "BoundHelm", "BoundBoots", "BoundShield", "BoundGloves", "Corpus", "Vampirism", "SummonCenturionSphere", "SunDamage", "StuntedMagicka", "SummonFabricant", "SummonCreature01", "SummonCreature02", "SummonCreature03", "SummonCreature04", "SummonCreature05"]

MAGIC_NAMES = ["Water Breathing", "Swift Swim", "Water Walking", "Shield", "Fire Shield", "Lightning Shield", "Frost Shield", "Burden", "Feather", "Jump", "Levitate", "SlowFall", "Lock", "Open", "Fire Damage", "Shock Damage", "Frost Damage", "Drain Attribute", "Drain Health", "Drain Magicka", "Drain Fatigue", "Drain Skill", "Damage Attribute", "Damage Health", "Damage Magicka", "Damage Fatigue", "Damage Skill", "Poison", "Weakness to Fire", "Weakness to Frost", "Weakness to Shock", "Weakness to Magicka", "Weakness to Common Disease", "Weakness to Blight Disease", "Weakness to Corprus Disease", "Weakness to Poison", "Weakness to Normal Weapons", "Disintegrate Weapon", "Disintegrate Armor", "Invisibility", "Chameleon", "Light", "Sanctuary", "Night Eye", "Charm", "Paralyze", "Silence", "Blind", "Sound", "Calm Humanoid", "Calm Creature", "Frenzy Humanoid", "Frenzy Creature", "Demoralize Humanoid", "Demoralize Creature", "Rally Humanoid", "Rally Creature", "Dispel", "Soultrap", "Telekinesis", "Mark", "Recall", "Divine Intervention", "Almsivi Intervention", "Detect Animal", "Detect Enchantment", "Detect Key", "Spell Absorption", "Reflect", "Cure Common Disease", "Cure Blight Disease", "Cure Corprus Disease", "Cure Poison", "Cure Paralyzation", "Restore Attribute", "Restore Health", "Restore Magicka", "Restore Fatigue", "Restore Skill", "Fortify Attribute", "Fortify Health", "Fortify Magicka", "Fortify Fatigue", "Fortify Skill", "Fortify Maximum Magicka", "Absorb Attribute", "Absorb Health", "Absorb Magicka", "Absorb Fatigue", "Absorb Skill", "Resist Fire", "Resist Frost", "Resist Shock", "Resist Magicka", "Resist Common Disease", "Resist Blight Disease", "Resist Corprus Disease", "Resist Poison", "Resist Normal Weapons", "Resist Paralysis", "Remove Curse", "Turn Undead", "Summon Scamp", "Summon Clannfear", "Summon Daedroth", "Summon Dremora", "Summon Ancestral Ghost", "Summon Skeletal Minion", "Summon Bonewalker", "Summon Greater Bonewalker", "Summon Bonelord", "Summon Winged Twilight", "Summon Hunger", "Summon Golden Saint", "Summon Flame Atronach", "Summon Frost Atronach", "Summon Storm Atronach", "Fortify Attack", "Command Creature", "Command Humanoid", "Bound Dagger", "Bound Longsword", "Bound Mace", "Bound Battle Axe", "Bound Spear", "Bound Longbow", "EXTRA SPELL", "Bound Cuirass", "Bound Helm", "Bound Boots", "Bound Shield", "Bound Gloves", "Corprus", "Vampirism", "Summon Centurion Sphere", "Sun Damage", "Stunted Magicka", "Summon Fabricant", "Detect Animal", "Call Wolf", "Call Bear", "Summon Bonewolf"]

MAGIC_SCHOOLS = ["Alteration", "Conjuration", "Destruction", "Illusion", "Mysticism", "Restoration"]

HARDCODED_FLAGS = [0x11c8, 0x11c0, 0x11c8, 0x11e0, 0x11e0, 0x11e0, 0x11e0, 0x11d0,
0x11c0, 0x11c0, 0x11e0, 0x11c0, 0x11184, 0x11184, 0x1f0, 0x1f0, 0x1f0, 0x11d2, 0x11f0, 0x11d0, 0x11d0, 0x11d1, 0x1d2, 0x1f0, 0x1d0, 0x1d0, 0x1d1, 0x1f0, 0x11d0, 0x11d0, 0x11d0, 0x11d0, 0x11d0, 0x11d0, 0x11d0, 0x11d0, 0x11d0, 0x1d0, 0x1d0, 0x11c8, 0x31c0, 0x11c0, 0x11c0, 0x11c0, 0x1180, 0x11d8, 0x11d8, 0x11d0, 0x11d0, 0x11180, 0x11180, 0x11180, 0x11180, 0x11180, 0x11180, 0x11180, 0x11180, 0x11c4, 0x111b8, 0x1040, 0x104c, 0x104c, 0x104c, 0x104c, 0x1040, 0x1040, 0x1040, 0x11c0, 0x11c0, 0x1cc, 0x1cc, 0x1cc, 0x1cc, 0x1cc, 0x1c2, 0x1c0, 0x1c0, 0x1c0, 0x1c1, 0x11c2, 0x11c0, 0x11c0, 0x11c0, 0x11c1, 0x11c0, 0x21192, 0x20190, 0x20190, 0x20190, 0x21191, 0x11c0, 0x11c0, 0x11c0, 0x11c0, 0x11c0, 0x11c0, 0x11c0, 0x11c0, 0x11c0, 0x11c0, 0x1c0, 0x11190, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x9048, 0x11c0, 0x1180, 0x1180, 0x5048, 0x5048, 0x5048, 0x5048, 0x5048, 0x5048, 0x1188, 0x5048, 0x5048, 0x5048, 0x5048, 0x5048, 0x1048, 0x104c, 0x1048, 0x40, 0x11c8, 0x1048, 0x1048, 0x1048, 0x1048, 0x1048, 0x1048]

class MagnitudeType(Enum):
    NONE = 0
    TIMES_INT = 1
    FEET = 2
    LEVEL = 3
    PERCENTAGE = 4
    POINTS = 5

WEATHERS = ["Clear", "Cloudy", "Foggy", "Overcast", "Rain", "Thunder", "Ash", "Blight", "Snow", "Blizzard"]

WEAPON_TYPES = ["ShortBladeOneHand", "LongBladeOneHand", "LongBladeTwoClose", "BluntOneHand", "BluntTwoClose", "BluntTwoWide", "SpearTwoWide", "AxeOneHand", "AxeTwoClose", "MarksmanBow", "MarksmanCrossbow", "MarksmanThrown", "Arrow", "Bolt"]

SPEL_TYPES = ["Spell", "Ability", "Blight", "Disease", "Curse", "Power"]

CREA_TYPES = ["Creature", "Daedra", "Undead", "Humanoid"]

BODY_PARTS = ["Head", "Hair", "Neck", "Chest", "Groin", "Hand", "Wrist", "Forearm", "Upper Arm", "Foot", "Ankle", "Knee", "Upper Leg", "Clavicle", "Tail"]
BODY_TYPES = ["Skin", "Clothing", "Armor"]

ENCH_TYPES = ["Cast Once", "Cast When Strikes", "Cast When Used", "Constant Effect"]
ENCH_RANGES = ["Self", "Touch", "Target"]

ARMO_TYPES = ["Helmet", "Cuirass", "Left Pauldron", "Right Pauldron", "Greaves", "Boots", "Left Gauntlet", "Right Gauntlet", "Shield", "Left Bracer", "Right Bracer"]
ARMO_PARTS = ["Head", "Hair", "Neck", "Cuirass", "Groin", "Skirt", "Right Hand", "Left Hand", "Right Wrist", "Left Wrist", "Shield", "Right Forearm", "Left Forearm", "Right Upper Arm", "Left Upper Arm", "Right Foot", "Left Foot", "Right Ankle", "Left Ankle", "Right Knee", "Left Knee", "Right Upper Leg", "Left Upper Leg", "Right Pauldron", "Left Pauldron", "Weapon", "Tail"]

CLOT_TYPES = ["Pants", "Shoes", "Shirt", "Belt", "Robe", "Right Glove", "Left Glove", "Skirt", "Ring", "Amulet"]

APPA_TYPES = ["Mortar/Pestle", "Alembic", "Calcinator", "Retort"]

LAND_DEFAULT_HEIGHT = -256
LAND_SIZE = 65
LAND_NUM_VERTS = LAND_SIZE * LAND_SIZE
LAND_TEXTURE_SIZE = 16
LAND_NUM_TEXTURES = LAND_TEXTURE_SIZE * LAND_TEXTURE_SIZE
LAND_LOD_SIZE = 9
LAND_NUM_LOD_VERTS = LAND_LOD_SIZE * LAND_LOD_SIZE

SNDG_TYPES = ["Left", "Right", "SwimLeft", "SwimRight", "Moan", "Roar", "Scream", "Land"]

DIAL_TYPES = ["Topic", "Voice", "Greeting", "Persuasion", "Journal"]

INFO_SCVR_TYPE = ["", "Function", "Global", "Local", "Journal", "Item", "Dead", "Not ID", "Not Faction", "Not Class", "Not Race", "Not Cell", "Not Local"]
INFO_SCVR_FUNCTION = ["Rank Low", "Rank High", "Rank Requirement", "Reputation", "Health Percent", "PC Reputation", "PC Level", "PC Health Percent", "PC Magicka", "PC Fatigue", "PC Strength", "PC Block", "PC Armorer", "PC Medium Armor", "PC Heavy Armor", "PC Blunt Weapon", "PC Long Blade", "PC Axe", "PC Spear", "PC Athletics", "PC Enchant", "PC Detruction", "PC Alteration", "PC Illusion", "PC Conjuration", "PC Mysticism", "PC Restoration", "PC Alchemy", "PC Unarmored", "PC Security", "PC Sneak", "PC Acrobatics", "PC Light Armor", "PC Short Blade", "PC Marksman", "PC Merchantile", "PC Speechcraft", "PC Hand to Hand", "PC Sex", "PC Expelled", "PC Common Disease", "PC Blight Disease", "PC Clothing Modifier", "PC Crime Level", "Same Sex", "Same Race", "Same Faction", "Faction Rank Difference", "Detected", "Alarmed", "Choice", "PC Intelligence", "PC Willpower", "PC Agility", "PC Speed", "PC Endurance", "PC Personality", "PC Luck", "PC Corpus", "Weather", "PC Vampire", "Level", "Attacked", "Talked to PC", "PC Health", "Creature Target", "Friend Hit", "Fight", "Hello", "Alarm", "Flee", "Should Attack", "Werewolf", "PC Werewolf Kills"]
INFO_SCVR_COMPARE = ["=", "!=", ">", ">=", "<", "<="]

records = defaultdict(list)
ordered_records = []
plugin_records = {}
default_records = ["TES3"]
game_settings = {}
object_ids = {}
info_ids = {}
interior_cells = {}
exterior_cells = {}

def readable_object(id):
    if id in object_ids:
        return str(object_ids[id])
    return id

def decimal_format(num):
    return "{:.2f}".format(num).rstrip("0").rstrip(".")