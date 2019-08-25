import numpy as np
from bs4 import BeautifulSoup
import requests


def compare_to_l2portal(drop_data):

    num_mobs = len(drop_data)
    count = 0

    for key, drop_actual in drop_data.items():

        url = f'http://gracia.l2portal.com/Npc.aspx?ID={key}'

        r  = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, features='html.parser')

        drop_data = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_GVNpcDrop'})
        spoil_data = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_GVNpcSpoil'})

        for drop_type in ['Drop', 'Spoil']:
            drops = []
            data = soup.find('table', {'id': f'ctl00_ContentPlaceHolder1_GVNpc{drop_type}'})
            for drop in data.find_all('tr'):
                if drop.has_attr('class') and drop['class'][0] == 'HeaderStyle2':
                    continue

                parts = drop.find_all('td')

                if len(parts) != 5:
                    # Assume that if len(parts)!=5 then not an item drop and move on:
                    continue

                item_id = eval(parts[1].select('a')[0]['href'].split('=')[-1])

                for span in parts[3].select('span'):
                    if 'LblMin' in span['id']:
                        item_min = eval(span.text)
                    elif 'LblMax' in span['id']:
                        item_max = span.text

                if item_max == '':
                    # If item_max is undefined, set it as same as item_min
                    item_max = item_min
                else:
                    # Else format accordingly:
                    item_max = eval(item_max.split('- ')[-1])

                chance = parts[4].select('span')[0].text
                # Some of the chances are fractions, and some percent, account for that here:
                if chance[-1] == '%':
                    item_chance = eval(chance[:-1])/100
                else:
                    item_chance = eval(parts[4].select('span')[0].text)

                drops.append([item_id, item_min, item_max, item_chance])

            same = check_same(drop_actual[drop_type.lower()], drops)
            if not same:
                print(f'Check Failed - mob_id: {key} - drop_type: {drop_type.lower()}')
                print(f'Drops Actual: {drop_actual[drop_type.lower()]})')
                print(f'Drops Web: {drops}')

        count += 1
        if count % 25 == 0 or count == num_mobs:
            print(f'Checked {count} / {num_mobs}')
    print('Checking complete')

def check_same(drops1, drops2):
    # Check if the provided lists of drops are equivalent
    drops1 = np.array(drops1)
    drops2 = np.array(drops2)

    if drops1.shape[0] == 0 and drops2.shape[0] == 0:
        if drops1.shape[0] != 0 or drops2.shape[0] != 0:
            return False
        return True

    i = np.argsort(drops1[:, 0])
    drops1 = drops1[i, :]

    i = np.argsort(drops2[:,0])
    drops2 = drops2[i, :]

    # First check that the drops and amounts are the same:
    if not np.array_equal(drops1[:, :3], drops2[:, :3]):
        return False

    # Now check that chances are same (within 1% tolerance):
    if not np.allclose(drops1[:, 3], drops2[:, 3], rtol=0.01):
        return False

    # If both above checks pass, return true:
    return True

def read_drop_file(drop_file):

    drop_data = {}

    with open(drop_file, 'r') as f:
        line = f.readline().strip()
        empty_count = 0
        while empty_count < 100:
            if not line:
                line = f.readline().strip()
                empty_count += 1
                continue
            else:
                empty_count = 0

            if line[0] == '(' and ('),' in line or ');' in line):
                try:
                    idx = line.index('),')
                except:
                    idx = line.index(');')

                data = eval(line[:idx+1])

                mob_id, item_id, item_min, item_max, category, chance = data

                if mob_id not in drop_data:
                    drop_data[mob_id] = {'drop': [], 'spoil': []}

                if category == -1:
                    drop_data[mob_id]['spoil'].append([item_id, item_min, item_max, chance/1e6])
                else:
                    drop_data[mob_id]['drop'].append([item_id, item_min, item_max, chance/1e6])

            line = f.readline().strip()

    return drop_data


if __name__ == '__main__':
    drop_file = 'droplist.sql'
    drop_data_actual = read_drop_file(drop_file)
    compare_to_l2portal(drop_data_actual)
