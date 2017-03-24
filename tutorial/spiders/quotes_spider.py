import scrapy
hero_dict={'roadhog': 1, 'junkrat': 2, 'lcio': 3, 'soldier-76': 4, 'zarya': 5, 'mccree': 6, 'tracer': 7, 'reaper': 8, 'widowmaker': 9, 'winston': 10, 'pharah': 11, 'reinhardt': 12, 'symmetra': 13, 'torbjrn': 14, 'bastion': 15, 'hanzo': 16, 'mercy': 17, 'zenyatta': 18, 'mei': 20, 'genji': 21, 'd-va': 22, 'ana': 23, 'sombra': 24, 'orisa': 25}
hero_name_dict={v: k for k, v in hero_dict.items()}

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'https://masteroverwatch.com/leaderboards/pc/global/hero/17/mode/ranked/category/time',
        ]
        for url in urls:
            yield scrapy.Request(url=url, method='GET', headers={'X-Requested-With': 'XMLHttpRequest', 'Content-Type': 'application/json; charset=UTF-8'}, callback=self.parse)

    def parse(self, response):
        hero_id = int(response.url.split("/")[-5])
        filename = '%s.html' % hero_name_dict[hero_id]
        with open(filename, 'wt', encoding='utf-8') as f:
            f.write('rank, name, link, time\n')
            for row in response.css('div.table-body div.table-row'):
                (name, link, rank, time) = ([s.strip() for s in row.css("span.table-name-block>strong::text").extract()][0], row.css('a.table-row-link::attr(href)').extract_first(), int(row.css("div.table-main-value strong::text").re(r'(\d+) *')[0]), int([s.replace(',', '') for s in row.css("span.table-name-block>small strong::text").extract()][0]))
                f.write('{:>5}, {:30}, {}, {:>4}\n'.format(rank, name, link, time))
        self.log('Saved file %s' % filename)

