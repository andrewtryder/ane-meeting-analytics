from flask import Flask, render_template
from zoommeeting import Zoom
import ms

app = Flask(__name__)

# List of meeting IDs
meetings = ['meeting1', 'meeting2', 'meeting3']

# Route to display list of meetings
@app.route('/')
def index():
    meetings = [{'meeting_id': '87270619114', 'date': 'April 2023', 'title': 'Agile, The Life-Size Board Game!'},
                {'meeting_id': '85923120072', 'date': 'March 2023', 'title': 'S.E.E.ing Your Projects Needs: Creating a Psychological Safety Plan'},
                {'meeting_id': '88189866002', 'date': 'February 2023', 'title': 'Everyone is...an Agile Coach'},
                {'meeting_id': '81555879346', 'date': 'January 2023', 'title': 'How to Minimize Stress in Corporate America'},
                {'meeting_id': '89033277712', 'date': 'December 2022', 'title': 'ANE and Agile - Our Past and Future'},
                {'meeting_id': '83479774433', 'date': 'November 2022', 'title': 'Wickd Agility - Agile and Planetary Challenges by Damon Edwards'},
                {'meeting_id': '81355532493', 'date': 'October 2022', 'title': 'The Fine Art of Zero F***s Given by Jessica Katz'},
                {'meeting_id': '82792015750', 'date': 'September 2022', 'title': 'Putting the Sec in DevOps by Sean Wright'},
                {'meeting_id': '85784277169', 'date': 'August 2022', 'title': 'Get Focused and Get Things Done: 6 Principles of Time Management by Jessica Katz'},
                {'meeting_id': '82588783947', 'date': 'July 2022', 'title': 'FAST: An Innovative Way to Scale by James Shore'},
                {'meeting_id': '82266617679', 'date': 'June 2022', 'title': 'My Agile Journey by Kevin Ball'},
                {'meeting_id': '86755669262', 'date': 'May 2022', 'title': 'How GitLab Makes Agile Shine With Developers Spread Across 65+ Countries by Wayne Haber'},
                {'meeting_id': '82866273790', 'date': 'April 2022', 'title': 'Agile in Machine Learning by Kristina Doing-Harris'}
                ]
    return render_template('index.html', meetings=meetings)

@app.route('/meeting_stats/<meeting_id>')
def meeting_stats(meeting_id):
    #registrants = Zoom.get_meeting_registrants(meeting_id)
    participants = Zoom.get_meeting_attendees(meeting_id)
    print(participants)
    script, div = ms.process_participants(participants)
    return render_template('meeting_stats.html', meeting_id=meeting_id, plot_script=script, plot_div=div)

if __name__ == '__main__':
    app.run(debug=True)
