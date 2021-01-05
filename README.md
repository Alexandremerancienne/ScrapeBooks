# scraping_program

Scraping program for a book-selling website

# Description

This program aims at scraping book-selling website [Books To Scrape](http://books.toscrape.com/) to extract the following information for every book displayed :

* product_page_url 
* universal_ product_code (upc) 
* title price_including_tax 
* price_excluding_tax 
* number_available 
* product_description 
* category 
* review_rating 
* image_url

As books are organized by category (50 categories overall), each category is represented by a folder including :

* A CSV file with aforementioned information for all books within the same category.
* Cover pictures of the books within the same category.

The program uses the results and outputs of the fonctions defined by the two following programs :

* books.py (scraping useful information for any book of Books to Scrape website).
* categories.py (scraping useful information for any category of Books to Scrape website).

# Create and activate your virtual environment (venv) 

## Create venv

1. In your terminal, head to your project location.
2. Once inside the folder project, execute the command (Windows OS): `python -m venv <environment name>`

Usually, virtual environments are named env.

## Activate venv

On Windows, a virtual environment, once created, generates a batch file called activate.bat. This file is located in the Scripts folder.

To be used, a venv needs to be activated :

1. Execute activate.bat file : `\pathto\env\Scripts\activate.bat`
2. Your file path should change to reflect the activation of your venv.

If needed, you can deactivate your venv by replacing `activate.bat` by `deactivate.bat` in the previous command, and execute it.

# Execute script

Once your venv is activated, you must ensure all required Python packages have been installed, so as to execute the script correctly :

1. Open the requirements.txt file and install all mentioned packages. Make sure you install the correct version of each package (the versions are precised in the requirements file).
2. Download the files books.py, categories.py and scraping_main_file.py
3. **IMPORTANT : in categories.py file, line 60 : change folder path to indicate where you want to create your output folder : `category_folder = r'<path/of/your/folder>' + category`**
4. Run scraping_main_file.py with the following command in your terminal (Windows OS) : `python scraping_main_file.py`
