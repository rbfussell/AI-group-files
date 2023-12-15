import requests
import json
import re
from utils import load_config,get_baiduqianfan_access_token
from prompts import CLASSIFICATION_PROMPT

def classify_content(content, config_file='config\config.json'):
    """
    Classify the given content using the ChatGLM2_6B_32K model with a structured response format.
    """
    access_token = get_baiduqianfan_access_token()

    prompt = CLASSIFICATION_PROMPT.format(content)
    try:
        response = send_request(prompt, access_token)
        responseText = parse_response(response)
        print(f"Response from Llama-7B-chat: {responseText}")
        # Use regex to extract content within {{folder_name}}
        match = re.search(r'\{(.+?)\}', responseText)
        if match:
            folder_name = match.group(1).strip()
            # Further sanitize and shorten the folder name if necessary
            folder_name = re.sub(r'[^\w\s-]', '', folder_name)
            # folder_name = folder_name[:15].rstrip()
            return folder_name
        else:
            print("No valid folder name format found in the response.")
            return None

    except Exception as e:
        print(f"Error in calling ChatGLM2_6B_32K API: {e}")
        return None

def send_request(content, access_token):
    """
    Send a request to the ChatGLM2_6B_32K model with the provided content.
    """
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_2_7b?access_token={access_token}"
    payload = json.dumps({
        "messages": [
            {"role": "user", "content": content}
        ]
    })
    headers = {'Content-Type': 'application/json'}
    return requests.request("POST", url, headers=headers, data=payload)

def parse_response(response):
    """
    Parse the response from the ChatGLM2_6B_32K model.
    """
    if response.status_code != 200:
        print(f"API request failed with status code: {response.status_code}")
        return None
    
    response_data = response.json()
    # Extract and return the relevant part of the response
    # Modify the below line based on the actual response structure
    return response_data.get("result", {})

if __name__ == '__main__':
    test_content = "Your test content here"
    result = classify_content(test_content)
    print(f"Classification result: {result}")
