import streamlit as st
import requests
from io import BytesIO
from PIL import Image
import streamlit.components.v1 as components


# Base URL for your FastAPI endpoints
API_BASE_URL = "http://localhost:8000"  # Update if deployed elsewhere

st.set_page_config(layout="wide", page_title="E-commerce Ad & Image Generator")

# Title and app description
st.title("Ad generator for E-commerce products")

st.markdown(
    """
    **What does this app do?**

    This app extracts product information from an ecommerce store URL, generates a compelling ad copy for social media, and suggests creative visuals for your campaign. 
    It leverages advanced language models and image generation APIs to deliver a complete marketing solution—all in one easy-to-use interface.

    **How to use the app:**
    1. Enter your ecommerce product page URL.
    2. Optionally, add additional custom instructions.
    3. Click **Generate Ad** to see the generated ad text, image description, and video description.
    4. Click **Generate Image** to produce a visual for your ad.

    **Try it out with these example independent Shopify store links:**
    """
)

def copy_link_component(link: str):
    # HTML snippet with a clickable link and a copy button
    html_code = f"""
    <div style="display: flex; align-items: center; margin-bottom: 8px;">
      <a href="{link}" target="_blank" style="margin-right: 10px; font-size:16px;">{link}</a>
      <button onclick="navigator.clipboard.writeText('{link}')" style="padding:4px 8px; font-size:14px;">Copy</button>
    </div>
    """
    components.html(html_code, height=50)

# Sample independent Shopify store links for demonstration
copy_link_component("https://teddybaldassarre.com/en-int/products/orion-38mm")
copy_link_component("https://bruvi.com/collections/espresso/products/full-bloom")
copy_link_component("https://rothys.com/en-nl/products/womens-classic-clog-butternut")

st.markdown("---")
st.markdown("Below you can generate your own ad by providing your product page URL and optional additional instructions.")

# Initialize session state variables if not already set
if "ad_data" not in st.session_state:
    st.session_state.ad_data = None
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

st.title("Ad generator for E-commerce products")

# Input field for the store URL
url_input = st.text_input("Enter the URL of your product page:")

# Optional text area for additional instructions
additional_instructions = st.text_area(
    "Enter additional instructions (optional)",
    placeholder="For example, use a friendly tone and emphasize discounts."
)

# Button to generate the ad based on the URL (and optional instructions)
if st.button("Generate Ad"):
    if not url_input:
        st.warning("Please provide a valid URL.")
    else:
        # Prepare payload for the API request
        payload = {"url": url_input}
        if additional_instructions:
            payload["additional_instructions"] = additional_instructions
        try:
            response = requests.post(f"{API_BASE_URL}/generate_ad", json=payload)
            if response.status_code == 200:
                st.session_state.ad_data = response.json()
                st.session_state.generated_image = None  # Reset any previous image
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# If ad data is available, display the ad details and image generation section
if st.session_state.ad_data:
    # Create two columns with a 2:1 ratio
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Generated Ad")
        st.markdown("#### Ad Text")
        st.write(st.session_state.ad_data.get("ad_text", ""))
        st.markdown("#### Image Description")
        st.write(st.session_state.ad_data.get("image", ""))
        st.markdown("#### Video Description")
        st.write(st.session_state.ad_data.get("video", ""))
    
    with col2:
        st.subheader("Generated Image")
        image_slot = st.empty()
        if st.session_state.generated_image:
            image_slot.image(
                st.session_state.generated_image,
                caption="Generated Image",
                use_column_width=True
            )
        else:
            image_slot.info("Your image will appear here once generated.")
        
        # "Generate Image" button within the image section
        if st.button("Generate Image", key="generate_image_button"):
            try:
                image_prompt = st.session_state.ad_data.get("image", "")
                image_response = requests.post(
                    f"{API_BASE_URL}/generate_image",
                    json={"prompt": image_prompt}
                )
                if image_response.status_code == 200:
                    st.session_state.generated_image = Image.open(BytesIO(image_response.content))
                    image_slot.image(
                        st.session_state.generated_image,
                        caption="Generated Image",
                        use_column_width=True
                    )
                else:
                    st.error(f"Error {image_response.status_code}: {image_response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
