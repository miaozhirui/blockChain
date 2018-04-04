#封装交易数据的密封

#区块链的message交易记录

import datetime #时间日期类
import hashlib #信息安全加密解密模块
from transaction import Transaction

class DaDaMessage: #交易记录类
    def __init__(self,data): #初始化
        self.hash = None;#自身的哈希
        self.prev_hash = None; #上一个信息记录的哈希
        self.timestamp=datetime.datetime.now();#交易时间
        self.data=data;#交易信息
        self.payload_hash=self._hash_payload()#交易后的哈希

    def _hash_payload(self):#对于交易时间与交易数据进行哈希计算
        return hashlib.sha256( (str(self.timestamp)+str(self.data)).encode('utf-8') ).hexdigest()#去的数据的hash


    def _hash_message(self):#对交易进行锁定
        return hashlib.sha256((str(self.prev_hash) + str(self.payload_hash)).encode('utf-8')).hexdigest()

    def seal(self):#密封
        self.hash = self._hash_message();#对应数据锁定，对于交易前的链锁定

    def validate(self):
        if self.payload_hash != self._hash_payload() :#判断是否有人修改
            raise InvaliMessage("交易数据与时间被修改"+str(self));

        if self.hash != self._hash_message():#判断消息链
            raise InvaliMessage('交易的哈希链接被修改'+str(self))

        return "数据正常"+str(self);

    def __repr__(self):#返回对象的基本信息
        mystr="hash:{},prev_hash:{},data:{}".format(self.hash, self.prev_hash, self.data)
        return mystr;

    def link(self, Message):
        self.prev_hash=Message.hash #链接



class InvaliMessage(Exception):#异常
    def __init__(self, *args,**kwargs):#参数
        Exception.__init__(self,*args,**kwargs);




if __name__ == '__main__':#单模块测试
    try:
        t1 = Transaction("张三", "李四1", 0.0001);
        t2 = Transaction("张三", "李四2", 0.0002);
        t3 = Transaction("张三", "李四3", 0.0003);
        t4 = Transaction("张三", "李四4", 0.0004);

        m1 = DaDaMessage(t1);
        m2 = DaDaMessage(t2);
        m3 = DaDaMessage(t3);  # 交易记录
        m4 = DaDaMessage(t4);

        m1.seal();
        m2.link(m1)
        m2.seal();
        m3.link(m2);  # 链接
        m3.seal();  # 交易记录密封
        m4.link(m3);
        m4.seal();

        # 修改数据，模拟串改
        m2.data = "你妹的直播平台";
        m2.prev_hash = "他娘的直播平台";

        print(m1);
        print(m2);
        print(m3);  # 显示信息

        m1.validate()
        m2.validate()
        m3.validate()  # 校验
        m4.validate();
    except InvaliMessage as e:
        print(e);


