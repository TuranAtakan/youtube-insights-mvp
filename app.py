import streamlit as st
import re

st.title("YouTube Insights MVP")
st.write("Paste a YouTube video link to get basic insights.")

# Input
video_url = st.text_input("Enter YouTube video URL:")

if video_url:
    # Extract video ID
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", video_url)
    if match:
        video_id = match.group(1)
        st.write(f"Video ID: {video_id}")

        # Placeholder for insights
        st.write("Basic insights could include video title, description, views, e
