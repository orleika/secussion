# -*- coding: utf-8 -*-
from theme import Theme
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)
app.debug = True

@app.route('/theme/<string:order>', methods=['GET'])
def get_theme(order):
    # try:
    #     theme = Theme(order).get()
    # except:
    #     abort(404)
    theme = Theme(order).get()

    result = {
        "result": True,
        "data": {
            "opinions": theme
        }
    }

    return make_response(jsonify(result))

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
