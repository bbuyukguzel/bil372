import urllib
import requests
import re
import random


# TODO List
# get_source_code da s_index i kontrol et


def get_source_code(url):
        try:
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            headers = {'User-Agent': user_agent, }
            request = urllib.request.Request(url, None, headers)
            response = urllib.request.urlopen(request)
            code = response.read()

            # don't care between style tags
            while(code.find(b'<style>')!= -1):
                s_index = code.find(b'<style>')
                e_index = code.find(b'</style>', s_index)
                code = code[:s_index]+code[e_index+(len('</style>')):]
            # don't care between script tags
            while(code.find(b'<script') != -1):
                s_index = code.find(b'<script')
                e_index = code.find(b'</script>', s_index)
                code = code[:s_index]+code[e_index+(len('</script>')):]
            return code
        except requests.exceptions.RequestException as e:
            print(e)


def find_phone(source):
    pattern1 = b'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'
    pattern2 = b'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    print(re.findall(pattern2, source))


# returns random n lines in URL list file
def test(n):
    with open("URL.txt") as file:
        content = [line.rstrip('\n') for line in file]
    file.close()
    return random.sample(content, n)


def main(url):
    source = get_source_code(url)

    # parse functions add here
    # find_bla(source) etc.
    find_phone(source)

    print(url)
    print('-'*20)


print(list(map(main, test(5))))