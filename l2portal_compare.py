import sys
import numpy as np
from bs4 import BeautifulSoup
import requests


def compare_to_l2portal(drop_data):

    num_mobs = len(drop_data)
    count = 0

    for mob_id, drop_actual in drop_data.items():
        sys.stdout.flush()
        
        url = f"http://gracia.l2portal.com/Npc.aspx?ID={mob_id}"

        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, features="html.parser")

        mob_name = soup.find("head").find("title").text.split(' - ')[0].replace('\r\n\t','')

        drops = {"drop": [], "spoil": []}
        items = {}
        for drop_type in drops.keys():
            data = soup.find(
                "table", {"id": f"ctl00_ContentPlaceHolder1_GVNpc{drop_type.title()}"}
            )
            for drop in data.find_all("tr"):
                if drop.has_attr("class") and drop["class"][0] == "HeaderStyle2":
                    continue

                parts = drop.find_all("td")

                if len(parts) != 5:
                    # Assume that if len(parts)!=5 then not an item drop and move on:
                    continue

                item_id = eval(parts[1].select("a")[0]["href"].split("=")[-1])
                item_name = parts[1].select("a")[0].text
                items[item_id] = item_name

                for span in parts[3].select("span"):
                    if "LblMin" in span["id"]:
                        item_min = eval(span.text)
                    elif "LblMax" in span["id"]:
                        item_max = span.text

                if item_max == "":
                    # If item_max is undefined, set it as same as item_min
                    item_max = item_min
                else:
                    # Else format accordingly:
                    item_max = eval(item_max.split("- ")[-1])

                chance = parts[4].select("span")[0].text
                # Some of the chances are fractions, and some percent, account for that here:
                if chance[-1] == "%":
                    item_chance = eval(chance[:-1]) / 100
                else:
                    item_chance = eval(parts[4].select("span")[0].text)

                drops[drop_type].append([item_id, item_min, item_max, item_chance])

        diff_drop = find_diff(drop_actual["drop"], drops["drop"], type="drop", items=items)
        diff_spoil = find_diff(drop_actual["spoil"], drops["spoil"], type="spoil", items=items)
        if not (diff_drop == [] and diff_spoil == []):
            print(f"\nCheck Failed - mob_id: {mob_id} ({mob_name})")
            for i, diff in enumerate(diff_drop):
                if i == 0:
                    print("---Drops---")
                print(diff)

            for i, diff in enumerate(diff_spoil):
                if i == 0:
                    print("---Spoils---")
                print(diff)

        count += 1
        if count % 25 == 0 or count == num_mobs:
            print(f"\nChecked {count} / {num_mobs}\n")
    print("Checking complete")


def find_item_name(item_id):
    url = f"http://gracia.l2portal.com/gracia/Item.aspx?ID={item_id}"

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    item_name = soup.find("head").find("title").text.split(' - ')[0].replace('\r\n\t','')

    return item_name


def find_diff(drops1, drops2, type, items):
    # Check if the provided lists of drops are equivalent

    out = []
    drops1 = np.array(drops1)
    drops2 = np.array(drops2)

    if drops1.shape[0] == 0 or drops2.shape[0] == 0:
        if drops1.shape[0] != 0:
            for drop in drops1:
                out.append(f"Additional {type} in DB, item id: {drop[0]} ({find_item_name(drop[0])})")

        if drops2.shape[0] != 0:
            for drop in drops2:
                out.append(f"Additional {type} in Web, item id: {drop[0]} ({items[drop[0]]})")

        return out

    i = np.argsort(drops1[:, 0])
    drops1 = drops1[i, :]

    i = np.argsort(drops2[:, 0])
    drops2 = drops2[i, :]

    # First check that the drops and amounts are the same:
    if not np.array_equal(drops1[:, :3], drops2[:, :3]):
        all_drops = set(np.concatenate((drops1[:, 0].ravel(), drops2[:, 0].ravel())).astype(int))

        # if not np.array_equal(drops1[:, 0], drops2[:, 0]):
        #     for drop in drops1[:, 0].astype(int):
        #         if drop not in drops2[:, 0]:
        #             out.append(f"Additional {type} in DB: {drop} ({items[drop]})")
        #
        #     for drop in drops2[:, 0].astype(int):
        #         if drop not in drops1[:, 0]:
        #             out.append(f"Additional {type} in Web: {drop} ({items[drop]})")

        for drop in all_drops:
            w1 = np.where(drops1[:, 0] == drop)[0]
            w2 = np.where(drops2[:, 0] == drop)[0]
            if len(w1) == 0:
                out.append(f"Additional {type} in Web: {drop}  ({items[drop]})")

            elif len(w2) == 0:
                out.append(f"Additional {type} in DB: {drop} ({find_item_name(drop)})")

            else:
                d1 = drops1[w1[0], :]
                d2 = drops2[w2[0], :]

                if not np.array_equal(d1[1:3], d2[1:3]):
                    out.append(
                        f"Unequal {type} amount for item {drop} ({items[drop]}): "
                        f"{tuple(d1[1:3].astype(int))} (DB) "
                        f"vs {tuple(d2[1:3].astype(int))} (Web)"
                    )

                # Now check that chances are same (web within 1% tolerance of db):
                rtol = 0.01
                if not np.allclose(d1[3], d2[3], rtol=rtol):
                    out.append(
                        f"Unequal {type} chance for item {drop} ({items[drop]}):"
                        f"{d1[3]} (DB) vs {d2[3]} (Web)"
                    )

    return out


def read_drop_file(drop_file):

    drop_data = {}

    with open(drop_file, "r") as f:
        line = f.readline().strip()
        empty_count = 0
        while empty_count < 100:
            if not line:
                line = f.readline().strip()
                empty_count += 1
                continue
            else:
                empty_count = 0

            if line[0] == "(" and (")," in line or ");" in line):
                try:
                    idx = line.index("),")
                except ValueError:
                    idx = line.index(");")

                data = eval(line[: idx + 1])

                mob_id, item_id, item_min, item_max, category, chance = data

                if mob_id not in drop_data:
                    drop_data[mob_id] = {"drop": [], "spoil": []}

                if category == -1:
                    drop_data[mob_id]["spoil"].append([item_id, item_min, item_max, chance / 1e6])
                else:
                    drop_data[mob_id]["drop"].append([item_id, item_min, item_max, chance / 1e6])

            line = f.readline().strip()

    return drop_data


if __name__ == "__main__":
    drop_file = "droplist.sql"
    drop_data_actual = read_drop_file(drop_file)
    compare_to_l2portal(drop_data_actual)
