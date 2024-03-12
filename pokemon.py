## html : pokeA,result,error
## css : poke15,result1
## font awesome ==> in folder static

from flask import Flask, render_template,jsonify,request
import requests
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('pokeA.html')

@app.route('/result', methods=['GET','POST'])
def poke():
    if request.method == 'POST':
        pokemonCari = request.form['poke']
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemonCari}'
        data = requests.get(url)
        if data.status_code == 200:
            pokemon = data.json()
            id = pokemon['id']
            height = pokemon['height']
            weight = pokemon['weight']
            name = pokemon['name']
            image = pokemon['sprites']['front_default']
            poke = ({
                'id':id,'height':height,'weight':weight,
                'name':name,'image':image
            })
            return render_template('result.html', poke=poke)
        
        else:
            return render_template('error.html')


        
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)