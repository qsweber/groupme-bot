import datetime
import operator

from groupme_bot.groupme_api_client import get_messages, post_as_bot


LOOKBACK = 7


def main(data, lookback=None, *args):
    post_as_bot('Checking leaderboard...')

    try:
        lookback = int(lookback)
    except TypeError:
        lookback = LOOKBACK

    messages, user_names = get_messages(
        datetime.datetime.now() - datetime.timedelta(days=lookback)
    )

    data = {
        username: sum([
            len(message['likers'])
            for message_id, message in messages.items()
            if message['user'] == user_id
        ]) for user_id, username in user_names.items()
    }

    text = '\n'.join([
        '{}: {}'.format(key, val)
        for key, val in sorted(
            data.items(),
            reverse=True,
            key=operator.itemgetter(1),
        )
    ])

    post_as_bot('here it is for the last {} days:'.format(lookback))
    post_as_bot(text)

    return True
