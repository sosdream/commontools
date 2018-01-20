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
GET /username/article/details/number HTTP/1.1
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

def select_article(flusher):
    fast_articles = flusher.get_fast_articles()
    slow_articles = flusher.get_slow_articles()
    randnum = np.random.randint(0, 10)
    if randnum == 10:
        index = np.random.randint(0, len(slow_articles) - 1)
        article = slow_articles[index]
    else:
        index = np.random.randint(0, len(fast_articles) - 1)
        article = fast_articles[index]
    
    return article

class Article:
    def __init__(self, url, username, max_count = 5000, single_interval=30.0):
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

        self.priority = 0
        self.prev_read = 0
        self.flush_max_count = max_count
        self.prev_flush_time = 0.0
        self.single_interval = single_interval
        self.errors = 0
        self.flush_succes_count = 0
    def show(self):
        print("%s->[success %d, failed %d]"%(self.url,
                                            self.flush_succes_count,
                                            self.errors))
    def update_read_count(self, count):
        if self.prev_read > 0:
            if count > self.prev_read:
                self.prev_flush_time = time.time()
                self.flush_succes_count = self.flush_succes_count + 1
            else:
                self.errors = self.errors + 1
        self.prev_read = count
        if count > self.flush_max_count:
            return False
        return True
    def canbe_flush(self):
        cur_time = time.time()
        if (cur_time - self.prev_flush_time) > self.single_interval:
            self.prev_flush_time = cur_time
            return True
        return False

class Flusher:
    def __init__(self, interval = 1):
        self.fast_article_list = []
        self.slow_article_list = []
        self.flush_interval = interval
        self.article_all_num = 0
        self.req = ''
        pass
    def get_fast_articles(self):
        return self.fast_article_list
    def get_slow_articles(self):
        return self.slow_article_list
    def add_fast_flush_aticle(self, article):
        article.priority = 0
        self.article_all_num = self.article_all_num + 1
        self.fast_article_list.append(article)
        pass
    def add_slow_flush_aticle(self, article):
        article.priority = 1
        self.article_all_num = self.article_all_num + 1
        self.slow_article_list.append(article)
        pass
    def remove_article(self, article):
        self.article_all_num = self.article_all_num - 1
        if article.priority == 0:
            self.fast_article_list.remove(article)
        else:
            self.slow_article_list.remove(article)
    def run(self):
        try_num = 0
        
        while True:
            # random select one url to request
            article = select_article(self)
            if article.canbe_flush() == False:
                try_num = try_num + 1
                if try_num > self.article_all_num/2:
                    time.sleep(1)
                continue

            f = request.urlopen(article.req)
            content = gzip_uncompress(f).decode("utf-8").split('\n')
            for line in content:
                if line.find("icon-read") != -1:
                    break;
            # for debug
            # print("line: %s"%(line))
            readed = int(line.split('>')[5].split('<')[0])
            if article.update_read_count(readed) == False:
                self.remove_article(article)
            article.show()
            time.sleep(self.flush_interval)
            try_num = 0
            f.close()
        pass

def usage(program, description = ""):
    if description != "":
       print(description)
    print("Usage: %s [-h|--help] --fast=file --slow=file"%(program))
    sys.exit(0)

if __name__ == '__main__':
    try:
        options,args = getopt.getopt(sys.argv[1:],"h",["help","fast=","slow="])
    except getopt.GetoptError:
        sys.exit()

    username=""
    for name,value in options:
        if name in ("-h","--help"):
            usage(sys.argv[0])
        elif name in ("--fast"):
            fast_flush_file = value
        elif name in ("--slow"):
            slow_flush_file = value
        else:
            usage(sys.argv[0], "Unkown option!")

    # Construct articles
    flusher = Flusher()
    try:
        f = open(fast_flush_file)
        for line in f.readlines():
            if line[0] == '#':
                continue
            items = line.split(' ')
            username = items[0].split('.')[2].split('/')[1]
            if len(items) == 3:
                flusher.add_fast_flush_aticle(Article(items[0],
                                 username,
                                 max_count = int(items[1]),
                                 single_interval = float(items[2])))
            else:
                flusher.add_fast_flush_aticle(Article(items[0], username))

        f.close()
    except Exception:
        usage(sys.argv[0], "Open fast file Error!")
        sys.exit()
    try:
       f = open(slow_flush_file)
       for line in f.readlines():
           if line[0] == '#':
               continue
           items = line.split(' ')
           username = items[0].split('.')[2].split('/')[1]
           if len(items) == 3:
               flusher.add_slow_flush_aticle(Article(items[0],
                                username,
                                max_count = int(items[1]),
                                single_interval = float(items[2])))
           else:
               flusher.add_slow_flush_aticle(Article(items[0], username))

       f.close()
    except Exception:
        usage(sys.argv[0], "Open slow file error!")
        sys.exit()
    # Make the flusher running
    flusher.run()
