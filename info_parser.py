import re
import json


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
        pattern = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
        # url fonksiyonu eklendiginde contact ve turevi sayfalarda da arama yap
        # mailto ile başlayabilir
        # print(re.findall(pattern, self.source))
        return re.findall(pattern, self.source)
