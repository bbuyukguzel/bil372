import re
import json
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, URL="", source=""):
        self.URL = URL
        self.source = source

    def find_phone(self):
        pattern = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        # print(re.findall(pattern, self.source))
        return re.findall(pattern, self.source)

    def find_name(self):

        char, i = "", 0
        pattern = '(<title>\s*|<TITLE>\s*)(.*)(\s*<\/title>|\s*<\/TITLE>)'
        res = re.findall(pattern, self.source)
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

        return name.strip()

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
        pattern1 = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
        pattern2 = r'(^([mailto:(\s)?a-zA-Z0-9_.+-])+(@|(\s?(\{|\(|\[)\s?(at|AT)\s?(\}|\)|\])\s?)|(\s(at|AT|@)\s))[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'


        res1 = re.findall(pattern1, self.source)
        if(len(res1) == 0):
            return re.findall(pattern2, self.source)
        else:
            return res1

        # mailto ile başlayabilir


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
                    print("*** i: " + str(i) )


        soup_in = BeautifulSoup(source, "lxml")

        for t_in in soup_in.findAll('p'):
            t_in = re.sub('<[^>]*>|\[.*\]|\s{2,}', '', str(t_in))
            publications.append(t_in)

        for i in publications:
            print(i)


    def find_publication(self):
        print("Hello world****************")
        soup = BeautifulSoup(self.source)
        source = ""
        re_year = r'(19[0-9]{2})|(20(0|1)[0-9])'

        # Remove before "publication"
        keys = ['publications', 'publication', 'Publications:', 'Publications', 'Publication']
        tags = soup.findAll(['strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        for t_out in tags:
            for i in keys:
               if i in t_out:
                   source = self.source[self.source.index(i):]
        # end remove



        soup2 = BeautifulSoup(source)

        if(soup.select("li p")):
           for lip in soup.select("li p"):
               text = lip.get_text()
               if(re.findall(re_year, text) and len(text)>4):
                    print(text.strip())
                    print("************")


        if(soup.select("div p")):
            for divp in soup.select("div p"):
                text = divp.get_text()
                if(re.findall(re_year, text) and len(text)>50):
                    print(text.strip())
                    print("************")


        if(soup.select("li span")):
            for lispan in soup.select("li span"):
                text = lispan.get_text()
                if(re.findall(re_year, text) and len(text)>50):
                    print(text.strip())
                    print("************")


        if(soup.select("div span")):
            for divspan in soup.select("div span"):
                text = divspan.get_text()
                if(re.findall(re_year, text) and len(text)>50):
                    print(text.strip())
                    print("************")

        if(soup.select("li")):
           for li in soup.select("li"):
                text = li.get_text()
                if(re.findall(re_year, text) and len(text)>50):
                    print(text.strip())
                    print("************")
