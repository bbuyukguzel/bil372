import urllib, urllib.request
import requests, requests.exceptions
import re
import random
import codecs


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
        return codecs.decode(code, 'utf-8', 'ignore')
    except requests.exceptions.RequestException as e:
        print(e)


def find_phone(source):
    # pattern1 = b'(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'
    pattern2 = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
    print(re.findall(pattern2, source))


def find_name(code):
    char, i = "", 0
    pattern = '(<title>|<TITLE>)(.*)(<\/title>|<\/TITLE>)'
    res = re.findall(pattern, code)
    print(res)
    title = str(res[0][1])  # between title tags

    # Remove texts after the name
    for char in title:
        if (char in {'|', '\'', ',', ':', '-'}):
            break
        i += 1
    if (i == len(title)):
        name = title
    else:
        name = title[:title.index(char)]

    return name


# returns random n lines in URL list file
def test(n=5, sample=True):
    with open('URL.txt') as file:
        content = [line.rstrip('\n') for line in file]
    file.close()
    if sample:
        return random.sample(content, n)
    else:
        return content


def main(url):
    print('-' * 20)
    print(url)
    source = get_source_code(url)

    # parse functions add here
    # find_bla(source) etc.
    find_phone(source)
    
def check_link(source, string):
    soup = BeautifulSoup(source)
    for href_ in soup.find_all('a'):
        reg = re.search('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', str(href_))
        if reg:
            # print(reg.group(0), "---->", reg.group(0).find(str('teach')))
            if reg.group(0).lower().find(str(string)) == 0:
                return reg.group(0)
    return False

#It finds links, if main cant parse
def check_link(source, string):
    soup = BeautifulSoup(source)
    for href_ in soup.find_all('a'):
        reg = re.search('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?', str(href_))
        if reg:
            # print(reg.group(0), "---->", reg.group(0).find(str('teach')))
            if reg.group(0).lower().find(str(string)) == 0:
                return reg.group(0)
    return False


# test function for find_number(source)
def get_names():
    for url in test():
        isTrueURLPattern = "^(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$"
        if re.search(isTrueURLPattern, str(url)):
            src = get_source_code(url)
            print(url + "-->" + find_name(src))

if __name__ == '__main__':
    # print(list(map(main, test(5))))
    get_names()
