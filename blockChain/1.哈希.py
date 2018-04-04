#######哈希
import hashlib;#加密模块

# sha = hashlib.sha256()#加密算法，sha256
# sha = hashlib.md5();#加密算法，md5
sha = hashlib.sha512();
sha.update('1234568'.encode('utf-8'));#转换二进制
print(sha.hexdigest());#哈希值

#哈希算法(数据加工抽象)
#sha256哈希算法有可能重复，重复的概率是1万亿份之一
#15%10=5  数据加工抽象