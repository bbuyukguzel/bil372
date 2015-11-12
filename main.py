import urllib
import requests


def get_source_code(url):
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            headers = {'User-Agent': user_agent, }
            request = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(request)
            return response.read()
        except requests.exceptions.RequestException as e:
            print(e)



def url_list():
    content = [line.rstrip('\n') for line in open('./URL')]
    return content
