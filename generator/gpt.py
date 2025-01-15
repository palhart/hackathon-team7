import requests
import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from preprocess import encode_image
from preprocess import get_images_path



load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
print(api_key)

class GPT:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    
    def create_prompt_using_images(self, deck_images, fields: list):
        content = [{"type": "text", "text": f"Extract the following info (set to None if you can't deduce the answer): {', '.join(fields)}"}]
        for deck_image in deck_images:
            content.append({
                "type": "image_url", 
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encode_image(deck_image)}" 
                }
            })
        
        content += "\n\nPlease respond only with a valid JSON object containing the requested fields."
        
        return content
    
    def completion_request(self, deck_images, fields, max_tokens=1500):
        prompt = self.create_prompt_using_images(deck_images, fields)


        payload = {
            "model": "gpt-4o",  # "gpt-4o" if it's an optimized version available in your environment
            "messages": [
                {"role": "system", "content": "You are a data extraction assistant."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,  # Adjust based on the output size
            "temperature": 0.7,  # Balances creativity and determinism
            "top_p": 1,  # Ensures diverse output while staying within logical boundaries
            "frequency_penalty": 0,  # Avoid penalizing repeated terms
            "presence_penalty": 0,  # Neutral stance on introducing new topics
            "response_format": {"type": "json_object"}
        }

        completion = self.client.chat.completions.create(**payload)
        
        return completion
    

    def extract_data(self, deck_images, fields):
        completion = self.completion_request(deck_images, fields)


        json_response = completion.choices[0].message.content
        return json_response



if __name__ == '__main__':
    gpt = GPT(api_key=api_key)
    deck_images = get_images_path('/data/images') 
    fields = ['Headcount_Count', 'Headcount_Growth', 'Headcount_Breakdown_of_employees', 'Fundraising_Total_amount', 'Fundraising_Date_of_last_round', 'Financials_GMV' , 'Financials_Net_Sales' , 'Financials_CAC', 'Fundraising_Total_amount' , 'Fundraising_Date_of_last_round']
    data = gpt.extract_data(deck_images, fields)
    print(data)
    


    