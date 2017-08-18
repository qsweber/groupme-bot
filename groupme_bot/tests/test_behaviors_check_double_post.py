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
