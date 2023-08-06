
import requests

__all__ = ["qoute"]

def qoute(limit=None,topic=None):
    url = "https://jovytestingcdn.3525nikolas.repl.co/qoutes?"
    url= url+f"topic={topic}&" if topic != None else url
    url = url+ f"limit={limit}" if limit != None else url

    data = requests.get(url).json()
    
    return data


    