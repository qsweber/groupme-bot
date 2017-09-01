import datetime
import os
import re

from groupme_bot.groupme_api_client import get_messages, post_as_bot


def _url_from_text(text):
    pattern = "(https?):\/\/(.*)"
    for word in text.split():
        result = re.search(pattern=pattern, string=word)
        if result:
            return result.groups(1)[1]

    return None


def is_double_post(data):
    test_url = _url_from_text(data['text'])

    if not test_url:
        return False

    lookbacks = [
        1, 7, 30, 365, 700
    ]
    for lookback in lookbacks:
        messages, user_names = get_messages(
            datetime.datetime.now() - datetime.timedelta(days=lookback)
        )

        for message_id, message in messages.items():
            if message_id == data['id']:
                continue

            if message['text']:
                url = _url_from_text(message['text'])
                if url:
                    if url == test_url:
                        if message['user'] == data['user']:
                            poster = 'you'
                        else:
                            poster = user_names[message['user']]

                        return 'Nice try! {} already posted that on {}'.format(
                            poster,
                            message['created'].strftime('%B %d, %Y'),
                        )

    return False


def main(data):
    response_message = is_double_post(data)
    if response_message:
        post_as_bot(response_message)
        extra_response = os.getenv(
            'GROUPME_DOUBLE_POST_RESPONSE',
        )
        if extra_response:
            post_as_bot(extra_response)

        return True

    return False
