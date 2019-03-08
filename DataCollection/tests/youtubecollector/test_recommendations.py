from unittest import TestCase

from utils_for_test import read_json_from_file
from youtubecollector.recommendations import convert_to_recommendations, recommendation


class RecommendationsTest(TestCase):

    def test_get_full_recommendation(self):
        response = read_json_from_file("recommendation.json")
        actual = convert_to_recommendations(response,"id_of_video")

        expected = [
            recommendation(video_id="id_of_video",
                           target_video_id="id of first target video",
                           published_at='2018-01-01T01:01:01.000Z',
                           channel_id='channel Id of first video',
                           video_title='title of first video',
                           video_description='Description of first recommendation'),
            recommendation(video_id='id_of_video',
                           target_video_id='id of second target video',
                           published_at='2018-10-10T10:10:10.000Z',
                           channel_id='channel id of second video',
                           video_title='title of second video',
                           video_description='description of second video')
        ]
        self.assertEqual(actual, expected)