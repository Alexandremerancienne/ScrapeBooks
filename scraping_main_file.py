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

from categories import *

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

    # For each category extracted :

    for category_url in categories_urls_list:

        # Scraping of the name of the category

    	name_of_category = get_category_name(category_url)

        # Creation of a folder dedicated to this category

    	create_folder_for_category(category_name)

        # Extraction of the number of pages to scrape

    	scraped_pages = get_category_pages_to_scrape(category_url)

        # For every page scraped, extraction of the URLs of all books 
        # Belonging to the same category

    	category_urls = get_category_books_urls(scraped_pages)

        # Extraction of every book description from the URLs collected

    	category_descriptions = get_category_books_descriptions(category_urls)

        # For each category, transfer of all the books' descriptions 
        # to a CSV file. 
        # Each CSV file is located in the folder dedicated to the category

    	save_books_descriptions_to_csv(category_descriptions)

        # Extraction of the cover pictures of all books

    	save_books_pictures_for_category(category_urls)