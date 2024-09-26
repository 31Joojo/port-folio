import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from utils import *

def app():
    ### Page title
    st.title("Analysis of my personal listening data")

    ### Subtitle
    st.subheader("Analyzing my listening data :", divider=True)

    ### Introduction
    st.write("""
            In this section, I'll examine and analyze my musical listening habits.
             Using data collected over time, I'll explore my favorite artists, genres and tracks, as well as my listening trends.
             This will help me identify my preferences and better understand how my music consumption is evolving.
             """)
    
    ### Data cleaning
    music_play_daily = load_data('data/Apple Music - Play History Daily Tracks copie.csv')

    new_column_info: dict = {
        'Play Duration Seconds': (convert_data, 'Play Duration Milliseconds'),
        'Year': ('date_split', 'Date Played'),
        'Month': ('date_split', 'Date Played'),
        'Day': ('date_split', 'Date Played'),
        'Artist': (split_data, 'Track Description', ' - ', 0),
        'Song': (split_data, 'Track Description', ' - ', 1)
    }

    music_play_daily = clean_data(music_play_daily,
                                  columns_to_drop=['Country', 'Media type', 'Track Reference',
                                                   'Track Description', 'Track Identifier',
                                                   'Ignore For Recommendations', 'Play Duration Milliseconds'],
                                  new_column_info=new_column_info,
                                  date_column='Date Played',
                                  date_format='%Y%m%d')

    music_play_daily = filter_data(music_play_daily, "Year in (2020, 2021, 2022, 2023, 2024)")

    st.write('Here is the dataframe.')
    st.dataframe(music_play_daily, height=600)

    ### Analysis of the reasons for stopping reading
    st.subheader('Analysis of the reasons for stopping reading :', divider=True)

    reasons_stopping_reading = count_data(music_play_daily, 'End Reason Type', 'index')

    fig = px.pie(reasons_stopping_reading,
                 values=reasons_stopping_reading.values,
                 names=reasons_stopping_reading.index,
                 title='Analysis of the reasons for stopping reading')

    st.plotly_chart(fig)

    st.write("""
    We can see that the general trend is for me to let pieces finish naturally before they change :
    this represents 91.1% of total pieces over the years 2023 and 2024.
    """)

    ### Musical activity according to the month
    st.subheader('Musical activity according to the month :', divider=True)

    month_activity = count_data(music_play_daily, 'Month', 'index')

    fig = px.density_heatmap(month_activity,
                             x=month_activity.values,
                             y=month_activity.index,
                             nbinsx=20, nbinsy=20,
                             marginal_x="histogram",
                             title='Musical activity according to the month')

    st.plotly_chart(fig)

    ### Musical activity according to the day
    st.subheader('Musical activity according to the day :', divider=True)

    day_activity = count_data(music_play_daily, ['Day Name', 'Year'], 'index')

    day_activity = day_activity.reset_index()

    fig = px.line(day_activity,
                  x='Day Name',
                  y='count',
                  color='Year',
                  title='Musical activity according to the day')

    st.plotly_chart(fig)

    ### Most-listened-to artists

    st.subheader('Musical activity :', divider=True)

    st.write("First, we'll look at the number of listens, then at the number of hours.")
    st.markdown("**Most-listened-to artits depending on the number of listenings**")

    artists_most_listened = count_data(music_play_daily, 'Artist', 'value')

    artists_most_listened.columns = ['Artist', 'Frequency']

    fig = px.bar(artists_most_listened,
                 x=artists_most_listened.index,
                 y=artists_most_listened.values,
                 title='Most-listened-to artists from 2023 to 2024',
                 labels={'Artist': 'Artist', 'Frequency': 'Frequency'})

    st.plotly_chart(fig)

    st.write("Which is a fact, we can see that the artist I listen to most is BTS.")
    st.markdown("**Most-listened-to artists depending on the day and the number of listening hours**")

    ert_day_duration = group_data(music_play_daily, ['End Reason Type', 'Date Played'],
                                  'Play Duration Seconds', 'sum')

    fig = plt.figure(figsize=(20, 20))
    fig = px.scatter_3d(ert_day_duration,
                        x='Date Played',
                        y='End Reason Type',
                        z='Play Duration Seconds',
                        title="Total listening duration by end reason type and by day",
                        color='End Reason Type',
                        labels={'Play Duration Seconds': 'Total Listening Duration (Seconds)'})

    st.plotly_chart(fig)

    ### Most-listened-to artists
    st.subheader("Most-listened-to artists :", divider=True)

    songs_mots_listened = count_data(filter_data(music_play_daily, '(Year == 2023) or (Year == 2024)'),
                                     'Song', 'value')

    fig = px.bar(songs_mots_listened,
                 x=songs_mots_listened.index,
                 y=songs_mots_listened.values,
                 title='Most-listened-to artists from 2023 to 2024',)

    st.plotly_chart(fig)

    st.write("""
    Surprisingly, I thought that the first music I listened to the most was, at first, in my main library,
    and also would be K-Pop, but obviously not. That said, this data is spread over the last two years,
    because I think the trend would reverse.
    However, this may be due to the fact that I have a very particular way of listening to the music in my libraries.
    """)

    st.subheader("Correlation between listening time and number of plays per song", divider=True)

    fig = px.scatter(music_play_daily,
                     x='Play Count',
                     y='Play Duration Seconds',
                     title='Correlation between listening duration and play count',
                     color='Year',
                     labels={
                         'Play Duration Seconds': 'Listening Duration (Seconds)',
                         'Play Count': 'Number of Plays'
                     })

    st.plotly_chart(fig)

    st.write("""As we can see, there is no real correlation between the variables
             `number of listenings` and `listening time`.""")
