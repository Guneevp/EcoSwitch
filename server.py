from flask import Flask, request, jsonify

import requests
from pprint import pprint

from google import genai

client = genai.Client(api_key="AIzaSyAWaizpDISZdr7r1ZkX0BYoui639JvCMLs")
def prompt_ai(prompt: str):
    return client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )

app = Flask(__name__)

def _gemini_simplifier(long_title: str):
    """ Take a long title from an amazon product
    page and shorten in order to make query searches
    for sustainable alternatives.
    >>> _gemini_simplifier("very long title").text

    """
    return prompt_ai(f'Hey can you shorten this amazon product title? I\'m '
              f'trying to query amazon and I need this title without all the extra fluff: "{long_title}"')

def _gemini_sustainability_score(data: dict) -> dict:
    """ Take an input data set of amazon search data
    and feed each product into gemini, and return a list
    of products that have met the sustainability score
    given by gemini
    """
    scores = []
    for product in data["results"][0]["content"]["results"]['organic']:
        product_id = product['asin']

        to_api = {
            'source': 'amazon_product',
            'query': product_id,
            'parse': True
        }
        pr_info = requests.request(
            'POST',
            url='https://realtime.oxylabs.io/v1/queries',
            auth=('Sustainable', 'IwhzpW5gsq9+'),
            json=to_api,
        ).json()

        title = pr_info['title']
        description = pr_info["description"]

        prompt = f'''
     Evaluate the sustainability of this product based on the following factors:

Ingredients (30%): Organic, natural, non-toxic?
Packaging (25%): Recyclable, plastic-free, biodegradable?
Environmental Impact (20%): Carbon footprint, waste generation?
Certifications (15%): Fair Trade, FSC, cruelty-free?
Company Practices (10%): Ethical sourcing, sustainability initiatives?

    Here is the product name:"{title}"
    
    and here is the description:{description}

    Can you give the score to be the last 3 digits of your response?
    '''
        scores.append(prompt_ai(prompt).text[-3:])
    # Gemini calls above
    index = scores.index(max(scores))



    return data["results"][0]["content"]["results"]['organic'][index]

@app.route('/process', methods=['POST'])
def get_product_info():
    data = request.json
    url = data.get("url", "No URL received")
    pr_id = url[url.rfind('/'):]

    to_api = {
        'source':'amazon_product',
        'query':pr_id,
        'parse':True
    }
    pr_info = requests.request(
        'POST',
        url = 'https://realtime.oxylabs.io/v1/queries',
        auth = ('Sustainable', 'IwhzpW5gsq9+'),
        json= to_api,
    ).json()

    name_to_find = _gemini_simplifier(pr_info["title"]) # figure out how to find title

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
    ).json()

    product =  _gemini_sustainability_score(possible_items)

    return product['title']




if __name__ == '__main__':
    app.run(port=5000)
