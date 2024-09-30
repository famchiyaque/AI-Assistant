import wolframalpha
from config import WOLFRAM_API_KEY

wolframClient = wolframalpha.Client(WOLFRAM_API_KEY)

def list_or_dict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']

def search_wolframalpha(query = ''):
    response = wolframClient.query(query)

    # @success: Wolfram was able to resolve the query
    # @numpods: Number of results returned
    # pod: list of results. Can also contain subpods
     
    if response['@success'] == 'false':
        return "Could not compute"
    
    # query resolved
    else:
        result = ' '
        # Question
        pod0 = response['pod'][0]

        pod1 = response['pod'][1]
        # may contain the answer, pod with highest confidence value
        # if it's primary or has the title of result or definition, then it's the official result
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = list_or_dict(pod1['subpod'])
            # remove bracketed section
            return result.split('(')[0]
        else:
            question = list_or_dict(pod0['subpod'])
            return question.split('(')[0]
            # search wikipedia instead
        # else:
        #     speak('Computation failed, querying universal databank')
        #     return wiki_search(question)