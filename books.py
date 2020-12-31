import requests
from bs4 import BeautifulSoup
import csv


def scrape_book(book_url):
    """Function designed to scrape infos from book URL

    Output : 

    - scraped infos
    - .csv file with book title"""

    response = requests.get(book_url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        information_table = soup.find('table', class_='table table-striped').find_all('td')
        universal_product_code = information_table[0].text
        title = soup.h1.text.replace(':','-')
        price_includ_tax = information_table[3].text.replace('Â', '')
        price_exclud_tax = information_table[2].text.replace('Â', '')
        number_available = information_table[5].text
        if soup.find('div', id='product_description'):
                product_description = soup.h2.find_next('p').text.replace('âs', "'s").replace('â', '-').replace('â', '"').replace('â', '"')
        else:
            product_description = "No description available"
        category = soup.find('ul', class_='breadcrumb').find_all('a')[2].text
        review_rating = soup.find('p', class_='star-rating')['class'][1]
        picture_url = soup.find('div', class_='item active').find('img')['src'].replace('../..', 'http://books.toscrape.com')

        file = open(title + '.csv', 'w', encoding='utf-8') 
        file.write('Product Page URL ; Universal Product Code (UPC) ; Title ; Price Including Tax ; Price Excluding Tax ; Availability ; Product Description ; Category ; Review Rating ; Picture URL ; \n')
        file.write(book_url + ';' + universal_product_code + ';' + title + ';' + price_includ_tax + ';' + price_exclud_tax + ';' + number_available + ';' + product_description + ';' + category + ';' + review_rating + ';' + picture_url + '\n')
        file.close()

# Testing function 

if __name__ == '__main__':
    scrape_book('http://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html')
