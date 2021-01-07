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


book_name = []


def get_book_name(book_url):
    """Function scraping the name of the category"""

    response = requests.get(book_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        name_of_book = soup.h1.text
        name_of_book = slugify(name_of_book)
        book_name.append(name_of_book)


book_description = []


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

        book_features = [book_url, universal_product_code, slug,
                         price_includ_tax, price_exclud_tax,
                         number_available, summary,
                         category, review_rating, picture_url]
        book_description.append(book_features)

        return(book_description[-1])


def save_scraped_data_to_csv(data_description_list, file_name):
    """Function saving scraped data - represented as a list - to CSV file"""

    try:
        with open(file_name + '.csv', 'w', newline='',
                  encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Product Page URL',
                             'Universal Product Code (UPC)', 'Title',
                             'Price Including Tax', 'Price Excluding Tax',
                             'Availability', 'Product Description',
                             'Category', 'Review Rating', 'Picture URL'])
            writer.writerows(data_description_list)
    except FileNotFoundError:
        print("Scraped data cannot be saved to CSV file")


# Testing function


if __name__ == '__main__':
    book_url = 'http://books.toscrape.com/catalogue/soumission_998/index.html'
    get_book_name(book_url)
    get_book_description_from_url(book_url)
    save_scraped_data_to_csv(book_description, book_name[-1])