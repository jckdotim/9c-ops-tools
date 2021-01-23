from threading import Thread

from flask import Flask, request, jsonify
import requests

from common import (core_addr,
                    get_state,
                    get_characters_block)


app = Flask(__name__)

@app.route('/activated', methods=['GET', 'POST'])
def activated():
    """Check given address is activated or not"""
    activated_accs = [
        f'0x{b.hex()}' 
        for b 
        in get_state(core_addr(8))['accounts']
    ]
    return jsonify(request.values['text'].lower() in activated_accs)


@app.route('/inspect', methods=['GET', 'POST'])
def inspect():
    """Inspect given address characters"""
    def response_result(address, response_url):
        result = get_characters_block(address)
        requests.post(response_url, json=result)

    thread = Thread(target=response_result, kwargs={'address': request.values['text'], 'response_url': request.values['response_url']})
    thread.start()
    return jsonify({
        "response_type": "in_channel",
        "text": 'Okay. Please wait...'
    })


if __name__ == '__main__':
    app.run()