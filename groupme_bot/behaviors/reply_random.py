import datetime
import os
import random

from groupme_bot.groupme_api_client import get_messages, post_as_bot


def main(data):
    if random.random() > 0.98:
        if data.get('sender_type') != 'bot':
            messages, user_names = get_messages(
                datetime.datetime.now() - datetime.timedelta(days=700)
            )
            reply = os.environ.get('RANDOM_REPLY')
            name = user_names[data['sender_id']]
            if reply:
                post_as_bot('{}, {}'.format(name, reply))
                return True

    return False
