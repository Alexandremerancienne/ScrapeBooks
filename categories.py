"""This program extends the work realized in books.py program \
by extracting relevant information for every book of a category.

Collected data is sent to a CSV file.

Each category is represented by a folder containing the CSV file, \
as well as all cover pictures of the books in the same category."""


import os.path
import urllib.request

import requests
from bs4 import BeautifulSoup

from books import get_book_description_from_url
from books import save_scraped_data_to_csv


def get_category_name(category_url):
    """Function scraping the name of the category"""

    category_name = []
    response = requests.get(category_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        name_of_category = soup.find('h1').text
        category_name.append(name_of_category)

    return category_name


def create_folder_for_category(category_name):
    """Function creating a folder for each category to visualize output"""

    try:
        category_folder_path = r'./Scraping Program/' + category_name[0] + '/'
        if not os.path.exists(category_folder_path):
            os.makedirs(category_folder_path)
    except FileNotFoundError:
        print("Folder cannot be created for the category:", category_name)

    return category_folder_path


def get_category_pages_to_scrape(category_url):
    """Function returning the pages to scrape for a category"""

    pages_to_scrape = []
    first_page = category_url
    pages_to_scrape.append(first_page)
    for i in range(2, 9):
        page_no_i = first_page.replace('index', 'page-' + str(i))
        response = requests.get(page_no_i)
        if response.ok:
            pages_to_scrape.append(page_no_i)

    return pages_to_scrape


def get_category_books_urls(pages_to_scrape):
    """Function displaying the URLs of all the books from a category"""

    category_books_urls = []
    for page in pages_to_scrape:
        response = requests.get(page)
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('h3')
        for book in books:
            url_root = 'http://books.toscrape.com/catalogue/'
            book_url = book.find('a')['href'].replace('../../../', url_root)
            category_books_urls.append(book_url)

    return category_books_urls


def get_category_books_descriptions(category_books_urls):
    """Function displaying the content of all the books from a category."""

    category_books_descriptions = []
    for category_book_url in category_books_urls:
        category_book_description = \
                     get_book_description_from_url(category_book_url)
        category_books_descriptions.extend(category_book_description)

    return category_books_descriptions


def save_category_books_pictures(category_books_urls, category_folder_path):
    """Function uploading the book covers of all the books from a \
    category. The covers are saved as .jpg pictures """

    for book_url in category_books_urls:
        book_description = get_book_description_from_url(book_url)
        book_description = book_description[0]
        picture_url = book_description[-1]
        picture_title = book_description[2]
        urllib.request.urlretrieve(picture_url, category_folder_path
                                   + picture_title + '.jpg')

# Testing function


if __name__ == '__main__':
    url_root = 'http://books.toscrape.com/catalogue/'
    category_url = url_root + 'category/books/mystery_3/index.html'
    category_name = get_category_name(category_url)
    create_folder_for_category(category_name)
    category_folder_path = create_folder_for_category(category_name)
    pages_to_scrape = get_category_pages_to_scrape(category_url)
    category_books_urls = get_category_books_urls(pages_to_scrape)
    category_books_descriptions = \
        get_category_books_descriptions(category_books_urls)
    file_name = category_folder_path + category_name[0]
    save_scraped_data_to_csv(category_books_descriptions, file_name)
    save_category_books_pictures(category_books_urls, category_folder_path)