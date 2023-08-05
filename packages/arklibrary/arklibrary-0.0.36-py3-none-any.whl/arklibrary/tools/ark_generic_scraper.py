from bs4 import BeautifulSoup
from pathlib import Path
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from time import sleep


items_id_webpage = "https://ark.fandom.com/wiki/Item_IDs"
creatures_id_webpage = "https://ark.fandom.com/wiki/Creature_IDs"

def get_driver():
    d = webdriver.Chrome(executable_path=r"C:\Users\optimus\OneDrive\Developer\.id\.drivers\chrome\windows\94.0.4606.61\chromedriver.exe")
    return d



def click_show(driver: webdriver.Chrome):
    driver.get(items_id_webpage)
    driver.refresh()
    sleep(3)
    spans = driver.find_elements_by_tag_name('span')
    show_spans = []
    for span in spans:
        if span.text.lower() == 'show':
            show_spans.append(span)
    for show in show_spans:
        show.click()
        sleep(0.3)


def get_table_elements(driver: webdriver.Chrome):
    loaded = driver.find_elements_by_tag_name('table')
    tables = []
    for t in loaded:
        tables.append(t.find_elements_by_tag_name('tr'))
    return tables


def extract_data_from_table(table: list[WebElement]):
    header_list = table[0].find_elements_by_tag_name('th')
    headers = ['_'.join(h.text.lower().replace("-", "_").split()) for h in header_list]
    print(headers)
    data = []
    for element in table[1:]:
        row_elements = element.find_elements_by_tag_name('td')
        assert len(row_elements) == len(headers)
        data.append(dict(zip(headers, row_elements)))
    return data


def clean_data(data: list[dict]):
    cleaned = []
    for row in data:
        row_data = {}
        for col_name, element in row.items():
            if col_name == 'name':
                row_data[col_name] = element.text
                row_data['url'] = None
                for e in element.find_elements_by_tag_name('a'):
                    if e.text != '':
                        row_data['url'] = e.get_property('href')
            else:
                text = element.text
                row_data[col_name] = None if text == '-' or text == '' else text
        cleaned.append(row_data)
    return cleaned


if __name__ == "__main__":
    driver = get_driver()
    sleep(5)
    driver.get(items_id_webpage)
    sleep(5)
    click_show(driver)
    table_elements = get_table_elements(driver)
    extracted = []
    for te in table_elements:
        try:
            extracted.append(extract_data_from_table(te))
        except:
            pass

    data = []
    for ext in extracted:
        data.append(clean_data(ext))

    for i, d in enumerate(data):
        with open(f"tools/data/items/{i}.json", 'w') as w:
            json.dump(d, w)

    driver.quit()
