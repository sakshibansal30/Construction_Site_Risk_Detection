import os
import time
import cv2
import sys
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tensorflow as tf
import keras_preprocessing
import streamlit as st
import numpy as np
import pandas as pd
from numpy import argmax
from PIL import Image , ImageEnhance
from resizeimage import resizeimage
from utils import label_map_util
from utils import visualization_utils as vis_util
from keras.preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from pathlib2 import Path
import base64
from io import BytesIO
tf.executing_eagerly() #implemented by default in tensorflow2


MODEL_NAME = 'C:/Streamlit_Application/Construction_Site_Risk_Detection/object_detection/inference_graph'
IMAGE_NAME = 'C:/Streamlit_Application/Construction_Site_Risk_Detection/object_detection/images'

CWD_PATH = os.getcwd()

PATH_TO_CKPT = os.path.join('C:/Streamlit_Application/Construction_Site_Risk_Detection/object_detection/inference_graph/frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join('C:/Streamlit_Application/Construction_Site_Risk_Detection/object_detection/label_map.pbtxt')
PATH_TO_IMAGE = os.path.join('C:/Streamlit_Application/Construction_Site_Risk_Detection/object_detection/images/out.jpg')

NUM_CLASSES = 6


label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.compat.v1.GraphDef()
    with  tf.compat.v2.io.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.compat.v1.Session(graph=detection_graph)

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Load image using OpenCV and
# expand image dimensions to have shape: [1, None, None, 3]
# i.e. a single-column array, where each item in the column has the pixel RGB value
in_image = cv2.imread(PATH_TO_IMAGE)
image_rgb = cv2.cvtColor(in_image, cv2.COLOR_BGR2RGB)
image_expanded = np.expand_dims(
    image_rgb, axis=0)

# Perform the actual detection by running the model with the image as input
(boxes, scores, classes, num) = sess.run(
    [detection_boxes, detection_scores, detection_classes, num_detections],
    feed_dict={image_tensor: image_expanded})

# Draw the results of the detection (aka 'visulaize the results')

vis_util.visualize_boxes_and_labels_on_image_array(
    in_image,
    np.squeeze(boxes),
    np.squeeze(classes).astype(np.int32),
    np.squeeze(scores),
    category_index,
    use_normalized_coordinates=True,
    line_thickness=8,
    min_score_thresh=0.60)

def get_image_download_link(img,filename,text):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/jpg;base64,{img_str}" download="{filename}">{text}</a>'
    return href

#@st.cache
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()
	

def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)
    #with open('style.css') as f:
     #   st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
    st.markdown('<style>body{-webkit-app-region: drag;}</style>', unsafe_allow_html=True)
    st.title("Construction Site Risk Detection")
   # st.text("Build with Streamlit and Tensorflow")
    activities = ["About" ,"Risk Detection","Contact"]
    choice = st.sidebar.selectbox("Select Activty",activities)
    #enhance_type = st.sidebar.radio("Type",["Detection","Classification","Treatment"])
    
    if choice =='About':
        
        intro_markdown = read_markdown_file("C:/Streamlit_Application/Construction_Site_Risk_Detection/doc/about.md")
        st.markdown(intro_markdown, unsafe_allow_html=True)
        
    elif choice == 'Risk Detection':
      #  st.header("Upload an image to see the results!")
        image_file = st.file_uploader("Upload Image",type=['jpg','png','jpeg'])
        st.markdown("* * *")
        
        
        if image_file is not None:
            file_details = {"FileName":image_file.name,"FileType":image_file.type}
            st.write(file_details)
            our_image = Image.open(image_file)
            im = our_image.save('C:/Streamlit_Application/Construction_Site_Risk_Detection/object_detection/images/out.jpg')
            st.image(our_image, caption='Uploaded Image.')
          
       
            
            
            if st.button('Detect'):
                st.image(in_image , use_column_width=True,channels='RGB')
            st.image(our_image , use_column_width=True,channels='RGB')
      
       
            
    elif choice =='Contact':
        
     st.markdown(""" <style> .font {
     font-size:35px ; font-family: 'Sans serif'; color: #FEFEFF;} 
     </style> """, unsafe_allow_html=True)
     st.markdown('<p class="font">Contact Form</p>', unsafe_allow_html=True)
     with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        #st.write('Please help us improve!')
       Name=st.text_input(label='Please Enter Your Name') #Collect user feedback
       Email=st.text_input(label='Please Enter Your Email') #Collect user feedback
       Message=st.text_input(label='Please Enter Your Query') #Collect user feedback
       submitted = st.form_submit_button('Submit')
       if submitted:
          st.write('Thanks for contacting us. We will respond to your questions or inquiries as soon as possible!')
            
        
                            
main()