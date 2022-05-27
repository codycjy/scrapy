import queue
import time
import pymysql


class sqlOperation:
    def __init__(self):
        self.dataDic = None
        self.db = pymysql.connect(host='localhost', user='fish', port=3306, db='scrapy')
        self.cursor = self.db.cursor()

    def createTable(self):
        with open('CreatDB.sql', 'r') as f:
            createSql = f.read()
        self.cursor.execute(createSql)

    def dropTable(self):
        self.cursor.execute("DROP TABLE IF EXISTS `suzhou_com_cn`")
    def resart(self):
        self.dropTable()
        self.createTable()
    def select(self):
        self.cursor.execute("SELECT * FROM `suzhou_com_cn`")
        data = self.cursor.fetchall()
        return data
    def insert(self, qu):
        cnt=0
        while True :
            while not qu.empty():
                self.dataDic = qu.get()
                try:
                    InsertSql = """
                INSERT INTO `suzhou_com_cn`
                (
                
                    `title`,
                    `content`,
                    `publish_time`,
                    `firstReplyMember`,
                    `firstReplyContent`,
                    `firstReplyTime`,
                    `secondReplyMember`,
                    `secondReplyContent`,
                    `secondReplyTime`,
                    `district`,
                    `views`,
                    `reply`
                )
                VALUES
                (
                 "%s","%s","%s","%s","%s","%s","%s","%s","%s","%s",%s,%s
                )
                """ % (
                    self.dataDic['title'], self.dataDic['content'], self.dataDic['time'],
                    self.dataDic['firstReply'][0], self.dataDic['firstReply'][1], self.dataDic['firstReply'][2],
                    self.dataDic['secondReply'][0], self.dataDic['secondReply'][1], self.dataDic['secondReply'][2],
                    self.dataDic['position'], self.dataDic['view'], self.dataDic['reply']
                )
                except IndexError:
                    print(self.dataDic)
                    continue

                try:
                    self.cursor.execute(InsertSql)
                    self.db.commit()
                    print('insert success')
                except:
                    print(InsertSql)
                    self.db.rollback()
            time.sleep(5)
            cnt+=1
if __name__=="__main__":
    s=sqlOperation()
    s.resart()
    # data=s.select()
    # with open('final.csv','w') as f:
    #     for i in data:
    #         i=list(map(str,i))
    #         f.write(','.join(i)+'\n')


