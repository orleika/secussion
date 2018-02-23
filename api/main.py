# -*- coding: utf-8 -*-
from theme import Theme
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)
app.debug = True
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

@app.route('/theme', methods=['POST'])
def post_theme():
    order = request.json['message']
    # try:
    #     theme = Theme(order).get()
    # except:
    #     abort(404)
    theme = Theme(order).get()

    result = {
        "result": True,
        "data": {
            "keywords": theme.keywords,
            "opinions": theme.opinions
        }
    }

    return make_response(jsonify(result))

@app.route('/opinion', methods=['POST'])
def post_opinion():
    keywords = request.json['keywords']
    opinion = request.json['opinion']
    # try:
    #     theme = Theme(order).get()
    # except:
    #     abort(404)
    op = Opinion(keywords, opinion).get()

    result = {
        "result": True,
        "data": {
            "posOpinions": op.positives,
            "negOpinions": op.negatives
        }
    }

    return make_response(jsonify(result))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
