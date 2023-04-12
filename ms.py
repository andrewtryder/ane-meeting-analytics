# my libs
import os
import pytz
import time
from typing import Dict, List, Optional, Union, Any

import pandas as pd
from authlib.jose import jwt
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, DatetimeAxis, HoverTool, Div, Label
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.tickers import DatetimeTicker
from bokeh.palettes import Category10
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.layouts import column as bokeh_column




import requests
from requests import Response

# helper functions
def total_participants(df):
    return df['id'].nunique()

def total_duration(df):
    return (df['leave_time'] - df['join_time']).sum().total_seconds()

def avg_duration(df):
    return total_duration(df) / total_participants(df)

def full_duration_attendees(df):
    max_duration = (df['leave_time'] - df['join_time']
                    ).max().total_seconds()
    return df[(df['leave_time'] - df['join_time']).dt.total_seconds() == max_duration]['id'].nunique()

def total_attentiveness_score(df):
    return df['attentiveness_score'].sum()

def avg_attentiveness_score(df):
    return df['attentiveness_score'].mean()

def process_participants(list_of_participants):
    df: DataFrame = pd.DataFrame(list_of_participants)
    df.join_time = pd.to_datetime(df.join_time).dt.tz_convert("America/New_York").dt.tz_localize(None)
    df.leave_time = pd.to_datetime(df.leave_time).dt.tz_convert("America/New_York").dt.tz_localize(None)
    df_grouped = df.groupby('user_email').agg({
        'join_time': 'min',
        'leave_time': 'max'
        }).reset_index()

    df_grouped = df_grouped.drop(df_grouped[df_grouped['user_email'] == 'is@agilenewengland.org'].index)

    # Assuming df_grouped is the DataFrame containing the consolidated view of the meeting participants
    df_grouped['attendance_time'] = (df_grouped['leave_time'] - df_grouped['join_time']).dt.total_seconds() / 60
    avg_attendance_time = df_grouped['attendance_time'].mean()
    min_attendance_time = df_grouped['attendance_time'].min()
    max_attendance_time = df_grouped['attendance_time'].max()
    avg_attendance_time = df_grouped['attendance_time'].mean()
    num_attendees = df_grouped.shape[0]
    std_attendance_time = df_grouped['attendance_time'].std()

    # Create a new dataframe with one row for each minute that any user is in the meeting
    users = pd.DataFrame(columns=['time', 'user'])
    for idx, row in df.iterrows():
        start = row['join_time']
        end = row['leave_time']
        times = pd.date_range(start=start, end=end, freq='T')
        user_data = pd.DataFrame({'time': times, 'user': row['user_email']})
        users = pd.concat([users, user_data], ignore_index=True)

    # Group the users dataframe by 5-minute intervals and count the number of unique users in each interval
    df_concurrent = users.groupby(pd.Grouper(key='time', freq='5T')).nunique()['user']
    # Create a ColumnDataSource object with the concurrent users data
    df_concurrent = df_concurrent.reset_index(name='user')
    source = ColumnDataSource(df_concurrent)
    # Create a Bokeh figure object
    fig = figure(x_axis_type='datetime', title='Number of Concurrent Users Online', width=800, height=1000)
    fig.xaxis.axis_label = 'Time'
    fig.yaxis.axis_label = 'Concurrent Users Online'
    fig.xaxis.formatter = DatetimeTickFormatter(hours=["%m/%d %H:%M"])
    
    # Plot the data using a line glyph
    fig.line(x='time', y='user', source=source, line_width=2)
    # Add hover tool to show the exact number of concurrent users in each interval
    hover = HoverTool(tooltips=[('Concurrent Users', '@user')])
    fig.add_tools(hover)

    all_label = Label(x=50, y=10, x_units='screen', y_units='screen',
                    text=f"# of Attendees: {num_attendees} - Avg (Time): {avg_attendance_time:.2f} - Min (Time): {min_attendance_time:.2f} - Max (Time): {max_attendance_time:.2f} - std dev (Time): {std_attendance_time:.2f}",
                    text_font_size='10pt',
                    text_align='left')

    # add the labels to the plot
    fig.add_layout(all_label)
    script, div = components(fig)
    return script, div