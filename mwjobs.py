import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import seaborn as sns
import tkinter as tk
import record.mwtes3 as mwtes3
import record.mwgmst as mwgmst
import record.mwglob as mwglob
import record.mwclas as mwclas
import record.mwfact as mwfact
import record.mwrace as mwrace
import record.mwsoun as mwsoun
import record.mwskil as mwskil
import record.mwmgef as mwmgef
import record.mwscpt as mwscpt
import record.mwregn as mwregn
import record.mwbsgn as mwbsgn
import record.mwltex as mwltex
import record.mwstat as mwstat
import record.mwdoor as mwdoor
import record.mwmisc as mwmisc
import record.mwweap as mwweap
import record.mwcont as mwcont
import record.mwspel as mwspel
import record.mwcrea as mwcrea
import record.mwbody as mwbody
import record.mwligh as mwligh
import record.mwench as mwench
import record.mwnpc_ as mwnpc_
import record.mwarmo as mwarmo
import record.mwclot as mwclot
import record.mwrepa as mwrepa
import record.mwacti as mwacti
import record.mwappa as mwappa
import record.mwlock as mwlock
import record.mwprob as mwprob
import record.mwingr as mwingr
import record.mwbook as mwbook
import record.mwalch as mwalch
import record.mwlevi as mwlevi
import record.mwlevc as mwlevc
import record.mwcell as mwcell
import record.mwland as mwland
import record.mwpgrd as mwpgrd
import record.mwsndg as mwsndg
import record.mwdial as mwdial
import record.mwinfo as mwinfo
import record.mwsscr as mwsscr
import mwglobals

def region_location_changes(plugin1, plugin2):
    locations1 = []
    locations2 = []
    for cell in mwglobals.records["CELL"]:
        if not cell.is_interior:
            if cell.file_name == plugin1:
                for ref in cell.references:
                    if hasattr(ref, "door_cell"):
                        locations1 += [cell.region + ": " + ref.door_cell]
            elif cell.file_name == plugin2:
                for ref in cell.references:
                    if hasattr(ref, "door_cell"):
                        locations2 += [cell.region + ": " + ref.door_cell]
    for loc in locations1:
        if loc not in locations2:
            print("-" + loc)
    for loc in locations2:
        if loc not in locations1:
            print("+" + loc)

def find_usage(id):
    for npc in mwglobals.records["NPC_"]:
        for item in npc.items:
            if item == id:
                print(str(npc))
                break
    for creature in mwglobals.records["CREA"]:
        for item in creature.items:
            if item == id:
                print(str(creature))
                break
    for cell in mwglobals.records["CELL"]:
        for ref in cell.references:
            if ref.id == id:
                print(str(cell))
                break
    for container in mwglobals.records["CONT"]:
        for item in container.items:
            if item == id:
                print(str(container))
                break
    for leveled_list in mwglobals.records["LEVI"]:
        for item in leveled_list.items:
            if item.id == id:
                print(str(leveled_list))
                break
    for leveled_creature in mwglobals.records["LEVC"]:
        for creature in leveled_creature.creatures:
            if creature.id == id:
                print(str(leveled_creature))
                break
    for script in mwglobals.records["SCPT"]:
        if id in script.text:
            print(str(script))

def find_item_usage(id, file_names=None):
    usages = []
    for npc in mwglobals.records["NPC_"]:
        if file_names is None or npc.file_name in file_names:
            for item in npc.items:
                if item == id:
                    count = npc.items[item]
                    if count == 1:
                        usages += ["Carried by {{" + mod_shortcut(npc) + "|" + npc.name + "}}"]
                    else:
                        usages += ["Carried by {{" + mod_shortcut(npc) + "|" + npc.name + "}} (&times;" + str(count) + ")"]
                    break
    for creature in mwglobals.records["CREA"]:
        if file_names is None or creature.file_name in file_names:
            for item in creature.items:
                if item == id:
                    count = creature.items[item]
                    if count == 1:
                        usages += ["Carried by {{" + mod_shortcut(creature) + "|" + creature.name + "}}"]
                    else:
                        usages += ["Carried by {{" + mod_shortcut(creature) + "|" + creature.name + "}} (&times;" + str(count) + ")"]
                    break
    for cell in mwglobals.records["CELL"]:
        if file_names is None or cell.file_name in file_names:
            count = 0
            for ref in cell.references:
                if ref.id == id:
                    count += 1
            if count == 1:
                usages += [str(cell)]
            elif count > 1:
                usages += [str(cell) + " (&times;" + str(count) + ")"]
    for container in mwglobals.records["CONT"]:
        if file_names is None or container.file_name in file_names:
            for item in container.items:
                if item == id:
                    for loc in find_item_usage(container.id, file_names=file_names):
                        count = container.items[item]
                        if count == 1:
                            usages += [loc + " (" + container.name + ")"]
                        else:
                            usages += [loc + " (&times;" + str(count) + ", in " + container.name + ")"]
                    break
    for leveled_list in mwglobals.records["LEVI"]:
        if file_names is None or leveled_list.file_name in file_names:
            for item in leveled_list.items:
                if item.id == id:
                    usages += [leveled_list.id]
                    break
    return usages

def faction_members(faction, file_name):
    npcs = [npc for npc in mwglobals.records["NPC_"] if npc.faction == faction and npc.file_name == file_name]
    npcs.sort(key=lambda x: x.name)
    for npc in npcs:
        print("|-")
        print("!{{TR3|" + npc.name + "}}")
        data = "|" + npc.get_sex_template()
        data += "||[[Morrowind:" + npc.get_wiki_race() + "|" + npc.get_wiki_race() + "]]||[[Morrowind:" + npc.get_wiki_class() + "|" + npc.class_ + "]]||" + str(npc.faction_rank) + " " + npc.get_faction_rank_name() + "||"
        for cell in mwglobals.records["CELL"]:
            for ref in cell.references:
                if ref.id == npc.id:
                    data += str(cell)
                    break
        data += "||"
        if npc.service_weapons or npc.service_armor or npc.service_clothing or npc.service_books or npc.service_ingredients or npc.service_picks or npc.service_probes or npc.service_lights or npc.service_apparatus or npc.service_repair_items or npc.service_miscellaneous or npc.service_magic_items or npc.service_potions:
            data += "{{TR3|Merchants|Merchant}}"
        if npc.service_spells:
            data += "{{TR3|Spell Merchants|Spell Merchant}}"
        if npc.service_training:
            data += "{{TR3|Trainers|Trainer}}"
        if npc.service_spellmaking:
            data += "{{TR3|Spellmaker}}"
        if npc.service_enchanting:
            data += "{{TR3|Enchanter}}"
        if npc.service_repair:
            data += "{{TR3|Blacksmith|Blacksmith}}"
        print(data)

def all_record_details(file_name=None):
    for record_type in mwglobals.RECORD_TYPES:
        if record_type == "INFO":
            continue
        print_type = True
        for record in mwglobals.records[record_type]:
            if file_name != None and record.file_name != file_name:
                continue
            if print_type and hasattr(record, "record_details"):
                print("==== " + record_type + " ====\n\n")
                print_type = False
            print(record.record_details())
            print()
            print()

def unique_dialogue(actor_id):
    for dial in mwglobals.records["DIAL"]:
        infos = dial.filter_infos(actor=actor_id)
        if len(infos) > 0:
            print("* '''" + dial.name + "''':")
            for info in infos:
                if info.disposition != 0:
                    print("Disposition >= " + str(info.disposition))
                for filter in info.func_var_filters:
                    print(filter)
                print("** ''\"" + info.response + "\"''")
                if info.result != None:
                    print(info.result)
                print()

def exterior_doors(file):
    doorfile = open('mwdoorexceptions.txt','r')
    doorlist = doorfile.read().splitlines()
    cols = ['Name', 'GridX', 'GridY', 'PosX', 'PosY', 'ID', 'Check']
    data = []
    for cell in mwglobals.exterior_cells.values():
        for ref in cell.references:
            obj = mwglobals.object_ids[ref.id]
            if isinstance(obj, mwdoor.MwDOOR) and not ref.deleted:
                if hasattr(ref, "door_cell"):
                    check = 1
                elif obj.id in doorlist:
                    check = 2
                else:
                    check = 0
                data.append([cell.get_name(), cell.grid_x, cell.grid_y, ref.pos_x, ref.pos_y, obj.id, check])
    doors = pd.DataFrame(data, columns=cols)
    doors.to_csv(file, index=False, header=True)

def door_map(file, img, top, bottom, left, right):
    door_locs = pd.read_csv(file)
    door_locs = door_locs[door_locs.Check != 2]
    door_locs.PosX = door_locs.PosX/pow(2,13)
    door_locs.PosY = door_locs.PosY/pow(2,13)
    cellexp = plt.imread(img)
    h, w, _ = cellexp.shape
    h = h/256
    w = w/256
    fig, ax = plt.subplots()
    l = ax.figure.subplotpars.left
    r = ax.figure.subplotpars.right
    t = ax.figure.subplotpars.top
    b = ax.figure.subplotpars.bottom
    figw = float(w)/(r-l)
    figh = float(h)/(t-b)
    ax.figure.set_size_inches(figw, figh)
    ax.grid(color='grey', linestyle='-', linewidth=2, alpha=0.5, which='both')
    ax.get_xaxis().set_minor_locator(MultipleLocator(1))
    ax.get_yaxis().set_minor_locator(MultipleLocator(1))
    ax.imshow(cellexp, extent=(left, right+1, bottom, top+1))
    g = sns.scatterplot(x='PosX', y='PosY', hue='Check', data=door_locs, ax=ax, marker='.', size=2, edgecolor=None)
    g.legend([],[], frameon=False)
    fig.savefig("Doors.png", dpi=256)

def print_trainers_by_skill():
    trainers = {}
    for skill in SKILLS:
        trainers[skill] = []
    for npc in mwglobals.records["NPC_"]:
        for skill, value in npc.trained_skills():
            trainers[skill] += [(npc.name, value)]
    for skill in trainers:
        trainers[skill] = sorted(trainers[skill], key=lambda x:x[1], reverse=True)
        print(skill)
        for trainer, value in trainers[skill]:
            print(trainer, value)
        print()

def deprecated_check():
    deprecated_ids = []
    for name in mwglobals.records:
        for record in mwglobals.records[name]:
            if hasattr(record, "name") and record.name != None and "deprecated" in record.name.lower():
                deprecated_ids += [record.id]
    
    print("Cells:")
    for cell in mwglobals.records["CELL"]:
        for ref in cell.references:
            if ref.id in deprecated_ids:
                print(str(cell) + ": " + ref.id)
    print()
    print("NPCs:")
    for npc in mwglobals.records["NPC_"]:
        for item in npc.items:
            if item in deprecated_ids:
                print(npc.id + ": " + item)
    print()
    print("Creatures:")
    for creature in mwglobals.records["CREA"]:
        for item in creature.items:
            if item in deprecated_ids:
                print(creature.id + ": " + item)
    print()
    print("Containers:")
    for container in mwglobals.records["CONT"]:
        for item in container.items:
            if item in deprecated_ids:
                print(container.id + ": " + item)
    print()
    print("Scripts:")
    for script in mwglobals.records["SCPT"]:
        for id in deprecated_ids:
            if id in script.text:
                print(script.id + ": " + id)
    print()
    print("Leveled Items:")
    for list in mwglobals.records["LEVI"]:
        for item in list.items:
            if item.id in deprecated_ids:
                print(list.id + ": " + item.id)
    print()
    print("Leveled Creatures:")
    for list in mwglobals.records["LEVC"]:
        for creature in list.creatures:
            if creature.id in deprecated_ids:
                print(list.id + ": " + creature.id)

def mod_shortcut(obj):
    if obj.file_name.startswith("Tamriel_"):
        return "TD3"
    elif obj.file_name.startswith("TR_"):
        return "TR3"
    elif obj.file_name.startswith("Sky_"):
        return "SHOTN"
    elif obj.file_name.startswith("Cyrodiil_"):
        return "PC3"

def view_heightmap(window_width=800, window_height=600, downscale=5, lod=False):
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for land in mwglobals.records["LAND"]:
        if land.grid_x < min_x:
            min_x = land.grid_x
        elif land.grid_x > max_x:
            max_x = land.grid_x
        if land.grid_y < min_y:
            min_y = land.grid_y
        elif land.grid_y > max_y:
            max_y = land.grid_y
    if lod:
        cell_size = LAND_LOD_SIZE
    else:
        cell_size = int(LAND_SIZE / downscale)
    world_width = (max_x - min_x) * cell_size
    world_height = (max_y - min_y) * cell_size
    half_width = int(world_width / 2)
    half_height = int(world_height / 2)
    
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.grid(row=0, column=0)
    
    canvas = tk.Canvas(frame, width=window_width, height=window_height, scrollregion=(0, 0, world_width, world_height))
    img = tk.PhotoImage(width=world_width, height=world_height)
    for land in mwglobals.records["LAND"]:
        if not lod:
            land.load_terrain()
        x = (land.grid_x - min_x) * cell_size
        y = (max_y - land.grid_y) * cell_size
        for i in range(cell_size):
            for j in range(cell_size):
                if lod:
                    height = land.lod_heights[i + j * LAND_LOD_SIZE]
                else:
                    height = int(land.heights[i * downscale + j * downscale * LAND_SIZE] / 10)
                color = "#{0:02x}{0:02x}{0:02x}".format(height) if height >= 0 else "#{0:02x}{0:02x}{1:02x}".format(255 + height, 255)
                img.put(color, (x + i, y + cell_size - j))
    canvas.create_image((half_width, half_height), image=img, state="normal")
    
    hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    hbar.config(command=canvas.xview)
    hbar.pack(side=tk.BOTTOM, fill=tk.X)
    vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    vbar.config(command=canvas.yview)
    vbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    
    root.mainloop()