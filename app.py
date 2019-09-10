import os
from flask import Flask, render_template, url_for, request, redirect
import requests

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") # this connects to heroku database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from sqlalchemy.orm import sessionmaker

# tis part is needed to create session to query database.  this should be JUST BELOW app.config..
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
engine = create_engine(os.getenv("DATABASE_URL"), echo = True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


# BUILD DATABASE CLASS HERE
class EasySeach_Feedback(Base):
	__tablename__ = 'easysearch_feedback'
	id = Column('id', Integer, primary_key=True)
	name = Column('name', String(30))
	experience = Column('experience', String(12))
	functionality = Column('functionality', String(12))
	aesthetics = Column('aesthetics', String(12))
	comment = Column('comment', String(800))

	def __init__(self, name, experience, functionality, aesthetics, comment):
		self.name = name
		self.experience = experience
		self.functionality = functionality
		self.aesthetics = aesthetics
		self.comment = comment

Session = sessionmaker(bind = engine)
session = Session()


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

		querystring = {"query":f"{ing}","includeIngredients":f"{ing}","excludeIngredients":"bacon","ranking":"2","instructionsRequired":"true","addRecipeInformation":"true","limitLicense":"true","number":"1"}

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

@app.route('/easyseach_feedback', methods=['GET', 'POST'])
def easysearch_feedback():
	if request.method == 'GET':
		data = session.query(EasySeach_Feedback).all()
		return render_template('easysearch_feedback.html', data=data)
	else:
		name = request.form.get('name')
		exp = request.form.get('experience')
		func = request.form.get('functionality')
		looks = request.form.get('aesthetics')
		message = request.form.get('subject')

		db_data = EasySeach_Feedback(name, exp, func, looks, message)
		session.add(db_data)
		session.commit()

		data = session.query(EasySeach_Feedback).all()

		return render_template('easysearch_feedback.html', data=data)


@app.route('/foods_feed')
def foods_feed(): 
	url = ('https://newsapi.org/v2/everything?'
       'q=cooking&food&culinary&chef&recipes&kitchen&cuisine&health&nutrition&'
       'from=2019-09-10&'
       'sortBy=popularity&'
       'apiKey=134b50d54e2948399817da7fa47477b0')

	response = requests.get(url)

	r = response.json()

	newsBlock = r['articles']
	return render_template('foods_feed.html', newsBlock=newsBlock)




if __name__ == '__main__':
    app.run(debug=True)
