# ane-meeting-analytics

Zoom Meeting Analytics.

This is a Python Flask App that displays the statistics for Agile New England's Monthly meetings. 
I wanted to play around with the Zoom API and see if I could generate some basic analytics for our monthly meetings.

It gave me a chance to also play around with Bokeh, the awesome visualization library that has a Python module to work with the JS frontend.

The app's code is hosted here and I use a GitHub Action to deploy to fly.dev. 

To use with your own projects, you will need a ZOOM API key and secret. In app.py, you will also need to modify the meeting_id variables to match your own.

Besides this, the ZOOM api credentials need to be set in a local .env file or on fly's platform via secret variables:

```
flyctl secrets set ZOOM_API_SECRET=
flyctl secrets set ZOOM_API_KEY=
```
