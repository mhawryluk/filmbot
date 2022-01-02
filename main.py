from flask import Flask, request, render_template
import requests
from keys import headers, url


app = Flask(__name__)


def get_year(movie):
    response = requests.request("GET", url+movie, headers=headers)
    if response.status_code == 200:
        return response.json()['year']
    else:
        print(response.status_code)


def get_rating(movie):
    response = requests.request("GET", url+movie, headers=headers)
    if response.status_code == 200:
        return response.json()['rating']
    else:
        print(response.status_code)


def get_length(movie):
    response = requests.request("GET", url+movie, headers=headers)
    if response.status_code == 200:
        return response.json()['length']
    else:
        print(response.status_code)


def list_actors(movie):
    response = requests.request("GET", url+movie, headers=headers)
    print(response.json())
    if response.status_code == 200:
        cast = ""
        for entry in response.json()['cast']:
            cast += f'{entry["actor"]} jako {entry["character"]}\n'

        return cast[:-1]
    else:
        print(response.status_code)


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = ''

    query_result = req['queryResult']

    movie = None

    if 'NazwaFilmu' in query_result['parameters']:
        movie = query_result['parameters']['NazwaFilmu']
    elif 'nazwafilmu' in query_result['parameters']:
        movie = query_result['parameters']['nazwafilmu']
    else:
        for context in query_result['outputContexts']:
            if context['name'] == 'film-wybrany':
                movie = context["parameters"]['nazwafilmu']
                break
        else:
            for context in query_result['outputContexts']:
                if 'nazwafilmu' in context['parameters']:
                    movie = context["parameters"]['nazwafilmu']
                    break
            else:
                return {
                    'fulfillmentText': "Nie wiem o jaki film chodzi"
                }

    movie = movie.strip('"')
    action = query_result['action']
    print(action)

    if action == 'obsada':
        query = list_actors(movie)
        fulfillmentText = f'Obsada filmu {movie}:\n{query}'

    elif action == 'ocena':
        query = get_rating(movie)
        fulfillmentText = f'Film {movie} oceniono na {query}/10.'

    elif action == 'rok':
        query = get_year(movie)
        fulfillmentText = f'Film {movie} wyszedł w roku {query}'

    elif action == 'length':
        query = get_length(movie)
        fulfillmentText = f'Film {movie} trwa {query}'

    return {
        'fulfillmentText': fulfillmentText,
        'displayText': '25',
        'source': 'webhookdata'
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

