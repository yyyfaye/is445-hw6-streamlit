import streamlit as st
import pandas as pd
import altair as alt

st.title('UFO Sightings: Trends and Shapes')
st.write('An exploration of reported UFO sightings over time and by shape.')

url = 'https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/ufo-scrubbed-geocoded-time-standardized-00.csv'
df = pd.read_csv(url, low_memory=False)
df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['year'] = df['datetime'].dt.year
df = df.dropna(subset=['year', 'shape'])
df = df[(df['year'] >= 1950) & (df['year'] <= 2014)]
df['year'] = df['year'].astype(int)

st.header('1. Sightings over time')
st.write('Use the slider to change the time period shown in both charts.')
years = st.slider('Select year range', 1950, 2014, (1990, 2014))
filtered = df[(df['year'] >= years[0]) & (df['year'] <= years[1])]

annual = filtered.groupby('year').size().reset_index(name='sightings')
chart1 = alt.Chart(annual).mark_line(point=True).encode(
    x=alt.X('year:Q', title='Year', axis=alt.Axis(format='d')),
    y=alt.Y('sightings:Q', title='Number of reported sightings'),
    tooltip=['year:Q', 'sightings:Q']
).properties(height=350)
st.altair_chart(chart1, use_container_width=True)
st.write('This line chart highlights how the number of reported UFO sightings changes over time. I used year on the horizontal axis and report counts on the vertical axis because a line chart makes temporal patterns easy to compare. The points help identify individual years. If I had more time, I would investigate whether changes in reporting platforms or public interest help explain these trends.')

st.header('2. Most commonly reported shapes')
st.write('Choose how many shapes to compare using the dropdown below.')
number = st.selectbox('Number of shapes', [5, 10, 15], index=1)
shapes = filtered.groupby('shape').size().reset_index(name='sightings')
shapes = shapes.sort_values('sightings', ascending=False).head(number)
chart2 = alt.Chart(shapes).mark_bar().encode(
    x=alt.X('sightings:Q', title='Number of reported sightings'),
    y=alt.Y('shape:N', sort='-x', title='Reported shape'),
    color=alt.Color('shape:N', legend=None),
    tooltip=['shape:N', 'sightings:Q']
).properties(height=400)
st.altair_chart(chart2, use_container_width=True)
st.write('This horizontal bar chart compares the most frequently reported UFO shapes. Bar length represents the number of sightings, and sorting from most to least common makes comparisons easier. The dropdown lets readers explore different numbers of categories. If I had more time, I would compare how reported shapes vary across states or decades.')

st.caption('Data: UIUC IS 445 UFO sightings dataset. These are reports, not verified extraterrestrial events. Charts and written analysis were newly created for HW6.1.')
