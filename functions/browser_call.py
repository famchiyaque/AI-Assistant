import webbrowser

platforms = ['youtube', 'netflix', 'football', 'prime']
urls = ['https://www.youtube.com/', 'https://www.netflix.com/browse', 'https://www.dazn.com/es-MX/home', 'https://www.amazon.com/Amazon-Video/b/?&node=2858778011&redirectToCMP=1']

def open_platform(platform):
    print("inside open platform function")
    print(platform)
    if platform in platforms:
        print("platform was found")
        urlIndex = platforms.index(platform)
        print("resulting urlIndex: ", urlIndex)
        webbrowser.get('edge').open_new(urls[urlIndex])
        return ''
    else:
        return "didn't find valid platform to open"



def look_up(query):
    platform = ''
    detail = ''
    for word in query:
        if word in platforms:
            platform = platforms[query.index(word)]
            break
    if platform != '':
        urlIndex = platforms.index(platform)
        finalUrl = urls[urlIndex]
        if platform == 'youtube':
            for i in range(len(query)):
                if query[i] == 'open':
                    detail = query[i + 1]
                    break
            finalUrl += detail
        webbrowser.get('edge').open_new_tab(finalUrl)
        return ''
    else:
        return "didn't find valid platform to open"
    