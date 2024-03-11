import requests
from bs4 import BeautifulSoup


def extract():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    }
    url = f"https://www.naukri.com/flutter-developer-jobs-in-delhi?k=flutter%20developer&l=delhi%2C%20gurugram%2C%20noida&experience=1"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'cust-job-tuple layout-wrapper')
    return len(divs)

a = extract()
print(transform(a))