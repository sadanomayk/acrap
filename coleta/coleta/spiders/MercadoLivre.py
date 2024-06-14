import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "MercadoLivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-masculino"]

    def parse(self, response):
        products = response.css('div.ui-search-result__content')
        
        for product in products:
            # Extrai o link do produto
            product_link = product.css('a.ui-search-link::attr(href)').get()

            # Extrai a categoria do produto
            category = product.css('a.ui-search-breadcrumb__link::text').get()

            # Extrai a localização do vendedor
            seller_location = product.css('span.ui-search-item__location::text').get()

            # Extrai o preço antigo
            old_price_parts = product.css('.andes-money-amount--previous .andes-money-amount__fraction::text').getall()
            old_price_cents = product.css('.andes-money-amount--previous .andes-money-amount__cents::text').getall()
            old_price = ''.join(old_price_parts).strip() + ',' + ''.join(old_price_cents).strip() if old_price_parts else None
            
            # Extrai o preço novo
            new_price_fraction = product.css('.andes-money-amount__fraction::text').get()
            new_price_cents = product.css('.andes-money-amount__cents--superscript-24::text').get() or '00'  # Adiciona '00' se não houver centavos
            new_price = f'{new_price_fraction},{new_price_cents}' if new_price_fraction else None
            
            yield {
                'image_url': product.css('img.ui-search-result-image__element::attr(src)').get(),
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'name': product.css('h2.ui-search-item__title::text').get(),
                'old_price': old_price,
                'new_price': new_price,
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get(),
                'seller': product.css('p.ui-search-official-store-label.ui-search-item__group__element.ui-search-color--GRAY::text').get(),
                'product_link': product_link,
                'category': category,
                'seller_location': seller_location,
                # Adicione aqui outros campos que deseja extrair
            }
