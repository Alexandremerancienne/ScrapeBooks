"""This program aims at scraping book-selling website \
"Books To Scrape" (http://books.toscrape.com/) to extract \
the following information for a specific book:

- product_page_url
- universal_ product_code (upc)
- title price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url"""


import csv

import requests
from bs4 import BeautifulSoup
from slugify import slugify


def get_book_description_from_url(book_url):
    """Function scraping the following info from book URL :
    - Universal Product Code (UPC)
    - Title
    - Price including tax
    - Price excluding tax
    - Number available
    - Product description
    - Category
    - Review rating
    - Picture URL"""

    response = requests.get(book_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table table-striped').find_all('td')
        universal_product_code = table[0].text
        title = soup.h1.text
        slug = slugify(title)
        price_includ_tax = table[3].text
        price_exclud_tax = table[2].text
        number_available = table[5].text
        if soup.find('div', id='product_description'):
            summary = soup.h2.find_next('p').text
            summary = summary.replace(':', '-').replace(';', '-')
        else:
            summary = "No description available"
        category = soup.find('ul', class_='breadcrumb').find_all('a')[2].text
        review_rating = soup.find('p', class_='star-rating')['class'][1]
        picture_url = soup.find('div', class_='item active').find('img')['src']
        url_root = 'http://books.toscrape.com'
        picture_url = picture_url.replace('../..', url_root)

        return [book_url, universal_product_code, slug,
                price_includ_tax, price_exclud_tax,
                number_available, summary,
                category, review_rating, picture_url]


def save_book_description_to_csv(book_url):
    """Function saving book description to CSV file"""

    book_description = get_book_description_from_url(book_url)
    title = book_description[2]
    with open(title + '.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Product Page URL', 'Universal Product Code (UPC)',
                         'Title', 'Price Including Tax',
                         'Price Excluding Tax', 'Availability',
                         'Product Description', 'Category', 'Review Rating',
                         'Picture URL'])
        writer.writerow(book_description)

# Testing function


if __name__ == '__main__':
    book_url = 'http://books.toscrape.com/catalogue/soumission_998/index.html'
    save_book_description_to_csv(book_url)