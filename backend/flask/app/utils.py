from . import twitchClient


def twitch_channel_name_to_id(channel_name):
    channels = twitchClient.users.translate_usernames_to_ids([channel_name])
    if channels and len(channels) > 0:
        channel = channels[0]
        return channel.id
    return None
