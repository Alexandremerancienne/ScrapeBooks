"""This program aims at scraping book-selling website "Books To Scrape" (http://books.toscrape.com/) to extract the following information for every book displayed :

- product_page_url 
- universal_ product_code (upc) 
- title price_including_tax 
- price_excluding_tax 
- number_available 
- product_description 
- category 
- review_rating 
- image_url

As books are organized by category (50 categories overall), each category is represented by a folder including :

- A CSV file with aforementioned information for all books within the same category
- Cover pictures of the books within the same category

The program uses the results and outputs of the fonctions previously defined by the following programs :

- books.py (scraping useful information for any book of "Books to Scrape" website)
- categories.py (scraping useful information for any category of "Books to Scrape" website)"""


import requests
from bs4 import BeautifulSoup

from categories import save_books_descriptions_to_csv
from categories import save_books_pictures_for_category

website_url = 'http://books.toscrape.com/index.html'

response = requests.get(website_url)
if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')
    categories_urls_list = []
    categories_tags = soup.find('ul', class_='nav nav-list').find_all('a')[1:]
    for category_tag in categories_tags:
        category_url = 'http://books.toscrape.com/' + category_tag.get('href')
        categories_urls_list.append(category_url)

    for category_url in categories_urls_list:

    # Extraction of the URLs of all categories
        save_books_descriptions_to_csv(category_url)

    # Extraction of the cover pictures of all books
        save_books_pictures_for_category(category_url)