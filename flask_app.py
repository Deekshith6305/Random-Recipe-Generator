from flask import Flask, request

import google.generativeai as genai

app = Flask(__name__)

def generate_recipe(ingredients, filters, dine_preference, diet_preference, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Generate a {diet_preference} {dine_preference} recipe using the following ingredients: {', '.join(ingredients)}"

    # Add filtering options to the prompt
    if filters:
        prompt += f" with {', '.join(filters)}"

    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Recipe Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
            }

            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }

            h2 {
                color: #333;
            }

            form label {
                display: block;
                margin-bottom: 5px;
            }

            form input[type="text"],
            form select {
                width: 100%;
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }

            form input[type="submit"] {
                background-color: #007bff;
                color: #fff;
                padding: 10px 20px;
                border: none;
                border-radius: 3px;
                cursor: pointer;
            }

            form input[type="submit"]:hover {
                background-color: #0056b3;
            }
        </style>
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
    user_input = request.form['ingredients']
    ingredients = [ingredient.strip() for ingredient in user_input.split(',')]

    user_filters = request.form['filters']
    filters = [f.strip() for f in user_filters.split(',')]

    dine_preference = request.form['dine_preference']
    diet_preference = request.form['diet_preference']

    api_key = 'AIzaSyCrUlzPEtNAWEANTmLcM7dOgcQiV1M7zAs'
    generated_recipe = generate_recipe(ingredients, filters, dine_preference, diet_preference, api_key)
    return f'''
    <html>
    <head>
        <title>Generated Recipe</title>
        <link rel="stylesheet" type="text/css" href="/static/styles.css">
    </head>
    <body>
        <div class="container generated-recipe">
            <h2>Generated Recipe</h2>
            <p>{generated_recipe}</p>
            <br>
            <a href="/">Back to Recipe Generator</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, port=6000)
