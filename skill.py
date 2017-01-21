import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

follow_up = "Can I do anything else for you today?"

fridge = []

@ask.launch

def start_cooking():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("makeRecipe")

def create_recipe():
    dish = "Spaghetti"
    instructions = "Bring 3 quarts of water to a boil, add a teaspoon of salt, add a box of Spaghetti, cook for 7-9 minutes"
    recipe_msg = render_template('recipe', dish=dish, instructions=instructions)

    return statement(recipe_msg).simple_card(title='How to make {}'.format(dish), text=instructions)


@ask.intent("addIngredient")

def add_ingredient(ingredient):

    fridge.append(ingredient)

    msg = render_template('addIngredient', ingredient=ingredient)

    return statement(msg)

@ask.intent("removeIngredient")

def remove_ingredient(ingredient):

    if ingredient in fridge:
        fridge.remove(ingredient)
        msg = render_template('removeIngredient', ingredient=ingredient)
    else:
        msg = render_template('missingIngredient', ingredient=ingredient)

    return statement(msg)

#TODO, turn all statements into questions, create noIntent if the user no longer wishes to continue

if __name__ == '__main__':

    app.run(debug=True)