import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to call Gemini model
def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_prompt, image[0]])
    return response.text

# Function to prepare uploaded image for model
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("File not Uploaded")

# Set page config

# Title
st.title("🍽️ Calories Tracker")

# Split layout: sidebar for image upload, main area for output
with st.sidebar:
    st.header("Upload Food Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    submit = st.button("Tell me about the total calories")

# If file is uploaded, show it in sidebar
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Image", use_coloumn_width=True)

# Prompt for Gemini
input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of
every food item with calories intake
in below format

1. Item 1 - no of calories
2. Item 2 - no of calories
----
----

Finally you can also mention whether the food is healthy or not and also mention the
percentage split of the ratio of carbohydrates, fats, fibers, sugar and other
things required in our diet
"""

# Output area with increased font
if submit and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)

    st.subheader("The Response is")
    st.markdown(f"""
    <div style='font-size:24x; line-height:1.6;'>{response}</div>
    """, unsafe_allow_html=True)
