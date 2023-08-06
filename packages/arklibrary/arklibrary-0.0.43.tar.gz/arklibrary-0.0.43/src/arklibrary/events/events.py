default = [-366253, 53155, -48967]

from gamedriver import Admin
from gamedriver import Island
from time import sleep
from random import choices
import numpy as np
from pathlib import Path


default = [358401, 24641, -3101]

import json


def save_current_coordinates(map, name, num_drops, coords):
    """ Stores the coordinates into file with a name
    :param name: str, name for the coordinates
    """
    data = {"center": {}, "gen1": {}, "gen2": {}, "island": {},
            "scortched": {}, "ragnarok": {}, "extinction": {}, "aberration": {}}
    if map not in data:
        raise NotImplemented("'{}' isn't part of the map list: {}".format(map, data.keys()))
    file_path = Path.cwd() / Path('logs/saved_coordinates.json')
    if file_path.exists():
        with open(file_path, 'r') as r:
            data = json.load(r)
    if str(num_drops) not in data[map][name]:
        data[map][name][str(num_drops)] = coords
    with open(file_path, "w") as w:
        json.dump(data, w)


def generate_obelisk_drop_coords(admin, map: str, color: str, number_of_drops: int):
    with open("logs/saved_coordinates.json", 'r') as r:
        data = json.load(r)
    coords = None
    name = None
    if color.lower() == 'blue':
        coords = data[map]['blue_obelisk']
        name = 'blue_obelisk_drops'
    elif color.lower() == 'green':
        coords = data[map]['green_obelisk']
        name = 'green_obelisk_drops'
    elif color.lower() == 'red':
        coords = data[map]['red_obelisk']
        name = 'red_obelisk_drops'
    x, y, z, _, _ = coords.values()
    circumference_coords = obelisk_circle_coords([x, y, z], spokes=number_of_drops)
    coordinates = []
    finished = False
    while not finished:
        try:
            coordinates.clear()
            for i, ccc in enumerate(circumference_coords):
                admin.teleport_xyz(*ccc).execute()
                sleep(8)
                admin.driver.copy_coords()
                new_ccc_str = admin.driver.app.get_from_clipboard()
                coordinates.append([float(c) for c in new_ccc_str.split()][:3])
                if len(coordinates) == number_of_drops:
                    finished = True
                elif i + 1 != len(coordinates):
                    break
        except Exception:
            pass
        except KeyboardInterrupt:
            finished = True
    save_current_coordinates(map, name, number_of_drops, coordinates)


def obelisk_circle_coords(obelisk_center_coord, spokes=10):
    x_center, y_center, _ = obelisk_center_coord
    radius = 1763.2620338452252
    offsets = np.linspace(0, 360, spokes)
    coords = []
    for offset in offsets:
        x = radius * np.cos(offset)
        y = radius * np.sin(offset)
        coords.append((x_center + x, y + y_center, 0))
    return coords


def drop_the_supplies(admin, map, quantity=8, quality=0, only=False):
    drops = [
        Island.WHITE_BEACON,
        Island.WHITE_BEACON_DOUBLE_ITEMS,
        Island.GREEN_BEACON,
        Island.GREEN_BEACON_DOUBLE_ITEMS,
        Island.BLUE_BEACON,
        Island.BLUE_BEACON_DOUBLE_ITEMS,
        Island.PURPLE_BEACON,
        Island.PURPLE_BEACON_DOUBLE_ITEMS,
        Island.YELLOW_BEACON,
        Island.YELLOW_BEACON_DOUBLE_ITEMS,
        Island.RED_BEACON,
        Island.RED_BEACON_DOUBLE_ITEMS
    ][quality:]

    with open("gamedriver/saved_coordinates.json", 'r') as r:
        data = json.load(r)
    red = data[map]['red_obelisk_drops'][str(quantity)]
    green = data[map]['green_obelisk_drops'][str(quantity)]
    blue = data[map]['blue_obelisk_drops'][str(quantity)]

    if only:
        for ob_coords in [red, green, blue]:
            for coords in ob_coords:
                x, y, z = coords
                admin.teleport_xyz(x, y, z)
                admin.spawn_beacon(drops[0])
    else:
        weights = (100, 90, 80, 70, 60, 50, 30, 25, 20, 15, 10, 5)[quality:]
        for ob_coords in [red, green, blue]:
            shuffled_drops = choices(drops, weights=weights, k=len(ob_coords))
            for pair in zip(ob_coords, shuffled_drops):
                coords, drop = pair
                x, y, z = coords
                admin.teleport_xyz(x, y, z)
                admin.spawn_beacon(drop)
    admin.teleport_xyz(*default)
    admin.execute()


def event_supply_drops(admin, map, quantity=4, quality=4):
    if quality < 4:
        message = "Gamma Supply Drop: Event in {} seconds. Random drops will spawn at every obelisks. PVP is allowed."
    if 4 <= quality < 8:
        message = "Beta Supply Drop: Event in {} seconds. Random drops will spawn at every obelisks. PVP is allowed."
    if 8 <= quality:
        message = "Alpha supply: drop Event in {} seconds. Random drops will spawn at every obelisks. PVP is allowed."
    admin.broadcast(message.format(60))
    admin.execute()
    sleep(30)
    admin.broadcast(message.format(30))
    admin.execute()
    sleep(20)
    admin.broadcast(message.format(5))
    admin.execute()

    drop_the_supplies(admin, map, quantity, quality)


if __name__ == '__main__':
    pass