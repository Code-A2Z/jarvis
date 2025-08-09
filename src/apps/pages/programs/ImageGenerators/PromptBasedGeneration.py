from google import genai
from google.genai import types  # type:ignore
from PIL import Image
from io import BytesIO
import base64
import streamlit as st  # type:ignore

# Streamlit UI for API key input and text input


def PromptBasedGeneration():
    st.title("AI Image Generator")
    api_key = st.text_input("Enter your Gemini API key for image generation:")
    prompt = st.text_area("Enter a prompt for image generation:")

    # Button to trigger image generation
    if st.button("Generate Image"):
        if not api_key:
            st.error("Please enter a valid API key.")
        elif not prompt:
            st.error("Please enter a prompt for image generation.")
        else:
            try:
                # Initialize the client
                client = genai.Client(api_key=api_key)

                # Generate content
                response = client.models.generate_content(
                    model="gemini-2.0-flash-preview-image-generation",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=['TEXT', 'IMAGE']
                    )
                )

                # Process the response
                for part in response.candidates[0].content.parts:
                    if part.text is not None:
                        st.write("Generated Text:", part.text)
                    elif part.inline_data is not None:
                        # Decode and display the image
                        image = Image.open(BytesIO(part.inline_data.data))
                        st.image(image, caption="Generated Image")
                        st.success("Image generated successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    st.subheader("Generate AI Images :frame_with_picture:")
