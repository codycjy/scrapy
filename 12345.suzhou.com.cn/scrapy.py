import requests
from lxml import etree
import queue
from time import sleep
from collections import defaultdict
from sqlOperation import sqlOperation

rooturl = 'https://www.12345.suzhou.com.cn/'
indexurl = "https://www.12345.suzhou.com.cn/bbs/forum.php?mod=forumdisplay&fid=2&page="
# queueIndex = queue.Queue()
# queueTitle = queue.Queue()
# queueContent = queue.Queue()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}
# for i in range(2, 5):
#     queueIndex.put(i)
# ans = []


class scrapy:
    def __init__(self):
        self.result = None
        self.time = None
        self.officialReply = None
        self.content = None
        self.posts = None
        self.htmlContent = None
        self.reqContent = None
        self.info = None
        self.reply = None
        self.view = None
        self.position = None
        self.title = None
        self.content_url = None
        self.htmlIndex = None
        self.reqIndex = None
        self.iurl = None
        self.index = None

    def getIndex(self,queueIndex,queueTitle):

        while not queueIndex.empty():
            self.index = queueIndex.get()
            self.iurl = indexurl + str(self.index)
            self.reqIndex = requests.get(self.iurl, headers=headers)
            self.htmlIndex = etree.HTML(self.reqIndex.text)
            for i in range(1, 51):
                self.title = self.htmlIndex.xpath(f'//*[@id="moderate"]/div//li[{i}]/div//div[1]/p/a/text()')
                self.title = self.title[0].strip()
                self.content_url = self.htmlIndex.xpath(f'//*[@id="moderate"]/div//li[{i}]/div//div[1]/p/a/@href')[0]
                self.position = self.htmlIndex.xpath(f"//div[@id='threadlist']//ul/li[{i}]//div[3]/div[1]/text()")[0]
                self.view = self.htmlIndex.xpath(f"//div[@id='threadlist']//li[{i}]//div[3]/div[2]/i[1]/text()")[0]
                try:
                    self.reply = self.htmlIndex.xpath(f"//div[@id='threadlist']//li[{i}]//div[3]/div[2]/i[2]/text()")[0]
                except IndexError:
                    self.reply = 0

                self.info = defaultdict(str)
                self.info['title'] = self.title
                self.info['content_url'] = self.content_url
                self.info['position'] = self.position
                self.info['view'] = self.view
                self.info['reply'] = self.reply
                # print(self.info)
                queueTitle.put(self.info)
                print('index success')


    def getContent(self,queueTitle,queueContent):
        cnt=0
        while True and cnt<10:

            while not queueTitle.empty():
                # print('start')
                self.info = queueTitle.get()
                self.content_url = self.info['content_url']
                self.title = self.info['title']
                self.content_url = rooturl + self.content_url
                self.reqContent = requests.get(self.content_url, headers=headers)
                self.htmlContent = etree.HTML(self.reqContent.text)
                self.posts = self.htmlContent.xpath("//div[@class='post_block']/@id")
                self.content = self.htmlContent.xpath('.//td[@class="t_f"]/text()')
                self.content = list(map(str.strip, self.content))
                self.content = ' '.join(self.content)
                self.content = self.content.replace('\n', '')
                self.content = self.content.replace(',', '，')
                if self.content == ' ': continue
                self.time = self.htmlContent.xpath('//td[2]/div[1]/div[2]/div[2]/em/text()')
                self.officialReply = []
                for i in self.posts:
                    id = i[5:]
                    usergroup = self.htmlContent.xpath(f'//*[@id="favatar{id}"]/p/a/text()')
                    if usergroup:
                        if usergroup[0] == '便民服务员':
                            user = self.htmlContent.xpath(f'//*[@id="favatar{id}"]/div[3]/a/text()')
                            comments = self.htmlContent.xpath(f'//*[@id="postmessage_{id}"]/text()')
                            try:
                                comments = [comments[0].replace(',', ' ')]
                            except IndexError:
                                print(comments)
                            comment_time = self.htmlContent.xpath(f'//*[@id="authorposton{id}"]/span/@title')
                            if not comment_time:
                                comment_time = [self.htmlContent.xpath(f'//*[@id="authorposton{id}"]/text()')[0][4:]]
                            try:
                                self.officialReply.append([user[0], comments[0].strip(), comment_time[0].replace('/', '-')])
                            except IndexError:
                                pass
                firstReply = ['', '', '']
                secondReply = ['', '', '']
                if self.officialReply:
                    firstReply = self.officialReply[0]
                    if len(self.officialReply) > 1:
                        secondReply = self.officialReply[-1]
                if not self.content:
                    print(self.content)
                    continue
                self.time = self.time[0][4:]
                self.result = defaultdict(str)
                self.result['title'] = self.title
                self.result['content'] = self.content
                self.result['time'] = self.time.replace('/', '-')
                self.result['firstReply'] = firstReply
                self.result['secondReply'] = secondReply
                self.result['position'] = self.info['position']
                self.result['view'] = self.info['view']
                self.result['reply'] = self.info['reply']

                # print(self.result, self.content_url)
                queueContent.put(self.result)
                print('content success')
            sleep(1)
            cnt+=1

    def toFile(self):
        while not queueContent.empty():
            result = queueContent.get()
            frep = result['firstReply'] if result['firstReply'] else [' ', ' ', ' ']
            srep = result['secondReply'] if result['secondReply'] else [' ', ' ', ' ']
            with open('example.csv', 'a', encoding='utf-8') as f:
                f.write(f'{result["title"]},{result["content"]},{result["time"]},'
                        f'{frep[0]},{frep[1]},{frep[2]},{srep[0]},{srep[1]},{srep[2]},'
                        f'{result["position"]},{result["view"]},{result["reply"]}\n')


if __name__ == '__main__':
    s = scrapy()
    s.getIndex()
    s.getContent()
    # s.toFile()
    sql=sqlOperation()
    sql.dropTable()
    sql.createTable()

