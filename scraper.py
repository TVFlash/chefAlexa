import requests

from bs4 import BeautifulSoup

split = '%2C'
base_site = 'http://www.epicurious.com'
def search_bot(ingredients):
	payload = '/search/?content=recipe&include='
	for ingredient in ingredients:
		payload = payload + ingredient + split
	r = requests.get(base_site + payload) #Todo, remove last 3 chars
	soup = BeautifulSoup(r.content, "html.parser")
	results = soup.findAll('article', attrs={'class': 'recipe-content-card'})
	for result in results: 
		recipe = result.findAll('a')[0]
		print recipe.text #title
		print base_site + recipe.get('href') #url

if __name__ == "__main__":
	search_bot(['bacon', 'eggs'])