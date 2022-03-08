import queue
from scrapy import scrapy
from sqlOperation import sqlOperation
import threading
from time import sleep

rooturl = 'https://www.12345.suzhou.com.cn/'
indexurl = "https://www.12345.suzhou.com.cn/bbs/forum.php?mod=forumdisplay&fid=2&page="
queueIndex = queue.Queue()
queueTitle = queue.Queue()
queueContent = queue.Queue()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.100 Safari/537.36 '
}
for i in range(2,401):
    queueIndex.put(i)




def index():
    s = scrapy()
    s.getIndex(queueIndex, queueTitle)


def content():
    s = scrapy()
    s.getContent(queueTitle, queueContent)


def insert():
    s = sqlOperation()
    s.insert(queueContent)


def main():
    threadsi=[]
    threadc=[]
    threadins=[]
    for _ in range(5):
        i = threading.Thread(target=index)
        threadsi.append(i)
    for _ in range(10):
        c = threading.Thread(target=content)
        threadc.append(c)
    for _ in range(3):
        ins = threading.Thread(target=insert)
        threadins.append(ins)
    for i in threadsi:
        i.start()
    sleep(3)
    for c in threadc:
        c.start()
    sleep(5)
    for ins in threadins:
        ins.start()
def toFile():
    s=sqlOperation()
    data=s.select()
    with open('final.csv','w') as f:
        for i in data:
            i=list(map(str,i))
            f.write(','.join(i)+'\n')
if __name__ == '__main__':
    pass
    main()

