# 基于flask实现网络共识
import hashlib; #信息安全加密
import json; #互联网传递消息的格式
import datetime; #时间
from urllib.parse import urlparse; #url编码，解码
from uuid import uuid4; #签名
import requests;#请求
from flask import  Flask, jsonify, request;#网络的框架

class BlockChain:
    def __init__(self): #初始化
        self.chain = []; #区块的列表
        self.current_transaction=[];#交易的列表
        self.nodes = set()#节点
        self.new_block(previous_hash=1,proof=100)#创建第一个区块

    # 新的区块
    def new_block(self,proof,previous_hash=None): #新建一个区块，需要计算才能追加
        block = {
            "index":len(self.chain)+1,#索引
            "tiemstamp":datetime.datetime.now(),#时间
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
    def valid_proof(last_proof,proof):
        guess = f'{last_proof}{proof}'.encode('utf-8');#计算的字符串编码
        guess_hash=hashlib.sha256(guess).hexdigest();#哈希计算

        return guess_hash[:6]=="000000" #调整计算难度

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
            # if response.sta


        if new_chain:#判断是否为空
            self.chain = new_chain #更新成功
            return True
        else:
            return False;




    def hash(block):
        #模块进行hash处理 #json.dumps(block, sort_keys=True)区块转成字符串
        block_string = json.dumps(block,sort_keys=True).encode('utf-8');
        return hashlib.sha256(block_string).hexdigest(); #返回块的哈希值

