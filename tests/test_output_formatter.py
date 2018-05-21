import csv
import json
from bs4 import BeautifulSoup

from amazon.scraper import Scraper
from amazon.output_formatter import OutputFormatter

scraper = Scraper()
output_formatter = OutputFormatter()

query = 'game+of+thrones'

scraper.request_html(category='fashion', sort='price-asc', prime_only=True, query=query)

products = scraper.get_products(True, no_sponsored=False)
result_count = scraper.get_result_count()

detail_data = {}


if products is not None and result_count is not None:
    detail_data = dict(result_count, **{
        'url': scraper.get_url(),
        'num_of_returned_products': len(products)
    })


def test_csv():
    csv_output = output_formatter.to_csv(products, detail_data)
    output = list(csv.reader(csv_output.splitlines()))
    assert len(output) > 1  # assuming header row is always there


def test_html():
    html_output = output_formatter.to_html(products, detail_data)
    output = BeautifulSoup(html_output, 'html.parser')
    rows = output.find_all('tr')

    assert output is not None
    assert isinstance(output, BeautifulSoup)
    assert len(rows) > 1  # assuming header row is always there


def test_json():
    json_output = output_formatter.to_json(products, detail_data)
    output = json.loads(json_output)

    assert output is not None
    assert output['detail_data'] is not None
    assert output['products_data'] is not None
    assert len(output['products_data']) > 0
