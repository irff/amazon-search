import re

from amazon.product import Product
from settings.urls import base_url


class ProductSoup():
    def __init__(self, soup):
        self.soup = soup

    def get_asin(self):
        return self.soup.get('data-asin')

    def get_image(self):
        image_html = self.soup.find('img', 's-access-image')

        if image_html is not None:
            return image_html.get('src')

        return Product.NONE

    def get_link(self):
        link_a = self.soup.find('a', 's-access-detail-page')

        if link_a is not None:
            link = link_a.get('href')

            if not re.compile('^%s' % base_url).match(link):
                link = base_url + link

            return link

        return Product.NONE

    def get_price(self):
        """
        There are multiple ways to get the price of a certain product. I found four ways
        so far, and this method will return the most commonly seen prices first.
        """
        price_offscreen_span = self.soup.find('span', class_='a-offscreen', text=re.compile('^\$'))
        price_splitted_span = self.soup.find('span', 'sx-price')
        price_small_span = self.soup.find('span', 's-price')
        price_offer_listing_a = self.soup.find('a', href=re.compile('/offer-listing/'))

        if price_offscreen_span is not None:
            return price_offscreen_span.get_text()

        if price_splitted_span is not None:
            text = [t for t in price_splitted_span.stripped_strings]

            if len(text) == 3:
                price = '{}{}.{}'.format(text[0], text[1], text[2])
                return price

        if price_small_span is not None:
            return price_small_span.get_text()

        # If there are no Amazon price available, return lowest offer listing price
        # Offer listings products are sold by third parties and may include used products
        # Generally it has this text: More Buying Choices, $7.30 (33 used & new offers)
        if price_offer_listing_a is not None:
            price_offer_listing_span = price_offer_listing_a.find('span', text=re.compile('^\$'))

            if price_offer_listing_span is not None:
                return price_offer_listing_span.get_text()

        return Product.NONE

    def get_prime(self):
        prime_html = self.soup.find('i', 'a-icon-prime')

        if prime_html is not None:
            return Product.YES

        return Product.NO

    def get_rating(self):
        rating_html = self.soup.find('i', 'a-icon-star')

        if rating_html is not None:
            rating_text = rating_html.get_text()
            rating_text_splitted = rating_text.split(' ')

            if len(rating_text_splitted) > 0:
                return rating_text_splitted[0]

        return Product.NONE

    def get_reviews(self):
        reviews_html = self.soup.find('a', href=re.compile('#customerReviews'))

        if reviews_html is not None:
            return reviews_html.get_text()

        return Product.NONE

    def get_sponsored(self):
        link_a = self.soup.find('a', 's-access-detail-page')

        if link_a is not None:
            link = link_a.get('href')

            # Sponsored products doesn't have amazon.com prefix as URL
            # It generally has long URL and use redirection
            if not re.compile('^{}'.format(base_url)).match(link):
                return Product.YES

        return Product.NO

    def get_title(self):
        title_h2 = self.soup.find('h2')

        if title_h2 is not None:
            return title_h2.get('data-attribute')

        return Product.NONE
