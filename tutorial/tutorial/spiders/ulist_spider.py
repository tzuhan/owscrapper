import json
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
hero_dict={'roadhog': 1}#, 'junkrat': 2, 'lcio': 3, 'soldier-76': 4, 'zarya': 5, 'mccree': 6, 'tracer': 7, 'reaper': 8, 'widowmaker': 9, 'winston': 10, 'pharah': 11, 'reinhardt': 12, 'symmetra': 13, 'torbjrn': 14, 'bastion': 15, 'hanzo': 16, 'mercy': 17, 'zenyatta': 18, 'mei': 20, 'genji': 21, 'd-va': 22, 'ana': 23, 'sombra': 24}#, 'orisa': 25}
hero_name_dict={v: k for k, v in hero_dict.items()}
add_num=50
rank_name = ['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond', 'Master', 'Grandmaster']
rank_score_list = [1, 1500, 2000, 2500, 3000, 3500, 4000]
rank_count = [0]*len(rank_score_list)

class QuotesSpider(scrapy.Spider):
    name = "ulist"

    def start_requests(self):
        url = "https://masteroverwatch.com/leaderboards/pc/global/hero/{}/mode/ranked/category/time"
        for hero, hero_id in hero_dict.items():
            if hero_id:
                format_url = url.format(hero_id)
                yield scrapy.Request(url=format_url, callback=self.parse)

    def create_ajax_request(self, hero_id, user_number):
        ajax_url = 'https://masteroverwatch.com/leaderboards/pc/global/mode/ranked/category/time/hero/{}/role/overall/data?offset={}'.format(hero_id, user_number)
        yield scrapy.Request(url=ajax_url, method='GET', headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'}, encoding={'utf-8'}, callback=self.parse2)

    def parse(self, response):
        hero_id = int(response.url.split("/")[-5])
        filename = 'user_list/%s.csv' % hero_name_dict[hero_id]
        with open(filename, 'wt', encoding='utf-8') as f:
            f.write('rank, name, link, time\n')
            user_num = 1
            for row in response.css('div.table-body div.table-row'):
                name = row.css("span.table-name-block>strong::text").extract_first().strip()
                link = row.css('a.table-row-link::attr(href)').extract_first()
                area_rated_text = row.css("span.table-name-block>small::text").extract_first().split()
                area = area_rated_text[0]
                if (area_rated_text[-1] != 'Rating'):
                    #Unrated, skip this person
                    continue
                rank = int(row.css("span.table-name-block>small>strong::text").extract_first().replace(',', ''))
                time = int(row.css("div.table-main-value strong::text").re(r'(\d+) *')[0])
                user_num += 1
                f.write('{:5}, {:20}, {:40}, {:>4}\n'.format(rank, name, link, time))
                for index, value in enumerate(rank_score_list):
                    if value > rank:
                        rank_count[index-1] += 1
                        break
            #if (user_num < 100) :
            #    yield self.create_ajax_request(hero_id, user_num+add_num)
        #self.log('Saved file %s' % filename)

    def parse2(self, response):
        hero_id = int(response.url.split("/")[-4])
        doc = response.body.decode('unicode-escape')
        filename = 'user_list/%s.csv' % hero_name_dict[hero_id]
        with open(filename, 'at', encoding='utf-8') as f:
            print('~~~~~~~~~~~~~~', Selector(text=doc).css('div.table-row'))
            print('~~~~~~~~~~~~~~', response.selector.css('div'))
            for row in response.selector.css('div.table-row'):
                name = row.css("span.table-name-block>strong::text").extract_first().strip()
                link = row.css('a.table-row-link::attr(href)').extract_first()
                area_rated_text = row.css("span.table-name-block>small::text").extract_first().split()
                area = area_rated_text[0]
                if (area_rated_text[-1] != 'Rating'):
                    #Unrated, skip this person
                    continue
                rank = int(row.css("span.table-name-block>small>strong::text").extract_first().replace(',', ''))
                time = int(row.css("div.table-main-value strong::text").re(r'(\d+) *')[0])
                #print(name, link, area, rank, time)
                #f.write('{:5}, {:20}, {:40}, {:>4}\n'.format(rank, name, link, time))
            #if (line of %s.csv < 100) :
                #yield self.create_ajax_request(user_num + add_num)
        #self.log('Saved file %s' % filename)
