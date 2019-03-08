from unittest import TestCase

from utils_for_test import read_json_from_file
from youtubecollector.comments import convert_to_comments, comment


class CommentTest(TestCase):

    def test_get_full_comment(self):
        response = read_json_from_file("comment_full.json")
        actual = convert_to_comments(response)

        expected = [
            comment(video_id='the video id', comment_id='The comment id that is used',
                    author_display_name='Author name',
                    author_channel_url='http://www.youtube.com/channel/someone',
                    author_channel_id='someone',
                    comment_text='The text that is displayed',
                    comment_like_count=4,
                    comment_dislike_count=2,
                    comment_time='2017-11-02T19:25:12.000Z',
                    reply_count=0)
        ]

        self.assertEqual(actual, expected)

    def test_get_minimal_comment(self):
        response = read_json_from_file("comment_minimal.json")
        actual = convert_to_comments(response)

        expected = [
            comment(video_id='the video id', comment_id='The comment id that is used',
                    author_display_name='Author name',
                    author_channel_url='http://www.youtube.com/channel/someone',
                    author_channel_id='not set',
                    comment_text='The text that is displayed',
                    comment_like_count=4,
                    comment_dislike_count=0,
                    comment_time='2017-11-02T19:25:12.000Z',
                    reply_count=0)
        ]

        self.assertEqual(actual, expected)

    def test_get_comments_with_replies(self):
        response = read_json_from_file("comment_with_reply.json")
        actual = convert_to_comments(response)

        expected = [
            comment(video_id='the video id', comment_id='The comment id that is used',
                    author_display_name='Author name',
                    author_channel_url='http://www.youtube.com/channel/someone',
                    author_channel_id='someone',
                    comment_text='The text that is displayed',
                    comment_like_count=4,
                    comment_dislike_count=2,
                    comment_time='2017-11-02T19:25:12.000Z',
                    reply_count=0),
            comment(video_id='some video id', comment_id='The parent id.the reply id',
                    author_display_name='Responder',
                    author_channel_url='http://www.youtube.com/channel/responder',
                    author_channel_id='responder channel id',
                    comment_text='The response text',
                    comment_like_count=1,
                    comment_dislike_count='',
                    comment_time='2017-11-02T19:55:27.000Z',
                    reply_count='')
        ]

        self.assertEqual(actual, expected)
