import datetime #时间日期类
import hashlib #信息安全加密解密模块
from Message import DaDaMessage
from transaction import Transaction
from Message import InvaliMessage
class Block:
    def __init__(self,*args): #初始化
        self.messagelist=[]#存储多个交易记录
        self.timestamp=None#存储多个记录最终锁定的时间
        self.hash=None;#当前的哈希散列
        self.prev_hash=None;#上一块的哈希散列

        if args:
            for arg in args:
                self.add_message(arg);

    def add_message(self,message):#增加交易信息
        #区分第一条与后面多条,是否需要链接
        if len(self.messagelist) > 0:
            message.link(self.messagelist[-1]) #链接(给当前添加的消息记录添加上一个消息记录的hash)
        message.seal()#密封
        message.validate()#校验
        self.messagelist.append(message) #追加记录

    def link(self,block): #把区块链链接
        self.prev_hash = block.hash;
    def seal(self): #密封
        self.timestamp=datetime.datetime.now()#密封确定当前时间
        self.hash = self._hash_block()#密封当前的哈希值
    def _hash_block(self):#密封 上一块哈希，时间线，交易记录的最后一个
        return hashlib.sha256( (str(self.prev_hash)+
                             str(self.timestamp)+
                             str(self.messagelist[-1].hash)).encode('utf-8')).hexdigest();
    def validate(self):#校验
        for i, message in enumerate(self.messagelist):#每个交易记录校验一下
            message.validate();#每一条记录进行校验一下
            if i > 0 and message.prev_hash!=self.messagelist[i-1].hash:

                # raise "无效block, 交易记录被修改为在第{}条记录".format(i);
                raise InvaliBlock("无效block, 交易记录被修改为在第{}条记录".format(i)+str(self));


    def __repr__(self):#类的对象描述
        return "money block=hash:{},prehash={},len:{},time={}".format(self.hash,self.prev_hash,len(self.messagelist),self.timestamp);


class InvaliBlock(Exception):#异常
    def __init__(self, *args,**kwargs):#参数
        Exception.__init__(self,*args,**kwargs);


if __name__ == "__main__":
    try:
        t1 = Transaction("张三", "赵六1", 0.0001);
        t2 = Transaction("张三", "赵六2", 0.0002);
        t3 = Transaction("张三", "赵六3", 0.0003);
        t4 = Transaction("张三", "赵六4", 0.0004);

        # 创建了4条交易记录
        # 创建了4条交易记录
        m1 = DaDaMessage(t1);
        m2 = DaDaMessage(t2);
        m3 = DaDaMessage(t3);
        m4 = DaDaMessage(t4);

        yin = Block(m1, m2, m3);  # 一口气加入4条数据
        yin.seal();

        # m3.data = "你妹的直播"; #直接修改message;
        yin.messagelist[2] = m4;
        print(yin.validate())
    except InvaliMessage as e: #定位消息被修改
        print(e);
    except InvaliBlock as e: #定位区块被需改
        print(e);



