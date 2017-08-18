import datetime
import operator

from groupme_bot.groupme_api_client import get_messages, post_as_bot


LOOKBACK = 7


def get_totals(lookback):
    messages, user_names = get_messages(
        datetime.datetime.now() - datetime.timedelta(days=lookback)
    )

    return {
        username: {
            'likes_received': sum([
                len(message['likers'])
                for message_id, message in messages.items()
                if message['user'] == user_id
            ]),
            'messages_posted': len([
                message
                for message_id, message in messages.items()
                if message['user'] == user_id
            ]),
        }
        for user_id, username in user_names.items()
    }


def main(data, lookback=None, *args):
    post_as_bot('Checking leaderboard...')

    try:
        lookback = int(lookback)
    except TypeError:
        lookback = LOOKBACK

    totals = get_totals(lookback)

    total_likes = {
        username: user_totals['likes_received']
        for username, user_totals in totals.items()
    }

    text = '\n'.join([
        '{}: {}'.format(key, val)
        for key, val in sorted(
            total_likes.items(),
            reverse=True,
            key=operator.itemgetter(1),
        )
    ])

    post_as_bot('here it is for the last {} days:'.format(lookback))
    post_as_bot(text)

    return True
