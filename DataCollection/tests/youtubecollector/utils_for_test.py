import json
from os.path import join, split

from googleapiclient.discovery import build
from googleapiclient.http import HttpMockSequence


def get_file_from_test_resource(filename):
    return join(split(__file__)[0], "resources", filename)


def get_content_from_file(filename):
    with open(get_file_from_test_resource(filename)) as handle:
        return handle.read()


def read_json_from_file(filename):
    with open(get_file_from_test_resource(filename)) as json_file:
        return json.loads(json_file.read())


def create_test_client_with_response(response_json_file, status_code):
    test_response = get_content_from_file(response_json_file)
    service_json = get_content_from_file("youtube_service.json")
    url = HttpMockSequence([
        ({'status': '200'}, service_json),
        ({'status': str(status_code)}, test_response)
    ])

    return build("youtube", "v3", http=url, developerKey="key")
