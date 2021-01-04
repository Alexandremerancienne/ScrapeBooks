import csv
import os

import requests
from bs4 import BeautifulSoup

from categories import get_books_descriptions_from_category


def get_categories_urls_from_website(website_url):
	"""Function displaying all categories' URLS from website"""

	response = requests.get(website_url)
	if response.ok:
		soup = BeautifulSoup(response.content, 'html.parser')
		categories_urls_list = []
		categories_tags = soup.find('ul', class_ = 'nav nav-list').find_all('a')[1:]
		for category_tag in categories_tags:
			category_url = category_tag.get_text(strip=True)
			categories_urls_list.append(content)

		return categories_urls_list	

def get_categories_names_from_website(website_url):
	"""Function displaying all categories' names from website"""

	response = requests.get(website_url)
	if response.ok:
		soup = BeautifulSoup(response.content, 'html.parser')
		categories_names_list = []
		categories_tags = soup.find('ul', class_ = 'nav nav-list').find_all('a')[1:]
		for category_tag in categories_tags:
			category_name = category_tag.get_text(strip=True)
			categories_names_list.append(category_name)

		return categories_names_list

def create_folders_for_categories(website_url):

	categories_names_list = get_categories_names_from_website(website_url)

	folders_paths_list = []
	for category_name in categories_names_list:
		category_folder = r'C:/Users/Utilisateur/Desktop/Scraping Program/' + category_name
		if not os.path.exists(category_folder):
			os.makedirs(category_folder)
		folders_paths_list.append(category_folder)
	return folders_paths_list

# Testing function

if __name__ == '__main__':
    create_folders_for_categories('http://books.toscrape.com/index.html')
