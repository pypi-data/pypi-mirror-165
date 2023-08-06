字符串 = str
编码 = ord
解码 = chr
def 小写(string):
    return string.lower()

def 大写(string):
    return string.upper()

def 首字母大写(string):
    return string.title()

def 分开成列表(string,fen=None,ci=1):
    return string.split(fen,ci)

def 连接字符串(lian,List):
    return lian.join(List)