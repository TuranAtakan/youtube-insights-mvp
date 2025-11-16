import streamlit as st
import pandas as pd

st.title("YouTube Insights MVP")
st.write("Upload your YouTube watch history to get insights.")

uploaded_file = st.file_uploader("Choose your YouTube watch history CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of your watch history:")
    st.dataframe(df.head())
