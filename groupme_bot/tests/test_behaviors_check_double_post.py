import pytest

import groupme_bot.behaviors.check_double_post as module


@pytest.mark.parametrize(
    'text, expected',
    [
        ('abc def ghi https://google.com/abc', 'google.com/abc'),
        ('abc def ghi', None),
        ('https://www.nytimes.com/abc?_r=0', 'www.nytimes.com/abc?_r=0'),
        ('http://mobile.nytimes.com/abc?_r=0', 'mobile.nytimes.com/abc?_r=0'),
    ]
)
def test_url_from_text(text, expected):
    actual = module._url_from_text(text)

    assert actual == expected


@pytest.mark.parametrize(
    'messages, data, expected',
    [
        (
            (
                {
                    '1': {
                        'text': 'http://www.test.com',
                        'user': 1,
                        'created': module.datetime.datetime(2017, 1, 1),
                    },
                },
                {1: 'foo user'}
            ),
            {'text': 'http://www.test.com', 'id': '100', 'user': 2},
            'Nice try! foo user already posted that on January 01, 2017',
        ),
        (
            (
                {
                    '1': {
                        'text': 'http://www.test1.com',
                        'user': 1,
                        'created': module.datetime.datetime(2017, 1, 1),
                    },
                },
                {1: 'foo user'}
            ),
            {'text': 'http://www.test.com', 'id': '100', 'user': 2},
            False,
        ),
        (
            (
                {
                    '1': {
                        'text': 'abc',
                        'user': 1,
                        'created': module.datetime.datetime(2017, 1, 1),
                    },
                },
                {1: 'foo user'}
            ),
            {'text': 'abc', 'id': '100', 'user': 2},
            False,
        ),
        (
            (
                {
                    '1': {
                        'text': 'http://www.test.com',
                        'user': 1,
                        'created': module.datetime.datetime(2017, 1, 1),
                    },
                },
                {1: 'foo user'}
            ),
            {'text': 'http://www.test.com', 'id': '100', 'user': 1},
            'Nice try! you already posted that on January 01, 2017',
        ),
    ]
)
def test_is_double_post(messages, data, expected, mocker):
    mocker.patch.object(
        module,
        'get_messages',
        return_value=messages
    )

    actual = module.is_double_post(data)

    assert actual == expected
