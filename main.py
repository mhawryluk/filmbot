from flask import Flask, request, render_template
import requests
from keys import headers, url, celeb_headers, celeb_url


app = Flask(__name__)


def get_year(movie):
    response = requests.request("GET", url+movie, headers=headers)
    print(response.json())
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
    if response.status_code == 200:
        cast = ""
        for entry in response.json()['cast']:
            cast += f'{entry["actor"]} jako {entry["character"]}, '

        return cast[:-1]
    else:
        return None


CELEB_NOT_FOUND = -1
INFO_NOT_FOUND = -2


def get_info_celeb(name, info):
    response = requests.request(
        "GET", celeb_url, headers=celeb_headers, params={"name": name})
    if response.status_code == 200:
        json = response.json()

        if len(json) == 0:
            return CELEB_NOT_FOUND

        if info not in json[0]:
            return INFO_NOT_FOUND

        return json[0][info]

    else:
        return CELEB_NOT_FOUND


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    fulfillmentText = 'Przepraszam, coś poszło nie tak.'

    query_result = req['queryResult']
    action = query_result['action']

    # filmy
    if action in {"obsada", "ocena", "rok", "length"}:
        movie = None

        if 'NazwaFilmu' in query_result['parameters']:
            movie = query_result['parameters']['NazwaFilmu']
        elif 'nazwafilmu' in query_result['parameters']:
            movie = query_result['parameters']['nazwafilmu']
        else:
            for context in query_result['outputContexts']:
                if context['name'].endswith('film-wybrany'):
                    movie = context["parameters"]['nazwafilmu']
                    break
            else:
                for context in query_result['outputContexts']:
                    if 'nazwafilmu' in context['parameters']:
                        movie = context["parameters"]['nazwafilmu']
                        break

        if movie is None:
            return {
                'fulfillmentText': "Nie wiem o jaki film chodzi."
            }

        movie = movie.strip('"')

        if action == 'obsada':
            query = list_actors(movie)
            if query is not None:
                fulfillmentText = f'Obsada filmu {movie}:\n{query}'
            else:
                fulfillmentText = f'Nie udało mi się znaleźć informacji o filmie "{movie}". Obawiam się, że nie ma go w mojej bazie.'

        elif action == 'ocena':
            query = get_rating(movie)

            if query is not None:
                fulfillmentText = f'Film {movie} oceniono na {query}/10.'
            else:
                fulfillmentText = f'Nie udało mi się znaleźć informacji o filmie "{movie}". Obawiam się, że nie ma go w mojej bazie.'

        elif action == 'rok':
            query = get_year(movie)
            if query is not None:
                fulfillmentText = f'Film {movie} wyszedł w roku {query}'
            else:
                fulfillmentText = f'Nie udało mi się znaleźć informacji o filmie "{movie}". Obawiam się, że nie ma go w mojej bazie.'

        elif action == 'length':
            query = get_length(movie)
            if query is not None:
                fulfillmentText = f'Film {movie} trwa {query}'
            else:
                fulfillmentText = f'Nie udało mi się znaleźć informacji o filmie "{movie}". Obawiam się, że nie ma go w mojej bazie.'
    # celebs
    elif action in {'age', 'birthday', 'occupation', 'height'}:
        celeb = None

        if 'person' in query_result['parameters']:
            celeb = query_result['parameters']['person']['name']
        else:
            for context in query_result['outputContexts']:
                if context['name'].endswith('osoba-wybrana'):
                    celeb = context["parameters"]['person']['name']
                    break
            else:
                for context in query_result['outputContexts']:
                    if 'person' in context['parameters']:
                        celeb = context["parameters"]['person']['name']
                        break

        if celeb is None:
            return {
                'fulfillmentText': "Nie wiem o kogo chodzi."
            }

        if action == 'age':
            value = get_info_celeb(celeb, 'age')
            if value == CELEB_NOT_FOUND:
                fulfillmentText = f"Nie znalazłem osoby o imieniu `{celeb}` w mojej bazie."
            elif value == INFO_NOT_FOUND:
                fulfillmentText = f"Nie znalazłem wieku osoby o imieniu `{celeb}`."
            else:
                fulfillmentText = f'{celeb} ma {value} lat.'

        elif action == 'birthday':
            value = get_info_celeb(celeb, 'birthdy')
            if value == CELEB_NOT_FOUND:
                fulfillmentText = f"Nie znalazłem osoby o imieniu `{celeb}` w mojej bazie."
            elif value == INFO_NOT_FOUND:
                fulfillmentText = f"Nie znalazłem informacji o urodzinach osoby o imieniu `{celeb}`."
            else:
                fulfillmentText = f'Dnia {value} na świecie powitaliśmy {celeb}.'

        elif action == 'height':
            value = get_info_celeb(celeb, 'height')
            if value == CELEB_NOT_FOUND:
                fulfillmentText = f"Nie znalazłem osoby o imieniu `{celeb}` w mojej bazie."
            elif value == INFO_NOT_FOUND:
                fulfillmentText = f"Nie znalazłem informacji o wzroście osoby o imieniu `{celeb}`."
            else:
                fulfillmentText = f'{celeb} ma {value}m wzrostu.'

        elif action == 'occupation':
            value = get_info_celeb(celeb, 'occupation')
            if value == CELEB_NOT_FOUND:
                fulfillmentText = f"Nie znalazłem osoby o imieniu `{celeb}` w mojej bazie."
            elif value == INFO_NOT_FOUND:
                fulfillmentText = f"Nie znalazłem informacji o obszarze działalności osoby o imieniu `{celeb}`."
            else:
                fulfillmentText = f'{celeb} można określić jako: {value}'

    return {
        'fulfillmentText': fulfillmentText,
        'displayText': '25',
        'source': 'webhookdata'
    }


if __name__ == '__main__':
    print(get_info_celeb("Brad pitt", "age"))
    app.run(host='0.0.0.0', port=8080)
