import requests
from bs4 import BeautifulSoup
from books import *
import csv

def scrape_category(category_url):
	"""Function designed to scrape the URLs of all products
	for a page of a category"""

	books_urls = []
	for i in range(1,9):
		page_no_i = category_url.replace('index', 'page-' + str(i))
		response = requests.get(page_no_i)
		if response.ok : 
			soup = BeautifulSoup(response.text, 'html.parser')
			category = soup.find('h1').text
			books = soup.find_all('h3')
			for book in books:
				book_url = book.find('a')['href']
				book_url = book_url.replace('../../../', 'http://books.toscrape.com/catalogue/')
				books_urls.append(book_url)

			txtfile = open(category + '.txt', 'w') 
			for book_url in books_urls:
				txtfile.write(book_url + '\n')
			txtfile.close()
			
			txtfile = open(category + '.txt', 'r')
			csvfile = open (category + '.csv', 'w', encoding='utf-8')
			csvfile.write('Product Page URL ; Universal Product Code (UPC) ; Title ; Price Including Tax ; Price Excluding Tax ; Availability ; Product Description ; Category ; Review Rating ; Picture URL ; \n')
			for row in txtfile:
				book_url = row.strip()
				scrape_book(book_url)
			txtfile.close()
			csvfile.close()

# Testing function

if __name__ == '__main__':
    scrape_category('http://books.toscrape.com/catalogue/category/books/fiction_10/index.html')
