import streamlit as st
import re
from googleapiclient.discovery import build

# Streamlit secret: st.secrets["YOUTUBE_API_KEY"]
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]

st.title("YouTube Insights MVP")
st.write("Paste a YouTube video link to get basic insights.")

# Input
video_url = st.text_input("Enter YouTube video URL:")

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None

def fetch_video_details(video_id):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.videos().list(part="snippet,statistics", id=video_id)
    response = request.execute()
    if response["items"]:
        return response["items"][0]
    return None

if video_url:
    video_id = extract_video_id(video_url)
    if video_id:
        st.write(f"Video ID: {video_id}")
        video_data = fetch_video_details(video_id)
        if video_data:
            snippet = video_data["snippet"]
            stats = video_data["statistics"]
            st.write({
                "title": snippet.get("title"),
                "description": snippet.get("description"),
                "channel": snippet.get("channelTitle"),
                "published_at": snippet.get("publishedAt"),
                "views": stats.get("viewCount"),
                "likes": stats.get("likeCount")
            })
        else:
            st.error("Could not fetch video details.")
    else:
        st.error("Invalid YouTube URL.")
