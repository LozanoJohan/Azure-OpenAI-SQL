from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

openai = OpenAI(
  organization= 'org-7HxWJNIFnAfbR4mtTC45X11P',
  api_key= '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'
)

def get_completion_from_messages(system_message, user_message, model="gpt-3.5-turbo", temperature=0, max_tokens=500) -> str:

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{user_message}"}
    ]
    
    completion = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    system_message = "You are a helpful assistant"
    user_message = "Hello, how are you?"
    print(get_completion_from_messages(system_message, user_message))