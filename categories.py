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


category_name = []


def get_category_name(category_url):
    """Function scraping the name of the category"""

    response = requests.get(category_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        name_of_category = soup.find('h1').text
        category_name.append(name_of_category)

    return category_name[-1]


def create_folder_for_category(category_name):
    """Function creating a folder for each category to visualize output"""

    try:
        category_folder_path = r'./Scraping Program/' + category_name[-1] + '/'
        if not os.path.exists(category_folder_path):
            os.makedirs(category_folder_path)
    except FileNotFoundError:
        print("Folder cannot be created for the category:", category_name)

    return category_folder_path


pages_to_scrape = []


def get_category_pages_to_scrape(category_url):
    """Function giving the number of pages to scrap for a category"""

    number_of_pages = 0
    first_page = category_url
    pages_to_scrape.append(first_page)
    for i in range(2, 9):
        page_no_i = first_page.replace('index', 'page-' + str(i))
        response = requests.get(page_no_i)
        if response.ok:
            number_of_pages += 1
            pages_to_scrape.append(page_no_i)

    return pages_to_scrape[(-number_of_pages-1):]


category_books_urls = []


def get_category_books_urls(pages_to_scrape):
    """Function displaying the URLs of all the books from a category"""

    number_of_urls = 0
    for page in pages_to_scrape:
        response = requests.get(page)
        soup = BeautifulSoup(response.content, 'html.parser')
        books = soup.find_all('h3')
        for book in books:
            url_root = 'http://books.toscrape.com/catalogue/'
            book_url = book.find('a')['href'].replace('../../../', url_root)
            category_books_urls.append(book_url)
            number_of_urls += 1

    return category_books_urls[(-number_of_urls):]


category_books_descriptions = []


def get_category_books_descriptions(category_books_urls):
    """Function displaying the content of all the books from a category."""

    number_of_books_descriptions = 0
    for category_book_url in category_books_urls:
        category_book_description = \
                     get_book_description_from_url(category_book_url)
        category_books_descriptions.append(category_book_description)
        number_of_books_descriptions += 1
        return category_books_descriptions[(-number_of_books_descriptions):]


def save_books_descriptions_to_csv(category_books_descriptions):
    """Function saving category description to CSV file"""

    category_folder_path = create_folder_for_category(category_name)
    file_name = category_folder_path + category_name[-1]
    save_scraped_data_to_csv(category_books_descriptions, file_name)


def save_books_pictures_for_category(category_books_urls):
    """Function uploading the book covers of all the books from a \
    category. The covers are saved as .jpg pictures """

    category_folder_path = create_folder_for_category(category_name)
    for book_url in category_books_urls:
        book_description = get_book_description_from_url(book_url)
        picture_url = book_description[-1]
        picture_title = book_description[2]
        urllib.request.urlretrieve(picture_url, category_folder_path
                                   + picture_title + '.jpg')

# Testing function


if __name__ == '__main__':
    url_root = 'http://books.toscrape.com/catalogue/'
    category_url = url_root + 'category/books/mystery_3/index.html'
    get_category_name(category_url)
    create_folder_for_category(category_name)
    get_category_pages_to_scrape(category_url)
    get_category_books_urls(pages_to_scrape)
    get_category_books_descriptions(category_books_urls)
    save_books_descriptions_to_csv(category_books_descriptions)
    save_books_pictures_for_category(category_books_urls)