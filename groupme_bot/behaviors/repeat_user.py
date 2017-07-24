import os
import random

from groupme_bot.groupme_api_client import post_as_bot


def main(data):
    if data['sender_id'] == os.environ.get('USER_TO_REPEAT'):
        if random.random() > 0.9:
            post_as_bot(data['text'])
            return True

    return False
