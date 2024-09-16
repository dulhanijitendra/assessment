# # pip install streamlit-ace
# # pip install streamlit_autorefresh
# import streamlit as st
# import cv2
# import os
# import time
# import threading
# from streamlit_ace import st_ace
# import io
# import contextlib
# from datetime import datetime


# # Global variable to control the capture loop
# stop_capture = threading.Event()

# def execute_code(code):
#     try:
#         # Redirect stdout to capture print statements
#         buffer = io.StringIO()
#         with contextlib.redirect_stdout(buffer):
#             exec(code, globals())
#         return buffer.getvalue()
#     except Exception as e:
#         return str(e)


# # Add custom CSS to style the buttons and headings
# st.markdown("""
#     <style>
#     .css-ffhzg2.edgvbvh3 {
#         background-color: green;
#         color: white;
#     }
#     .css-1d391kg.edgvbvh3 {
#         background-color: green;
#         color: white;
#     }
#     h1, h2, h3, h4, h5, h6 {font-size: 24px;
#         color: green;
#     }
#     .center-align {
#         display: flex;
#         justify-content: center;
#     }
#     </style>
# """, unsafe_allow_html=True)


# # Add this JavaScript code to your Streamlit app to detect tab visibility
# # Add JavaScript to detect tab visibility and user inactivity
# st.markdown("""
#     <script>
#     let timer;
#     document.addEventListener('visibilitychange', function() {
#         if (document.hidden) {
#             alert('Please do not switch tabs or minimize the browser.');
#         } else {
#             resetTimer();
#         }
#     });

#     function resetTimer() {
#         clearTimeout(timer);
#         timer = setTimeout(function() {
#             alert('Please do not switch tabs or minimize the browser.');
#         }, 1000); // 1 second
#     }
#     resetTimer();
#     </script>
# """, unsafe_allow_html=True)

# def capture_photos(name,  candidate_id):
#     """Function to capture and save photos every minute."""
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         st.write("Failed to open camera.")
#         return
    
#     start_time = time.time()
#     max_duration = 1 * 60  # 30 minutes in seconds
    
#     while not stop_capture.is_set():
#         current_time = time.time()
#         elapsed_time = current_time - start_time

#         if elapsed_time >= max_duration:
#             st.write("30 minutes have passed. Stopping capture.")
#             break
        
#         ret, frame = cap.read()
#         if not ret:
#             st.write("Failed to grab frame.")
#             break

#         # Generate a filename with metadata and timestamp
#         timestamp = time.strftime("%Y%m%d_%H%M%S")
#         photo_filename = os.path.join(
#             os.getcwd(), f"{name}_{candidate_id}_{timestamp}.jpg"
#         )

#         # Save the captured frame
#         cv2.imwrite(photo_filename, frame)

#         # Wait for 1 minute (60 seconds)
#         time.sleep(60)

#     # Release the camera
#     cap.release()
#     cv2.destroyAllWindows()

# # Initialize Streamlit app
# st.title("AI & Data Hiring- Python Assessment.")
# st.write("Only the responses submitted in first attempt would be used for evaluation> The responses are manually submitted when you apply changes to the code IDEs below")
# st.write('The responses submitted after 30 minutes will not be considered for evaluation')

# # Input fields for metadata
# name = st.text_input("Enter Name", key="name_input")
# candidate_id = st.text_input("Enter Candidate ID", key="candidate_id_input")

# # Submit button
# if st.button("Submit"):
#     if name and candidate_id:
#         st.write(f"Capturing photos every minute for {name} with Candidate ID: {candidate_id}")

#         # Start the capture in a separate thread
#         stop_capture.clear()
#         capture_thread = threading.Thread(target=capture_photos, args=(name, candidate_id))
#         capture_thread.start()

#         st.success("Capture started.")
#     else:
#         st.warning("Please fill in all fields.")

# st.write('Write a Python Code to test if a number is a prime number. The changes that you last apply would be used for assessment')
# code_1 = st_ace(value="print('Hello, world!')", language='python', theme='monokai', key='code_1')
# if st.button('Test your last applied code changes', key='Run1'):
#     result1 = execute_code(code_1)
#     st.write("**Output:**")
#     st.code(result1)

# st.write('Write a Python Code to test if a string is a palindrome. The changes that you last apply would be used for assessment')
# code_2 = st_ace(value="print('Hello, world!')", language='python', theme='monokai', key='code_2')
# if st.button('Test your last applied code changes', key='Run2'):
#     result2 = execute_code(code_2)
#     st.write("**Output:**")
#     st.code(result2)

# with open('submitted_code_1.py', 'w') as f:
#             f.write(code_1)

# with open('submitted_code_2.py', 'w') as f:
#             f.write(code_2)


import streamlit as st
import io
import contextlib
import threading
import time
import os
from streamlit_ace import st_ace
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from PIL import Image
import av
import numpy


# Global variable for managing the video file
video_file_path = "Candidate Video.mp4"

    # Initialize Streamlit app
st.title("Hiring- Python Assessment- JD.")
st.write("The responses are manually submitted when you apply changes to the code IDEs below")
st.write("The responses last submitted within 30 minutes will be used for evaluation")
st.write('The responses submitted after 30 minutes will not be considered for evaluation')

st.write('Follow these steps (a) Turn On Camera (b) Select Device (c) Fill in your responses in Code IDEs (d) Come back and confirm if you have completed')

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.video_writer = av.open(video_file_path, mode='w', format='mp4', options={'crf': '23'})
        self.start_time = time.time()

    def transform(self, frame):
        # Append video frames to the file
        if self.video_writer:
            img = frame.to_image()
            img = img.convert("RGB")
            frame_data = np.array(img)
            frame = av.VideoFrame.from_ndarray(frame_data, format='rgb24')
            self.video_writer.mux(frame)
            
        # Automatically stop after 30 minutes
        if time.time() - self.start_time >= 30 * 60:
            self.close()
        
        return frame

    def close(self):
        if self.video_writer:
            self.video_writer.close()
# Manage camera state with session state
if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

def toggle_camera():
    st.session_state.camera_on = not st.session_state.camera_on
    if st.session_state.camera_on:
        st.session_state.start_time = time.time()
        st.write("Camera is now on. The video will be saved after 30 minutes or when you click 'Done'.")
    else:
        st.session_state.start_time = None

st.button('Turn On Camera', on_click=toggle_camera)

if st.session_state.camera_on:
    # Start video streaming
    webrtc_ctx = webrtc_streamer(key="example", video_transformer_factory=VideoTransformer)
    
    # Add a button to save and stop recording
    if st.button('I have applied changes to the code and completed the assessment'):
        if webrtc_ctx.video_transformer:
            webrtc_ctx.video_transformer.close()
        st.write(f"Video saved to {video_file_path}")
        st.session_state.camera_on = False
else:
    st.write("Click 'Turn On Camera' to start capturing video.")


def execute_code(code):
    try:
        # Redirect stdout to capture print statements
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exec(code, globals())
        return buffer.getvalue()
    except Exception as e:
        return str(e)

# Add custom CSS to style the buttons and headings
st.markdown("""
    <style>
    .css-ffhzg2.edgvbvh3 {
        background-color: green;
        color: white;
    }
    .css-1d391kg.edgvbvh3 {
        background-color: green;
        color: white;
    }
    h1, h2, h3, h4, h5, h6 {font-size: 24px;
        color: green;
    }
    .center-align {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# Add JavaScript to detect tab visibility and user inactivity
st.markdown("""
    <script>
    let timer;
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            alert('Please do not switch tabs or minimize the browser.');
        } else {
            resetTimer();
        }
    });

    function resetTimer() {
        clearTimeout(timer);
        timer = setTimeout(function() {
            alert('Please do not switch tabs or minimize the browser.');
        }, 1000); // 1 second
    }
    resetTimer();
    </script>
""", unsafe_allow_html=True)

st.write('Edit the hello world function below to include your name as Candidate ID. For example if your candidate ID is 4356, the output should return Hello 5356.')
code_10 = st_ace(value="print('Hello, world!')", language='python', theme='monokai', key='code_10')
if st.button('Test your last applied code changes', key='Run10'):
    result1 = execute_code(code_10)
    st.write("**Output:**")
    st.code(result1)

st.write('Write a Python Code to test if a number is a prime number. The changes that you last apply would be used for assessment')
code_1 = st_ace(value="print('Hello, world!')", language='python', theme='monokai', key='code_1')
if st.button('Test your last applied code changes', key='Run1'):
    result1 = execute_code(code_1)
    st.write("**Output:**")
    st.code(result1)

st.write('Write a Python Code to test if a string is a palindrome. The changes that you last apply would be used for assessment')
code_2 = st_ace(value="print('Hello, world!')", language='python', theme='monokai', key='code_2')
if st.button('Test your last applied code changes', key='Run2'):
    result2 = execute_code(code_2)
    st.write("**Output:**")
    st.code(result2)

with open('submitted_name.py', 'w') as f:
    f.write(code_10)

with open('submitted_code_1.py', 'w') as f:
    f.write(code_1)

with open('submitted_code_2.py', 'w') as f:
     f.write(code_2)
