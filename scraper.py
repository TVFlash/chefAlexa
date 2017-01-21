import requests

from bs4 import BeautifulSoup

split = '%2C'
base_site = 'http://www.epicurious.com'
def recipe_search(ingredients):
	recipe = {}
	payload = '/search/?content=recipe&include='
	for ingredient in ingredients:
		payload = payload + ingredient + split
	r = requests.get(base_site + payload) #Todo, remove last 3 chars
	soup = BeautifulSoup(r.content, "html.parser")
	results = soup.findAll('article', attrs={'class': 'recipe-content-card'})

	for result in results: 
		raw_recipe = result.findAll('a')[0]
		title = raw_recipe.text
		url = base_site + raw_recipe.get('href')
		recipe[title] = url

	return recipe

if __name__ == "__main__":
	print recipe_search(['bacon', 'eggs'])

