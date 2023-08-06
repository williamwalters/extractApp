import streamlit as st
from streamlit_player import st_player
import numpy as np
#import moviepy as mp
import yt_dlp
from yt_dlp import YoutubeDL
import pandas as pd
import os
import subprocess
import moviepy.editor as mp
from datetime import datetime, timedelta, time

st.set_page_config(page_title="Extract Section from Video", page_icon="youtube", layout="wide")

if 'num' not in st.session_state:
    st.session_state.num = 1
if 'data' not in st.session_state:
    st.session_state.data = []

video_url = 'https://www.youtube.com/watch?v=dLk9pzmaFHY'

urlInput = st.text_input(' ', value='input url here:', max_chars=None, key=None, type='default', help=None, args=None, kwargs=None)
 

def extractClip(beginTime, endTime):
    if os.path.exists('outPath.mp4'):
        os.remove('outPath.mp4')
    try:
    # Code for downloading the video goes here
        yt_dlp.main([video_url, '-f', 'best[height>=720]', '--download-sections', beginEnd, '-o', 'outPath.mp4'])
    except SystemExit:
        print("Download completed, but program was about to exit.")

def main(url):
    vidPlayer = st_player(url)
    
if urlInput[:4] != 'http':
    main(video_url)
    print('main ', urlInput)
    ydl = yt_dlp.YoutubeDL({})
    video_info = ydl.extract_info(video_url, download=False)
elif urlInput[:4] == 'http':
    main(urlInput)
    print('main elif', urlInput)
    ydl = yt_dlp.YoutubeDL({})
    video_info = ydl.extract_info(urlInput, download=False)


hmsString = video_info.get('duration_string').split(':')
if len(hmsString) == 3:
    vidTime = time(hour=int(hmsString[0]), minute=int(  hmsString[1]), second=int(hmsString[2]))
elif len(hmsString) == 2:
    vidTime = time(minute=int(hmsString[0]), second=int(hmsString[1]))
elif len(hmsString) == 1:
    vidTime = time(second=int(hmsString[0]))

extractRange = st.slider('', vidTime.min, value=(vidTime.min, vidTime), 
                         max_value=vidTime, step=timedelta(seconds=1), format = 'HH:mm:ss')

container = st.container()
cols = container.columns(3)
cols[1].text('Choose Time Range: ' + str(extractRange[0]) + ' - ' + str(extractRange[1]))

#container = st.container()
#cols = container.columns(3)
#cols[0].text('Start Time: ')
#cols[1].text('Choose Time Range: ' + str(extractRange[0]) + ' - ' + str(extractRange[1]))
#cols[2].write('Choose Time Range to Extract: ', extractRange[0], ' to ', extractRange[1])
#st.write('Choose Time Range to Extract: ', extractRange[0], ' to ', extractRange[1])
#dButton = st.button("download", on_click=printSection(extractRange[0], extractRange[1]))
#yt_dlp.main([video_url, '-f', 'best[height>=720]', '--download-sections', beginEnd, '-o', 'outPath.mp4'])


container2 = st.container()
container2Cols = container.columns(3)
if container2Cols[1].button("Prepare Clip for Download", on_click=None, use_container_width=True):
    if os.path.exists('outPath.mp4'):
        os.remove('outPath.mp4')
    beginEnd = '*'+str(extractRange[0])+'-'+str(extractRange[1])
    try:
    # Code for downloading the video goes here
        yt_dlp.main([urlInput, '-f', 'best[height>=720]', '--download-sections', beginEnd, '-o', 'outPath.mp4'])
    except SystemExit:
        print("Download completed, but program was about to exit.")
    print('outPath = ', os.path.dirname(os.path.realpath(__file__)) + '/outPath.mp4')
    with open("outPath.mp4", "rb") as file:
        btn = container2Cols[1].download_button(
                label="Download Clip",
                data=file,
                file_name="extracted.mp4",
                #on_click=extractClip(extractRange[0], extractRange[1]), #printSection(extractRange[0], extractRange[1]),
                mime="video/mp4",
                use_container_width=True
              )




#with open("outPath.mp4", "rb") as file:
#    btn = st.download_button(
#            label="a do it",
#            data=file,
#            file_name="extracted.mp4",
#            on_click=extractClip(extractRange[0], extractRange[1]), #printSection(extractRange[0], extractRange[1]),
#            mime="video/mp4"
#          )
#elif not os.path.exists('outPath.mp4'):
#    st.button("set selection", on_click=printSection(extractRange[0], extractRange[1]))
    #printSection(extractRange[0], extractRange[1])
#    with open("outPath.mp4", "rb") as file:
#printSection(extractRange[0], extractRange[1])
#        btn = st.download_button(
#                label="a download",
#                data=file,
#                file_name="extracted.mp4",
#                on_click=printSection(extractRange[0], extractRange[1]),
#                mime="video/mp4"
#              )
    #ytdlp.main([video_url, '-f', 'best[height>=720]', '--download-sections', beginEnd, '-o', 'outPath.mp4'])
    #with open("outPath.mp4", "rb") as file:
    #print('something after yt downloead')
#else:
#    None

#dlData = yt_dlp.main([video_url, '-f', 'best[height>=720]', '--download-sections', beginEnd, '-o', 'outPathD.mp4'])
#dButtoon = st.download_button(label="Download", data='outPathD.mp4', file_name="outPath2.mp4", 
#                              mime="video/mp4", key=None, help=None, on_click = printSection(extractRange[0], extractRange[1]), 
#                              args=None, kwargs=None)


#st.download_button(label="Download", data=printSection(extractRange[0], extractRange[1]), file_name="outPath2.mp4", mime="video/mp4", key=None, help=None, args=None, kwargs=None)
#st.download_button(label="Download", data='outPath.mp4', file_name="outPath2.mp4", mime=mp4, key=None, help=None, args=None, kwargs=None)
#st.button("download", on_click=printSection(extractRange[0], extractRange[1]))