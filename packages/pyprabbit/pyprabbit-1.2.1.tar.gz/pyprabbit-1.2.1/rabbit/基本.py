import time
def fun():
    pass
def 空代码():
    pass
def 导入(名称):
    mod = __import__(名称)
    exec(名称 + ' = mod')

def 当(条件,代码):
    while 条件:
        代码()

def 遍历(变量,对象,代码):
    exec('for '+变量+' in '+对象+':\n'+代码)

def 如果(条件,成立代码,不成立代码=空代码):
    if 条件:
        成立代码()
    else:
        不成立代码()

def 返回(zhi):
    exec('return '+str(zhi))

序列 = range

def 函数(参数,代码):
    global fun
    exec('def fun(' + 参数 + '):\n  ' + 代码)
    return fun

def 类(canshu,daima):
    global fun
    exec('class fun:\n  def __init__(self,' + canshu + '):\n        ' + daima)

def 删除(duixiang):
    del duixiang

长度 = len

def 存在于(a,b):
    return a in b

执行代码 = exec
表达式 = eval
时间 = time.gmtime
等待 = time.sleep

def 对象赋值(o,v,c):
    exec('with o as v:\nc()')


时间格式化 = time.strftime
def 开启或归零计时器():
    start = time.perf_counter()

计时器 = time.perf_counter()


