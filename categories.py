"""This program extends the work realized in books.py program by extracting relevant information for every book of a category.

Collected data is sent to a CSV file.

Each category is represented by a folder containing the CSV file, as well as all cover pictures of the books belonging to the same category."""


import os.path
import csv
import urllib.request

import requests
from bs4 import BeautifulSoup

from books import get_book_description_from_url


def get_pages_to_scrap(category_url):
    """Function giving the number of pages to scrap for a category"""

    pages_to_scrap = []
    first_page = category_url
    pages_to_scrap.append(first_page)
    for i in range(2, 9):
        page_no_i = first_page.replace('index', 'page-' + str(i))
        response = requests.get(page_no_i)
        if response.ok:
            pages_to_scrap.append(page_no_i)

    return pages_to_scrap


def get_books_urls_from_category(category_url):
    """Function displaying all books' URLs from a category"""

    books_urls = []
    pages_to_scrap = get_pages_to_scrap(category_url)
    for page in pages_to_scrap:
        response = requests.get(page)
        soup = BeautifulSoup(response.content, 'html.parser')
        category = soup.find('h1').text
        books = soup.find_all('h3')
        for book in books:
            book_url = book.find('a')['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
            books_urls.append(book_url)

    return [category, books_urls]


def get_books_descriptions_from_category(category_url):
    """Function displaying the content of all books from a category."""

    books_descriptions = []
    category_books_urls = get_books_urls_from_category(category_url)
    category = category_books_urls[0]
    books_urls_list = category_books_urls[1]
    for book_url in books_urls_list:
        book_description = get_book_description_from_url(book_url)
        books_descriptions.append(book_description)

    return [category, books_descriptions]


def create_folder_for_category(category_url):
    """Function creating a folder for each category to visualize output"""

    category_description = get_books_descriptions_from_category(category_url)
    category = category_description[0]
    category_folder_path = r'C:/Users/Utilisateur/Desktop/Scraping Program/' + category
    if not os.path.exists(category_folder_path):
        os.makedirs(category_folder_path)
    return category_folder_path


def save_books_descriptions_to_csv(category_url):
    """Function saving category description to CSV file"""

    category_folder_path = create_folder_for_category(category_url)
    category_description = get_books_descriptions_from_category(category_url)
    category = category_description[0]
    books_descriptions = category_description[1]
    with open(category_folder_path + '/' + category + '.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Product Page URL', 'Universal Product Code (UPC)', 'Title', 'Price Including Tax', 'Price Excluding Tax', 'Availability', 'Product Description', 'Category', 'Review Rating', 'Picture URL'])
        writer.writerows(books_descriptions)


def save_books_pictures_for_category(category_url):
	"""Function uploading the book covers of all the books of a category. The covers are saved as .jpg pictures """  

    category_folder_path = create_folder_for_category(category_url)
    category_books_urls = get_books_urls_from_category(category_url)
    books_urls = category_books_urls[1]
    for book_url in books_urls:
        book_description = get_book_description_from_url(book_url)
        picture_url = book_description[-1]
        picture_title = book_description[2]
        urllib.request.urlretrieve(picture_url, category_folder_path + '/' + picture_title + '.jpg')

# Testing function


if __name__ == '__main__':
    save_books_pictures_for_category('http://books.toscrape.com/catalogue/category/books/mystery_3/index.html')