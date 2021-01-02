import requests
from bs4 import BeautifulSoup
from books import *
import csv


categories = []
books_urls = []

def extract_book_list(category_url):
	"""Function designed to extract the list of all books in a category"""

	for i in range(1,9):
		page_no_i = category_url.replace('index', 'page-' + str(i))
		response = requests.get(page_no_i)
		if response.ok : 
			soup = BeautifulSoup(response.text, 'html.parser')
			category = soup.find('h1').text
			categories.append(category)
			books = soup.find_all('h3')
			for book in books:
				book_url = book.find('a')['href'].replace('../../../', 'http://books.toscrape.com/catalogue/')
				books_urls.append(book_url)

def scrape_category(category_url):
	"""Function designed to scrape the following infos for all books of a category : 
    - Universal Product Code (UPC)
    - Title
    - Price including tax
    - Price excluding tax
    - Number available
    - Product description
    - Category
    - Review rating
    - Picture URL"""
	
	extract_book_list(category_url)
	for book_url in books_urls:
		scrape_book(book_url)


def save_category_features(category_url):
	"""Function designed collected infos in a CSV file"""

	scrape_category(category_url)
	category = categories[0]
	for category in categories:
		csvfile = open(category + '.csv', 'w', newline ='', encoding='utf-8')
		writer = csv.writer(csvfile, delimiter=';')
		writer.writerow(['Product Page URL', 'Universal Product Code (UPC)', 'Title', 'Price Including Tax', 'Price Excluding Tax', 'Availability', 'Product Description', 'Category', 'Review Rating', 'Picture URL'])
		writer.writerows(books) 

# Testing function

if __name__ == '__main__':
    save_category_features('http://books.toscrape.com/catalogue/category/books/fiction_10/index.html')