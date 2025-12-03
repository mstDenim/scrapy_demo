import scrapy
from scrapy.http import Response

class BookspiderSpider(scrapy.Spider):
    name = "bookspider" 
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response: Response):
        books = response.css("article.product_pod")
        for book in books:
            yield{
                'name' : book.css('h3 a').attrib['title'],
                'price' : book.css('div p.price_color::text').get(),
                'availability' : book.css('div p.instock.availability::text').get(),
            }
        next_page = response.css('div li.next ::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
