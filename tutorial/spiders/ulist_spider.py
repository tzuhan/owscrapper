import scrapy
hero_dict={'roadhog': 1, 'junkrat': 2, 'lcio': 3, 'soldier-76': 4, 'zarya': 5, 'mccree': 6, 'tracer': 7, 'reaper': 8, 'widowmaker': 9, 'winston': 10, 'pharah': 11, 'reinhardt': 12, 'symmetra': 13, 'torbjrn': 14, 'bastion': 15, 'hanzo': 16, 'mercy': 17, 'zenyatta': 18, 'mei': 20, 'genji': 21, 'd-va': 22, 'ana': 23, 'sombra': 24, 'orisa': 25}
hero_name_dict={v: k for k, v in hero_dict.items()}

class QuotesSpider(scrapy.Spider):
    name = "ulist"

    def start_requests(self):
        urls = [
            'https://masteroverwatch.com/leaderboards/pc/global/hero/1/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/2/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/3/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/4/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/5/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/6/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/7/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/8/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/9/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/10/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/11/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/12/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/13/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/14/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/15/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/16/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/17/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/18/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/20/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/21/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/22/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/23/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/24/mode/ranked/category/time',
            'https://masteroverwatch.com/leaderboards/pc/global/hero/25/mode/ranked/category/time',
        ]
        for url in urls:
            yield scrapy.Request(url=url, method='GET', headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'}, callback=self.parse)

    def parse(self, response):
        hero_id = int(response.url.split("/")[-5])
        filename = 'user_list/%s.csv' % hero_name_dict[hero_id]
        with open(filename, 'wt', encoding='utf-8') as f:
            f.write('rank, name, link, time\n')
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
                print(name, area, rank, time)

                #f.write('{:>5}, {:30}, {}, {:>4}\n'.format(rank, name, link, time))
        self.log('Saved file %s' % filename)

