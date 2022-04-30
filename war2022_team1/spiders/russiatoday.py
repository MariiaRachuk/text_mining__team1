import scrapy


class RussiatodaySpider(scrapy.Spider):
    name = 'russiatoday'
    allowed_domains = ['russian.rt.com']
    start_urls = ['https://russian.rt.com/business/']

    def parse(self, response, **kwargs):
        for link in response.css('div.card__heading.card__heading_sections.card__heading_sections_1 a::attr(href)'):
            yield response.follow(link, callback=self.text)
        for i in range(1, 50):
            next_page = f'https://russian.rt.com/business#'
            yield response.follow(next_page, callback=self.parse)

    def text(self, response):

        yield {
            'link': response.css('link::attr(href)')[9].get(),
            'text': ''.join(response.css('h1.article__heading.article__heading_article-page::text').getall()),
            'date': response.css('time.date::attr(datetime)').get()
        }
