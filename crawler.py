import urllib.request
import requests.exceptions
from info_parser import Parser
from bs4 import BeautifulSoup
import codecs
import queue


class Crawler:

    def __init__(self, URL):
        self.URL = URL
        self.__URLQueue = queue.Queue()
        self.__p = None
        self.__keywords = {"contact", "research", "biography", "publication", "class"}
        self.__fields = {"name": "", "uni": "", "tel": "", "email": "", "publication": "", "rank":"", "dept":""}

    @staticmethod
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

    def get_links(self, source, url):
        from urllib.parse import urlparse, urljoin
        soup = BeautifulSoup(source, "lxml")
        wholeLinks = set([i["href"] for i in soup.find_all('a', href=True)])
        for link in wholeLinks:
            if any(j in link for j in self.__keywords):
                if(link.startswith("http")):
                    if(urlparse(link).netloc == urlparse(url).netloc):
                        self.__put_link(link)
                else:
                    combinedLink = urljoin(url, link)
                    self.__put_link(combinedLink)

    # put the links existed in home page into URLQueue
    def __put_link(self, url):
        self.__URLQueue.put(url)

    # Get a link from URLQueue and apply parser functions on it
    def traverse(self):
        while not self.__URLQueue.empty():
            URL = self.__URLQueue.get()

            self.__p = Parser(source=self.get_source_code(URL), url=URL)
            try:
                """
                if(self.__fields["name"] != None and len(self.__fields["name"]) == 0):
                    self.__fields["name"] = self.__p.find_name()

                if(self.__fields["uni"] != None and len(self.__fields["uni"]) == 0):
                    self.__fields["uni"] = self.__p.find_uniname()

                if(self.__fields["tel"] != None and len(self.__fields["tel"]) == 0):
                    self.__fields["tel"] = self.__p.find_phone()

                if(self.__fields["email"] != None and len(self.__fields["email"]) == 0):
                    self.__fields["email"] = self.__p.find_email()
                    print(self.__fields["email"])


                if("publica" in URL.lower() or
                        "research" in URL.lower() or
                        "article" in URL.lower() or
                        URL.lower() == self.URL.lower()):

                    if(self.__fields["publication"] != None and len(self.__fields["publication"]) == 0):
                        self.__p.find_publication()
                    break
                    """
                #if(self.__fields['rank'] != None and len(self.__fields['rank']) == 0):
                #    self.__fields['rank'] = self.__p.find_rank()
                if(self.__fields['dept'] != None and len(self.__fields['dept']) == 0):
                    self.__fields['dept'] = self.__p.find_dept()
            except Exception as e:
                continue

    def run(self):
        self.__URLQueue.put(self.URL)
        self.get_links(self.get_source_code(self.URL), self.URL)
        # print(self.__URLQueue.queue)
        self.traverse()


