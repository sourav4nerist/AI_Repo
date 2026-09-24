import os
from openai import OpenAI
from dotenv import load_dotenv
from scrapper import fetch_website_content

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")
base_url = os.environ.get("OPENROUTER_BASE_URL")
model = os.environ.get("OPENROUTER_MODEL")

client = OpenAI(base_url=base_url, api_key=api_key)

system_prompt = """
You are helpful assistant that analyzes content of a website, 
and provides a short summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here is the url of the website. Provide the short summary of the website.
If it includes news and announcements, summarize that too.

"""


# Function to generate message for LLM api call
def message_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website},
    ]


# Call LLM API endpoint to generate summary of website content
def summarize(url):
    website = fetch_website_content(url=url)
    response = client.chat.completions.create(
        model=model, messages=message_for(website)
    )
    return response.choices[0].message.content


# A function to display output nicely using markdown
def display_summary(url):
    summary = summarize(url)
    print(summary)


display_summary("https://edwarddonner.com")
