import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import Markdown, display, update_display
from ai_projects.scrapper import fetch_website_content, fetch_website_links

load_dotenv()

# mode to run, can be one of these
# ollama - for local llm
# openrouter - for frontier models through openrouter

# run_mode = "openrouter"
run_mode = "ollama"

api_key = os.environ.get("OPENROUTER_API_KEY") if run_mode == "openrouter" else "dummy"
base_url = (
    os.environ.get("OPENROUTER_BASE_URL")
    if run_mode == "openrouter"
    else "http://localhost:11434/v1"
)
model = os.environ.get("OPENROUTER_MODEL") if run_mode == "openrouter" else "llama3.2"

client = OpenAI(base_url=base_url, api_key=api_key)

link_system_prompt = """
You are provided with list of urls from a website.
You are able to decide which of the provided provided urls are relevant to generate a brochure about the company,
such as links to an About page, Company information page or Careers/Jobs page.
You should respond in json format as below example:

{
    "links":[
    {"type":"about page","url":"https://company.com/info/about"},
    {"type":"career page","url":"https://another.company.com/careers"}
    ]
}
"""


def get_links_user_prompt(url):
    user_prompt = f"""
    Here is the list of links from a website : {url}.
    Please decide which urls are relevant to generate a brochure for the company,
    respond with the full urls in form of json.
    Please do not include Terms of services, privacy.

    Links(some might be relative links)

    """
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt


def select_relevant_links(url):
    print(f"Selecting relevant links from url {url} using model {model}")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(url)},
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    links = json.loads(result)
    print(f"Found {len(links['links'])} relevant links")
    return links


def fetch_content_with_relevant_links(url):
    content = fetch_website_content(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page: \n\n {content}\n## Relevant Links:\n"
    for link in relevant_links["links"]:
        result += f"\n\n## Link: {link['type']}\n"
        result += fetch_website_content(link["url"])
    return result


## Step 2: Generate Brochure using above generated data

brochure_system_prompt = """
You are an assistant that analyzes contents of the given company website and it's relative urls,
and creates a short brochure about the comapany for prospective customers, investors and recruits.
Respond in markdown with no code block.
Include details of company culture, customers and career/jobs if you have that informations.
"""


def get_brochure_user_prompt(company, url):
    user_prompt = f"""
    You are looking at webpage of company: {company}.
    Here are the contents of it's landing page and other relavant urls.
    Generate a short brochure of the company using the provided information in markdown withpout code blocks.\n\n
    """
    user_prompt += fetch_content_with_relevant_links(url)
    user_prompt = user_prompt[:5000]
    return user_prompt


def create_brochure(company, url):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": brochure_system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company, url)},
        ],
    )
    result = response.choices[0].message.content
    display(Markdown(result))  ## for interactive window
    # print(Markdown(result))


create_brochure("HuggingFace", "https://huggingface.co")
