from streamlit_player import st_player
import streamlit as st
import threading
import yt_dlp
import uuid
import time as t
import subprocess
from datetime import timedelta, time, datetime
from streamlit.config import set_option
import asyncio
from streamlit.runtime import get_instance
from streamlit.runtime.scriptrunner import get_script_run_ctx
import sys
import os




def run_page():
    st.set_page_config(page_title="Extract Section from Video", page_icon="🎬", layout="wide")
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
    #container2Cols = container.columns(3)
    formats = []
    resolutions = []
    isCombo = []
    button_text = []
    for format_dict in video_info['formats']:
        if format_dict.get('acodec') != 'none' and format_dict.get('vcodec') != 'none':
            #download_buttons.append(container2Cols[1].button(format_dict.get('resolution'), on_click=None, use_container_width=True))
            resolutions.append(format_dict.get('resolution'))
            formats.append(format_dict.get('format_id'))
            isCombo.append(True)
            button_text.append(f'quick extraction available')

    if video_info['formats'][-1].get('acodec') == 'none' or video_info['formats'][-1].get('vcodec') == 'none':
        resolutions.append(format_dict.get('resolution'))
        formats.append(format_dict.get('format_id'))
        isCombo.append(False)
        button_text.append(f'slower extraction times')
    
    
    def quick_download(column_num, url, format_id, outPath, beginEnd, isCombo):
        if isCombo:
            command = [sys.executable, '-m', 'yt_dlp', url, '-f', format_id, '--download-sections', beginEnd, '-o', outPath, '--ignore-no-formats-error']

        elif not isCombo:
            command = [sys.executable, '-m', 'yt_dlp', url, '-f', '137+140', '--merge-output-format', 'mp4', '--download-sections', beginEnd, '-o', outPath, '--ignore-no-formats-error']

        extract_len = get_len_seconds(extractRange[1], extractRange[0])
        done_flag = {'done': False}
        subprocess_thread = threading.Thread(target=run_subprocess, args=(command, done_flag))
        # Start the thread
        subprocess_thread.start()
        start_time = t.time()
        last_time = None
        if 'current_file' not in st.session_state:
            st.session_state['current_file'] = outPath
        elif 'current_file' in st.session_state:
            st.session_state['current_file'] = outPath
        while not done_flag['done']:
            elapsed_time = t.time() - start_time
            if int(elapsed_time) != last_time:
                download_progress = (elapsed_time/extract_len)+.3
                if download_progress > 1.0:
                    download_progress = 1.0
                p_bar.progress(download_progress)
                last_time = int(elapsed_time)
        p_bar.progress(1.0)
        subprocess_thread.join()

    container2Cols = container.columns(len(resolutions))
    files = []
    for i in range(len(resolutions)):
        outPath = f'{video_info.get("title").split(" ")[0]}_{str(uuid.uuid4().hex)[-4:]}_{resolutions[i].split("x")[-1]}.mp4'
        files.append(outPath)
        beginEnd = '*'+str(extractRange[0])+'-'+str(extractRange[1])
        container2Cols[i].button(resolutions[i], on_click=quick_download, 
                                 args = [i, urlInput, formats[i], outPath, beginEnd, isCombo[i]], 
                                 use_container_width=True)
        container2Cols[i].text(button_text[i])
    print('st state ', st.session_state)
    btn = False
    if 'current_file' in st.session_state:
        if os.path.exists(st.session_state['current_file']):
            with open(st.session_state['current_file'], "rb") as file:
                btn = st.download_button(
                        label="download clip",
                        data=file,
                        file_name=st.session_state['current_file'],
                        mime="video/mp4",
                        use_container_width=True
                      )
                
                print('before id ', type(st._main))
                print('root id ', st._main._root_container)
                print('root cursor ', st._main._cursor)
                print('root parent ', st._main._parent)
                btn = True

    p_bar = st.progress(0)
    if 'current_file' in st.session_state and btn:
        if os.path.exists(st.session_state['current_file']):
            os.remove(st.session_state['current_file'])
    #    if os.path.exists(st.session_state['current_file']):
    #            os.remove(st.session_state['current_file'])
    #else:
    #    return ''

#async def watch(test):
#    runtime = run_page()
#    ctx = get_script_run_ctx()
#    while runtime.is_active_session(ctx.session_id):
#        pass
#
#test = st.empty()
#
#asyncio.run(watch(test))
#
#print('end of session')

if __name__ == "__main__":
    runtime = run_page()
    #ctx = get_script_run_ctx()
    #while runtime.is_active_session(ctx.session_id):
    #    pass
    #asyncio.run(watch(test))
    print('these are created files ')