import yt_dlp
import uuid
import os
import sys
import time 
import subprocess
import multiprocessing
import threading
vid_url = 'https://www.youtube.com/watch?v=Up4JxG-rZGY&t=10454s'
beginEnd = '*00:00:00-00:00:24'
outPath = f'appFiles/{str(uuid.uuid4().hex)}.mp4'
command = [sys.executable, '-m', 'yt_dlp', vid_url, '-f', '137+140', '--merge-output-format', 'mp4', '--download-sections', beginEnd, '-o', outPath, '--ignore-no-formats-error']
def run_subprocess(command, done_flag):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = process.communicate()
    done_flag["done"] = True
    return stdout, stderr, process.returncode

# Create a thread to run the subprocess
done_flag = {'done': False}
subprocess_thread = threading.Thread(target=run_subprocess, args=(command, done_flag))

# Start the thread
subprocess_thread.start()
start_time = time.time()
last_time = None

while not done_flag['done']:
    elapsed_time = time.time() - start_time
    if int(elapsed_time) != last_time:
        last_time = int(elapsed_time)
        print(f"Elapsed Time: {elapsed_time:.0f} seconds")

subprocess_thread.join()



