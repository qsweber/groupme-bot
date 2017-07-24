import pytest

import groupme_bot.app as module


@pytest.mark.parametrize(
    'text, expected',
    [
        ('https://www.nytimes.com/abc?_r=0', 'nytimes.com/abc'),
        ('https://mobile.nytimes.com/abc?_r=0', 'nytimes.com/abc'),
    ]
)
def test_simplify_text(text, expected):
    actual = module._simplify_text(text)

    assert actual == expected


@pytest.mark.parametrize(
    'text, expected',
    [
        ('abc def ghi https://google.com/abc', 'google.com/abc'),
        ('abc def ghi', None),
    ]
)
def test_url_from_text(text, expected):
    actual = module._url_from_text(text)

    assert actual == expected


@pytest.mark.parametrize(
    'env_value, expected',
    [
        ('1', True),
        ('0', False),
        ('foo', False),
    ]
)
def test_is_bot_enabled(env_value, expected):
    module.os.environ['GROUPME_BOT_ENABLED'] = env_value

    assert module._is_bot_enabled() == expected
