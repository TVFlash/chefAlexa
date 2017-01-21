import requests

from bs4 import BeautifulSoup

split = '%2C'

def search_bot(ingredients):
	payload = 'http://www.epicurious.com/search?include='
	for ingredient in ingredients:
		payload = payload + ingredient + split
	r = requests.get(payload) #Todo, remove last 3 chars

	titles = [article.text for article in soup.findAll('article', attrs={'class': 'recipe-content-card'})]

	#TODO select one of the returned results and grab the recipe link
