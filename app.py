from flask import Flask, render_template
from zoommeeting import Zoom
import ms

app = Flask(__name__)

# List of meeting IDs
meetings = ['meeting1', 'meeting2', 'meeting3']

# Route to display list of meetings
@app.route('/')
def index():
    meetings = [{'meeting_id': '87270619114', 'date': 'April 2023', 'title': 'Damon'},
                {'meeting_id': '85923120072', 'date': 'March 2023', 'title': ''},
                {'meeting_id': '88189866002', 'date': 'February 2023', 'title': ''},
                {'meeting_id': '81555879346', 'date': 'January 2023', 'title': ''},
                {'meeting_id': '89033277712', 'date': 'December 2022', 'title': ''},
                {'meeting_id': '83479774433', 'date': 'November 2022', 'title': ''},
                {'meeting_id': '81355532493', 'date': 'October 2022', 'title': ''},
                {'meeting_id': '82792015750', 'date': 'September 2022', 'title': ''},
                {'meeting_id': '85784277169', 'date': 'August 2022', 'title': ''}
            
                ]
    print(meetings)
    return render_template('index.html', meetings=meetings)

@app.route('/meeting_stats/<meeting_id>')
def meeting_stats(meeting_id):
    #registrants = Zoom.get_meeting_registrants(meeting_id)
    participants = Zoom.get_meeting_attendees(meeting_id)
    script, div = ms.process_participants(participants)
    return render_template('meeting_stats.html', meeting_id=meeting_id, plot_script=script, plot_div=div)

if __name__ == '__main__':
    app.run(debug=True)
