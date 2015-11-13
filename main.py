# !/usr/bin/python
import re
import urllib

import requests
from bs4 import BeautifulSoup


def check_link(source, string):
    soup = BeautifulSoup(source)
    for href_ in soup.find_all('a'):
        reg = re.search('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', str(href_))
        if reg:
            # print(reg.group(0), "---->", reg.group(0).find(str('teach')))
            if reg.group(0).lower().find(str(string)) == 0:
                return reg.group(0)
    return False


def get_source_code(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
        headers = {'User-Agent': user_agent, }
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        code = response.read()

        # don't care between style tags
        while (code.find(b'<style>') != -1):
            s_index = code.find(b'<style>')
            e_index = code.find(b'</style>', s_index)
            code = code[:s_index] + code[e_index + (len('</style>')):]
        # don't care between script tags
        while (code.find(b'<script') != -1):
            s_index = code.find(b'<script')
            e_index = code.find(b'</script>', s_index)
            code = code[:s_index] + code[e_index + (len('</script>')):]
        return code
    except requests.exceptions.RequestException as e:
        print(e)


def find_phone(code):
    pattern2 = b'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    print(re.findall(pattern2, code))


def url_list():
    content = [line.rstrip('\n') for line in open('./URL.txt')]
    return content


def url_parser():
    for link in url_list():
        print(check_link(get_source_code(link), "research"))


url_parser()
