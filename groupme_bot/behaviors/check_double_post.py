import datetime
import re
import urllib

from groupme_bot.groupme_api_client import get_messages, post_as_bot


def _simplify_text(text):
    res = urllib.parse.urlparse(text)

    return '.'.join(res.netloc.split('.')[-2:]) + res.path


def _url_from_text(text):
    pattern = "(https?):\/\/.*"
    for word in text.split():
        if re.search(pattern=pattern, string=word):
            return _simplify_text(word)

    return None


def main(data):
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
            if message['text']:
                url = _url_from_text(message['text'])
                if url:
                    if url == test_url:
                        post_as_bot(
                            'Nice try! {} already posted that on {}'.format(
                                user_names[message['user']],
                                message['created'].strftime('%B %d, %Y'),
                            )
                        )
                        return True

    return False
