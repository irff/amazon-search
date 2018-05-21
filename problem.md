Amazon.py
=========

Create a command line application called amazon.py.  The application accepts a
couple of command line flags and an user query, and then prints out the results
formatted in a easy to read way (example below).

Example
-------

    $ ./amazon.py --sort rating --desc office chairs

    AmazonBasics High-Back Executive Chair - Black
    Price: $109.99
    Rating: ★★★★☆ (3,128 reviews)
    Prime: yes
    Url: https://www.amazon.com/AmazonBasics-High-Back-Executive-Chair-Black

    AmazonBasics Mid-Back Office Chair, Black
    Price: $64.99
    Rating: ★★★★☆ (2,949 reviews)
    Prime: yes
    Url: https://www.amazon.com/AmazonBasics-Mid-Back-Office-Chair-Black

    ...hiding additional results for brevity...

    $ ./amazon.py --json office chairs
    [
        {
            "title": "AmazonBasics Mid-Back Office Chair, Black",
            "price": 64.99,
            "rating": 4,
            "reviews": 2949,
            "url": "https://www.amazon.com/AmazonBasics-Mid-Back-Office-Chair-Black",
        },
        {
            "title": "AmazonBasics High-Back Executive Chair - Black",
            "price": 109.99,
            "rating": 4,
            "reviews": 3128,
            "url": "https://www.amazon.com/AmazonBasics-High-Back-Executive-Chair-Black",
        },
        ...hiding additional results for brevity...
    ]

## Requirements/guidelines

* The program must scrape the HTML of the following page:
  https://www.amazon.com/s/?field-keywords=QUERY
    * The program should use query-string paramaters (similar to field-keywords)
      to specify additional user options like sorting or filters.
* The program can use any python dependencies.
* The program must allow the user to specify a search query as positional
  arguments.
* The program must accept the following flags
    * `--sort {rating, price, name}` which column to sort by
    * `--asc or --desc` mutually exclusive flags that determine sort order
    * `--prime` only include items elegible for Amazon Prime
    * `--json` all output to STDOUT is valid JSON
* The program should return the first page of results, if there is more than one
  page of results the program should tell the user how many additional pages
  there are.
* The submission should include a requirements.txt file that specifies all python
  dependencies used along with specific versions for each.

## Judging criteria

* Meets or exceeds all of the above requirements
* Program runs without errors, handles unexpected responses from Amazon in a
  user-friendly way.
* Code is well architected, it is easy to understand how it works
* Tests are included with the code