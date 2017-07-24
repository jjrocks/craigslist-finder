import requests
from bs4 import BeautifulSoup

def fetch_search_results():
	base = "https://sfbay.craigslist.org/search/sfc/roo"
	resp = requests.get(base, timeout=3)
	resp.raise_for_status()
	return resp.content, resp.encoding

def parse_source(html, encoding='utf-8'):
	parsed = BeautifulSoup(html, "html.parser", from_encoding=encoding)
	return parsed

def extract_listings(parsed):
	listings = parsed.find_all('li', class_='result-row')
	return listings

def get_prices(listing):
	prices = listing.find_all(class_="result-price")
	if len(prices) > 0:
		return prices[0].string
	return 0

def get_district(listing):
	hood = listing.find_all(class_="result-hood")
	if len(hood) > 0:
		return hood[0].string
	return "N/A"

def get_title(listing):
	title = listing.find_all(class_="result-title")
	return title[0].string

def get_link(listing):
	link = listing.find_all("a", class_="result-title")
	return link.
	

results = fetch_search_results()
doc = parse_source(results[0], encoding=results[1])
listings = extract_listings(doc)
# print(len(listings))
print(listings[0].prettify())
for listing in listings:
	print(get_prices(listing))
	print(get_district(listing))
	print(get_title(listing))
	print(get_link(listing))