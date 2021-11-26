import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS

POKEMONS = [
    {
        'id': uuid.uuid4().hex,
        'name': 'Charizard',
        'pokeType': 'Fire',
        'caught': True
    },
    {
        'id': uuid.uuid4().hex,
        'name': 'Bulbasaur',
        'pokeType': 'Grass',
        'caught': False
    },
    {
        'id': uuid.uuid4().hex,
        'name': 'Squirtle',
        'pokeType': 'Water',
        'caught': True
    }
]


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/')
def home():
    return jsonify({'message': 'Hello from the Pokedex!'}), 200


def remove_pokemon(pokemon_id):
    for pokemon in POKEMONS:
        if pokemon['id'] == pokemon_id:
            POKEMONS.remove(pokemon)
            return True
    return False


@app.route('/pokemons', methods=['GET', 'POST'])
def all_pokemons():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        POKEMONS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'pokeType': post_data.get('pokeType'),
            'caught': post_data.get('caught')
        })
        response_object['message'] = 'Pokemon added!'
    else:
        response_object['pokemons'] = POKEMONS
    return jsonify(response_object)


@app.route('/pokemons/<pokemon_id>', methods=['PUT', 'DELETE'])
def single_pokemon(pokemon_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_pokemon(pokemon_id)
        POKEMONS.append({
            'id': uuid.uuid4().hex,
            'name': post_data.get('name'),
            'pokeType': post_data.get('pokeType'),
            'caught': post_data.get('caught')
        })
        response_object['message'] = 'pokemon updated!'
    if request.method == 'DELETE':
        remove_pokemon(pokemon_id)
        response_object['message'] = 'pokemon removed!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()
