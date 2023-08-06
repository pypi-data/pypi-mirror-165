Welcome to jwcnotipy's documentation!
=====================================

This package was built to facillitate sending notifications to slack at runtime!

Notifications can be attached to specific functions with a handy decorator:

   ```
   from jwcnotipy import notify_on_exec

   @notify_on_exec(jwc_test_app, 'U037LP9TM8P')
   def sum(a,b):
      return a + b

   sum(3,1)
   ```

Or at any other key point using notify_me:

   ```
   from jwcnotipy import notify_me

   sum(3,1)
   notify_me(jwc_test_app, 'U037LP9TM8P')
   ```

The notifications are set up to post to a single channel defined by the
JWCNOTIPY_CHANNEL environment variable, but can be sent to another specific
channel by setting the channel keyword argument. NOTE only the user specified
in the function call can see the notifications! This will be extended to allow
a set of specific users and non-ephemeralised messages in a future build.


Contribute
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/$project/$project

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@google-groups.com

License
-------

The project is licensed under the BSD license.