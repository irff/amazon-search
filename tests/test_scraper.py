from bs4 import BeautifulSoup

from amazon.scraper import Scraper

scraper = Scraper()
prime_only = False
no_sponsored = False

query = 'iron+man'
scraper.request_html(category='books', sort='rating-desc', prime_only=True, query=query)


def test_amazon_accessible():
    scraper = Scraper()
    is_amazon_accessible = scraper.is_amazon_accessible()
    assert is_amazon_accessible is True


def test_request_html():
    assert scraper.url == (
        'https://www.amazon.com/s?' 
        'rh=n%3A283155%2Cp_85%3A2470955011%2Ck:iron+man&sort=review-rank'
    )

    assert scraper.html is not None
    assert isinstance(scraper.html, BeautifulSoup)


def test_result_count():
    result_count = scraper.get_result_count()

    assert result_count['num_of_products_per_page'] > 0
    assert result_count['num_of_products'] > 0
    assert result_count['num_of_pages'] > 0


def test_get_products():
    products = scraper.get_products(prime_only, no_sponsored)

    assert len(products) > 0
