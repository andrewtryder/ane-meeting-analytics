# ane-meeting-analytics

Zoom Meeting Analytics.

This is a Python Flask App that displays the statistics for Agile New England's Monthly meetings. 
I wanted to play around with the Zoom API and see if I could generate some basic analytics for our monthly meetings.

It gave me a chance to also play around with Bokeh, the awesome visualization library.

The app's code is hosted here and I use a GitHub Action to deploy to fly.dev. 

You will need to set either in .env or on fly's platform two variables, ZOOM_API_KEY and ZOOM_API_SECRET
