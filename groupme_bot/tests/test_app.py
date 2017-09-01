import pytest

import groupme_bot.app as module
from groupme_bot.groupme_api_client import logger


@pytest.mark.parametrize(
    'data, expected_messages_posted',
    [
        ({'sender_type': 'bot'}, []),
    ]
)
def test_index_data(data, expected_messages_posted, mocker):
    mocked_logger = mocker.patch.object(logger, 'info', autospec=True)

    module._index_data(data)

    mocked_logger.assert_has_calls(expected_messages_posted, any_order=False)
