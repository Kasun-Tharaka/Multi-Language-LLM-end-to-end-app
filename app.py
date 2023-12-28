from dotenv import load_dotenv
#load all the env vaiables
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOLE_API_KEY'))


#function to load Gemini Pro Visin
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input, image, prompt):
    #input:- how model's behavior should be. how to act.
    response = model.generate_content([input, image[0], prompt])

    return response.text


def input_image_details(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



#streamlit application
st.set_page_config(page_title='Multi Language Gemini LLM')
st.header('Gemini LLM')

input = st.text_input('input prompt :', key='input')
uploaded_file = st.file_uploader('Choose an image...', type=['png', 'jpg', 'jpeg'])

image = ""
if uploaded_file is not None:
    #open the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='uploaded image', use_column_width=True)

submit = st.button("Tell me about the image")


input_prompt = """
you are a expert in understanding images, what ever in an image such as text or pictures
anything. we will upload an image to get full understand about image.you will have to
answer any question based on the uploaded image
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("response :")
    st.write(response)