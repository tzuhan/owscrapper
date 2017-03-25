from urllib.parse import urljoin
from lxml import html
from lxml.html.clean import clean_html
import requests
hero_dict={'roadhog': 1, 'junkrat': 2, 'lcio': 3, 'soldier-76': 4, 'zarya': 5, 'mccree': 6, 'tracer': 7, 'reaper': 8, 'widowmaker': 9, 'winston': 10, 'pharah': 11, 'reinhardt': 12, 'symmetra': 13, 'torbjrn': 14, 'bastion': 15, 'hanzo': 16, 'mercy': 17, 'zenyatta': 18, 'mei': 20, 'genji': 21, 'd-va': 22, 'ana': 23, 'sombra': 24, 'orisa': 25}
hero_name_dict={v: k for k, v in hero_dict.items()}

def getUsersByTotalTime(hero_name):
    URL='https://masteroverwatch.com/leaderboards/pc/global/hero/{}/mode/ranked/category/time'.format(hero_dict[hero_name])
    page = requests.get(URL)
    doc = html.fromstring(page.text)
    names = doc.cssselect('span.table-name-block > strong')
    ranks = doc.cssselect('span.table-name-block small strong')
    times = doc.cssselect('div[class="table-main-value col-xs-3"] > strong')
    for name, rank, time in zip(names, ranks, times):
        print('{}, {}, {}'.format(name.text.strip(), int(rank.text.replace(',','')), int(time.text.split(' ')[0])))

def main():
    getUsersByTotalTime('mercy');
main()
