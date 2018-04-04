import hashlib; #加密模块
import datetime;#时间模块

class DaDaBlockCoin:#电子货币，达达币
    def __init__(self,index,#索引
                 timestamp,#交易时间
                 data,#交易记录
                 next_hash):#下个hash
        self.index = index;#索引
        self.timestamp = timestamp;#交易时间
        self.data=data;#交易记录
        self.next_hash = next_hash;  # 下一个hash
        self.selfhash=self.hash_DaDaBlockCoin(); #自身哈希



    def hash_DaDaBlockCoin(self):
        sha = hashlib.sha256();#加密算法
        datastr = str(self.index)+str(self.timestamp)+str(self.data)+str(self.next_hash);#对于数据整体加密

        sha.update(datastr.encode('utf-8'))#转成二进制数据
        return sha.hexdigest();

#创世的区块没有上一块，这个0可以随便写
def create_first_DadaBlock():#创世区块链第一块
    return DaDaBlockCoin(0,datetime.datetime.now(),"Love Data", "0");

def create_money_DadaBlock(last_block):#区块链的其他块,参数就是上一个区块
    this_index = last_block.index+1;#索引加1
    this_timestamp = datetime.datetime.now();#当前时间
    this_data="love Data"+str(this_index);#模拟交易数据
    this_hash=last_block.selfhash;#取得上一块的哈希
    return DaDaBlockCoin(this_index, this_timestamp, this_data,this_hash);



DaDaBlockCoins = [create_first_DadaBlock()];#区块链列表，只有一个创世区块
nums = 10;
head_block=DaDaBlockCoins[0];
print(head_block.index,head_block.timestamp,head_block.selfhash,head_block.next_hash);
for i in range(nums):
    dadaBlock_add = create_money_DadaBlock(head_block);#创建一个区块链的节点
    DaDaBlockCoins.append(dadaBlock_add);#加入区块链
    head_block = dadaBlock_add #保存最新创建的区块链
    print(dadaBlock_add.index,dadaBlock_add.timestamp,dadaBlock_add.selfhash,dadaBlock_add.next_hash);






