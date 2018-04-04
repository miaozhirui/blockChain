#该类的作用是封装交易类

#电子货币的交易类
import datetime;

class Transaction:
    def __init__(self,payer,#付款方
                 recer,#收款方
                 money):#数字货币的数字

        self.payer = payer;#付款方
        self.recer = recer;#收款方
        self.money = money;#数字货币的数字
        self.timestamp = datetime.datetime.now();#交易时间

    def __repr__(self):

        return str(self.payer) + " pay " + str(self.recer) + " " + str(self.money)+ " " +str(self.timestamp);

# t1 = Transaction("张三","李四",0.0001);#交易类，后期需要整合公钥私钥
# print(t1);
