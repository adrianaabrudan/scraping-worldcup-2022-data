import scrapy


class WorldCupSpider(scrapy.Spider):
    name = "worldcup"
    allowed_domains = ['www.mykhel.com']
    start_urls = ['https://www.mykhel.com/football/fifa-world-cup-2022-player-stats-l4/']

    def parse(self, response, *args, **kwargs):
        rows = response.xpath('//*[@id="overview_loading_body"]//tr')
        data = []

        for row in rows[1:]:
            items = dict()
            items['Player'] = row.xpath('.//td/a/@title').extract_first()
            items['Team'] = row.xpath('.//td[2]/text()').extract_first()
            items['Matches'] = row.xpath('.//td[3]/text()').extract_first()
            items['Goals'] = row.xpath('.//td[4]/text()').extract_first()
            items['TimePlayed'] = row.xpath('.//td[5]/text()').extract_first()
            data.append(items)
        yield {'rows': data}

