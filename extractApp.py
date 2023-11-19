from streamlit_player import st_player
import streamlit as st
import threading
import yt_dlp
import uuid
import time as t
import subprocess
from datetime import timedelta, time
import sys
import os


st.set_page_config(page_title="Extract Section from Video", page_icon="youtube", layout="wide")


# ======================== This  section will remove the hamburger and watermark and footer and header from streamlit ===========
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            footer:after {
                            content:''; 
	                        visibility: visible;
	                        display: block;
	                        position: relative;
	                        #background-color: red;
	                        padding: 5px;
	                        top: 2px;
                        }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# not sure what session state is for
if 'num' not in st.session_state:
    st.session_state.num = 1
if 'data' not in st.session_state:
    st.session_state.data = []

video_url = 'https://www.youtube.com/watch?v=dLk9pzmaFHY'

urlInput = st.text_input(' ', value='input url here:', max_chars=None, key=None, type='default', help=None, args=None, kwargs=None)
 
def display_vid(url):
    #vidPlayer = st_player(url)
    vidPlayer = st.video(url)

def run_subprocess(command, done_flag):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    done_flag["done"] = True
    return stdout, stderr, process.returncode

if urlInput[:4] != 'http':
    display_vid(video_url)
    ydl = yt_dlp.YoutubeDL({})
    video_info = ydl.extract_info(video_url, download=False)

elif urlInput[:4] == 'http':
    display_vid(urlInput)
    ydl = yt_dlp.YoutubeDL({})
    video_info = ydl.extract_info(urlInput, download=False)

def get_len_seconds(t_one, t_two):
    """Convert a datetime.time object to seconds since midnight."""
    t_one_seconds =  t_one.hour * 3600 + t_one.minute * 60 + t_one.second
    t_two_seconds =  t_two.hour * 3600 + t_two.minute * 60 + t_two.second
    return t_one_seconds - t_two_seconds

hmsString = video_info.get('duration_string').split(':')
if len(hmsString) == 3:
    vidTime = time(hour=int(hmsString[0]), minute=int(  hmsString[1]), second=int(hmsString[2]))
elif len(hmsString) == 2:
    vidTime = time(minute=int(hmsString[0]), second=int(hmsString[1]))
elif len(hmsString) == 1:
    vidTime = time(second=int(hmsString[0]))

extractRange = st.slider('', vidTime.min, value=(vidTime.min, vidTime), 
                         max_value=vidTime, step=timedelta(seconds=1), format = 'HH:mm:ss')

# container creates the layout of the page element, the choose time text goes in the middle column
container = st.container()
cols = container.columns(3)
cols[1].text('Choose Time Range: ' + str(extractRange[0]) + ' - ' + str(extractRange[1]))


# container creates the layout of the page element, the prepare button goes in the middle column
container2 = st.container()
container2Cols = container.columns(3)


if container2Cols[1].button("Prepare Clip for Download", on_click=None, use_container_width=True):
    outPath = f'{str(uuid.uuid4().hex)}.mp4'

    if os.path.exists(outPath):
        os.remove(outPath)
    beginEnd = '*'+str(extractRange[0])+'-'+str(extractRange[1])
    
    extract_len = get_len_seconds(extractRange[1], extractRange[0])
    print('beginEnd: ', beginEnd, 'extract len ', extract_len)
    status = st.empty()
    
    command = [sys.executable, '-m', 'yt_dlp', urlInput, '-f', '137+140', '--merge-output-format', 'mp4', '--download-sections', beginEnd, '-o', outPath, '--ignore-no-formats-error']

    # Create a thread to run the subprocess
    done_flag = {'done': False}
    subprocess_thread = threading.Thread(target=run_subprocess, args=(command, done_flag))

    # Start the thread
    subprocess_thread.start()
    start_time = t.time()
    last_time = None
    p_bar = st.progress(0)
    while not done_flag['done']:
        elapsed_time = t.time() - start_time
        if int(elapsed_time) != last_time:
            #download_speed = os.path.getsize(outPath)/elapsed_time
            download_progress = elapsed_time/extract_len
            print(download_progress)
            if download_progress > 1.0:
                download_progress = 1.0
            p_bar.progress(elapsed_time/extract_len)
            last_time = int(elapsed_time)
    p_bar.progress(1.0)

    subprocess_thread.join()

    print('temp file name: ', outPath)
    print('current wk dir: ', os.getcwd())
    with open(outPath, "rb") as file:
        btn = container2Cols[1].download_button(
                label="Download Clip",
                data=file,
                file_name=outPath,
                #on_click=extractClip(extractRange[0], extractRange[1]), #printSection(extractRange[0], extractRange[1]),
                mime="video/mp4",
                use_container_width=True
              )
    status.empty()
    edit_container = st.container()
    editor_cols = edit_container.columns(1)
    editor_cols[0].video(outPath)
    

