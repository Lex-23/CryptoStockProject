import requests
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/cryptocurrencies"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
parse_names = soup.find_all("td", attrs={"aria-label": "Symbol"})
parse_descriptions = soup.find_all("td", attrs={"aria-label": "Name"})
parse_price = soup.find_all("td", attrs={"aria-label": "Price (Intraday)"})

parse_all = soup.find_all("tr")

assets_list = []
for name, desc, price in zip(parse_names, parse_descriptions, parse_price):
    asset = {
        "name": name.text.split("-")[0],
        "description": desc.text.split()[0],
        "price": price.text.replace(",", ""),
    }
    assets_list.append(asset)

print(assets_list)
