import os
import random

from groupme_bot.groupme_api_client import post_as_bot


def main(data):
    if random.random() > 0.98:
        if data.get('sender_type') != 'bot':
            reply = os.environ.get('RANDOM_REPLY')
            if reply:
                post_as_bot('{}, {}'.format(data['name'], reply))
                return True

    return False
