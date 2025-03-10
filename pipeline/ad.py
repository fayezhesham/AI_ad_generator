import json

class Ad:
    def __init__(self, ad_text: str, image_prompt: str, video_prompt: str):
        self.ad_text = ad_text
        self.image_prompt = image_prompt
        self.video_prompt = video_prompt

    @classmethod
    def from_llm_response(cls, response: str) -> 'Ad':
        """
        Parses a JSON string from an LLM response and returns an Ad instance.
        The JSON should contain the keys:
            - "ad text" for the advertisement text
            - "image" for the image prompt/description
            - "video" for the video description
        """
        response_data = json.loads(response)

        ad_text = response_data.get("ad text")
        image_prompt = response_data.get("image")
        video_prompt = response_data.get('video')

        return cls(ad_text, image_prompt, video_prompt)

    def __str__(self):
        return f"Ad(ad_text={self.ad_text}, ad_image={self.image_prompt}, ad_video={self.video_prompt})"