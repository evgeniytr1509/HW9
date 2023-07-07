import requests
from bs4 import BeautifulSoup
import json

# Функция для извлечения информации о цитатах
def scrape_quotes():
    quotes = []
    page = 1
    while True:
        url = f"http://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        quote_divs = soup.find_all('div', class_='quote')
        if not quote_divs:
            break
        for quote_div in quote_divs:
            quote = {
                'quote': quote_div.find('span', class_='text').get_text(),
                'author': quote_div.find('small', class_='author').get_text(),
                'tags': [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]
            }
            quotes.append(quote)
        page += 1
    return quotes

# Функция для извлечения информации об авторах
def scrape_authors(quotes):
    authors = []
    for quote in quotes:
        author = {
            'fullname': quote['author'],
            'born_date': '',
            'born_location': '',
            'description': ''
        }
        if author not in authors:
            authors.append(author)
    return authors

# Функция для извлечения даты рождения и места рождения автора
def scrape_author_details(author):
    url = f"http://quotes.toscrape.com/author/{author['fullname'].replace(' ', '-')}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    born_date = soup.find('span', class_='author-born-date').get_text()
    born_location = soup.find('span', class_='author-born-location').get_text()[3:]
    description = soup.find('div', class_='author-description').get_text().strip()
    author['born_date'] = born_date
    author['born_location'] = born_location
    author['description'] = description
    return author

# Скрапинг цитат
quotes = scrape_quotes()

# Запись цитат в файл quotes.json
with open('quotes.json', 'w') as f:
    json.dump(quotes, f, indent=4)

# Скрапинг информации об авторах и их деталей
authors = scrape_authors(quotes)
authors_with_details = [scrape_author_details(author) for author in authors]

# Запись информации об авторах в файл authors.json
with open('authors.json', 'w') as f:
    json.dump(authors_with_details, f, indent=4)
