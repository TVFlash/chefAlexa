import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def start_cooking():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)


@ask.intent("makeRecipe")

def create_recipe():
    dish = "Spaghetti"
    instructions = "Bring  3 QT of water to a boil, add a teaspoon of salt, add a box of Spaghetti, cook for 7-9 minutes"
    recipe_msg = render_template('recipe', dish=dish, instructions=instructions)

    #session.attributes['numbers'] = numbers[::-1]  # reverse

    return statement(recipe_msg)


@ask.intent("addIngredient", convert={ 'date': 'date'})

def answer(ingredient, date):

    #TODO Appended ingr and date to session var

    msg = render_template('addIngredient')

    return statement(msg)


if __name__ == '__main__':

    app.run(debug=True)