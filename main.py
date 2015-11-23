import random
from crawler import Crawler


# returns random n lines in URL list file
def test(n=5, sample=True):
    with open('URL.txt') as file:
        content = [line.rstrip('\n') for line in file]
    file.close()
    if sample:
        return random.sample(content, n)
    else:
        return content


if __name__ == '__main__':

    for url in test(5, sample=False):
        print(url)
        c = Crawler(url)
        print(c.run())
