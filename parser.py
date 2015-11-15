import re


class Parser:
    def __init__(self, source):
        self.source = source
        self.find_phone()
        self.find_name()

    def find_phone(self):
        pattern2 = '(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
        print(re.findall(pattern2, self.source))

    def find_name(self):
        char, i = "", 0
        pattern = '(<title>|<TITLE>)(.*)(<\/title>|<\/TITLE>)'
        res = re.findall(pattern, self.source)
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
