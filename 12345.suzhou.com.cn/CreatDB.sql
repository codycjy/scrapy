create table IF NOT EXISTS suzhou_com_cn
(
    id INT  PRIMARY KEY AUTO_INCREMENT,
    title varchar(500) Not Null,
    content varchar(5000) ,
    publish_time DATETIME ,
    firstReplyMember VARCHAR(100),
    firstReplyContent VARCHAR(2000),
    firstReplyTime VARCHAR (100),
    secondReplyMember VARCHAR(100),
    secondReplyContent VARCHAR(2000),
    secondReplyTime VARCHAR (100),
    district VARCHAR(100),
    views INT,
    reply INT
)