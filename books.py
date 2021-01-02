import requests
from bs4 import BeautifulSoup
import csv

books = []
book_title = []

def scrape_book(book_url):
    """Function designed to scrape the following infos from book URL : 
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
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='table table-striped').find_all('td')
        universal_product_code = table[0].text
        title = soup.h1.text.replace(':','-')
        book_title.append(title)
        price_includ_tax = table[3].text.replace('Â', '')
        price_exclud_tax = table[2].text.replace('Â', '')
        number_available = table[5].text
        if soup.find('div', id='product_description'):
            product_description = soup.h2.find_next('p').text.replace('âs', "'s").replace('â', '-').replace('â', '"').replace('â', '"')
        else:
            product_description = "No description available"
        category = soup.find('ul', class_='breadcrumb').find_all('a')[2].text
        review_rating = soup.find('p', class_='star-rating')['class'][1]
        picture_url = soup.find('div', class_='item active').find('img')['src'].replace('../..', 'http://books.toscrape.com')

        book_features = [book_url, universal_product_code, title, price_includ_tax, price_exclud_tax, number_available, product_description, category, review_rating, picture_url]       
        books.append(book_features)

def save_book_features(book_url):
    """Function designed collected infos in a CSV file"""
    
    scrape_book(book_url)
    title = book_title[0]
    for book in books:
        csvfile = open(title + '.csv', 'w', newline ='', encoding='utf-8')
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['Product Page URL', 'Universal Product Code (UPC)', 'Title', 'Price Including Tax', 'Price Excluding Tax', 'Availability', 'Product Description', 'Category', 'Review Rating', 'Picture URL'])
        writer.writerow(book)  

# Testing function 

if __name__ == '__main__':
    save_book_features('http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html')