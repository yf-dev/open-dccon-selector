from . import twitchClient
from requests.exceptions import RequestException


def twitch_channel_name_to_id(channel_name):
    try:
        channels = twitchClient.get_users(login_names=channel_name)
    except RequestException as e:
        if e.response.status_code != 401:
            raise e
        twitchClient.get_oauth()
        channels = twitchClient.get_users(login_names=channel_name)

    if channels and len(channels) > 0:
        channel = channels[0]
        return channel.id
    return None
