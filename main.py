from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import io
from typing import Optional


from pipeline import Ad
from pipeline import load_url_content, parse_listing
from pipeline import extract_product_details, generate_ad
from pipeline import generate_image

app = FastAPI()

# Define request and response models
class AdRequest(BaseModel):
    url: str
    additional_instructions: Optional[str] = ""

class AdResponse(BaseModel):
    ad_text: str
    image: str
    video: str

class ImageRequest(BaseModel):
    prompt: str

# Make this function asynchronous
async def generate_ad_response(url: str, additional_instructions: str) -> dict:
    page_data = load_url_content(url)
    res = extract_product_details(page_data)
    listing = parse_listing(res)
    
    # Await the async generate_ad function to get its actual result
    ad_response = generate_ad(listing, additional_instructions=additional_instructions)
    
    # Now, ad_response should be a proper JSON string, not a coroutine
    ad = Ad.from_llm_response(response=ad_response)
    
    return {
        "ad_text": ad.ad_text,
        "image": ad.image_prompt,
        "video": ad.video_prompt
    }

@app.post("/generate_ad", response_model=AdResponse)
async def generate_ad_endpoint(ad_request: AdRequest):
    result = await generate_ad_response(ad_request.url, ad_request.additional_instructions)
    if result is None:
        raise HTTPException(status_code=400, detail="Unable to generate ad for the provided URL")
    return result



@app.post("/generate_image")
async def generate_image_endpoint(request: ImageRequest):
    prompt = request.prompt
    try:
        image_bytes = generate_image(prompt)
        if not image_bytes:
            raise HTTPException(status_code=500, detail="Image generation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    image_stream = io.BytesIO(image_bytes)
    return StreamingResponse(image_stream, media_type="image/png")