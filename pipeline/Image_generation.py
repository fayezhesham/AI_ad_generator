import requests
import os
from dotenv import load_dotenv



# Load environment variables from a .env file (must contain HUGGING_FACE_API_KEY)
load_dotenv()

# Retrieve your Hugging Face API key (access token)
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")


def generate_image(image_prompt):
    # Set the model you want to use
    model_id = "runwayml/stable-diffusion-v1-5"  # or try "stabilityai/stable-diffusion-2-1"runwayml/stable-diffusion-v1-5  CompVis/stable-diffusion-v1-4
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
    }

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    # Prompt for an image description
    image_description = image_prompt + ", realistic style, social media ad creative"

    # Generate the image
    image_bytes = query({"inputs": image_description})

    return image_bytes