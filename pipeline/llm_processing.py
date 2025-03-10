from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()



llm = ChatGroq(
        temperature=0, 
        groq_api_key=os.getenv("GROQ_API_KEY"), 
        model_name="llama-3.3-70b-versatile"
    )

def extract_product_details(page_data):
    prompt_extract = PromptTemplate.from_template(
            """
            ### Scraped Website Content:
            {page_data}

            ### Instructions:
            You are provided with raw scraped text from an ecommerce website. Your task is to extract all relevant product details and output them as a valid JSON object. The JSON object must include the following keys:

            - "Product": The name of the product.
            - "Brand": The brand of the product.
            - "Product Variations": A list of any product variations (if applicable).
            - "Store Name": The name of the ecommerce store.
            - "Description": A detailed description of the product.
            - "Product Images Links": A list of URLs for the product images found on the page.
            - "Price With Currency": The product price along with its currency.
            - "Discount": Any discount information available.
            - "Product Features": Key features of the product.
            - "Product Categories": The categories under which the product falls.
            - "Ratings And Reviews": Aggregated ratings and review details.
            - "Unique Selling Points": Special attributes that set the product apart.

            Return only the JSON object with the specified keys, with no additional commentary or preamble.

            """
    )

    chain_extract = prompt_extract | llm 
    res = chain_extract.invoke(input={'page_data':page_data})
    return res



def generate_ad(listing, additional_instructions = ""):
    if additional_instructions != "":
        additional_instructions = "- Incorporate the following additional instructions as needed: " + additional_instructions
    prompt_ad = PromptTemplate.from_template(
            """
            ### Product listing details:
            {Product_listing}
            
            ### INSTRUCTION:
            You are an experienced ecommerce copywriter. Your task is to craft a compelling ad copy for the product described above. The ad copy will be used for social media platforms (Facebook, Instagram, Twitter, Google Ads, etc.), so it must be engaging and persuasive.

            Requirements:
            - Highlight any product variations and unique selling points.
            - Emphasize discounts or special offers if available; if none are present, omit discount references.
            - Include a clear, strong call-to-action.
            {additional_prompt}.
            - Additionally, suggest an ad creative approach by describing either an image or a video concept to visually support the ad.
            also as a copywriter, provide a suggestion for the ad creative that will be used whether an image or a video and describe the content of the ad creative.
            Do not provide a preamble.

            ### Output:
            Return your response as a JSON object with exactly three keys:
            - "ad text": The crafted ad copy.
            - "image": Your suggestion for the image creative.
            - "video": Your suggestion for the video creative.
            ### Ensure that you give me the response as a raw json dict format without introduction or commentary (NO PREAMBLE):
            
            """
            )

    chain_ad = prompt_ad | llm
    res = chain_ad.invoke({"Product_listing": str(listing), "additional_prompt": str(additional_instructions)})
    response = res.content
    return response