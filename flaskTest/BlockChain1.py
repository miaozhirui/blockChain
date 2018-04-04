#多节点

# 基于flask实现网络共识
import hashlib; #信息安全加密
import json; #互联网传递消息的格式
# import datetime; #时间
import time;
from urllib.parse import urlparse; #url编码，解码
from uuid import uuid4; #签名
import requests;#请求
from flask import  Flask, jsonify, request;#网络的框架

class BlockChain:#实现一个区块链
    def __init__(self): #初始化
        self.chain = []; #区块的列表
        self.current_transaction=[];#交易的列表
        self.nodes = set()#节点,与别的电脑连接
        self.new_block(previous_hash=1,proof=100)#创建第一个区块

    def register_node(self,address):#在集合中添加其他的节点
        parsed_url = urlparse(address)#地址注册
        if parsed_url.netloc:#可以连接网络的情况
            self.nodes.add(parsed_url.netloc)

        elif parsed_url.path:
            self.nodes.add(parsed_url.path)

        else:
            raise ValueError('url无效');


    # 新的区块
    def new_block(self,proof,previous_hash=None): #新建一个区块，需要计算才能追加
        block = {
            "index":len(self.chain)+1,#索引
            "tiemstamp":time.time(),#时间
            "transactions": self.current_transaction,#交易
            "proof":proof, #计算力的凭证
            "previous_hash": previous_hash or self.hash(self.chain[-1]),#上一个区块的hash
        }

        self.current_transaction = [] #开辟新的区块，交易需要被清空
        self.chain.append(block) #增加一个区块

        return block;

    # 新的交易
    def new_transaction(self,sender, #付款方
                        recipient, #收款方
                        amount):  #交易金额

        #添加一个信息的交易
        self.current_transaction.append({
            "sender":sender,
            "recipient":recipient,
            "amount":amount
        })

        return self.last_block["index"]+1;


    @property
    def last_block(self): #代表取最后一块
        return self.chain[-1];

    #工作量的证明
    def proof_of_work(self,last_block):#挖矿获取工作量证明

        last_proof=last_block["proof"] #取出计算力的凭证
        last_hash=self.hash(last_block); #取出hash

        proof=0; #循环求解
        while self.valid_proof(last_proof,proof,last_hash) is False:
            proof += 1;

        return proof;


    @staticmethod #类的静态函数

    # 验证工作量证明
    def valid_proof(last_proof,proof,last_hash):
        guess = f'{last_proof}{proof}{last_hash}'.encode('utf-8');#计算的字符串编码
        guess_hash=hashlib.sha256(guess).hexdigest();#哈希计算

        if guess_hash[:4] == "0000":
            print('=======')
            print(last_proof)
            print(proof)
            print(last_hash)
            print('=======')
            print(guess_hash);
            print(guess_hash[:4]);
            return True;
        else:
            return False
        # return guess_hash[:4]=="0000" #调整计算难度,hash挖矿

    def valid_chain(self,chain):#区块校验
        last_block = chain[0] #从第一块开始校验
        current_index = 1 #索引为1
        while current_index < len(chain): #循环每一个区块进行校验
            block = chain[current_index]; #取得当前块

            if block["previous_hash"] != self.hash(last_block): #区块校验
                return False;

            #创建一个区块依赖算力计算，
            if not self.valid_proof(last_block['proof'],
                                    block['proof'],
                                    last_block['previous_hash']):
                return False;


            last_block = block
            current_index +=1;

    def resolve_conflicts(self):#冲突，一致性算法的一种
        #取得互联网中最长的链替换当前的链表
        #区块链同步算法
        neighbours = self.nodes #备份节点 127.0.0.1 192.168.0.1
        new_chain = None;#新的链表
        max_length = len(self.chain)#最长的长度，先保存当前节点的长度

        for node in neighbours: #刷新每个网络节点，取得最长更新
            response = requests.get(f'http://{node}/chain') #取得其他节点的区块链
            if response.status_code == 200:
                length = response.json()['length'] #取得长度
                chain = response.json()['chain'] #取得区块链表

                #刷新保存最长的区块链与已完成校验
                if length > max_length and self.valid_chain(chain):
                    max_length=length
                    new_chain = chain


        if new_chain:#判断是否为空
            self.chain = new_chain #更新成功
            return True
        else:
            return False;

    def hash(self,block):
        # 模块进行hash处理 #json.dumps(block, sort_keys=True)区块转成字符串
        block_string = json.dumps(block, sort_keys=True).encode('utf-8');
        return hashlib.sha256(block_string).hexdigest();  # 返回块的哈希值

app = Flask(__name__) #flask的网络框架


#为当前节点制造一个独一无二的地址
node_id=str(uuid4()).replace("-","")#模拟钱包的地址
print("钱包地址",node_id);

blockchain = BlockChain() #构造一个区块链

@app.route('/')#系统工作正常

#1
def index_page():
    return '欢迎来到dada电子货币系统，韭菜你好flask网络工作正常'

#2
@app.route('/chain',methods=['GET']) #显示所有的区块
def chain():
    response = {
        "chain":blockchain.chain, #区块信息
        "length":len(blockchain.chain) #区块长度
    }

    return jsonify(response), 200; #返回网络信息，200网络相应码


#3
#新的交易
@app.route('/transaction/new',methods=['POST'])
def new_transaction():

    values = request.get_json(); #传递交易信息,客户端需要发json格式的数据
    required = ["sender","recipient", "amount"]; #交易的信息，付款，收矿方，金额

    if not all(k in values for k in required):
        return "小伙子你的交易信息有误，本大爷不执行",400;#交易失败

    #索引，创建一个交易操作
    index = blockchain.new_transaction(values["sender"],values["recipient"],values["amount"]);
    response={"message":f"交易被增加到区块{index}"}

    return jsonify(response), 201;

#4
@app.route('/mine',methods=['GET'])#挖矿
def mine():
    lastblock=blockchain.last_block#取的区块链表最后一个区块

    proof=blockchain.proof_of_work(lastblock)#挖矿延时，创建新的区块

    blockchain.new_transaction(sender="0", recipient=node_id,amount=10)#系统奖励的币
    previous_hash=blockchain.hash(lastblock)#记录上一块的哈希
    block=blockchain.new_block(proof,previous_hash)#创建一个新的区块

    #描述区块的基本信息
    response = {
        "message":"NewBlock Forged",
        "index":block["index"],
        "transactions":block["transactions"],
        "proof":block["proof"],
        "previous_hash":block["previous_hash"]

    }

    return jsonify(response), 200; #返回信息


#5 网络同步
@app.route('/nodes/resolve',methods=['GET'])#共识算法用最长的替换当下
def nodes_resolve():
    replaced = blockchain.resolve_conflicts();

    if replaced:
        response = {
            "message":"区块链信息已经被同步",
            "new_chain":blockchain.chain
        }
    else:
        response = {
            "message": "当前区块链是权威最长无需替换",
            "chain": blockchain.chain
        }

    return jsonify(response), 200;


@app.route('/nodes/register',methods=['POST'])

#6. 节点注册
def nodes_register():
    values = request.get_json()#抓取网络信息,链接其他节点
    nodes = values.get('nodes'); #读取节点

    if nodes is None:
        return "Error:没有找到其他节点信息",400

    for node in nodes:
        blockchain.register_node() #注册网络节点

    response = {

        "message":"新的网络节点列表已经追加",
        "total_nodes":list(blockchain.nodes) #所有节点
    }

    return jsonify(response), 200 #返回信息



if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000)
