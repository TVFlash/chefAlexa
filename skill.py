import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from scraper import recipe_search, recipe_parse

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

follow_up = " Can I do anything else for you today?"

step_prompt = " Say next step to continue or last step to go back."

instructions = []

fridge = []

dish = ""

index = 0

@ask.launch

def start_cooking():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("makeRecipe")

def create_recipe():
    recipes = recipe_search(fridge)
    global dish
    global instructions
    dish, instructions = recipe_parse(recipes[0]) #TODO add math.random
    return read_step()


@ask.intent("nextStep")

def next_step():
    global index
    index = index + 1
    return read_step()


@ask.intent("lastStep")

def last_step():
    return read_step()


def read_step():
    if index >= len(instructions):
        return statement("Bon appetit")

    if index is 0:
        recipe_msg = render_template('recipe', dish=dish, instructions=instructions[index])
    else:
        recipe_msg = render_template('step', instructions=instructions[index])

    return question(recipe_msg + step_prompt).simple_card(title='How to make {} step {}:'.format(dish, index), content=instructions[index]) 


@ask.intent("addIngredient")

def add_ingredient(ingredient):

    fridge.append(ingredient)

    msg = render_template('addIngredient', ingredient=ingredient)

    return question(msg + follow_up)


@ask.intent("addTwoIngredients")

def add_two_ingredients(firstIngredient, secondIngredient):

    fridge.append(firstIngredient)
    fridge.append(secondIngredient)

    msg = render_template('addIngredient', ingredient=firstIngredient + ' and ' + secondIngredient)

    return question(msg + follow_up)


@ask.intent("removeIngredient")

def remove_ingredient(ingredient):

    if ingredient in fridge:
        fridge.remove(ingredient)
        msg = render_template('removeIngredient', ingredient=ingredient)
    else:
        msg = render_template('missingIngredient', ingredient=ingredient)

    return question(msg + follow_up)


@ask.intent("inFridge")

def display_fridge():
    fridge_msg = render_template('contents', ingredients=fridge)
    return question(fridge_msg)


@ask.intent("finishCooking")

def finish_cooking():

    return statement("Goodbye")
#TODO, turn add / remove into questions, create noIntent if the user no longer wishes to continue

if __name__ == '__main__':

    app.run(debug=True)