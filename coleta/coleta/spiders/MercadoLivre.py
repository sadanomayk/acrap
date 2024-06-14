import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "MercadoLivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-masculino"]

    def parse(self, response):
        pass
