import wikipedia

def wiki_search(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print("No wikipedia results")
        return "No results recieved"
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary 