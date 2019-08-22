from flask import Flask, render_template, url_for, request, redirect
import requests

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/random', methods=["GET", "POST"])
def random():
	if request.method == 'GET':
		url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"

		querystring = {"number":"1",}

		headers = {
		    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
		    'x-rapidapi-key': "670505dc3fmsh9cd923658f74705p10c323jsnc8539188f679"
		    }

		response = requests.request("GET", url, headers=headers, params=querystring)

		# print(response.text)

		# Dictionary key='recipe' value=list(dict())
		data = response.json()

		# List with dictionary inside
		data = data['recipes']

		# Accessing the dictionary
		recipe = data[0]

		# Name of recipe
		title = data[0]['title']


		# To get Acces to Ingredients
		extendedIng = data[0]['extendedIngredients']
		ex = extendedIng[0]
		rec = recipe['extendedIngredients']

		# # List of Ingredients
		# for x in rec:
		# 	print(x['originalString'])

		# Recipe instructions
		instruct = data[0]['instructions']

		# Source Url of recipe
		source = data[0]['sourceUrl']

		# Acces to just one of the ingredients (we need all)
		x1 = ex['originalString']

		return render_template('random_recipe.html', title=title, rec=rec, instruct=instruct, source=source)

@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		return render_template('search.html')
	else:
		ing = request.form.get("ingredients")

		if ing:

			url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/searchComplex"
			querystring = {"query":f"{ing}","includeIngredients":"onions, garlic, tomato","excludeIngredients":"bacon","ranking":"2","instructionsRequired":"true","addRecipeInformation":"true","limitLicense":"true","number":"1"}

			headers = {
			    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
			    'x-rapidapi-key': "670505dc3fmsh9cd923658f74705p10c323jsnc8539188f679"
			    }
			response = requests.request("GET", url, headers=headers, params=querystring)
			data = response.json()

			# Accessing dictionary
			data = data['results'][0]

			# Title of recipe
			title = data['title']

			# Time to cook
			duration = data['readyInMinutes']

			# image URL
			image = data['image']

			# URL source
			url_source = data['sourceUrl']

			# List of recipes
			analyzedInstructions = data['analyzedInstructions'][0]
			steps = analyzedInstructions['steps']


			return render_template('search.html', title=title, duration=duration, image=image, url_source=url_source, steps=steps)

if __name__ == '__main__':
    app.run(debug=True)
