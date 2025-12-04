import scrapy
from scrapy.http import Response

class BookspiderSpider(scrapy.Spider):
    name = "bookspider" 
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response: Response):
        books = response.css("article.product_pod")
        for book in books:
            individual_book = book.css('div a::attr(href)').get()
            if individual_book is not None:
                yield response.follow(individual_book, callback = self.parse_individual_bookpage)

        next_page = response.css('div li.next ::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)

    def parse_individual_bookpage(self, response: Response):
        book = response.css("article.product_page")
        yield{
            # why is the list in reverse order xD
            # has to have something to do with 
            # A: how -O in scrapy writes to a file 
            # B: because of the way i call it here
            'name' : book.css("div h1::text").get(),
            'price' : book.css("div p.price_color::text").get(),
            'product-description' : book.xpath('//div[@id="product_description"]/following-sibling::p/text()').get(),
            'category' : book.xpath('//ul[@class = "breadcrumb"]/li[@class = "active"]/preceding-sibling::li[1]/a/text()')
            .get(),


        }
        pass
