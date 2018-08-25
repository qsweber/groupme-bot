import os
import random

from groupme_bot.groupme_api_client import post_as_bot


random_places = [
    'Olive Garden',
    'Eataly',
    'Maggiano\'s',
    'Subway',
    'Jersey Mike\'s',
    'Long John Silvers',
]


def main(data):
    if data['sender_id'] == os.environ.get('USER_TO_TEASE'):
        if random.random() > float(os.environ.get('TEASE_RATE')):
            post_as_bot(
                os.environ.get('USER_TO_TEASE_NAME') + ', ' + os.environ.get('TEASE_PHRASE') + ' ' + random.choice(random_places),
            )
            return True

    return False
