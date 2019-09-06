import json
import os
from bs4 import BeautifulSoup
import numpy as np
import scipy.stats

import parse_xml_npc

key_str2int = lambda d: {int(k) if k.lstrip("-").isdigit() else k: v for k, v in d.items()}


def create_new_xml(old_xml_dir, new_xml_dir, new_data_file, has_diff):

    npcs_data = json.load(open(new_data_file, "r"), object_hook=key_str2int)

    npc_files = []
    for file in os.listdir(old_xml_dir):
        if file.endswith(".xml"):
            npc_files.append(file)

    if not os.path.exists(new_xml_dir):
        os.makedirs(new_xml_dir)

    soups = {}
    for file in npc_files:
        with open(os.path.join(old_xml_dir, file), "r") as f:
            contents = f.read()
        soups[file] = BeautifulSoup(contents, "xml")

    soups = step_1(soups, npcs_data)
    soups = step_2(soups, npcs_data, has_diff)
    soups = step_3(soups, npcs_data, old_xml_dir)

    for file, soup in soups.items():
        with open(os.path.join(new_xml_dir, file), "w") as f:
            f.write(soup.prettify())


def step_1(soups, npcs_data):
    print("Step 1: Fix spoils for all mobs")

    for file, soup in soups.items():

        npcs = soup.find_all("npc")

        for npc in npcs:
            npc_id = eval(npc["id"])

            try:
                npc_data = npcs_data[npc_id]
            except:
                continue

            drops = npc.select("drops")[0]

            category = drops.find("category", {"id": -1})
            if category is None:
                new_category = soup.new_tag("category", id="-1")
                drops.append(new_category)
                drops.append("\n")
                category = new_category

            category.string = ""
            category.append("\n")
            for spoil in npc_data["spoil"]:
                item_id, item_min, item_max, item_chance = spoil
                item_chance = round(item_chance * 1e6)
                new_drop = soup.new_tag(
                    "drop", itemid=item_id, min=item_min, max=item_max, chance=item_chance
                )
                category.append(new_drop)
                category.append("\n")

    return soups


def step_2(soups, npcs_data, has_diff):

    print("Step 2: Fix the mobs that have the exact same drops")
    print("Step 2a: Remove drops from mobs where l2portal says they have none")

    ids_no_diff = has_diff[np.where(has_diff[:, 1] == 0)[0], 0]

    for file, soup in soups.items():

        npcs = soup.find_all("npc")

        for npc in npcs:
            npc_id = eval(npc["id"])

            try:
                npc_data = npcs_data[npc_id]
            except:
                continue

            if npc_id not in list(ids_no_diff) and npc_data["drop"] != []:
                continue

            drops = npc.select("drops")[0]
            categories = drops.select("category")

            for drop in npc_data["drop"]:
                item_id, item_min, item_max, item_chance = drop
                item_chance = round(item_chance * 1e6)

                for category in categories:
                    category_id = eval(category["id"])

                    if category_id == -1:
                        # Spoils are already done, no need to worry about them here
                        continue
                    else:
                        d = category.find("drop", {"itemid": item_id})
                        if d is not None:
                            d["chance"] = str(item_chance)
                            d["min"] = str(item_min)
                            d["max"] = str(item_max)

            # This part performs step 2a
            if npc_data["drop"] == []:
                for category in categories:
                    category_id = eval(category["id"])

                    if category_id == -1:
                        # Spoils are already done, no need to worry about them here
                        continue
                    else:
                        category.string = ""

    return soups


def step_3(soups, npcs_data, old_xml_dir):
    print(
        "Step 3: Add categories for items that have a unanimous category for mobs "
        "that have less than 4 categories, and no title"
    )
    d1 = parse_xml_npc.parse_xml(old_xml_dir)
    items = get_unanimous_item_categories(d1)
    for file, soup in soups.items():

        npcs = soup.find_all("npc")

        for npc in npcs:
            npc_id = eval(npc["id"])
            npc_title = npc["title"]

            if npc_title != "":
                continue

            try:
                npc_data = npcs_data[npc_id]
            except:
                continue

            drops = npc.select("drops")[0]
            categories = drops.select("category")

            if len(categories) > 4:
                continue

            needed_categories = [-1]
            for drop in npc_data["drop"]:
                item_id, item_min, item_max, item_chance = drop
                if item_id not in items:
                    break
                else:
                    needed_categories.append(items[item_id])
            else:
                needed_categories = np.unique(needed_categories)
                for cat_id in needed_categories:
                    cat = drops.find("category", {"id": str(cat_id)})
                    if cat is None:
                        new_category = soup.new_tag("category", id=str(cat_id))
                        drops.append(new_category)
                        drops.append("\n")
                    elif cat_id != -1:
                        cat.string = ""
                        cat.append("\n")

                categories = drops.select("category")

                for category in categories:
                    category_id = eval(category["id"])
                    if category_id == -1:
                        # Spoils are already done, no need to worry about them here
                        continue

                    for drop in npc_data["drop"]:
                        item_id, item_min, item_max, item_chance = drop
                        item_chance = round(item_chance * 1e6)
                        correct_cat = items[item_id]
                        if correct_cat == category_id:
                            new_drop = soup.new_tag(
                                "drop",
                                itemid=item_id,
                                min=item_min,
                                max=item_max,
                                chance=item_chance,
                            )
                            category.append(new_drop)
                            category.append("\n")

    return soups


def parse_xml_item(item_dir):
    # Categories:
    #   1: Weapon/Armor
    item_files = []
    for file in os.listdir(item_dir):
        if file.endswith(".xml"):
            item_files.append(file)

    for file in item_files:
        with open(os.path.join(item_dir, file), "r") as f:
            contents = f.read()
        soup = BeautifulSoup(contents, "xml")
    return


def find_item_categories(npc_dir):
    npc_files = []
    for file in os.listdir(npc_dir):
        if file.endswith(".xml"):
            npc_files.append(file)

    count = 0
    items = {}
    mobs = {}
    mob_count = {}
    for file in npc_files:
        with open(os.path.join(npc_dir, file), "r") as f:
            contents = f.read()
        soup = BeautifulSoup(contents, "xml")

        npcs = soup.find_all("npc")
        for npc in npcs:
            npc_id = eval(npc["id"])
            mob_count[npc_id] = 0
            categories = npc.find_all("category")
            for category in categories:
                category_id = eval(category["id"])

                if category_id == -1:
                    # No need to consider spoils
                    continue

                drops = category.find_all("drop")
                for drop in drops:
                    item_id = eval(drop["itemid"])
                    if item_id not in items:
                        items[item_id] = []
                        mobs[item_id] = []
                    items[item_id].append(category_id)
                    mobs[item_id].append(npc_id)

    for id in items.keys():
        cat_mode = scipy.stats.mode(items[id]).mode[0]
        for i, cat in enumerate(items[id]):
            if cat != cat_mode:
                mob_count[mobs[id][i]] += 1

    mob_count_ = []
    for mob_id, count in mob_count.items():
        mob_count_.append([mob_id, count])
    mob_count_ = np.array(mob_count_)

    s = np.argsort(mob_count_[:, 1])[::-1]

    return items


def find_item_diffs(drop_file_xml, drop_file_l2portal):
    drop_file_xml = "drop_data_xml.json"
    drop_file_l2portal = "drop_data_l2portal.json"

    key_str2int = lambda d: {int(k) if k.lstrip("-").isdigit() else k: v for k, v in d.items()}

    drop_data_xml = json.load(open(drop_file_xml, "r"), object_hook=key_str2int)
    drop_data_l2portal = json.load(open(drop_file_l2portal, "r"), object_hook=key_str2int)

    has_additional = []
    for npc_id in drop_data_xml.keys():

        d1 = np.array(drop_data_xml[npc_id]["drop"])
        d2 = np.array(drop_data_l2portal[npc_id]["drop"])

        if d1.shape[0] == 0 and d2.shape[0] != 0:
            has_additional.append([npc_id, 1, 0, 0])
            continue

        if d2.shape[0] == 0 and d1.shape[0] != 0:
            num_cats = len(np.unique(d1[:, -1]))
            has_additional.append([npc_id, 1, num_cats])
            continue

        num_cats = len(np.unique(d1[:, -1]))
        d1s = set(d1[:, 0])
        d2s = set(d2[:, 0])
        if d1s != d2s:
            has_additional.append([npc_id, 1, num_cats])
            continue

        has_additional.append([npc_id, 0, num_cats])

    has_additional = np.array(has_additional)

    return has_additional


def perform_checks(new_data_file):
    print("--Performing Checks--")

    npc_dir = os.path.join(os.getcwd(), "npcs_new")
    d1 = parse_xml_npc.parse_xml(npc_dir)
    d2 = json.load(open(new_data_file, "r"), object_hook=key_str2int)

    #if d1.keys() != d2.keys():
    #    raise ValueError("Sources have different NPCs")

    check_step_1(d1, d2)
    remaining_ids = check_step_2(d1, d2)
    # remaining_ids = check_step_3(d1, d2, remaining_ids)
    print("remaining_ids: " + str(remaining_ids))
    print("--All Checks Passed--")


def check_step_1(d1, d2):

    for id in d1.keys():
        s1 = d1[id]["spoil"]
        s2 = d2[id]["spoil"]

        if s1 == [] and s2 == []:
            continue
        if s1 == [] or s2 == []:
            print("id:" + str(id))
            print("s1:" + str(s1))
            print("s2:" + str(s2))
            raise ValueError("check_step_1 failed")

        dd1 = np.array(s1)[:, :-1]
        dd2 = np.array(s2)
        if not np.allclose(dd1, dd2, rtol=0.01):
            print("id:"+ str(id))
            print("s1:"+ str(s1))
            print("s2:"+ str(s2))
            raise ValueError("check_step_1 failed")
    print("check_step_1 passed")


def check_step_2(d1, d2):
    count = 0
    count_ = 0
    remaining_ids = []
    for id in d1.keys():
        s1 = d1[id]["drop"]
        s2 = d2[id]["drop"]

        if s1 == [] and s2 == []:
            count += 1
            continue
        if s1 == [] or s2 == []:
            count_ += 1
            remaining_ids.append(id)
            continue

        dd1 = np.array(s1)[:, :-1]
        dd2 = np.array(s2)

        idx1 = np.argsort(dd1[:, 0])
        idx2 = np.argsort(dd2[:, 0])

        dd1 = dd1[idx1, :]
        dd2 = dd2[idx2, :]

        if np.array_equal(dd1[:, 0], dd2[:, 0]):
            count += 1
            if not np.allclose(dd1, dd2, rtol=0.01):
                raise ValueError("check_step_2 failed")
        else:
            remaining_ids.append(id)
            count_ += 1
    print("check_step_2 passed, " + str(len(remaining_ids)) + " items remaining")
    print("checked: " + str(count) + ", remaining: " + count_)
    return remaining_ids


def get_unanimous_item_categories(d1):

    items = {}
    for id in d1.keys():
        if d1[id]["title"] != "":
            continue
        s1 = d1[id]["drop"]

        if s1 == []:
            continue

        dd1 = np.array(s1)
        num_cats = len(np.unique(dd1[:, -1]))

        if num_cats <= 3:
            for i in range(dd1.shape[0]):
                item_id = dd1[i, 0].astype(int)
                item_cat = dd1[i, -1].astype(int)
                if item_id not in items:
                    items[item_id] = []
                items[item_id].append(item_cat)

    items_ = items.copy()
    for item_id, item_cats in items_.items():
        if len(np.unique(item_cats)) == 1:
            items[item_id] = item_cats[0]
        else:
            # print(item_id)
            del items[item_id]

    return items


if __name__ == "__main__":

    old_xml_dir = os.path.join(os.getcwd(), "npcs")
    new_xml_dir = os.path.join(os.getcwd(), "npcs_new")
    old_data_file = "drop_data_xml.json"
    new_data_file = "drop_data_l2informer.json"

    # item_dir = os.path.join(os.getcwd(), "items")
    # item_data = parse_xml_item(item_dir)
    npc_dir_old = os.path.join(os.getcwd(), "npcs")
    item_categories = find_item_categories(npc_dir_old)

    has_diff = find_item_diffs(old_data_file, new_data_file)
    print has_diff
    create_new_xml(old_xml_dir, new_xml_dir, new_data_file, has_diff)

    # Check results
    #perform_checks(new_data_file)
