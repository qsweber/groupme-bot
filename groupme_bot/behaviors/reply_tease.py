import os
import random

from groupme_bot.clients.s3 import S3Client
from groupme_bot.groupme_api_client import post_as_bot


def main(data):
    if data['sender_id'] == os.environ.get('USER_TO_TEASE'):
        s3_client = S3Client()
        if random.random() > float(os.environ.get('TEASE_RATE')):
            contents = s3_client.get_file_contents(os.environ.get('STATEMENTS_BUCKET'), 'groupme-bot/statements.txt')
            post_as_bot(
                os.environ.get('USER_TO_TEASE_NAME') + ', ' + random.choice(contents.decode().split('\n')),
            )
            return True

    return False
