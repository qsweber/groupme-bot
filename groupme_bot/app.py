import logging
import logging.config
import os
import string

from flask import Flask, request, jsonify

from groupme_bot.behaviors import (
    check_double_post,
    repeat_user,
    reply_random,
    query_leaderboard,
)
from groupme_bot.groupme_api_client import post_as_bot


logging.config.fileConfig('groupme_bot/logging.ini')
logger = logging.getLogger(__name__)

app = Flask(__name__)

QUERY_WORD_MAP = {
    'leaderboard': query_leaderboard.main,
    'leaders': query_leaderboard.main,
}


@app.route('/', methods=['POST'])
def index():
    data = request.get_json()

    return _index_data(data)


def _index_data(data):
    if data.get('sender_type') == 'bot':
        logger.info('sender is bot, return early')
        return 'ok', 200

    if check_double_post.main(data):
        return 'ok', 200

    if repeat_user.main(data):
        return 'ok', 200

    if reply_random.main(data):
        return 'ok', 200

    words = [
        word.translate(None, string.punctuation)
        for word in data.get('text').lower().split()
    ]
    if not words:
        logger.info('no words found, return early')
        return 'ok', 200

    first_word = words.pop(0)
    if first_word != os.environ['GROUPME_BOT_NAME']:
        logger.info('bot not being invoked, return early')
        return 'ok', 200

    second_word = words.pop(0)

    try:
        func = QUERY_WORD_MAP[second_word]
    except KeyError:
        logger.info('failed attempt at query with {}'.format(second_word))
        post_as_bot('Sorry, I can\'t help you with that.')

        return 'ok', 200

    func(data, *words)

    return "ok", 200


@app.route('/api/v1/totals', methods=['GET'])
def totals():
    days = int(request.args.get('days', 7))

    totals = query_leaderboard.get_totals(days)

    response = jsonify(totals)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


@app.route('/api/v1/already_posted', methods=['GET'])
def already_posted(message=None):
    message = request.args.get('message')

    response_message = check_double_post.is_double_post({
        'text': message,
        'id': 0,
        'user': 0,
    })

    response_data = {'display': response_message}

    response = jsonify(response_data)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
