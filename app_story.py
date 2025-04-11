import streamlit as st
import os
import tempfile
import textwrap
import pathlib
import PIL.Image
from IPython.display import Image, Markdown, display
import openai
import google.generativeai as genai
from PIL import Image as PILImage

openai.api_key = "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"


# Configure Google Generative AI
genai.configure(api_key='AIzaSyArFsF8XTEyuPDbQhtvGjZfygziLN6RF7o')

def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            font-family: Arial, sans-serif;
        }
        .title {
            color: #3A6EA5;
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .upload-area {
            text-align: center;
            margin-bottom: 20px;
        }
        .description-box {
            background-color: BLACK;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
            font-size: 1rem;
        }
        .story-box {
            background-color: BLACK;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ffa726;
            font-size: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Function to describe an image using Gemini AI
def describe_image_with_gemini(image_path, mime_type):
    """
    Describe an image using Google Generative AI's Gemini model.
    """
    # Upload the image to Google Generative AI
    uploaded_file = genai.upload_file(image_path, mime_type=mime_type)
    
    # Generate content using Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content([uploaded_file, "\n\n", "Can you give me a short description of this image?"])
    
    # Extract and return the text description
    if result.candidates:
        return result.candidates[0].content.parts[0].text
    else:
        return "No description generated."

# Function to generate a story using OpenAI GPT
def generate_story_with_openai(description):
    """
    Generate a story based on a description using OpenAI's GPT model.
    """
    prompt = (
        f"Consider yourself a professional story writer. Write a complete story "
        f"based on the following description: {description}. "
        f"Use proper paragraphs and avoid starting sentences with 'as'."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Function to determine MIME type based on file extension
def get_mime_type(file_extension):
    """
    Determine the MIME type based on the file extension.
    """
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png"
    }
    return mime_types.get(file_extension.lower(), "application/octet-stream")

# Main function to run the application
def main():
    # Add custom CSS for styling
    add_custom_css()

    # Custom title
    st.markdown('<div class="title">AI-Driven Image Storyteller</div>', unsafe_allow_html=True)

    # File uploader with custom styling
    st.markdown('<div class="upload-area">Upload an image to get started:</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            image_path = temp_file.name

        # Determine MIME type
        file_extension = pathlib.Path(uploaded_file.name).suffix
        mime_type = get_mime_type(file_extension)

        # Display uploaded image
        st.image(PILImage.open(image_path), caption="Uploaded Image", use_column_width=True)

        # Generate image description with Gemini AI
        try:
            image_description = describe_image_with_gemini(image_path, mime_type)
            st.markdown("### Generated Description:")
            st.markdown(f'<div class="description-box">{image_description}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating description with Gemini: {e}")
            return

        # Generate a story based on the description with OpenAI GPT
        try:
            story = generate_story_with_openai(image_description)
            st.markdown("### Generated Story:")
            st.markdown(f'<div class="story-box">{story}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error generating story with OpenAI: {e}")


if __name__ == "__main__":
    main()