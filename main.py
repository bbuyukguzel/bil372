import urllib
import urllib.request
import requests
import requests.exceptions
import re
import random
import codecs
from bs4 import BeautifulSoup
from info_parser import Parser


def get_source_code(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        headers = {'User-Agent': user_agent, }
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        code = response.read()

        # don't care between style tags
        while code.find(b'<style>') != -1:
            s_index = code.find(b'<style>')
            e_index = code.find(b'</style>', s_index)
            code = code[:s_index] + code[e_index + (len('</style>')):]
        # don't care between script tags
        while code.find(b'<script') != -1:
            s_index = code.find(b'<script')
            e_index = code.find(b'</script>', s_index)
            code = code[:s_index] + code[e_index + (len('</script>')):]
        return codecs.decode(code, 'utf-8', 'ignore')
    except requests.exceptions.RequestException as e:
        print(e)


# returns random n lines in URL list file
def test(n=5, sample=True):
    with open('URL.txt') as file:
        content = [line.rstrip('\n') for line in file]
    file.close()
    if sample:
        return random.sample(content, n)
    else:
        return content


# It finds links, if main cant parse
def check_link(source, string):
    soup = BeautifulSoup(source)
    for href_ in soup.find_all('a', href=True):
        reg = re.search('(([a-zA-Z0-9])|(\/[a-z]+)|([a-zA-z0-9]*\/)|(https?:\/\/))((\/[a-zA-Z0-9]*)|(([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?))',
                        str(href_))
        if reg:
            if string in reg.group(0):
                return reg.group(0)
    return False


if __name__ == '__main__':

    for url in test(20):
        p = Parser(url, get_source_code(url))
        p.find_email()
