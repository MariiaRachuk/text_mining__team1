import scrapy
import logging

logger = logging.getLogger(__name__)
class LentaRuSpider(scrapy.Spider):
    name = "lenta"
    allowed_domains = ['lenta.ru']
    start_urls = ["https://lenta.ru/rubrics/economics/economy/"]

#response.css('a.card-full-news._subrubric::attr(href)').get()

    def parse(self, response, **kwargs):
        for link in response.css('a.card-full-news._subrubric::attr(href)'):
            yield response.follow(link, callback=self.text)
        for i in range(1,50):
            next_page = f'href="https://lenta.ru/rubrics/economics/economy/{i}/'
            yield response.follow(next_page, callback=self.parse)

    def text(self, response):

        yield {
            'link': response.css('link::attr(href)').get(),
            'text': ''.join(response.css('span.topic-body__title::text').getall()),
            'date': response.css('time.topic-header__item.topic-header__time::text').get()
        }