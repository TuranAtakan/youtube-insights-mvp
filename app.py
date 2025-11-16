import streamlit as st
import re
from googleapiclient.discovery import build

# Streamlit secret: st.secrets["YOUTUBE_API_KEY"]
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]

st.title("YouTube Insights MVP")
st.write("Paste a YouTube video link to get basic insights.")

# Input field
video_url = st.text_input("Enter YouTube video URL:")

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None

def fetch_video_details(video_id):
    """Fetch video details from YouTube API."""
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(part="snippet,statistics", id=video_id)
        response = request.execute()
        if response.get("items"):
            return response["items"][0]
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching video details: {e}")
        return None

if video_url:
    video_id = extract_video_id(video_url)
    if video_id:
        st.write(f"Video ID: {video_id}")
        video_data = fetch_video_details(video_id)
        if video_data:
            snippet = video_data.get("snippet", {})
            stats = video_data.get("statistics", {})
            st.write({
                "Title": snippet.get("title"),
                "Description": snippet.get("description"),
                "Channel": snippet.get("channelTitle"),
                "Published At": snippet.get("publishedAt"),
                "Views": stats.get("viewCount"),
                "Likes": stats.get("likeCount")
            })
        else:
            st.error("Could not fetch video details. Make sure the video is public.")
    else:
        st.error("Invalid YouTube URL. Make sure it's in the standard format.")
