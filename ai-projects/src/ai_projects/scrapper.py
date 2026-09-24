from bs4 import BeautifulSoup
import requests

# standard header to import a request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_content(url):
    """
    Return the title and content of the website at the given url.
    Truncate to 2000 characters as asensible limit.
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelavant in soup.body(["scripts", "style", "img", "input"]):
            irrelavant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2000]


def fetch_website_links(url):
    """
    Return links at the website of the given url.
    """
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]
