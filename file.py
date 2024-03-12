from flask import Flask, render_template, request
import requests

app = Flask(__name__)

from dotenv import load_dotenv
import os

# # Load environment variables from .env
# load_dotenv()

# # Access environment variables
# db_host = os.getenv("DB_HOST")
# db_user = os.getenv("DB_USER")
# db_password = os.getenv("DB_PASSWORD")


from config import DB_CONFIG
import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Replace with the actual PokéAPI endpoint for Pokémon data
POKEMON_API_URL = "https://pokeapi.co/api/v2/"

def get_pokemon_by_name(pokemon_name):
    url = f"{POKEMON_API_URL}/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        # Extract relevant information (e.g., name, stats, abilities, etc.)
        return pokemon_data
    else:
        return None
    
def get_pokemon_description(characteristic_id):
    url = f"https://pokeapi.co/api/v2/characteristic/{characteristic_id}/"
    response = requests.get(url)

    if response.status_code == 200:
        characteristic_data = response.json()
        description = characteristic_data['descriptions'][7]['description']
        return description
    else:
        return None

# Fetch all Pokémon names and URLs
def get_all_pokemon_all_type():
    response = requests.get(f"{POKEMON_API_URL}/type?limit=10")  # Adjust limit as needed
    data = response.json()
    return data["results"]

def get_characteristic_id(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    response = requests.get(url)

    if response.status_code == 200:
        pokemon_data = response.json()
        characteristic_id = pokemon_data['id']  # Use the Pokémon ID as the characteristic ID
        return characteristic_id
    else:
        return 0  # Default value if Pokémon not found


@app.route('/')
def dashboard():
    all_type = get_all_pokemon_all_type()

    return render_template('dashboard.html',all_type=all_type)

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('pokemon_name')
    if not query:
        return "Please enter a Pokémon name."

    result = get_pokemon_by_name(query)
    if result:
        # Assume characteristic ID 1 for now (you can replace with the actual ID)
        characteristic_id = get_characteristic_id(result['name']) #GET_BY_ID_CHARACTER
        description = get_pokemon_description(characteristic_id)
        result['description'] = description

        return render_template('result.html', pokemon=result)
    else:
        return "Nama pokemonmu salah"


# RATINGS
pokemon_ratings = {}

@app.route('/rate', methods=['POST'])
def rate_pokemon():
    pokemon_name = request.form.get('pokemon_name')
    rating = request.form.get('rating')

    if pokemon_name and rating:
        # Store the rating in the dictionary
        pokemon_ratings[pokemon_name] = int(rating)
        return f"Rated {pokemon_name} with a score of {rating}"
    else:
        return "Please provide both a Pokémon name and a rating."

# def post(cls, name):
#         try:
#             rules = {
#                 'star': ['required', 'numeric'], 
#                 'title': ['required', 'string'],
#                 'content': ['required', 'string']
#             }
#             # messages = {
#             #     'name.required': 'Yikes! The name is required',
#             #     'name.alpha': 'Yikes! The name must be a string',
#             # }
            
#             validator = Validator(rules=rules, request=request)
#             if validator.passes():
#                 user = PokeReview(
#                     id = uuid.uuid4(),
#                     star=request.json['star'],
#                     title=request.json['title'],
#                     content=request.json['content'],
#                     pokemon_name = name,
#                     user_ip=request.remote_addr,
#                     user_agent=request.user_agent.string
#                 )
#                 db.session.add(user)
#                 db.session.commit()

#                 return make_response(jsonify({'message': 'success'}), 200)
#             else:
#                 return make_response(jsonify(validator.messages()), 400)
#         except Exception as e:  
#             current_app.logger.error(traceback.format_exc())
#             return make_response(jsonify({'error': 'Internal Server Error'}), 500)
        
# def get(cls, name):
#         try:
#             rules = {
#                 'name': ['required', 'alpha']
#             }
#             messages = {
#                 'name.required': 'Yikes! The name is required',
#                 'name.alpha': 'Yikes! The name must be a string',
#             }
            
#             validator = Validator(rules=rules, messages=messages, request={'name': name})
#             if validator.passes():
#                 reviews = PokeReview.query.filter_by(pokemon_name=name).all()
#                 return make_response(jsonify([{
#                     'id': str(review.id),
#                     'star': review.star,
#                     'title': review.title,
#                     'content': review.content,
#                     'pokemon_name': review.pokemon_name,
#                     'user_ip': review.user_ip,
#                     'user_agent': review.user_agent,
#                     'created_at': review.created_at,
#                     'updated_at': review.updated_at
#                 } for review in reviews]), 200)
#             else:
#                 return make_response(jsonify(validator.messages()), 400)
#         except Exception as e:  
#             current_app.logger.error(traceback.format_exc())
#             return make_response(jsonify({'error': 'Internal Server Error'}), 500)


def get_pokemon_details(pokemon_url):
    response = requests.get(pokemon_url)
    return response.json()

# def get_all_pokemon_all_type():
#     response = requests.get("{POKEMON_API_URL}/type?limit=10")  # Adjust limit as needed
#     data = response.json()
#     return data["results"]

def get_list_pokemon():
    response = requests.get(f"{POKEMON_API_URL}/type/{id}")
    data = response.json()                            
    return data["results"]

def get_list_pokemon(type_name):
    type_url = f"{POKEMON_API_URL}/type/{type_name.lower()}"
    type_response = requests.get(type_url)
    type_data = type_response.json()

    pokemon_urls = [p["pokemon"]["url"] for p in type_data["pokemon"]]
    pokemon_list = []


    for url in pokemon_urls:
        pokemon_response = requests.get(url)
        pokemon_data = pokemon_response.json()
        # pokemon_details = pokemon_data["pokemon"]
        pokemon_list.append({
            "id": pokemon_data["id"],
            "name": pokemon_data["name"],
            "image": pokemon_data["sprites"]["front_default"],
            "image2" : pokemon_data["sprites"]["back_default"],
            "hp": pokemon_data["stats"][0]["base_stat"],
            "attack": pokemon_data["stats"][1]["base_stat"],
            "defense": pokemon_data["stats"][2]["base_stat"]
        })

    return pokemon_list

@app.route("/filter/type/<type_name>")
def filter_by_type(type_name):
    try:
        filtered_pokemon = get_list_pokemon(type_name)
        return render_template("filtered_pokemon.html", pokemon_list=filtered_pokemon)

    except Exception as e:
        return f"Error fetching Pokémon data: {str(e)}"

# @app.route("/filter/type/<type_name>")
# def filter_by_type(type_name):
#     try:
#         all_pokemon = get_all_pokemon_all_type()
#         # pokemon_list = get_list_pokemon()
#         filtered_pokemon = []

#         for pokemon in all_pokemon:
#             details = get_pokemon_details(pokemon["url"])
#             pokemon_types = [t["type"]["name"] for t in details["types"]]
            
#             pokemon_url = pokemon["pokemon"]["url"]
#             pokemon_response = requests.get(pokemon_url)
#             pokemon_data = pokemon_response.json()
            
#             if type_name.lower() in pokemon_types:
#                 # Extract relevant data (name, image, stats) and add to filtered_pokemon
#                 # Example: stats = details["stats"], image_url = details["sprites"]["front_default"]
#                 stats = details["stats"]
#                 image_url = pokemon_data["sprites"]["front_default"]
#                 filtered_pokemon.append({
#                     "name": pokemon["name"],
#                     "image": image_url,
#                     "hp": stats[0]["base_stat"],
#                     "attack": stats[1]["base_stat"],
#                     "defense": stats[2]["base_stat"]
#                 })

#         return render_template("filtered_pokemon.html", pokemon_list=filtered_pokemon)

#     except Exception as e:
#         return f"Error fetching Pokémon data: {str(e)}"
    
if __name__ == '__main__':
    app.run(debug=True)
