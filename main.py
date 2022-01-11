import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
from streamlit_webrtc import (

    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)
import av




class OpenCVVideoProcessor(VideoProcessorBase):



    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        gray = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)
        face = face_cascade.detectMultiScale(gray, 1.5, 4)
        for (x, y, w, h) in face:
            cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 5)
            roi_gray = gray[y:y + h, x:x + w]
            #roi_color = img_edges[y:y + h, x:x + w]

            # print(index)
            # cv2.putText(, index, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 2,color = (0, 0, 255),thickness = 2, cv2.LINE_AA)
            cv2.putText(gray, 'Face', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)




        return av.VideoFrame.from_ndarray(gray, format="bgr24")







st.write("# test app testing ")



webrtc_ctx = webrtc_streamer(
    key="opencv-filter",
    mode=WebRtcMode.SENDRECV,
    #rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=OpenCVVideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)
