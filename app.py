from flask import Flask, render_template
from zoommeeting import Zoom
import ms
from meetings import MEETINGS
import logging

app = Flask(__name__)

# Route to display list of meetings
@app.route('/')
def index():
    # define the list of meetings in meetings.py
    return render_template('index.html', meetings=MEETINGS)

@app.route('/meeting_stats/<meeting_id>')
def meeting_stats(meeting_id):
    try:
        participants = Zoom.get_meeting_attendees(meeting_id)
        app.logger.debug(participants)
        script, div = ms.process_participants(participants)
        return render_template('meeting_stats.html', meeting_id=meeting_id, plot_script=script, plot_div=div)
    except Exception as e:
        app.logger.error("Meeting Stats Exception: {0}".format(e))
        return "Error retriving meeting statistics for this meeting."

@app.route('/meeting_registrants/<meeting_id>')
def meeting_registrants(meeting_id):
    try:
        count, inperson = Zoom.get_meeting_registrants(meeting_id)
        app.logger.debug("COUNT {0} INPERSON {1}".format(count, inperson))
        return render_template('meeting_registrants.html', meeting_id=meeting_id, count=count, inperson=inperson)
    except Exception as e:
        app.logger.error("Meeting registrants Exception: {0}".format(e))
        return "Error retrieving meeting registrants for this meeting."


if __name__ == '__main__':
    app.run(debug=True)
