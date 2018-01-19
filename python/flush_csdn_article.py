import urllib.request as request
import gzip, binascii, sys
import time
import numpy as np
import getopt

def gzip_uncompress(c_data):
    f = gzip.GzipFile(mode = 'rb', fileobj = c_data)
    try:
        r_data = f.read()
    finally:
        f.close()
    return r_data

'''
GET /yxhlfx/article/details/79093456 HTTP/1.1
Host: blog.csdn.net
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://blog.csdn.net/yxhlfx
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2
'''

def select_article(reader):
    fast_articles = reader.get_fast_articles()
    slow_articles = reader.get_slow_articles()
    randnum = np.random.randint(0, 10)
    if randnum == 10:
        index = np.random.randint(0, len(slow_articles) - 1)
        article = slow_articles[index]
    else:
        index = np.random.randint(0, len(fast_articles) - 1)
        article = fast_articles[index]
    
    return article

class Article:
    def __init__(self, url, username, priority = 0):
        self.url = url
        self.req = request.Request(url)
        self.req.add_header('Connection', 'keep-alive');
        self.req.add_header('Cache-Control', 'max-age=0');
        self.req.add_header('Upgrade-Insecure-Requests', '1');
        self.req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36');
        self.req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8');
        self.req.add_header('Referer', 'http://blog.csdn.net/'+username);
        self.req.add_header('Accept-Encoding', 'gzip, deflate');
        self.req.add_header('Accept-Language', 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2');

        self.priority = priority
        self.prev_read = 0
    def show(self):
        print("Request: %s"%self.url)
    def update_read_count(self, count):
        if self.prev_read > 0:
            if count > self.prev_read:
                print("Flush the read count success!")
                print("Current read is : %d"%(count))
            else:
                print("Flush the read count failed!")
        self.prev_read = count
        pass

class Reader:
    def __init__(self, fast_article_list, slow_article_list, interval = 10):
        self.fast_article_list = fast_article_list
        self.slow_article_list = slow_article_list
        self.flush_interval = interval
        self.req = ''
        pass
    def get_fast_articles(self):
        return self.fast_article_list
    def get_slow_articles(self):
        return self.slow_article_list
    def run(self):
        while True:
            # random select one url to request
            article = select_article(self)
            article.show()
            f = request.urlopen(article.req)
            content = gzip_uncompress(f).decode("utf-8").split('\n')
            # for debug
            for line in content:
                if line.find("icon-read") != -1:
                    break;
            # print("line: %s"%(line))
            readed = int(line.split('>')[5].split('<')[0])
            article.update_read_count(readed)
            time.sleep(self.flush_interval)
        pass

def usage(program):
    print("Usage: %s [-h|--help] [-u username|--user=username]--fast=file --slow=file"%(program))
if __name__ == '__main__':
    try:
        options,args = getopt.getopt(sys.argv[1:],"hu:",["help","fast=","slow=","user"])
    except getopt.GetoptError:
        sys.exit()

    username=""
    for name,value in options:
        if name in ("-h","--help"):
            usage(sys.argv[0])
        elif name in ("-u", "--user"):
            username = value
        elif name in ("--fast"):
            fast_flush_file = value
        elif name in ("--slow"):
            slow_flush_file = value
        else:
            usage(sys.argv[0])

    # Construct articles
    fast_articles = []
    slow_articles = []

    try:
        f = open(fast_flush_file)
        for line in f.readlines():
            fast_articles.append(Article(line, username))
    except Exception:
        usage(sys.argv[0])
        sys.exit()
    finally:
        f.close()
    try:
       f = open(slow_flush_file)
       print(f)
       for line in f.readlines():
           fast_articles.append(Article(line, username, 1))
           pass
    except Exception:
        usage(sys.argv[0])
        sys.exit()
    finally:
        f.close()
    f.close()
    Reader(fast_articles, slow_articles).run()
