import requests

from bs4 import BeautifulSoup

split = '%2C'
base_site = 'http://www.epicurious.com'

def recipe_search(ingredients):
	recipes = []
	payload = '/search/?content=recipe&include='
	for ingredient in ingredients:
		payload = payload + ingredient + split
	r = requests.get(base_site + payload[:-3]) 
	soup = BeautifulSoup(r.content, "html.parser")
	results = soup.findAll('article', attrs={'class': 'recipe-content-card'})

	for result in results: 
		raw_recipe = result.find('a')
		title = raw_recipe.text
		url = base_site + raw_recipe.get('href')
		recipes.append([title,url])

	return recipes

def recipe_parse(recipe):
	instructions = []
	title = recipe[0]
	url = recipe[1]
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	steps = soup.findAll('li', attrs={'class': 'preparation-step'})

	for step in steps:
		instruction = step.text.strip().encode('ascii', 'ignore')
		instructions.append(instruction)

	return title, instructions

