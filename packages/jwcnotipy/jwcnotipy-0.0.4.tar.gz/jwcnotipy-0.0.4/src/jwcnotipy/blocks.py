'''
DESCRIPTION:
A collection of methods for generating methods with given payloads

PRIVATE METHODS:
--------------------------------------------------------------------------------
_success_block(
    notification_name, completion_time, elapsed_time, output) -> list:
    Generates the payload sent to slack upon successful execution of a
    function.
_failure_block(notification_name, failure_time, trace)->str:
    Generates the payload sent to slack upon the failure of a function.
_generic_block(notification_name, time, payload):
    Generates the payload for a generic notification.
'''

def _success_message(
    notification_name,
    completion_time,
    elapsed_time,
    output) -> list:

    '''
    DESCRIPTION:
    Generates the payload sent to slack upon successful execution of a
    function.

    notification_name, of type string.
        The name to use for this call so it can be identified in the slack
        channel.
    completion_time, of type string.
        The time at which the function finished.
    elapsed_time, of type int.
        The time taken by the function in seconds rounded to 3dp
    output, of unknown type.
        the output returned by the function

    RETURNS
    ----------------------------------------------------------------------------
    A list of dictionaries or 'blocks' used by slack to form a message
    '''

    message = [
        {
            "type": "header",
            "text": {
            "type": "plain_text",
            "text": "Notification from JWCNOTIPY!",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ':02_cheer: *App Completed Successfully!*'
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields":[
                {
                "type": "mrkdwn",
                "text": ":robot_face:  *App Name:*"
                },
                {
                "type": "mrkdwn",
                "text": "*:clock1:  Time Finished:*"
                },
                {
                "type": "mrkdwn",
                "text": f"{notification_name}"
                },
                {
                "type": "mrkdwn",
                "text": f"{completion_time}"
                },
                {
                "type": "mrkdwn",
                "text": ":residentsleeper: *Elapsed Time:*"
                },
                {
                "type": "mrkdwn",
                "text": " "
                },
                {
                "type": "mrkdwn",
                "text": f"{elapsed_time} seconds"
                },
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f'*Output*: \n```{output}```'
            }
        }
    ]

    return message

def _failure_message(notification_name, failure_time, trace)->str:

    '''
    DESCRIPTION:
    Generates the payload sent to slack upon the failure of a function.

    ARGUMENTS:
    ----------------------------------------------------------------------------
    notification_name, of type string.
        The name to use for this call so it can be identified in the slack
        channel.
    failure_time, of type string.
        The time at which the function failed
    trace, of type str.
        The stack trace for this failure

    RETURNS
    ----------------------------------------------------------------------------
    A list of dictionaries or 'blocks' used by slack to form a message
    '''

    message = [
        {
            "type": "header",
            "text": {
            "type": "plain_text",
            "text": "Notification from JWCNOTIPY!",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f':sadge: *Something Broke.*'
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields":[
                {
                "type": "mrkdwn",
                "text": ":robot_face:  *App Name:*"
                },
                {
                "type": "mrkdwn",
                "text": "*:clock1:  Time Failed:*"
                },
                {
                "type": "mrkdwn",
                "text": f"{notification_name}"
                },
                {
                "type": "mrkdwn",
                "text": f"{failure_time}"
                },
            ]
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f'*Stack Trace*: \n```{trace}```'
            }
        }
    ]

    return message

def _generic_message(notification_name, time, payload):

    '''
    DESCRIPTION:
    Generates the payload for a generic notification.

    ARGUMENTS:
    ----------------------------------------------------------------------------
    notification_name, of type string.
        The name to use for this call so it can be identified in the slack
        channel.
    time, of type string.
        The time at which the notification was generated
    payload, any type.
        An Optional payload for this message

    RETURNS
    ----------------------------------------------------------------------------
    A list of dictionaries or 'blocks' used by slack to form a message
    '''

    message = [
        {
            "type": "header",
            "text": {
            "type": "plain_text",
            "text": "Notification from JWCNOTIPY!",
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": ':alert:'
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields":[
                {
                "type": "mrkdwn",
                "text": ":robot_face:  *App Name:*"
                },
                {
                "type": "mrkdwn",
                "text": "*:clock1:  Time:*"
                },
                {
                "type": "mrkdwn",
                "text": f"{notification_name}"
                },
                {
                "type": "mrkdwn",
                "text": f"{time}"
                },
            ]
        }
    ]
    if payload != None:
        message.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f'*Stack Trace*: \n```{payload}```'
                }
            }
        )

    return message