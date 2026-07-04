from dotenv import load_dotenv
load_dotenv()
import os
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient

tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY"))

@tool 
def web_search(query:str):
    """Search the web for recent and reliable information on a topic. Returns a Title and urls and snippets   """
    
    tavily_response = tavily.search(query=query,num_results=3)
    
    results = []
    
    for result in tavily_response["results"]:
        results.append(f"Title: result['title']\n URL: result['url']\n Snippet: result['content']\n")
        
    return "\n".join(results)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"