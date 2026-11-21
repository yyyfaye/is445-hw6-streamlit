
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="UFO Sightings", layout="wide")

st.title("UFO Sightings: Trends and Shapes")
st.write("An exploration of reported UFO sightings over time and by shape.")

# Load data
url = "https://raw.githubusercontent.com/UIUC-iSchool-DataViz/is445_data/main/ufo-scrubbed-geocoded-time-standardized-00.csv"

df = pd.read_csv(url, low_memory=False)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# The first column contains the sighting date
df = df.rename(columns={df.columns[0]: "datetime"})

# Clean dates and shapes
df["datetime"] = pd.to_datetime(
    df["datetime"], errors="coerce", format="mixed"
)
df["year"] = df["datetime"].dt.year

df = df.dropna(subset=["year", "shape"])
df = df[(df["year"] >= 1950) & (df["year"] <= 2014)]
df["year"] = df["year"].astype(int)

# Interactive year selection
st.sidebar.header("Filters")
years = st.sidebar.slider(
    "Select year range",
    1950, 2014, (1990, 2014)
)

filtered = df[
    (df["year"] >= years[0]) &
    (df["year"] <= years[1])
]

st.write("Use the sidebar to select the years shown in both charts.")

# Visualization 1
st.header("1. UFO Sightings Over Time")

annual = filtered.groupby("year").size().reset_index(name="sightings")

chart1 = alt.Chart(annual).mark_line(
    point=True,
    color="steelblue"
).encode(
    x=alt.X("year:Q", title="Year", axis=alt.Axis(format="d")),
    y=alt.Y("sightings:Q", title="Number of Sightings"),
    tooltip=["year:Q", "sightings:Q"]
).properties(
    height=350
)

st.altair_chart(chart1, use_container_width=True)

st.write("""
This line chart highlights changes in the number of reported UFO
sightings over time. I chose a line chart because it clearly shows
trends across consecutive years. The horizontal axis represents
years, while the vertical axis shows the number of reports.
A blue line and individual points make the chart easy to read.
The interactive year slider allows users to focus on different
time periods. If I had more time, I would investigate how changes
in reporting platforms and public interest may have influenced
the number of sightings.
""")

# Visualization 2
st.header("2. Most Commonly Reported UFO Shapes")

number = st.selectbox(
    "Select number of shapes to display",
    [5, 10, 15],
    index=1
)

shapes = filtered.groupby("shape").size().reset_index(name="sightings")
shapes = shapes.sort_values("sightings", ascending=False).head(number)

chart2 = alt.Chart(shapes).mark_bar(
    color="teal"
).encode(
    x=alt.X("sightings:Q", title="Number of Sightings"),
    y=alt.Y("shape:N", sort="-x", title="Reported Shape"),
    tooltip=["shape:N", "sightings:Q"]
).properties(
    height=400
)

st.altair_chart(chart2, use_container_width=True)

st.write("""
This horizontal bar chart compares the most frequently reported
UFO shapes. I used horizontal bars because they make it easier
to compare categories with different names. The bars are sorted
from highest to lowest frequency, and the consistent teal color
keeps the design simple. Users can select the number of shapes
displayed using the dropdown menu. The year slider also updates
this chart, allowing comparisons across time periods.
If I had more time, I would explore how reported shapes differ
across geographic regions.
""")

# Homework 5 comparison
st.header("Comparison with Homework 5")

st.write("""
This project uses the same UFO sightings dataset as Homework 5.
For Homework 6, I created a Streamlit application with a line
chart showing annual sightings and a bar chart comparing reported
shapes. The Streamlit version introduces interactive year filtering
and a dropdown for selecting the number of categories.
The written explanations were newly written for this assignment.
""")

st.caption(
    "Data source: UIUC IS 445 UFO Sightings Dataset. "
    "Sightings are self-reported and are not verified extraterrestrial events."
)
