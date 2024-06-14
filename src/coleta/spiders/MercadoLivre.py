import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "MercadoLivre"
    allowed_domains = ["mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-masculino"]
    page_count = 1
    max_pages = 50

    def parse(self, response):
        # Seleciona todos os produtos na página
        products = response.css('div.ui-search-result__content')

        for product in products:
            # Extrai o link do produto
            product_link = product.css('a.ui-search-link::attr(href)').get()

            # Extrai a categoria do produto (se disponível)
            category = product.css('a.ui-search-breadcrumb__link::text').get()

            # Extrai a localização do vendedor
            seller_location = product.css('span.ui-search-item__location::text').get()

            # Extrai os preços
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents--superscript-24::text').getall()
            
            # Verifica se os preços e centavos foram encontrados
            old_price = None
            new_price = None
            
            if prices:
                old_price = f"{prices[0]},{cents[0]}" if cents else prices[0]
                if len(prices) > 1:
                    new_price = f"{prices[1]},{cents[1]}" if len(cents) > 1 else prices[1]

            # Extrai informações adicionais
            brand = product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get()
            name = product.css('h2.ui-search-item__title::text').get()
            reviews_rating_number = product.css('span.ui-search-reviews__rating-number::text').get()
            reviews_amount = product.css('span.ui-search-reviews__amount::text').get()
            seller = product.css('p.ui-search-official-store-label.ui-search-item__group__element.ui-search-color--GRAY::text').get()

            # Gera os dados extraídos
            yield {
                'brand': brand,
                'name': name,
                'old_price': old_price,
                'new_price': new_price,
                'reviews_rating_number': reviews_rating_number,
                'reviews_amount': reviews_amount,
                'seller': seller,
                'product_link': product_link,
                'category': category,
                'seller_location': seller_location,
            }

        # Lida com a paginação
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                # Faz a requisição para a próxima página
                yield scrapy.Request(url=next_page, callback=self.parse)

