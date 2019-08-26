import os
import sys
import json
from bs4 import BeautifulSoup
import requests


def save_npc_data(soup, mob_id, npc_file):
    html = soup.prettify("utf-8")
    with open(npc_file, "wb") as file:
        file.write(html)

def scrape_l2portal(drop_data_xml, out_file, npc_save_dir):

    if not os.path.exists(npc_save_dir):
        os.makedirs(npc_save_dir)

    num_mobs = len(drop_data_xml)
    count = 0

    drop_data = {}
    for mob_id, drop_actual in drop_data_xml.items():

        npc_file = os.path.join(npc_save_dir, f"{mob_id}.html")
        if not os.path.exists(npc_file):
            url = f"http://gracia.l2portal.com/Npc.aspx?ID={mob_id}"

            r = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, features="html.parser")

            save_npc_data(soup, mob_id, npc_file)
        else:
            with open(npc_file, "r") as f:
                contents = f.read()
            soup = BeautifulSoup(contents, features="html.parser")

        mob_name = soup.find("head").find("title").text.split(' - ')[0].replace('\r\n\t','')

        drops = {"drop": [], "spoil": []}
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

        drop_data[mob_id] = drops
        count += 1
        if count % 25 == 0 or count == num_mobs:
            json.dump(drop_data, open(out_file, 'w'))
            print(f"\nScraped & saved {count} / {num_mobs}\n")
            sys.stdout.flush()

    print("Scraping complete")
    return drop_data


def find_item_name(item_id):
    url = f"http://gracia.l2portal.com/gracia/Item.aspx?ID={item_id}"

    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    item_name = soup.find("head").find("title").text.split(' - ')[0].replace('\r\n\t','')

    return item_name

if __name__ == "__main__":
    drop_file = 'drop_data_xml.json'
    out_file = 'drop_data_l2portal.json'
    npc_save_dir = os.path.join(os.getcwd(), 'l2portal')

    key_str2int = lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()}
    drop_data_xml = json.load(open(drop_file, 'r'), object_hook=key_str2int)
    drop_data = scrape_l2portal(drop_data_xml, out_file, npc_save_dir)
