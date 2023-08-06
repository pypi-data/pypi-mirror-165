
import requests

__all__ = ["qoute"]

def qoute(limit=None,tags=None):
    url = "https://jovytestingcdn.3525nikolas.repl.co/qoutes?"
    url= url+f"tags={tags}&" if tags != None else url
    url = url+ f"limit={limit}" if limit != None else url

    #print(url)
    data = requests.get(url).json()
    #print(data)
    
    return data


qoute(1,"love")