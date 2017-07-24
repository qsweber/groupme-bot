import os

from flask import Flask, request

from groupme_bot.behaviors import (
    check_double_post,
    repeat_user,
    reply_random,
    query_leaderboard,
)
from groupme_bot.groupme_api_client import post_as_bot


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
        return 'ok', 200

    if check_double_post.main(data):
        return 'ok', 200

    if repeat_user.main(data):
        return 'ok', 200

    if reply_random.main(data):
        return 'ok', 200

    words = data.get('text').lower().split()
    first_word = words.pop(0)
    if first_word != os.environ['GROUPME_BOT_NAME']:
        return 'ok', 200

    second_word = words.pop(0)

    try:
        func = QUERY_WORD_MAP[second_word]
    except:
        post_as_bot('Sorry, I can\'t help you with that.')

        return 'ok', 200

    func(data, *words)

    return "ok", 200
