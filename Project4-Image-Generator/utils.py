import requests
import io
from PIL import Image 
from urllib.parse import quote
import time 

def generate_with_pollinations(prompt:str,width:int=1024,height:int=1024,model:str="flux"):
    """generate image with pollination api, totally free and return image"""
    encoded_prompt=quote(prompt)
    url=f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model={model}&nologo=true&seed={int(time.time())}"
    response=requests.get(url,timeout=60)
    response.raise_for_status()
    image=Image.open(io.BytesIO(response.content)).convert("RGB")
    return image,url

def generate_with_huggingface(
    prompt:str,
    token:str="",
    model:str="black-forest-labs/FLUX.1-schnell",
    width:int=512,
    height:int=512,
    negative_prompt:str="",
):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {token}"}
    
    payload={
        "inputs": prompt,
        "parameters": {
            "width": width,
            "height": height,
            "num_inference_steps":4 if "schnell" in model else 20,
        }
    }
    
    if negative_prompt:
        payload["parameters"]["negative_prompt"]=negative_prompt
        
    for attempt in range(3):
        response=requests.post(api_url,headers=headers,json=payload,timeout=120)
        
        if response.status_code==200:
            image=Image.open(io.BytesIO(response.content)).convert("RGB")
            return image, None
        
        elif response.status_code==503:
            wait=response.json().get("estimated_time",20)
            time.sleep(min(wait,60))
            
        elif response.status_code==401:
            raise Exception("Invalid token of hugging face")

        else:
            error_msg=response.json().get("error",response.text)
            raise Exception(error_msg)

    raise Exception("Failed to generate image")

def save_image(image:Image.Image,filename:str)->str:
    path=f"/tmp/{filename}"
    image.save(path,format="PNG")
    return path