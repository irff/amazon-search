amazon-search
=============

Search Amazon products through a neat CLI


## Usage
```
Usage: amazon.py [OPTIONS] [QUERY]...

  Search Amazon products through a neat CLI

Options:
  --category [
    apparel|appliances|arts-and-crafts|automotive|baby|beauty|books|
    collectibles|digital-music|dvd|electronics|fashion|gourmet-food|
    grocery|health-personal-care|home-garden|industrial|jewelry|
    kindle-store|kitchen|lawn-garden|magazines|miscellaneous|
    mobile-apps|mp3-downloads|music|musical-instruments|office-products|
    outdoor-living|pc-hardware|pet-supplies|photo|software|
    sporting-goods|tools|toys|vhs|video|videogames|watches|wireless|
    wireless-accessories]
                                  Category to filter

  --sort [price-asc|price-desc|rating-desc|date-desc]
                                  Sorting option

  --output [txt|json|html|csv]    Output format
  --prime                         Only include items eligible for Amazon Prime
  --no-sponsored                  Exclude sponsored items
  --help                          Show this message and exit.
```

## Enhancements
- Add fields:
    - `asin` (Amazon Standard Identification Number)
    - `image` (product image url)
    - `sponsored` (whether product is sponsored or not)
- Option to exclude sponsored products
- More output format:
    - `HTML`
    - `CSV`
- Filter by Category
    - I implemented this feature since it is very helpful in refining
      my search. Instead of adding more keywords, filtering by category
      has better accuracy.

## Assumption on price:
- When there are multiple prices on a product, for example a book may
  have a hardcover, paperback, or kindle prices, it will return the
  topmost price.
- When there are no Amazon prices available, it will return the cheapest
  offer listings (sold by third parties, including used products)

## Deviations
### Sorting options
The program combined sorting column and order option into a single parameter:
- `price-asc`
- `price-desc`
- `rating-desc`
- `date-desc` (newest to oldest added products)

If sorting option is not supplied, it will return products sorted by
`relevance`.

The following sorting options requested is not available due to
limitation in Amazon's search interface:
- `rating-desc`
- `title-asc`
- `title-desc`

### Output format
This program accepts `--output [txt|json|html|csv] ` to choose output
format since it's semantically better than having a separate flag for
each output format like `--json`

### Scraped URL
This program parsed `amazon.com` page through
`https://www.amazon.com/s?rh=k:QUERY` Instead of
`https://www.amazon.com/s/?field-keywords=QUERY` since from my
observationthe former has more functionalities than the latter.

## Dependencies
- `python3`
- `beautifulsoup4`
- `click`
- `pytest`
- `requests`

## Interpreter Compatibility
This program is developed using `Python 3.6.3` interpreter. It should work
in `Python 3.x`. Currently `Python 2.x` is not supported due to `Unicode`
encoding issue, I tried to solve this but it turned out to be very hard.
