import os
import requests
import markdown  # Import markdown module
from flask import Flask, request

app = Flask(__name__)

# Configure Gemini API
API_KEY = "AIzaSyCrUlzPEtNAWEANTmLcM7dOgcQiV1M7zAs"  # Hardcoded API key (not recommended)

def generate_recipe(ingredients, filters, dine_preference, diet_preference):
    prompt = f"Generate a {diet_preference} {dine_preference} recipe using the following ingredients: {', '.join(ingredients)}"
    if filters:
        prompt += f" with {', '.join(filters)}"
    
    # Call Gemini-2.0-Flash API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    
    if "candidates" in response_json:
        return response_json["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Error generating recipe. Please try again."

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Recipe Generator</title>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
    </head>
    <body>
        <div class="container">
            <h2>Generate Recipe</h2>
            <form action="/generate_recipe" method="post">
                <label for="ingredients">Enter ingredients (separated by commas):</label><br>
                <input type="text" id="ingredients" name="ingredients"><br><br>
                <label for="filters">Cuisine types (e.g., Italian, Mexican) (optional):</label><br>
                <input type="text" id="filters" name="filters"><br><br>
                <label for="dine_preference">Dine preference:</label><br>
                <select id="dine_preference" name="dine_preference">
                    <option value="breakfast">Breakfast</option>
                    <option value="lunch">Lunch</option>
                    <option value="snacks">Snacks</option>
                    <option value="night">Night (Dinner)</option>
                </select><br><br>
                <label for="diet_preference">Diet preference:</label><br>
                <select id="diet_preference" name="diet_preference">
                    <option value="healthy">Healthy</option>
                    <option value="junk">Junk Food</option>
                </select><br><br>
                <input type="submit" value="Generate Recipe">
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/generate_recipe', methods=['POST'])
def generate():
    ingredients = request.form.get("ingredients", "").split(',')
    filters = request.form.get("filters", "").split(',')
    dine_preference = request.form.get("dine_preference", "")
    diet_preference = request.form.get("diet_preference", "")
    
    generated_recipe = generate_recipe(ingredients, filters, dine_preference, diet_preference)

    # Convert Markdown syntax (**bold**, *italic*, etc.) to proper HTML
    formatted_recipe = markdown.markdown(generated_recipe)

    return f'''
    <html>
    <head>
        <title>Generated Recipe</title>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
    </head>
    <body>
        <div class="container generated-recipe">
            <h2>Generated Recipe</h2>
            <p>{formatted_recipe}</p>
            <br>
            <a href="/">Back to Recipe Generator</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=6000)

