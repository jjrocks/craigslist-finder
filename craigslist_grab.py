import requests
import re
from bs4 import BeautifulSoup

prefered_hoods = ["(mission district)", "(SOMA / south beach)", "(hayes valley)", "(noe valley)", "(castro / upper market)", "(haight ashbury)"]
total_beds = ["2br", "3br"]
max_price = {"2br": 4700, "3br": 5900}

def fetch_search_results():
	base = "https://sfbay.craigslist.org/search/sfc/apa?s=120"
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
		return int(prices[0].string[1:])
	return 0

def get_district(listing):
	hood = listing.find_all(class_="result-hood")
	if len(hood) > 0:
		return hood[0].string[1:]
	return "N/A"

def get_title(listing):
	title = listing.find_all(class_="result-title")
	return title[0].string

def get_link(listing):
	link = listing.find_all("a", class_="result-title")
	return "https://sfbay.craigslist.org" + link[0].get('href')

def get_beds(listing):
	housing = listing.find_all(class_="housing")
	if len(housing) > 0:
		result = re.search(r"\dbr", str(housing[0]))
		if (result):
			return result.group(0)
		return "N/A"
	return "N/A"

def filter_via_hood(listings):
	filtered_list = []
	for listing in listings:
		if listing.district in prefered_hoods:
			filtered_list.append(listing)
	return filtered_list

def filter_via_beds(listings):
	filtered_list = []
	for listing in listings:
		if listing.beds in total_beds:
			filtered_list.append(listing)
	return filtered_list

def filter_via_price(listings):
	filtered_list = []
	for listing in listings:
		if listing.price < max_price[listing.beds]:
			filtered_list.append(listing)
	return filtered_list

class Listing(object):

	price = 0
	district = ""
	title = ""
	link = ""
	beds = ""
	org_html = None

	"""docstring for Listing"""
	def __init__(self, listing_row):
		super(Listing, self).__init__()
		self.price = get_prices(listing_row)
		self.district = get_district(listing_row)
		self.title = get_title(listing_row)
		self.link = get_link(listing_row)
		self.beds = get_beds(listing_row)

	def __str__(self):
		return str(self.price) + " - " + str(self.beds) + " - " + str(self.district) + " - " + self.title + " - " self.link
	def __repr__(self):
		return str(self)
		
	

results = fetch_search_results()
doc = parse_source(results[0], encoding=results[1])
listings = extract_listings(doc)
all_listings = []

for listing in listings:
	get_beds(listing)
	classListing = Listing(listing)
	all_listings.append(classListing)

filtered_list = filter_via_hood(all_listings)
filtered_list = filter_via_beds(filtered_list)
filtered_list = filter_via_price(filtered_list)
for filt in filtered_list:
	print(filt)