from Block_data import Block;
from Block_data import  InvaliBlock;
from Message import DaDaMessage
from transaction import Transaction
from Message import InvaliMessage

class DadaBlockCoin:#区块链
    def __init__(self): #初始化
        self.blocklist = []; #装载所有的区块

    def add_block(self,block):  # 增加区块
        if len(self.blocklist) > 0:
            block.prev_hash = self.blocklist[-1].hash #区块链的hash

        block.seal();#密封
        block.validate()#校验
        self.blocklist.append(block) #增加区块

    def validate(self): #校验
        for i,block in enumerate(self.blocklist):
            try:
                block.validate()
            except InvaliBlock as e:
                raise InvalidBlockCoin("区块校验错误,区块索引{}".format(i));

    def __repr__(self): #字符串格式化
        return "Dada_BlockCoin:{}".format(len(self.blocklist)) #获取长度


class InvalidBlockCoin(Exception):
    def __init__(self, *args,**kwargs):#参数
        Exception.__init__(self,*args,**kwargs);


if __name__=="__main__":
    #创建交易记录
    try:
        t1 = Transaction("张三", "赵六1", 0.0001);
        t2 = Transaction("张三", "赵六2", 0.0002);
        t3 = Transaction("张三", "赵六3", 0.0003);
        t4 = Transaction("张三", "赵六4", 0.0004);
        t5 = Transaction("张三", "赵六4", 0.0004);
        t6 = Transaction("张三", "赵六4", 0.0004);

        m1 = DaDaMessage(t1);
        m2 = DaDaMessage(t2);
        m3 = DaDaMessage(t3);
        m4 = DaDaMessage(t4);
        m5 = DaDaMessage(t5);
        m6 = DaDaMessage(t6);

        yin1 = Block(m1, m2);
        yin1.seal();
        yin2 = Block(m3, m4);
        yin2.seal()
        yin3 = Block(m5, m6);
        yin3.seal();

        # 串改区块
        yin3.messagelist[0] = m1;

        mydada = DadaBlockCoin()  # 区块链
        mydada.add_block(yin1);
        mydada.add_block(yin2);
        mydada.add_block(yin3);
        mydada.validate()  # 校验
    except Exception as e:
        print(e);












