import requests

url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/mealplans/generate"

querystring = {"timeFrame":"day","targetCalories":"2000","diet":"vegetarian","exclude":"shellfish, olives"}

headers = {
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    'x-rapidapi-key': "670505dc3fmsh9cd923658f74705p10c323jsnc8539188f679"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data = response.json()

access = data['meals']

title = access[0]['title']

image = access[0]['image']



print(access[0]['image'])