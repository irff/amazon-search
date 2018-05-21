from bs4 import BeautifulSoup

from amazon.product import Product
from amazon.product_soup import ProductSoup

from tests.mock_data import product_html_string


product_html = BeautifulSoup(product_html_string, 'html.parser')
product_soup = ProductSoup(product_html)


def test_product_soup():
    title = product_soup.get_title()
    link = product_soup.get_link()
    price = product_soup.get_price()
    rating = product_soup.get_rating()
    reviews = product_soup.get_reviews()
    image = product_soup.get_image()
    prime = product_soup.get_prime()
    sponsored = product_soup.get_sponsored()

    assert title == 'Marvel Legends Iron Man Electronic Helmet'
    assert link == ('https://www.amazon.com/Marvel-Legends-Iron-Electronic-Helmet/dp/B01B4NLOW4/'
                    'ref=sr_1_1?ie=UTF8&qid=1526927761&sr=8-1&keywords=iron+man+helmet')
    assert price == '$304.86'
    assert rating == '4.3'
    assert reviews == '306'
    assert image == 'https://images-na.ssl-images-amazon.com/images/I/51+tIG3fxGL._AC_US218_.jpg'
    assert prime == Product.YES
    assert sponsored == Product.NO
