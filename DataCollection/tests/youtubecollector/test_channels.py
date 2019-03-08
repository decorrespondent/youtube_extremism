from unittest import TestCase

import pandas as pd

from utils_for_test import create_test_client_with_response
from youtubecollector.channels import get_channels, channel


class ChannelTest(TestCase):

    def test_get_full_channel(self):
        expected = [
            channel(channel_id='Some_ID', channel_title='The test channel',
                    channel_description='The Official YouTube Channel for testing',
                    channel_default_language='en', channel_country='US',
                    channel_uploads='UU_8WUrPbi8clO6sWt_FDvuA', channel_viewcount='2640735',
                    channel_commentcount='0', channel_subscribercount='9779', channel_videocount='258',
                    channel_topic_ids=['topic1', 'topic2', 'topic3'],
                    channel_topic_categories=['https://en.wikipedia.org/wiki/Society',
                                              'https://en.wikipedia.org/wiki/Politics'],
                    channel_branding_keywords='"Testing is fun", "More Testing"')
        ]
        channel_seed = pd.DataFrame([{"channel_id": "Some_ID"}])

        client = create_test_client_with_response("full_channel_response.json", "200")
        actual = get_channels(channel_seed, client)

        self.assertEqual(expected, actual)

    def test_get_minimal_channel(self):
        expected = [
            channel(channel_id='Some_ID', channel_title='The test channel',
                    channel_description='The Official YouTube Channel for testing',
                    channel_default_language='not set', channel_country='not set',
                    channel_uploads='', channel_viewcount='2640735',
                    channel_commentcount='0', channel_subscribercount='9779', channel_videocount='258',
                    channel_topic_ids="not set",
                    channel_topic_categories="not set",
                    channel_branding_keywords="not set")
        ]

        channel_seed = pd.DataFrame([{"channel_id": "Some_ID"}])

        client = create_test_client_with_response("nullable_fields_channel_response.json", "200")
        actual = get_channels(channel_seed, client)

        self.assertEqual(expected, actual)
