import csv

import requests
from bs4 import BeautifulSoup


def get_book_description_from_url(book_url):
    """Function scraping the following info from book URL : 
    - Universal Product Code (UPC)
    - Title
    - Price including tax
    - Price excluding tax
    - Number available
    - Product description
    - Category
    - Review rating
    - Picture URL"""

    response = requests.get(book_url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='table table-striped').find_all('td')
        universal_product_code = table[0].text
        title = soup.h1.text.replace(':','-')
        price_includ_tax = table[3].text
        price_exclud_tax = table[2].text
        number_available = table[5].text
        if soup.find('div', id='product_description'):
            product_description = soup.h2.find_next('p').text
        else:
            product_description = "No description available"
        category = soup.find('ul', class_='breadcrumb').find_all('a')[2].text
        review_rating = soup.find('p', class_='star-rating')['class'][1]
        picture_url = soup.find('div', class_='item active').find('img')['src'].replace('../..', 'http://books.toscrape.com')

        return [book_url, universal_product_code, title, price_includ_tax, price_exclud_tax, number_available, product_description, category, review_rating, picture_url]       

def save_book_description_to_csv(book_url):
    """Function designed collected infos in a CSV file"""
    
    book_description = get_book_description_from_url(book_url)
    title = book_description[2]
    with open(title + '.csv', 'w', newline ='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Product Page URL', 'Universal Product Code (UPC)', 'Title', 'Price Including Tax', 'Price Excluding Tax', 'Availability', 'Product Description', 'Category', 'Review Rating', 'Picture URL'])
        writer.writerow(book_description)  

# Testing function 

if __name__ == '__main__':
    save_book_description_to_csv('http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html')