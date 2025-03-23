from flask import Flask, request, jsonify
import requests
from pprint import pprint


app = Flask(__name__)

def _gemini_simplifier(long_title: str) -> str:
    """ Take a long title from an amazon product
    page and shorten in order to make query searches
    for sustainable alternatives.
    """

def _gemini_sustainability_score(data: dict) -> list[dict]:
    """ Take an input data set of amazon search data
    and feed each product into gemini, and return a list
    of products that have met the sustainability score
    given by gemini
    """

@app.route('/process', methods=['POST'])
def get_product_info():
    data = request.json
    url = data.get("url", "No URL received")
    pr_id = url[url.rfind('/'):]

    to_api = {
        'source':'amazon_product',
        'query':'B07FZ8S74R',
        'parse':True
    }
    pr_info = requests.request(
        'POST',
        url = 'https://realtime.oxylabs.io/v1/queries',
        auth = ('Sustainable', 'IwhzpW5gsq9+'),
        json= to_api,
    )

    name_to_find = Gemini_simplifier(pr_info["title"]) # figure out how to find title

    sustain_pr_payload = {
        'source':'amazon_search',
        'query':name_to_find,
        'parse':True,
        'pages': 2,
    }

    possible_items = requests.request(
        'POST',
        url = 'https://realtime.oxylabs.io/v1/queries',
        auth = ('Sustainable', 'IwhzpW5gsq9+'),
        json= sustain_pr_payload,
    )

    return _gemini_sustainability_score(possible_items)




if __name__ == '__main__':
    app.run(port=5000)
