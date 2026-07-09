import os
from dotenv import load_dotenv
load_dotenv()
from tavily import TavilyClient

Tavily_Client= TavilyClient(os.getenv("TAVILY_API_KEY"))

def tavily_search(query):

    response=Tavily_Client.search(
        query=query,
        max_results=5
    )

    results=[]


    for i,r in enumerate(response["results"],1):
        title=r.get("Title","Unknown"),
        url=r.get("URL",""),
        snippiet=r.get("Content","").strip   #Strip is used to remove extra space from content
    

        if len(snippiet)>3000:
            snippiet=snippiet[:300].rsplit("",1)[0]+"..."

        results.append(f"{i}.**{title}**\n {url}\n{snippiet}")

    return"\n\n".join(results)