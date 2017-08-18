import pytest

import groupme_bot.groupme_api_client as module


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
