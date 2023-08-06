Set up jwcnotipy.
=====================================
#. Install jwcnotipy using pip! ::
    pip install jwcnotipy
#. Get a bot token from the slack bot that will be posting the notifications
and set that as an environment variable called JWCNOTIPY_BOT_TOKEN.
    * from within the kernel::
        from os import environ
        environ['NOTIPY_BOT_TOKEN'] = <your-token>
    * from your command line::
        export NOTIPY_BOT_TOKEN=<your-token>
#. Set the default channel for the bot to write to by setting the
JWCNOTIPY_CHANNEL environment variable.
    * from withing the kernel::
        from os import environ
        environ['NOTIPY_CHANNEL'] = <your-channel>
    * from your command line::
        export NOTIPY_CHANNEL=<your-channel>