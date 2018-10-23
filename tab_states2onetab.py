import re
from collections import namedtuple

import requests
from fake_useragent import UserAgent
from lxml import html
from tqdm import tqdm

ua = UserAgent()
headers = {'User-Agent': ua.chrome}


def get_matches():
    regex = "(http(s?):\/\/|www[.])[-A-Za-z0-9+&amp;@#\/%?=~_()|!:,.;]*[-A-Za-z0-9+&amp;@#\/%=~_()|]"
    with open("tab_states/tab_state0", "rb") as file:
        byte = file.read().decode('ISO-8859-1')
    matches = list(re.finditer(regex, byte, re.MULTILINE))
    return matches


def get_title(url):
    try:
        page = requests.get(url, headers=headers)
        if page.status_code != 200:
            tqdm.write(f"!200 {url}")
        tree = html.fromstring(page.content)
        title = tree.findtext('.//title')
        if title:
            return title.strip()
        else:
            tqdm.write(f'empty title {url}')
            return title
    except requests.exceptions.ConnectionError:
        return "ConnectionError"


def get_tabs(matches):
    tabs = []
    Tab = namedtuple('Tab', ['url', 'title'])
    for match in tqdm(matches):
        url = match.group()
        title = get_title(url)
        tabs.append(Tab(url, title))
    return tabs


def generate_onetab_file(tabs):
    onetab = '\n'.join([f'{tab.url} | {tab.title}' for tab in tabs])
    with open('onetab.txt', 'w') as f:
        f.write(onetab)


def main():
    marches = get_matches()
    tabs = get_tabs(marches)
    generate_onetab_file(tabs)


if __name__ == '__main__':
    main()
