import openai
import re
import time
from utils import load_config


def classify_content(content, config_file='./config/config.json'):
    """
    Classify the given content using OpenAI's GPT-3.5 API with rate limit handling.
    """
    try:
        openai_api_key, baidu_api_key, baidu_api_secret = load_config(config_file)
        if not openai_api_key:
            print("API key not found. Please check the configuration file.")
            return None

        openai.api_key = openai_api_key

        prompt = f"You are a file organizing assistant. Based on this content, suggest a concise, valid folder name. this is content: '{content}'. Please format the response like {{folder_name}}, which means that your response should be enclosed within single braces"
        for attempt in range(3):  # Retry up to 3 times
            try:
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": prompt}
                    ]
                )
                responseText = completion.choices[0].message['content']
                print(f"Response from OpenAI: {responseText}")
                break  # Break the loop if successful
            except openai.error.RateLimitError:
                if attempt < 2:  # Wait only if more attempts are left
                    time.sleep(20)  # Wait for 20 seconds before retrying
                else:
                    raise  # Raise the exception if out of attempts

        match = re.search(r'\{(.+?)\}', responseText)
        if match:
            folder_name = match.group(1).strip()
            # Further sanitize and shorten the folder name if necessary
            folder_name = re.sub(r'[^\w\s-]', '', folder_name)
            # folder_name = folder_name[:15].rstrip()
            return folder_name
        

    except Exception as e:
        print(f"Error in calling OpenAI API: {e}")
        return None
