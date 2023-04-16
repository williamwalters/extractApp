import streamlit as st
from streamlit_player import st_player
import numpy as np
#import moviepy as mp
import yt_dlp
import pandas as pd
from datetime import datetime
from datetime import time


st.set_page_config(page_title="Extract Section from Video", page_icon="youtube", layout="wide")

if 'num' not in st.session_state:
    st.session_state.num = 1
if 'data' not in st.session_state:
    st.session_state.data = []


video_url = 'https://www.youtube.com/watch?v=dLk9pzmaFHY'

urlInput = st.text_input(' ', value='input url here:', max_chars=None, key=None, type='default', help=None, args=None, kwargs=None)

def printSection(start, end):
    print(start, end)

def main(url):
    vidPlayer = st_player(url)
    
if urlInput[:4] != 'http':
    main(video_url)
    ydl = yt_dlp.YoutubeDL({})
    video_info = ydl.extract_info(video_url, download=False)
    duration = video_info.get('duration')
elif urlInput[:4] == 'http':
    main(urlInput)
    ydl = yt_dlp.YoutubeDL({})
    video_info = ydl.extract_info(urlInput, download=False)
    duration = video_info.get('duration')

vidBegin = time(0, 0, 0)
vidTime = time(3, 45)
#vidLen = datetime.utcfromtimestamp(454)
extractRange = st.slider('vid length', min_value=vidBegin, value=(vidBegin, vidTime), max_value=vidTime)

st.button('push it push it', 
          key=None, help=None, 
          on_click=printSection(extractRange[0], extractRange[1]),
          args=None, 
          kwargs=None, type="secondary", 
          disabled=False, use_container_width=True)