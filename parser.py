import requests
from bs4 import BeautifulSoup

current_number = {
    "zhivotnye": 0
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def get_data(category):
    current_number[category] += 1
    link = f"https://www.avito.ru/moskva/{category}"
    response = requests.get(link)
    print(response.status_code)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")
    item = soup.select_one(f"[data-marker=item]:nth-of-type({current_number[category]})")
    print(item)


get_data("zhivotnye")
