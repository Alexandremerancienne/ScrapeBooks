import requests
from bs4 import BeautifulSoup

from categories import save_books_descriptions_to_csv
from categories import save_books_pictures_for_category

website_url = 'http://books.toscrape.com/index.html'

# Extraction of the URLs of all categories

response = requests.get(website_url)
if response.ok:
	soup = BeautifulSoup(response.content, 'html.parser')
	categories_urls_list = []
	categories_tags = soup.find('ul', class_ = 'nav nav-list').find_all('a')[1:]
	for category_tag in categories_tags:
		category_url = 'http://books.toscrape.com/' + category_tag.get('href')
		categories_urls_list.append(category_url)

	for category_url in categories_urls_list:
		save_books_descriptions_to_csv(category_url)
		save_books_pictures_for_category(category_url)