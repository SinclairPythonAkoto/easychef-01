from flask import Flask, render_template, url_for, request, redirect
import requests

app = Flask(__name__)

@app.route('/')
def start_pg():
	return render_template('start.html')

@app.route('/home')
def home():
	return render_template('home.html')

# @app.route('/random', methods=["GET", "POST"])
# def random():
# 	pass

		
@app.route('/search', methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		return render_template('search.html')
	else:
		ing = request.form.get("ingredients")

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

		# URL source
		url_source = data['sourceUrl']

		# image URL
		image = data['image']

		# List of recipes
		analyzedInstructions = data['analyzedInstructions'][0]
		steps = analyzedInstructions['steps']


		return render_template('search.html', title=title, duration=duration, image=image, url_source=url_source, steps=steps)

if __name__ == '__main__':
    app.run(debug=True)
