from 列表 import *
from 基本 import *
from 字符串 import *
try:
    from 游戏 import *
except (OSError, ImportError):
    pass
from 终端 import *
from 运算 import *
from 绘图 import *
from ascii码 import *
import sys

try:
    code = open(sys.argv[1], encoding='utf-8')
    exec(code.read())
except IndexError:
    print('win64的Rabbit 1.2.1（v1.2.1 发布于2022年8月16日13时02分）')
    while True:
        code = input('> ')
        if ':' in code:
            while yu == '':
                yu = input('. ')
                code += yu
        try:
            if (eval(code) == None):
                pass
            else:
                print(eval(code))
        except SyntaxError:
            try:
                exec(code)
            except Exception as error:
                print(error.__class__.__name__, error, sep=':')
        except Exception as error:
            print(error.__class__.__name__, error, sep=':')
