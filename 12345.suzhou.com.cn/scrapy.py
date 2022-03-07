import requests
from lxml import etree
import queue
from time import sleep
rooturl='https://www.12345.suzhou.com.cn/'
indexurl="https://www.12345.suzhou.com.cn/bbs/forum.php?mod=forumdisplay&fid=2&page="
queueIndex=queue.Queue()
queueTitle=queue.Queue()
queueContent=queue.Queue()
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
for i in range(2,5):
    queueIndex.put(i)
ans=[]
class scrapy:
    def __init__(self):
        title=""
        content=""
        time=""

    def getIndex(self):
        index=queueIndex.get()
        iurl=indexurl+str(index)
        reqIndex=requests.get(iurl,headers=headers)
        htmlIndex=etree.HTML(reqIndex.text)
        for i in range(1,51):
            title = htmlIndex.xpath(f'//*[@id="moderate"]/div//li[{i}]/div//div[1]/p/a/text()')
            title=title[0].strip()
            content_url = htmlIndex.xpath(f'//*[@id="moderate"]/div//li[{i}]/div//div[1]/p/a/@href')
            # print(title,content_url)
            queueTitle.put([title,content_url])
        sleep(1)
    def getContent(self):
        while not queueTitle.empty():
            title,content_url=queueTitle.get()

            content_url=rooturl+content_url[0]
            print(content_url)
            reqContent=requests.get(content_url,headers=headers)
            htmlContent=etree.HTML(reqContent.text)
            content=htmlContent.xpath('.//td[@class="t_f"]/text()')
            time=htmlContent.xpath('//td[2]/div[1]/div[2]/div[2]/em/text()')
            content=content[0].strip()
            if(content!=''):
                time=time[0][4:]
                print(time,content)
                queueContent.put([title,content,time])

    def toFile(self):
        while(queueContent.empty()==False):
            lst=queueContent.get()
            lst=map(str,lst)
            with open('12345.csv','a',encoding='utf-8') as f:
                f.write(','.join(lst)+'\n')


if __name__ == '__main__':
    s=scrapy()
    s.getIndex()
    s.getContent()
    s.toFile()



