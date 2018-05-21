import csv
import io
import json

from amazon.product import Product


class OutputFormatter():
    """
    Product output formatter. Given a list of products and result detail, return its representation
    in JSON, Text, CSV, or HTML
    """

    def to_json(self, products_data, detail_data):
        products_dict = [product.to_dict() for product in products_data]

        result_dict = {
            'detail_data': detail_data,
            'products_data': products_dict
        }

        result = json.dumps(result_dict, indent=4, sort_keys=True)
        return result

    def to_text(self, products, detail_data):
        result = ''
        result += 'Number of products per page: %s\n' % detail_data['num_of_products_per_page']
        result += 'Total number of products: %s\n' % detail_data['num_of_products']
        result += 'Number of pages: %s\n' % detail_data['num_of_pages']
        result += 'Number of returned products: %s\n' % detail_data['num_of_returned_products']
        result += 'Query Url: %s\n\n' % detail_data['url']

        if len(products) == 0:
            result += 'No products found. Please refine your query.'

        for product in products:
            result += '%s\n' % product.title
            result += 'ASIN: %s\n' % product.asin
            result += 'Price: %s\n' % product.price
            result += 'Rating: %s (%s reviews)\n' % (product.rating, product.reviews if product.reviews != '-' else 'no')
            result += 'Prime: %s\n' % product.prime
            result += 'Sponsored: %s\n' % product.sponsored
            result += 'Image: %s\n' % product.image
            result += 'Url: %s\n\n' % product.link

        return result

    def to_csv(self, products_data, detail_data):
        """
        To valid CSV format. Number of products and number of pages data are not included.
        """
        result_file = io.StringIO()

        fieldnames = Product().to_dict().keys()

        result_writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        result_writer.writeheader()

        for product in products_data:
            result_writer.writerow(product.to_dict())

        return result_file.getvalue()

    def to_html(self, products_data, detail_data):
        """
        To valid HTML Table format. Number of products and number of pages data are not included.
        """
        table_string = ''

        keys = Product().to_dict().keys()
        table_string += '<tr>' + ''.join(['<th>%s</th>' % key for key in keys]) + '</tr>\n'

        for product in products_data:
            values = product.to_dict().values()
            table_string += '<tr>' + ''.join(['<td>%s</td>' % value for value in values]) + '</tr>\n'

        table_string = '<table>\n%s</table>\n' % table_string

        return table_string
