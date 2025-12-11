import scrapy
from scrapy.http import Response
from first_scraper.items import BookItem

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
        table_rows = book.css("table tr")
        bookItem = BookItem()
            # why is the list in reverse order xD
            # has to have something to do with 
            # A: how -O in scrapy writes to a file 
            # B: because of the way i call it here
        bookItem['name'] = book.css("div h1::text").get(),
        bookItem['price'] = book.css("div p.price_color::text").get(),
        bookItem['product_description'] =  book.xpath('//div[@id="product_description"]/following-sibling::p/text()').get(),
        bookItem['category'] = book.xpath('//ul[@class = "breadcrumb"]/li[@class = "active"]/preceding-sibling::li[1]/a/text()').get(),
        bookItem['upc']= table_rows[0].css("tr td::text").get(),
        bookItem['product_type'] = table_rows[1].css("tr td::text").get(),
        bookItem['price_without_tax'] = table_rows[2].css("tr td::text").get(),
        bookItem['price_with_tax'] = table_rows[3].css("tr td::text").get(),
        bookItem['tax'] = table_rows[4].css("tr td::text").get(),
        bookItem['availability'] = table_rows[5].css("tr td::text").get(),
        bookItem['star_rating'] = book.css('p.star-rating ::attr(class)').get(),
        if type(bookItem) == BookItem:
            yield bookItem

