"""This program aims at scraping book-selling website \
"Books To Scrape" (http://books.toscrape.com/) \
to extract the following information for every book displayed :

- product_page_url
- universal_ product_code (upc)
- title price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

As books are organized by category (50 categories overall), \
each category is represented by a folder including :

- A CSV file with aforementioned information for all books \
within the same category
- Cover pictures of the books within the same category

The program uses the results and outputs of the fonctions \
previously defined by the following programs :

- books.py (scraping useful information for any book of \
"Books to Scrape" website)
- categories.py (scraping useful information for any category of \
"Books to Scrape" website)"""


import requests
from bs4 import BeautifulSoup

from books import save_scraped_data_to_csv

from categories import get_category_name
from categories import create_folder_for_category
from categories import get_category_pages_to_scrape
from categories import get_category_books_urls
from categories import get_category_books_descriptions
from categories import save_category_books_pictures

website_url = 'http://books.toscrape.com/index.html'

# Extracting the URLS of all book categories

response = requests.get(website_url)
if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')
    categories_urls_list = []
    categories_tags = soup.find('ul', class_='nav nav-list').find_all('a')[1:]
    for category_tag in categories_tags:
        category_url = 'http://books.toscrape.com/' + category_tag.get('href')
        categories_urls_list.append(category_url)

    # For each category URL collected :

    for category_url in categories_urls_list:

        # Scraping the name of the category

        category_name = get_category_name(category_url)

        # Creating a folder dedicated to this category

        create_folder_for_category(category_name)

        # While saving the path of the category folder

        category_folder_path = create_folder_for_category(category_name)

        # Extracting the pages to scrape

        pages_to_scrape = get_category_pages_to_scrape(category_url)

        # For every page collected, scraping the URLs of all books

        category_books_urls = get_category_books_urls(pages_to_scrape)

        # Extracting books' descriptions from the URLs collected

        category_books_descriptions = \
            get_category_books_descriptions(category_books_urls)

        # Formatting the name of the file to be created

        file_name = category_folder_path + category_name[0]

        # For each category, transfering all the books' descriptions
        # to a CSV file.
        # Each CSV file is located in the folder dedicated to the category

        save_scraped_data_to_csv(category_books_descriptions, file_name)

        # Extracting the cover pictures of all books

        save_category_books_pictures(category_books_urls, category_folder_path)