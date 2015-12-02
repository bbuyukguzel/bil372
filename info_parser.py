import re
import json
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url="", source=""):
        self.URL = url
        self.source = source

    def find_phone(self):
        pattern = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        # print(re.findall(pattern, self.source))
        return re.findall(pattern, self.source)

    def find_name(self):
        try:
            char, i = "", 0
            pattern = '(<title>\s*|<TITLE>\s*)(.*)(\s*<\/title>|\s*<\/TITLE>)'
            res = re.findall(pattern, self.source)
            title = str(res[0][1])
            for char in title:
                if (char in {'|', '\'', ',', ':', '-'}):
                    break
                i += 1
            if (i == len(title)):
                name = title
            else:
                name = title[:title.index(char)]
        except:
            return False
        name = name.replace('Home', '')
        name = name.replace('Page', '')
        name = name.replace('Web', '')
        name = name.replace('Main', '')
        name = name.strip()
        try:
            return (name[0:name.rindex(' ')], name[name.rindex(' ') + 1:])
        except:
            return False

    def find_rank(self):
        ranks = ['adjunct professor', 'assistant professor', 'associate Professor', 'professor', 'lecturer',
                 'senior lecturer', 'associate professor', 'research assistant', 'research associate',
                 'research professor', 'research fellow', 'research instructor', 'instructor', 'research assistant professor',
                 'research associate professor', 'postdoctoral researcher', 'agregation', 'docent', 'habilitation',
                 'privatdozent', 'teaching assistant', 'teaching associate', 'visiting professor', 'teaching professor'
                 'visiting research professor']

        rank_dic = {}
        for i in ranks:
            if i in self.source.lower():
                rank_dic[i] = self.source.lower().index(i)
        print(min(rank_dic, key=rank_dic.get))

    def find_uniname(self):

        pattern = "((http|https)://(www|[a-z\-]*)\.)([a-z\.]*(?=\/))"
        reg = re.findall(pattern, self.URL)
        uni_url = reg[0][3]

        with open("uni.json") as f:
            unis = json.load(f)
            for k in unis:
                if uni_url.endswith(k):
                    return unis[k].strip()

    def find_email(self):
        pattern1 = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c' \
                   r'\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]' \
                   r'*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)' \
                   r'{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f' \
                   r'\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
        pattern2 = r'^((<[^>]*>)*[mailto:(\sa-zA-Z0-9_.+-])+(@|(\s?(\{|\(|\[)\s?(at|AT)\s?(\}|\)|\])\s?)' \
                   r'|(\s(at|AT|@)\s))[a-zA-Z0-9-]+(\.|dot|\s)[a-zA-Z0-9-.]+'

        res1 = re.findall(pattern1, self.source, re.IGNORECASE)
        if(len(res1) == 0):
            result = re.findall(pattern2, self.source, re.IGNORECASE)
            return result
        else:
            return res1

    def find_publicationxxx(self):
        publications = []
        source = ''
        print("Bananas," in self.source)

        soup_out = BeautifulSoup(self.source, "lxml")
        keys = ['publications', 'publication', 'Publications:', 'Publications', 'Publication']
        tags = soup_out.findAll(['strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        for t_out in tags:
            for i in keys:
                if i in t_out.text:
                    source += str(t_out.parent)
                    print("*** i: " + str(i))

        soup_in = BeautifulSoup(source, "lxml")

        for t_in in soup_in.findAll('p'):
            t_in = re.sub('<[^>]*>|\[.*\]|\s{2,}', '', str(t_in))
            publications.append(t_in)

        for i in publications:
            print(i)

    def find_publication(self):
        PUB_LIMIT = 3
        print("Hello world****************")
        soup = BeautifulSoup(self.source)
        re_year = r'(19[0-9]{2})|(20(0|1)[0-9])'

        # Remove before "publication"
        source = self.__remove_before_pub(soup)

        soup2 = BeautifulSoup(source)
        if(len(soup2.select("li p")) > PUB_LIMIT):
            for lip in soup2.select("li p"):
                text = lip.get_text()
                self.__helper_pub(re_year, text, lip)

        elif(len(soup2.select("div p")) > PUB_LIMIT):
            for divp in soup2.select("div p"):
                text = divp.get_text()
                self.__helper_pub(re_year, text, divp.parent)

        elif(len(soup2.select("li span")) > PUB_LIMIT):
            for lispan in soup2.select("li span"):
                text = lispan.get_text()
                self.__helper_pub(re_year, text, lispan)

        if(len(soup2.select("div span")) > PUB_LIMIT):
            for divspan in soup2.select("div span"):
                text = divspan.get_text()
                self.__helper_pub(re_year, text, divspan)

        if(len(soup2.select("p")) > PUB_LIMIT):
            for p in soup2.select("p"):
                text = p.get_text()
                self.__helper_pub(re_year, text, p)

        if(len(soup2.select("li")) > PUB_LIMIT):
            for li in soup2.select("li"):
                text = li.get_text()
                self.__helper_pub(re_year, text, li)

    def __remove_before_pub(self, soup):
        keys = ['publications', 'publication', 'Publications:', 'Publications', 'Publication']
        tags = soup.findAll(['strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        for t_out in tags:
            for i in keys:
                if i in t_out.text:
                    source = self.source[self.source.index(str(t_out)):]
                    return source

    def __helper_pub(self, re_year, text, src):
        PUB_DESC_LIMIT = 50
        if (re.findall(re_year, text) and len(text) > PUB_DESC_LIMIT):
            print(self.__check_link_in_pub(src))
            print(text.strip())
            print("************")

    def __check_link_in_pub(self, src):
        hrefs = list()

        for i in src.find_all("a"):
            if("href" in i.attrs):
                if(i["href"] == "#"):
                    continue

                if("http" not in i["href"]):
                    from urllib.parse import urljoin
                    hrefs.append(urljoin(self.URL, i["href"]))
                else:
                    hrefs.append(i["href"])
        return hrefs

    def parse_publication(self, text):
        information = {}
        page_pattern = r'(\(?(pp|Pp).)(\s)?(\d+(\s?-\s?)\d+\)?)|(\d+(pp|Pp).)'
        date_pattern = r'\(?(((19[0-9]{2})|(20(0|1)[0-9])),?\s?)((January|February|March|April|May|June|July|August|' \
                       r'September|October|November|December)|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\.?)' \
                       r'?\s?([1-9]|[12]\d|3[01])?\)?|\(?((0[1-9]|[12]\d|3[01])?\s?((January|February|March|April|May' \
                       r'|June|July|August|September|October|November|December)|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|' \
                       r'Oct|Nov|Dec)\.?)\,?\s?((19[0-9]{2})|(20(0|1)[0-9]))\)?) '

        information['page'] = re.findall(page_pattern, self.source)
        information['date'] = re.findall(date_pattern, self.source)
        return information
