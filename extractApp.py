from streamlit_player import st_player
import streamlit as st
import yt_dlp

from datetime import timedelta, time
import os


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
    ydl = yt_dlp.YoutubeDL({})
    video_info = ydl.extract_info(video_url, download=False)
elif urlInput[:4] == 'http':
    main(urlInput)
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

container2 = st.container()
container2Cols = container.columns(3)
if container2Cols[1].button("Prepare Clip for Download", on_click=None, use_container_width=True):
    
    outPath = 'outPath.mp4'
    #str(Path(os.path.dirname(os.path.realpath(__file__))).parent) + '/outPath.mp4'

    if os.path.exists(outPath):
        os.remove(outPath)
    beginEnd = '*'+str(extractRange[0])+'-'+str(extractRange[1])
    try:
    # Code for downloading the video goes= here
        yt_dlp.main([urlInput, '-f', 'best[height>720]', '--download-sections', beginEnd, '-o', outPath])
        #yt_dlp.main([urlInput, '-f', '137+140', '--merge-output-format', 'mp4', '--download-sections', beginEnd, '-o', outPath, '--ignore-no-formats-error'])
        #yt_dlp.main([urlInput, '-f', 'best[height>720]', '--merge-output-format',  'mp4', '--download-sections', beginEnd, '-o', outPath, '--yes-playlist', '--ignore-no-formats-error'])
    except SystemExit:
        print("Download completed, but program was about to exit.")
    print('outPath: ', outPath)
    with open(outPath, "rb") as file:
        btn = container2Cols[1].download_button(
                label="Download Clip",
                data=file,
                file_name="extracted.mp4",
                #on_click=extractClip(extractRange[0], extractRange[1]), #printSection(extractRange[0], extractRange[1]),
                mime="video/mp4",
                use_container_width=True
              )

