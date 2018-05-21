import requests
import urllib.parse

from bs4 import BeautifulSoup
from http import HTTPStatus

from amazon.product import Product
from amazon.product_soup import ProductSoup
from settings.cookies import (
    session_id,
    session_id_time,
    session_token,
    ubid_main
)
from settings.headers import (
    accept,
    accept_encoding,
    host,
    user_agent
)
from settings.urls import (
    base_url,
    category_params,
    filter_param,
    prime_param,
    sorting_params
)


class Scraper:
    """
    Class to wrap Amazon.com website scraper

    """
    base_url = base_url
    query_url = '%s/s?' % base_url

    headers = {
        'Accept': accept,
        'Accept-Encoding': accept_encoding,
        'Host': host,
        'User-Agent': user_agent,
    }

    cookies = {
        'session-id': session_id,
        'session-id-time': session_id_time,
        'session-token': session_token,
        'ubid-main': ubid_main
    }

    def __init__(self):
        self.url = ''
        self.html = None

    def request(self, url):
        try:
            result = requests.get(url=url, headers=self.headers,
                                  cookies=self.cookies)

            if result.status_code == HTTPStatus.OK:
                return result.content

        except Exception as e:
            print('Error sending request: %s\n' % e)

    def is_amazon_accessible(self):
        result = self.request(self.base_url)

        if result is not None:
            return True

        return False

    def build_query(self, category, sort, prime_only, query):
        query_string = ''

        if category:
            category_suffix = 'n:%s' % category_params[category]
            query_string = '%s%s,' % (query_string, category_suffix)

        if prime_only:
            query_string = '%s%s,' % (query_string, prime_param)

        query_string = urllib.parse.quote_plus(query_string)
        query_string = '%sk:%s' % (query_string, query)

        if sort:
            sort_suffix = '&sort=%s' % sorting_params[sort]
            query_string = '%s%s' % (query_string, sort_suffix)

        encoded_url = '%s%s%s' % (self.query_url, filter_param, query_string)

        return encoded_url


    def request_html(self, category, sort, prime_only, query):

        self.url = self.build_query(category, sort, prime_only, query)

        content = self.request(self.url)

        if content is not None:
            self.html = BeautifulSoup(content, 'html.parser')

    def get_result_count(self):
        """
        Parses string at the top of search result page to get to get the number
        of products and pages.

        Example string: 1-16 of over 2,500 results for "jungle book"
        """
        num_of_products_per_page = 0
        num_of_products = 0
        num_of_pages = 0

        if self.html is not None:
            count_html = self.html.find('span', id='s-result-count')

            if count_html is not None:
                count_text = count_html.text.replace('-', ' ').replace(',', '')
                count_nums = [
                    int(s) for s in count_text.split(' ') if s.isdigit()
                ]

                if len(count_nums) >= 3:
                    num_of_products_per_page = count_nums[1]
                    num_of_products = count_nums[2]

                    if num_of_products_per_page > 0:
                        num_of_pages = int(num_of_products / num_of_products_per_page)

                elif len(count_nums) == 1:
                    num_of_products_per_page = count_nums[0]
                    num_of_products = num_of_products_per_page
                    num_of_pages = 1

        return {
            'num_of_products_per_page': num_of_products_per_page,
            'num_of_products': num_of_products,
            'num_of_pages': num_of_pages
        }

    def get_products(self, prime_only, no_sponsored):
        """
        Returns a list of Product objects
        """
        if self.html is not None:
            products_html = self.html.find_all('li', 's-result-item')
            products_data = []

            for product_html in products_html:
                product_soup = ProductSoup(product_html)
                asin = product_soup.get_asin()

                if asin is not None:
                    title = product_soup.get_title()
                    link = product_soup.get_link()
                    price = product_soup.get_price()
                    rating = product_soup.get_rating()
                    reviews = product_soup.get_reviews()
                    image = product_soup.get_image()
                    prime = product_soup.get_prime()
                    sponsored = product_soup.get_sponsored()

                    product = Product(asin=asin, title=title, price=price,
                                      rating=rating, link=link,
                                      reviews=reviews, image=image,
                                      prime=prime, sponsored=sponsored)

                    # Exclude products with specific criteria
                    if title != '-' and link != '-':
                        if not (no_sponsored and product.is_sponsored()):
                            if not (prime_only and not product.is_prime()):
                                products_data.append(product)

            return products_data

    def get_url(self):
        return self.url
