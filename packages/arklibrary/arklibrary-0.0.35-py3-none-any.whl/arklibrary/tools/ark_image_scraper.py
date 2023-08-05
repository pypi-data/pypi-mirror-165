from bs4 import BeautifulSoup
from pathlib import Path
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
import re
import difflib
import numpy as np
import cv2

creatures_folder = Path.cwd() / Path('xd/creatures')
items_folder = Path.cwd() / Path('xd/items')


def get_driver():
    d = webdriver.Chrome(
        executable_path=r"C:\Users\optimus\OneDrive\Developer\.id\.drivers\chrome\windows\94.0.4606.61\chromedriver.exe")
    return d


def iter_web_links(file: Path):
    data = []
    with open(file, 'r') as r:
        data = json.load(r)
    for item in data:
        yield item['name'], item['url']


def get_dino_img(driver: webdriver.Chrome, name: str):
    try:
        module = driver.find_element_by_xpath("//div[@class='info-arkitex info-module']")
        images = module.find_elements_by_tag_name("img")
    except:
        return []
    match = r'.*\.png|.*\.jpg|.*\.svg'
    links = []
    for img in images:
        try:
            alt = img.get_property('alt').lower()
            fromatted_alt = alt.replace("dossier ", "").replace("image", "").replace("img", "").replace(".svg", "")\
                .replace(".png", "").replace(".jpg", "").replace(".jpeg", "").replace("aberrant", "").replace("r-", "")\
                .replace("corrupted", "").replace("(alpha)", "").replace("(beta)", "")\
                .replace("(gamma)", "").replace("tek", "").replace("malfunctioned", "").replace("x-", "").strip()
            formatted_alt = "rock elemental" if "golem" in formatted_alt else formatted_alt
            formatted_name = name.lower().replace("aberrant", "").replace("r-", "").replace("corrupted", "")\
                .replace("brute", "").replace("tamed", "").replace("(alpha)", "").replace("(beta)", "")\
                .replace("(gamma)", "").replace("tek", "").replace("  ", " ").strip()
            seq = difflib.SequenceMatcher(None, formatted_name, fromatted_alt)
            if alt is not None:
                # links.append(img.get_property('src'))
                url = re.findall(match, img.get_property('src'))
                if len(url) > 0:
                    links += [(seq.ratio(), url[0])]
        except Exception as e:
            print(e)
    chosen = list(np.unique([l[1] for l in links if l[0] > 0.5]))
    if len(chosen) == 0:
        print('\033[34m' + f"[{name}]: {chosen}" + '\033[0m')
        text = input(f"Would you like to manually enter image url for {name}? ")
        if text is None or text.strip() == '':
            return chosen
        else:
            url = re.findall(match, text)
            chosen.append(url[0])
        text = input(f"Would you like to manually enter image url for {name}? ")
        if text is None or text.strip() == '':
            return chosen
        else:
            url = re.findall(match, text)
            chosen.append(url[0])
    if len(chosen) <= 0:
        print('\033[31m' + f"[{name}] Error: Didn't find images." + '\033[0m')
        raise Exception("Unable to find or choose a suitable an image url.")
    elif len(chosen) == 1:
        print('\033[34m' + f"[{name}]: {chosen}" + '\033[0m')
        text = input(f"Would you like to manually enter image url for {name}? ")
        if text is None or text.strip() == '':
            return chosen
        else:
            url = re.findall(match, text)
            chosen.append(url[0])
    img_weights = []
    for image in chosen:
        content = requests.get(image).content
        cv = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)
        area = cv.shape[0] * cv.shape[1]
        img_weights.append((area, image))
    img_weights.sort()
    sorted_chosen = [l[1] for l in img_weights]
    print('\033[92m' + f"[{name}]: {sorted_chosen}" + '\033[0m')
    return sorted_chosen


def get_item_img(driver: webdriver.Chrome, name: str):
    try:
        module = driver.find_element_by_xpath("//div[@class='info-arkitex info-module']")
        images = module.find_elements_by_tag_name("img")
    except:
        return []
    match = r'.*\.png|.*\.jpg|.*\.svg'
    links = []
    for img in images:
        try:
            alt = img.get_property('alt').lower()
            fromatted_alt = alt.replace("dossier ", "").replace("image", "").replace("img", "").replace(".svg", "")\
                .replace(".png", "").replace(".jpg", "").replace(".jpeg", "").replace("", "").replace("(", "")\
                .replace(")", "").replace("scortched earth", "").replace("extinction", "").replace("genesis", "")\
                .replace("%29", "").replace("%28", "").replace("aberration", "").strip()
            formatted_name = name.lower().replace("  ", " ").strip()
            seq = difflib.SequenceMatcher(None, formatted_name, fromatted_alt)
            if alt is not None:
                # links.append(img.get_property('src'))
                url = re.findall(match, img.get_property('src'))
                if len(url) > 0:
                    links += [(seq.ratio(), url[0])]
        except Exception as e:
            print(e)
    chosen = list(np.unique([l[1] for l in links if l[0] > 0.5]))
    if len(chosen) == 0:
        print('\033[34m' + f"[{name}]: {chosen}" + '\033[0m')
        text = input(f"Would you like to manually enter image url for {name}? ")
        if text is None or text.strip() == '':
            return None
        else:
            url = re.findall(match, text)
            chosen.append(url[0])
    if len(chosen) <= 0:
        print('\033[31m' + f"[{name}] Error: Didn't find images." + '\033[0m')
        raise Exception("Unable to find or choose a suitable an image url.")
    elif len(chosen) > 1:
        print('\033[34m' + f"[{name}]: {chosen}" + '\033[0m')
        text = input(f"Would you like to manually enter the ONLY image url for {name}? ")
        if text is None or text.strip() == '':
            return list(chosen)
        else:
            url = re.findall(match, text)
            print('\033[92m' + f"[{name}]: {url[0]}" + '\033[0m')
            return str(url[0])
    print('\033[92m' + f"[{name}]: {str(chosen[0])}" + '\033[0m')
    return str(chosen[0])


def save_image(content: bytes, url: str, name: str, map_file: Path, path: Path):
    relative = path / Path('images')
    root_dir = path / Path('images')
    if not root_dir.exists():
        root_dir.mkdir()
    json_path = path / Path('images/paths.json')
    if not json_path.exists():
        with open(json_path, 'w') as w:
            json.dump({}, w)
    extension = Path(url).suffix
    folder = relative / Path(map_file.stem)
    with open(json_path, 'r') as r:
        data = json.load(r)

    if name not in data:
        data[name] = []

    formatted = name.lower().replace("-", " ").replace(".", " ").replace("'", "")\
        .replace("`", "").replace(" ", "_").replace("\"", "")
    stem = f"{formatted}_{len(data[name])}"


    file = folder / Path(stem + extension)
    data[name].append(str(file.relative_to(relative)))

    with open(json_path, 'w') as w:
        json.dump(data, w)

    if not folder.is_dir():
        folder.mkdir()

    with open(file, 'wb') as w:
        w.write(content)

    print('\033[92m' + f"[SAVED] {name}: {str(file.relative_to(relative))}" + '\033[0m')


def get_description(driver: webdriver.Chrome):
    try:
        e = driver.find_element_by_xpath("//div[@class='dossier-background dossier-text']")
        print('\033[92m' + f"[DESC]: {e.text}" + '\033[0m')
        return e.text.replace("\n", "").replace("  ", "")
    except Exception as e:
        print(e)


def get_color_regions(driver: webdriver.Chrome):
    match = r'.*\.png|.*\.jpg|.*\.svg'

    try:
        data = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None}
        container = driver.find_element_by_class_name("paintregion-container")
        regions = container.find_elements_by_xpath("//div[@class='paintregion']")[:6]
        for i, reg in enumerate(regions):
            if 'not used' not in reg.text.lower():
                data[i] = {}
                data[i]['text'] = reg.text.replace("\n", " ")
                src = reg.find_element_by_tag_name("img").get_property('src')
                imgs = re.findall(match, src)
                if len(imgs) > 0:
                    data[i]['img'] = imgs[0]
                data[i]['color_ids'] = {}
                data[i]['rgb'] = []
                color_squares = reg.find_elements_by_class_name("color-square")
                for square in color_squares:
                    text = square.get_property('title')
                    color, code = text.replace(")", "").split("\xa0(")
                    data[i]['color_ids'][color] = int(code)
                    style = square.get_attribute('style')
                    html_color = re.findall(r'[0-9]+, [0-9]+, [0-9]+', style)[0]
                    data[i]['rgb'].append([int(v) for v in html_color.split(", ")])
        return data
    except Exception as e:
        print('\033[31m' + "[COLOR] Unable to locate color regions for this creature." + '\033[0m')
        print(e)


def get_short_description(driver: webdriver.Chrome):
    try:
        quote = driver.find_elements_by_xpath("//td[@class='quote-left']//parent::tr")[0].text
        return quote.replace("\n", " ").replace("“", "").replace("„", "").strip()
    except Exception as e:
        print('\033[31m' + "[DESC] Unable to locate a description for this creature." + '\033[0m')
        raise e


def get_by_name_from_map(name:str, map: Path):
    with open(map, 'r') as r:
        dinos = json.load(r)
    for dino in dinos:
        if name in dino:
            return dino


def get_creature_data():
    driver = get_driver()
    try:
        sleep(2)
        creatures_folder = Path.cwd() / Path('creatures')
        for file in creatures_folder.iterdir():
            data = {}
            with open(file, 'r') as r:
                data = json.load(r)
            iterlinks = iter_web_links(file)
            for name, link in iterlinks:
                driver.get(link)
                sleep(0.5)
                try:
                    if "brute" not in name.lower():
                        img = get_dino_img(driver, name)
                        desc = get_description(driver)
                        color = get_color_regions(driver)
                        for url in img:
                            content = requests.get(url).content
                            save_image(content, url, name, file, creatures_folder)
                    else:
                        img = None
                        desc = None
                        color = None
                    for i in range(len(data)):
                        if name in data[i]['name']:
                            data[i]['images'] = img
                            data[i]['description'] = desc
                            data[i]['color_regions'] = color
                except Exception as e:
                    print(f"Error at {file.name} on {name}")
                    print(e)

            with open(file, 'w') as w:
                json.dump(data, w)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def get_creature_images():
    driver = get_driver()
    try:
        sleep(3)
        creatures_folder = Path.cwd() / Path('creatures')
        for file in creatures_folder.iterdir():
            data = {}
            with open(file, 'r') as r:
                data = json.load(r)
            iterlinks = iter_web_links(file)
            for name, link in iterlinks:
                driver.get(link)
                sleep(0.5)
                try:
                    if "brute" in name.lower():
                        continue
                    img = get_dino_img(driver, name)
                    for i in range(len(data)):
                        if name in data[i]['name']:
                            data[i]['images'] = img
                    for url in img:
                        content = requests.get(url).content
                        save_image(content, url, name, file, creatures_folder)
                except Exception as e:
                    print(f"Error at {file.name} on {name}")
                    print(e)

            with open(file, 'w') as w:
                json.dump(data, w)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def get_items_data():
    driver = get_driver()
    try:
        sleep(1)
        items_folder = Path.cwd() / Path('items')
        tools = items_folder / Path("xd.json")
        recipes = items_folder / Path("recipes.json")
        for file in [tools, recipes]:
            if file.is_dir():
                continue
            data = {}
            with open(file, 'r') as r:
                data = json.load(r)
            iterlinks = iter_web_links(file)
            for name, link in iterlinks:
                driver.get(link)
                sleep(0.5)
                try:
                    img = get_item_img(driver, name)
                    short_desc = get_short_description(driver)
                    if type(img) == str:
                        content = requests.get(img).content
                        save_image(content, img, name, file, items_folder)
                    elif type(img) == list:
                        for url in img:
                            content = requests.get(url).content
                            save_image(content, url, name, file, items_folder)
                    for i in range(len(data)):
                        if name in data[i]['name']:
                            data[i]['image'] = img
                            data[i]['short_description'] = short_desc
                except Exception as e:
                    print(f"Error at {file.name} on {name}")
                    print(e)

            with open(file, 'w') as w:
                json.dump(data, w)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


if __name__ == "__main__":
    get_items_data()
    # "Archer Flex" Emote
    # "Bicep Smooch" Emote
    # "Dance" Emote
    # "Zombie" Emote
