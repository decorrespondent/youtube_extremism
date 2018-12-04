from googleapiclient.discovery import build as _build
import getpass as _getpass


def create_youtube_client(api_config_filename):
    youtube_api_service_name, youtube_api_version,developer_key = _get_api_config(api_config_filename)
    if developer_key is None:
        developer_key = _getpass.getpass("Google Developer Api key: ")
    return _build(youtube_api_service_name, youtube_api_version, developerKey=developer_key)


def _get_api_config(api_config_filename):
    with open(api_config_filename) as handle:
        config_local_vars = {}
        exec(handle.read(), {},config_local_vars)
        return (config_local_vars['youtube_api_service_name'],
                config_local_vars['youtube_api_version'],
                config_local_vars['developer_key'])
