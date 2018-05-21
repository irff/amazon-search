import click

from amazon.scraper import Scraper
from amazon.output_formatter import OutputFormatter
from settings.urls import sorting_params, category_params

TXT, JSON, HTML, CSV= 'txt', 'json', 'html', 'csv'
OUTPUT_PARAMS = [TXT, JSON, HTML, CSV]


@click.command()
@click.option('--category', type=click.Choice(category_params.keys()), help='Category to filter')
@click.option('--sort', type=click.Choice(sorting_params.keys()), help='Sorting option')
@click.option('--output', type=click.Choice(OUTPUT_PARAMS), default=TXT, help='Output format')
@click.option('--prime', is_flag=True, help='Only include items eligible for Amazon Prime')
@click.option('--no-sponsored', is_flag=True, help='Exclude sponsored items')
@click.argument('query', nargs=-1)
def amazon(category, sort, output, prime, no_sponsored, query):
    """
    Search Amazon products through a neat CLI
    """

    scraper = Scraper()
    output_formatter = OutputFormatter()

    query = '+'.join(query)

    scraper.request_html(category, sort, prime_only=prime, query=query)

    products = scraper.get_products(prime, no_sponsored)
    result_count = scraper.get_result_count()

    if products is not None and result_count is not None:
        detail_data = dict(result_count, **{
            'url': scraper.get_url(),
            'num_of_returned_products': len(products)
        })

        if output == TXT:
            print(output_formatter.to_text(products, detail_data))
        elif output == JSON:
            print(output_formatter.to_json(products, detail_data))
        elif output == HTML:
            print(output_formatter.to_html(products, detail_data))
        elif output == CSV:
            print(output_formatter.to_csv(products, detail_data))
        else:
            raise click.BadOptionUsage('Invalid output format')
    else:
        print('Could not retrieve data from Amazon. Might be internet issue.')


if __name__ == '__main__':
    amazon()
