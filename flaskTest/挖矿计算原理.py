#通过计算hash来挖区块
from hashlib import sha256 #加密算法
x=11
y=1
#找出x*y的哈希值以0结尾
#f'{x*y}'把x*y的结果转化为字符串 hexdigest十六进制
while sha256(f'{x*y}'.encode('utf-8')).hexdigest()[-10:] != "0000000000":
    y+=1;
    print(y);

print("y={}时刻,y求解".format(y));
