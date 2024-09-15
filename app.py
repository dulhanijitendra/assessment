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
from streamlit_ace import st_ace
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

# Global variable to control the capture loop
stop_capture = threading.Event()

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

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frames = []
    
    def transform(self, frame):
        # Add frame to the list (you can use these frames for further processing)
        self.frames.append(frame)
        img = frame.to_ndarray(format="bgr24")
        return img

def capture_photos(name, candidate_id):
    """Function to capture and save photos every minute."""
    video_transformer = VideoTransformer()
    
    # Streamlit WebRTC component for video capture
    def video_frame_callback(frame):
        if not stop_capture.is_set():
            video_transformer.transform(frame)
            if len(video_transformer.frames) > 0:
                frame = video_transformer.frames.pop()
                img = frame.to_ndarray(format="bgr24")
                
                # Generate a filename with metadata and timestamp
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                photo_filename = os.path.join(
                    os.getcwd(), f"{name}_{candidate_id}_{timestamp}.jpg"
                )
                
                # Save the captured frame
                cv2.imwrite(photo_filename, img)
    
    # Initialize Streamlit app
st.title("AI & Data Hiring- Python Assessment.")
st.write("Only the responses submitted in first attempt would be used for evaluation. The responses are manually submitted when you apply changes to the code IDEs below")
st.write('The responses submitted after 30 minutes will not be considered for evaluation')
st.write('Step 1: Fill in your details such as name and candidate ID. Do remember to submit these details')
st.write('Step 2: You have to start your camera by clicking on "Select Device". Please not click on done unless you have completed the assessment')

    # Input fields for metadata
name = st.text_input("Enter Name", key="name_input")
candidate_id = st.text_input("Enter Candidate ID", key="candidate_id_input")

    # Submit button
if st.button("Submit"):
    if name and candidate_id:
        st.write(f"Capturing photos every minute for {name} with Candidate ID: {candidate_id}")

            # Start the capture in a separate thread
        stop_capture.clear()
        capture_thread = threading.Thread(target=capture_photos, args=(name, candidate_id))
        capture_thread.start()

        st.success("Capture started.")
    else:
        st.warning("Please fill in all fields.")

    # Streamlit WebRTC component for real-time video capture
webrtc_streamer(key="video", video_transformer_factory=VideoTransformer)

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

with open('submitted_code_1.py', 'w') as f:
    f.write(code_1)

with open('submitted_code_2.py', 'w') as f:
    f.write(code_2)
