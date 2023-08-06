from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from functools import wraps
import time as time
import datetime as dt
import traceback
import sys
from os import environ
from math import floor

from .blocks import _success_message, _failure_message, _generic_message

'''
DESCRIPTION:s
A collection of methods for submitting notifications to slack at runtime.

PUBLIC METHODS:
--------------------------------------------------------------------------------
notify_me(notification_name, user_id, channel, payload = None) -> None:
    A function to send a notification to slack at a given point
notify_on_exec(notification_name, user_id, channel=environ['JWCNOTIPY_CHANNEL']):
    A decorator that wraps a function to trigger a slack notification once the
    code has been run.

PRIVATE METHODS:
--------------------------------------------------------------------------------
_format_elapsed_time(time_in_seconds) -> str:
    Handles the formatting of time measurements.
_notify(message, user_id, channel) -> None:
    A function to send a notification to slack.
_check_input(notification_name, user_id, channel) -> None:
    Checks the input provided for a given notification.
'''

def notify_me(
    notification_name,
    user_id,
    channel=environ['JWCNOTIPY_CHANNEL'],
    payload = None) -> None:

    '''
    DESCRIPTION:
    A function to send a notification to slack at a given point

    ARGUMENTS:
    ----------------------------------------------------------------------------
    notification_name, of type string.
        The name to use for this call so it can be identified in the slack
        channel.
    user_id, of type string.
        The user for which this notification should be visible.

    KEYWORD ARGUMENTS:
    ----------------------------------------------------------------------------
    channel, of type string or None.
        The channel the notifier should use. The channel must have the slack
        application installed. Default None.
    payload, of type list of dict or None.
        An optional custom payload for this notification

    RETURNS:
    ----------------------------------------------------------------------------
    None
    '''

    _check_input(notification_name, user_id, channel)

    message_to_send = _generic_message(
        notification_name,
        dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        payload
        )

    _notify(message_to_send, user_id, channel)


def notify_on_exec(
    notification_name,
    user_id,
    channel=environ['JWCNOTIPY_CHANNEL']
    ):

    '''
    DESCRIPTION:
    A decorator that wraps a function to trigger a slack notification once the
    code has been run.

    ARGUMENTS:
    ----------------------------------------------------------------------------
    notification_name, of type string.
        The name to use for this call so it can be identified in the slack
        channel.
    user_id, of type string.
        The user for which this notification should be visible. This can be
        found from your slack profile.

    KEYWORD ARGUMENTS:
    ----------------------------------------------------------------------------
    channel, of type string or None.
        The channel the notifier should use. The channel must have the slack
        application installed. Takes the value of the JWCNOTIPY_CHANNEL env
        variable by default.

    RETURNS:
    ----------------------------------------------------------------------------
    The function output
    '''

    # Check the provided args
    _check_input(notification_name, user_id, channel)

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start_time = time.time()
            #Execute Function
            try:
                output = func(*args, **kwargs)

                # Get time in seconds
                elapsed = round((time.time() - start_time),3)
                _notify(
                    _success_message(
                        notification_name,
                        dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        _format_elapsed_time(elapsed),
                        output
                    ),
                    user_id,
                    channel
                )

            except Exception as e:
                _notify(
                    _failure_message(
                        notification_name,
                        dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        traceback.format_exc()
                    ),

                    user_id,
                    channel
                )
                raise e

            return output

        return wrapper
    return decorator

def _format_elapsed_time(time_in_seconds) -> str:

    '''
    DESCRIPTION:
    Handles the formatting of time measurements.

    ARGUMENTS:
    ----------------------------------------------------------------------------
    time_in_seconds, of type int:
        The time taken to run in seconds

    RETURNS:
    ----------------------------------------------------------------------------
    A stringified time measurement
    '''

    if time_in_seconds < 60:
        return f'{time_in_seconds}s'
    elif time_in_seconds >= 60 and time_in_seconds < 60**2:
        n_minutes = floor(time_in_seconds/60)
        n_seconds = time_in_seconds - n_minutes*60
        return f'{n_minutes}m, {n_seconds}s'
    if time_in_seconds >= 60^2:
        n_hours = floor(time_in_seconds/60^2)
        n_minutes = floor(time_in_seconds/60) - n_hours*60^2
        n_seconds = time_in_seconds - n_minutes*60 - n_hours*60^2
        return f'{n_hours}h, {n_minutes}m, {n_seconds}s'


def _notify(message, user_id, channel) -> None:

    '''
    DESCRIPTION:
    A function to send a notification to slack.

    ARGUMENTS:
    ----------------------------------------------------------------------------
    notification_name, of type string.
        The name to use for this call so it can be identified in the slack
        channel.
    user_id, of type string.
        The user for which this notification should be visible.

    KEYWORD ARGUMENTS:
    ----------------------------------------------------------------------------
    channel, of type string or None.
        The channel the notifier should use. The channel must have the slack
        application installed. Default None

    RETURNS:
    ----------------------------------------------------------------------------
    None
    '''

    bot_token = environ['JWCNOTIPY_BOT_TOKEN']
    client = WebClient(bot_token)
    try:
        response = client.chat_postEphemeral(
            user = user_id,
            blocks = message,
            channel = channel
        )
    except SlackApiError as e:
        assert e.response["error"]

def _check_input(notification_name, user_id, channel) -> None:

    '''
    DESCRIPTION:
    Checks the input provided for a given notification.

    ARGUMENTS:
    ----------------------------------------------------------------------------
    notification_name, of type string.
        The name to use for this call so it can be identified in the slack
        channel.
    user_id, of type string.
        The user for which this notification should be visible. This can be
        found from your slack profile.

    KEYWORD ARGUMENTS:
    ----------------------------------------------------------------------------
    channel, of type string or None.
        The channel the notifier should use. The channel must have the slack
        application installed. Takes the value of the JWCNOTIPY_CHANNEL env
        variable by default.

    RETURNS:
    ----------------------------------------------------------------------------
    None
    '''

    # Check the provided args
    if type(notification_name) != str:
        raise ValueError(
            'app_Name should be of type str.'
        + f' Recieved {type(notification_name)} type instead'
        )
    if type(user_id) != str:
        raise ValueError(
            'user_id should be of type str.'
        + f' Recieved {type(user_id)} type instead. This can be found from your'
        + ' slack profile.'
        )
    if type(channel) != str:
        raise ValueError(
            'channel should be of type str.'
        + f' Recieved {type(user_id)} type instead.'
        )